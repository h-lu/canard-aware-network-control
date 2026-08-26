"""Stage-4 contract for direct projected return-Hessian bounds.

Stage 3 proves a lower bound on the stable projection norm and therefore
rules out the old scalar C_N=10 row.  It does not rule out a quantitative
stable graph.  This module records the sharper route: validate the six
independent stable/unstable blocks of the Poincare return Hessian directly
in split coordinates, and close a two-by-two positive Lyapunov--Perron
majorant.

The registered model adapter is intentionally incomplete.  It imports the
validated rates but leaves the stable power constant, the six Hessian
bounds, and the split return ball null.  The evaluator is executable on a
complete independent budget; no graph or pulse theorem is promoted here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from hashlib import sha256
from math import isqrt
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


SCHEMA_ID = "leaky-projected-return-hessian-stage4-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_projected_return_hessian_stage4_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_projected_return_hessian_stage4_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_projected_return_hessian_stage4_contract.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-projected-return-hessian-stage4-contract.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_projected_return_hessian_stage4_contract.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_projected_return_hessian_stage4_contract.py"
)
ARITHMETIC_SCOPE = (
    "exact rational evaluation of the two-by-two positive majorant from "
    "direct projected Hessian upper bounds; an integer square-root Perron "
    "upper bound; exact parent-byte and source-manifest binding; and an "
    "explicit physical-time first/second RFDE variational return contract"
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

HESSIAN_FIELD_NAMES = (
    "stable_output_ss_upper",
    "stable_output_su_upper",
    "stable_output_uu_upper",
    "unstable_output_ss_upper",
    "unstable_output_su_upper",
    "unstable_output_uu_upper",
)
MATRIX_REQUIRED_FIELDS = (
    "stable_power_constant_upper",
    "validated_return_map_split_ball_radius_lower",
)

TRUE_FLAGS = (
    "six_independent_projected_hessian_blocks_identified",
    "two_by_two_positive_majorant_evaluator_registered",
    "physical_time_second_return_variation_formula_registered",
    "direct_split_coordinate_route_avoids_black_box_norm_transfer",
)
FALSE_FLAGS = (
    "stable_power_constant_numeric_upper_validated",
    "six_projected_return_hessian_blocks_validated",
    "split_return_map_ball_validated",
    "matrix_lyapunov_perron_contraction_validated",
    "matrix_lyapunov_perron_self_map_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "graph_radius_1p7e_minus_3_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class ProjectedReturnHessianBlockBudget:
    """Uniform upper bounds on the six independent projected D2P blocks."""

    stable_output_ss_upper: str | None
    stable_output_su_upper: str | None
    stable_output_uu_upper: str | None
    unstable_output_ss_upper: str | None
    unstable_output_su_upper: str | None
    unstable_output_uu_upper: str | None
    evidence_status: str


@dataclass(frozen=True)
class MatrixLyapunovPerronInputBudget:
    """Inputs for the split-coordinate positive majorant."""

    stable_power_rate_upper: str
    unstable_backward_rate_upper: str
    stable_power_constant_upper: str | None
    unstable_backward_power_constant_upper: str
    sequence_weight_beta: str
    stable_seed_radius: str
    stable_graph_radius: str
    unstable_graph_radius: str
    validated_return_map_split_ball_radius_lower: str | None
    hessian_blocks: ProjectedReturnHessianBlockBudget
    evidence_status: str


@dataclass(frozen=True)
class MatrixLyapunovPerronEvaluation:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    input_order_conditions_hold: bool
    stable_kernel_coefficient_upper: str | None
    unstable_kernel_coefficient_upper: str | None
    unstable_quadratic_kernel_coefficient_upper: str | None
    derivative_lipschitz_matrix_upper: dict[str, str] | None
    perron_root_upper: str | None
    canonical_positive_weight_lower: dict[str, str] | None
    canonical_positive_weight_upper: dict[str, str] | None
    weighted_row_sum_upper: str | None
    nonlinear_value_vector_upper: dict[str, str] | None
    self_map_image_vector_upper: dict[str, str] | None
    self_map_slack_vector_lower: dict[str, str] | None
    fixed_point_derivative_sequence_vector_upper: dict[str, str] | None
    graph_height_upper: str | None
    graph_derivative_upper: str | None
    split_ball_contains_graph_box: bool
    contraction_closes: bool
    self_map_closes: bool
    graph_certificate_closes: bool
    formulas: dict[str, str]


@dataclass(frozen=True)
class Stage4ProjectedReturnContract:
    schema_id: str
    model_id: str
    branch: str
    split_coordinate_norm: str
    parent_result_sha256: dict[str, str]
    hessian_block_budget: dict[str, Any]
    matrix_input_budget: dict[str, Any]
    matrix_evaluation: dict[str, Any]
    variational_equation_contract: dict[str, Any]
    return_event_contract: dict[str, Any]
    projected_propagator_certificate_interface: dict[str, Any]
    adapted_norm_transfer_audit: dict[str, Any]
    radius_design_target: dict[str, Any]
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


def _finite_decimal(value: str | None, name: str) -> Decimal | None:
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


def _fraction(value: str | None, name: str) -> Fraction | None:
    number = _finite_decimal(value, name)
    return None if number is None else Fraction(number)


def _fraction_string(value: Fraction, rounding: str) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = rounding
        number = Decimal(value.numerator) / Decimal(value.denominator)
        return format(+number, "f")


def _upper(value: Fraction) -> str:
    return _fraction_string(value, ROUND_CEILING)


def _lower(value: Fraction) -> str:
    return _fraction_string(value, ROUND_FLOOR)


def _sqrt_fraction_upper(value: Fraction, digits: int = 120) -> Fraction:
    """Return a rigorous fixed-decimal upper bound for sqrt(value)."""

    if value < 0:
        raise ValueError("cannot take a real square root of a negative value")
    scale = 10**digits
    numerator = value.numerator * scale * scale
    denominator = value.denominator
    scaled_ceiling = (numerator + denominator - 1) // denominator
    root = isqrt(scaled_ceiling)
    if root * root < scaled_ceiling:
        root += 1
    return Fraction(root, scale)


def _evaluation_formulas() -> dict[str, str]:
    return {
        "component_derivative_bounds": (
            "L_i,s=C_i,ss*R_s+C_i,su*R_u; "
            "L_i,u=C_i,su*R_s+C_i,uu*R_u"
        ),
        "majorant_matrix": (
            "M=diag(K_s/(beta-rho_s),K_u*rho_u/(1-beta*rho_u))*L"
        ),
        "perron_gate": "rho(M)<1",
        "nonlinear_value_vector": (
            "Q_i=(C_i,ss*R_s^2)/2+C_i,su*R_s*R_u+"
            "(C_i,uu*R_u^2)/2"
        ),
        "self_map": (
            "K_s*r+a_s*Q_s<=R_s and a_u*Q_u<=R_u"
        ),
        "canonical_weight": "w=(I-M)^(-1)*(1,1), so M*w=w-(1,1)",
        "graph_height": (
            "||h||<=K_u*rho_u*Q_u/(1-beta^2*rho_u)"
        ),
        "graph_derivative": (
            "(d_s,d_u)=(I-M)^(-1)*(K_s,0); ||Dh||<=d_u"
        ),
    }


def evaluate_matrix_lyapunov_perron_majorant(
    budget: MatrixLyapunovPerronInputBudget,
) -> MatrixLyapunovPerronEvaluation:
    """Evaluate the exact-rational two-component graph-transform budget."""

    block_values = asdict(budget.hessian_blocks)
    missing = [
        name
        for name in MATRIX_REQUIRED_FIELDS
        if getattr(budget, name) is None
    ]
    missing.extend(
        f"hessian_blocks.{name}"
        for name in HESSIAN_FIELD_NAMES
        if block_values[name] is None
    )
    formulas = _evaluation_formulas()

    scalar_fields = {
        "stable_power_rate_upper": budget.stable_power_rate_upper,
        "unstable_backward_rate_upper": budget.unstable_backward_rate_upper,
        "stable_power_constant_upper": budget.stable_power_constant_upper,
        "unstable_backward_power_constant_upper": (
            budget.unstable_backward_power_constant_upper
        ),
        "sequence_weight_beta": budget.sequence_weight_beta,
        "stable_seed_radius": budget.stable_seed_radius,
        "stable_graph_radius": budget.stable_graph_radius,
        "unstable_graph_radius": budget.unstable_graph_radius,
        "validated_return_map_split_ball_radius_lower": (
            budget.validated_return_map_split_ball_radius_lower
        ),
    }
    parsed = {
        name: _fraction(value, name) for name, value in scalar_fields.items()
    }
    blocks = {
        name: _fraction(block_values[name], f"hessian_blocks.{name}")
        for name in HESSIAN_FIELD_NAMES
    }
    for name, value in blocks.items():
        if value is not None and value < 0:
            raise ValueError(f"hessian_blocks.{name} must be nonnegative")
    if missing:
        return MatrixLyapunovPerronEvaluation(
            input_complete=False,
            missing_inputs=tuple(missing),
            input_order_conditions_hold=False,
            stable_kernel_coefficient_upper=None,
            unstable_kernel_coefficient_upper=None,
            unstable_quadratic_kernel_coefficient_upper=None,
            derivative_lipschitz_matrix_upper=None,
            perron_root_upper=None,
            canonical_positive_weight_lower=None,
            canonical_positive_weight_upper=None,
            weighted_row_sum_upper=None,
            nonlinear_value_vector_upper=None,
            self_map_image_vector_upper=None,
            self_map_slack_vector_lower=None,
            fixed_point_derivative_sequence_vector_upper=None,
            graph_height_upper=None,
            graph_derivative_upper=None,
            split_ball_contains_graph_box=False,
            contraction_closes=False,
            self_map_closes=False,
            graph_certificate_closes=False,
            formulas=formulas,
        )

    if any(value is None for value in parsed.values()) or any(
        value is None for value in blocks.values()
    ):
        raise AssertionError("a complete matrix budget contains a null field")
    numbers = {name: value for name, value in parsed.items() if value is not None}
    constants = {name: value for name, value in blocks.items() if value is not None}
    rho_s = numbers["stable_power_rate_upper"]
    rho_u = numbers["unstable_backward_rate_upper"]
    k_s = numbers["stable_power_constant_upper"]
    k_u = numbers["unstable_backward_power_constant_upper"]
    beta = numbers["sequence_weight_beta"]
    seed = numbers["stable_seed_radius"]
    radius_s = numbers["stable_graph_radius"]
    radius_u = numbers["unstable_graph_radius"]
    return_ball = numbers["validated_return_map_split_ball_radius_lower"]
    order = (
        0 < rho_s < beta < 1
        and 0 < rho_u < 1
        and k_s >= 1
        and k_u >= 1
        and 0 < seed <= radius_s
        and radius_u > 0
        and return_ball > 0
    )
    if not order:
        raise ValueError("the matrix budget violates rate, power, or radius order")

    a_s = k_s / (beta - rho_s)
    a_u = k_u * rho_u / (1 - beta * rho_u)
    a_u_two = k_u * rho_u / (1 - beta * beta * rho_u)

    c_s_ss = constants["stable_output_ss_upper"]
    c_s_su = constants["stable_output_su_upper"]
    c_s_uu = constants["stable_output_uu_upper"]
    c_u_ss = constants["unstable_output_ss_upper"]
    c_u_su = constants["unstable_output_su_upper"]
    c_u_uu = constants["unstable_output_uu_upper"]
    l_ss = c_s_ss * radius_s + c_s_su * radius_u
    l_su = c_s_su * radius_s + c_s_uu * radius_u
    l_us = c_u_ss * radius_s + c_u_su * radius_u
    l_uu = c_u_su * radius_s + c_u_uu * radius_u
    m11 = a_s * l_ss
    m12 = a_s * l_su
    m21 = a_u * l_us
    m22 = a_u * l_uu
    matrix = {
        "m_ss": _upper(m11),
        "m_su": _upper(m12),
        "m_us": _upper(m21),
        "m_uu": _upper(m22),
    }

    trace = m11 + m22
    discriminant = (m11 - m22) ** 2 + 4 * m12 * m21
    perron = (trace + _sqrt_fraction_upper(discriminant)) / 2
    determinant_i_minus_m = (1 - m11) * (1 - m22) - m12 * m21
    contraction = (
        m11 < 1 and m22 < 1 and determinant_i_minus_m > 0
    )

    q_s = (
        c_s_ss * radius_s * radius_s / 2
        + c_s_su * radius_s * radius_u
        + c_s_uu * radius_u * radius_u / 2
    )
    q_u = (
        c_u_ss * radius_s * radius_s / 2
        + c_u_su * radius_s * radius_u
        + c_u_uu * radius_u * radius_u / 2
    )
    image_s = k_s * seed + a_s * q_s
    image_u = a_u * q_u
    slack_s = radius_s - image_s
    slack_u = radius_u - image_u
    self_map = slack_s >= 0 and slack_u >= 0
    split_ball = radius_s + radius_u <= return_ball
    height = a_u_two * q_u

    weight_lower = None
    weight_upper = None
    weighted_row = None
    derivative = None
    derivative_u = None
    if contraction:
        numerator_w_s = 1 - m22 + m12
        numerator_w_u = 1 - m11 + m21
        w_s = numerator_w_s / determinant_i_minus_m
        w_u = numerator_w_u / determinant_i_minus_m
        row_s = (m11 * w_s + m12 * w_u) / w_s
        row_u = (m21 * w_s + m22 * w_u) / w_u
        weighted_row_value = max(row_s, row_u)
        d_s = (1 - m22) * k_s / determinant_i_minus_m
        d_u = m21 * k_s / determinant_i_minus_m
        weight_lower = {"stable": _lower(w_s), "unstable": _lower(w_u)}
        weight_upper = {"stable": _upper(w_s), "unstable": _upper(w_u)}
        weighted_row = _upper(weighted_row_value)
        derivative = {"stable": _upper(d_s), "unstable": _upper(d_u)}
        derivative_u = _upper(d_u)

    closes = contraction and self_map and split_ball
    return MatrixLyapunovPerronEvaluation(
        input_complete=True,
        missing_inputs=(),
        input_order_conditions_hold=True,
        stable_kernel_coefficient_upper=_upper(a_s),
        unstable_kernel_coefficient_upper=_upper(a_u),
        unstable_quadratic_kernel_coefficient_upper=_upper(a_u_two),
        derivative_lipschitz_matrix_upper=matrix,
        perron_root_upper=_upper(perron),
        canonical_positive_weight_lower=weight_lower,
        canonical_positive_weight_upper=weight_upper,
        weighted_row_sum_upper=weighted_row,
        nonlinear_value_vector_upper={
            "stable": _upper(q_s),
            "unstable": _upper(q_u),
        },
        self_map_image_vector_upper={
            "stable": _upper(image_s),
            "unstable": _upper(image_u),
        },
        self_map_slack_vector_lower={
            "stable": _lower(slack_s),
            "unstable": _lower(slack_u),
        },
        fixed_point_derivative_sequence_vector_upper=derivative,
        graph_height_upper=_upper(height),
        graph_derivative_upper=derivative_u,
        split_ball_contains_graph_box=split_ball,
        contraction_closes=contraction,
        self_map_closes=self_map,
        graph_certificate_closes=closes,
        formulas=formulas,
    )


def _load_parent(
    repository: Path, relative: str, expected_hash: str, label: str
) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise ValueError(f"the bound {label} result changed")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the bound {label} result is malformed")
    return payload


def build_stage4_projected_return_contract(
    repository: Path,
) -> Stage4ProjectedReturnContract:
    repository = repository.resolve()
    stage2 = _load_parent(
        repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256, "Stage-2"
    )
    stage3 = _load_parent(
        repository, STAGE3_RESULT_RELATIVE_PATH, STAGE3_RESULT_SHA256, "Stage-3"
    )
    validate_stage2_stable_manifold_result(stage2, repository)
    validate_stage3_stable_projection_result(stage3, repository)
    stage2_contract = _mapping(stage2.get("contract"), "Stage-2 contract")
    spectral = _mapping(
        stage2_contract.get("strengthened_gamma01_spectral_ingress"),
        "strengthened Stage-2 spectral ingress",
    )
    stage3_certificate = _mapping(
        stage3.get("certificate"), "Stage-3 certificate"
    )
    geometry = _mapping(
        stage3_certificate.get("projection_geometry"), "Stage-3 geometry"
    )
    if geometry.get("stable_projection_norm_lower") != "2":
        raise ValueError("the Stage-3 projection lower bound changed")

    blocks = ProjectedReturnHessianBlockBudget(
        stable_output_ss_upper=None,
        stable_output_su_upper=None,
        stable_output_uu_upper=None,
        unstable_output_ss_upper=None,
        unstable_output_su_upper=None,
        unstable_output_uu_upper=None,
        evidence_status=(
            "open: no interval first/second-variational return enclosure has "
            "yet supplied the six projected block bounds"
        ),
    )
    budget = MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=str(
            spectral["working_stable_power_rate_upper"]
        ),
        unstable_backward_rate_upper=str(
            spectral["unstable_backward_rate_upper"]
        ),
        stable_power_constant_upper=None,
        unstable_backward_power_constant_upper=str(
            spectral["unstable_dichotomy_constant_upper_intrinsic"]
        ),
        sequence_weight_beta=str(spectral["sequence_weight_beta"]),
        stable_seed_radius="0.0002",
        stable_graph_radius="0.0010",
        unstable_graph_radius="0.0007",
        validated_return_map_split_ball_radius_lower=None,
        hessian_blocks=blocks,
        evidence_status=(
            "partial adapter: Stage-2 rates are validated; the stable power "
            "constant, split return ball, and Hessian blocks remain open"
        ),
    )
    evaluation = evaluate_matrix_lyapunov_perron_majorant(budget)
    if evaluation.input_complete or evaluation.graph_certificate_closes:
        raise AssertionError("the incomplete Stage-4 adapter was promoted")

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4ProjectedReturnContract(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        split_coordinate_norm=(
            "||(x_s,x_u)||_split=||x_s||_Y+|x_u|, with x_s in E_s and "
            "x_u in the one-dimensional E_u coordinate"
        ),
        parent_result_sha256={
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        },
        hessian_block_budget=asdict(blocks),
        matrix_input_budget=asdict(budget),
        matrix_evaluation=asdict(evaluation),
        variational_equation_contract={
            "first_variation": (
                "dU_h/dt=DF(X_t) U_h,t with U_h,0=h"
            ),
            "second_variation": (
                "dV_hk/dt=DF(X_t) V_hk,t+D2F(X_t)[U_h,t,U_k,t], "
                "with V_hk,0=0"
            ),
            "fast_current_voltage_hessian": (
                "-2*v(t)-6*epsilon*kappa_3*(v(t)-1)"
            ),
            "fast_delayed_voltage_hessian_each_delay": (
                "3*epsilon*kappa_3*(v(t-tau_j)-1), j=0,1"
            ),
            "mixed_and_recovery_hessian_entries": "zero",
            "fast_current_voltage_third_derivative": (
                "-2-6*epsilon*kappa_3"
            ),
            "fast_delayed_voltage_third_derivative_each_delay": (
                "3*epsilon*kappa_3, j=0,1"
            ),
            "time_orientation": (
                "physical time on history segments; normalized Fourier phase "
                "derivatives cannot be substituted"
            ),
        },
        return_event_contract={
            "section": "affine Route-C history section h_C=0",
            "return_orientation": (
                "first positive physical return near one period, with no "
                "earlier section hit on the validated tube"
            ),
            "event_speed": "a=Dh_C[dot(X_T)]>0 uniformly on the return tube",
            "first_return_time_variation": (
                "tau_h=-Dh_C[U_h(T)]/a"
            ),
            "second_event_core": (
                "W_hk=V_hk(T)+dot(U_h)(T)*tau_k+dot(U_k)(T)*tau_h+"
                "ddot(X_T)*tau_h*tau_k"
            ),
            "second_return_time_variation": (
                "tau_hk=-Dh_C[W_hk]/a"
            ),
            "return_hessian": (
                "D2P[h,k]=W_hk+dot(X_T)*tau_hk"
            ),
            "history_segment_requirement": (
                "all values, first variations, time derivatives, and second "
                "variations are enclosed as complete returned histories"
            ),
        },
        projected_propagator_certificate_interface={
            "input_space": (
                "the Route-C section split E_s direct-sum E_u, with E_u one "
                "dimensional and the declared split norm"
            ),
            "required_linear_outputs": (
                "direct stable propagator powers K_s*rho_s^n; direct unstable "
                "backward powers K_u*rho_u^n; physical-time return traces of "
                "U_s,U_u,dot(U_s),dot(U_u)"
            ),
            "required_second_variations": "V_ss, V_su, V_uu",
            "required_event_traces": (
                "tau_s,tau_u,W_ss,W_su,W_uu,tau_ss,tau_su,tau_uu"
            ),
            "required_projected_outputs": (
                "Pi_s D2P(ss), Pi_s D2P(su), Pi_s D2P(uu), "
                "Pi_u D2P(ss), Pi_u D2P(su), Pi_u D2P(uu)"
            ),
            "projection_order": (
                "apply the stable-history and unstable-scalar output "
                "coordinates before taking operator norms"
            ),
            "required_domain": (
                "one validated split return ball containing the entire graph box"
            ),
            "acceptable_proof_engine": (
                "directed method-of-steps, interval Taylor, or equivalent "
                "continuous-history enclosures with tail and event control"
            ),
            "insufficient_evidence": (
                "finite sampled variational matrices, binary SVDs, or an old "
                "sup-norm C2 constant transferred by norm equivalence"
            ),
        },
        adapted_norm_transfer_audit={
            "old_to_split_equivalence": (
                "||x||_old<=||x||_split<=(p_s_old+p_u_old)||x||_old"
            ),
            "black_box_hessian_transfer": (
                "C_split<=(p_s_old+p_u_old)*C_old"
            ),
            "projection_isometry_alone_guarantees_improvement": False,
            "direct_six_block_route_avoids_global_equivalence_factor": True,
            "section_or_quotient_coordinates_required": True,
        },
        radius_design_target={
            "stable_component_radius": "0.0010",
            "unstable_component_radius": "0.0007",
            "split_total_radius": "0.0017",
            "motivation": (
                "a graph radius above 1.7e-3 would make the wider diagnostic "
                "third-return crossing bracket relevant"
            ),
            "validated": False,
            "used_in_any_crossing_or_onset_claim": False,
        },
        claim_status=claims,
    )


def build_stage4_projected_return_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    contract = asdict(build_stage4_projected_return_contract(repository))
    return {
        "contract": contract,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "contract_sha256": canonical_sha256(contract),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
                STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "arithmetic": "fractions.Fraction plus directed Decimal output",
            },
        },
    }


def validate_stage4_projected_return_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"contract", "manifest"}:
        raise ValueError("the Stage-4 result has the wrong outer schema")
    contract = _mapping(payload.get("contract"), "Stage-4 contract")
    manifest = _mapping(payload.get("manifest"), "Stage-4 manifest")
    if set(contract) != {
        field.name for field in fields(Stage4ProjectedReturnContract)
    }:
        raise ValueError("the Stage-4 contract schema changed")
    if (
        contract.get("schema_id") != SCHEMA_ID
        or contract.get("model_id") != MODEL_ID
        or contract.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4 identity changed")

    claims = _mapping(contract.get("claim_status"), "Stage-4 claim status")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4 claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a registered Stage-4 contract statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4 theorem gate was promoted")

    blocks = _mapping(
        contract.get("hessian_block_budget"), "Stage-4 Hessian budget"
    )
    if set(blocks) != set(HESSIAN_FIELD_NAMES) | {"evidence_status"}:
        raise ValueError("the six-block Hessian schema changed")
    if any(blocks.get(name) is not None for name in HESSIAN_FIELD_NAMES):
        raise ValueError("an unvalidated projected Hessian block was filled")
    budget = _mapping(
        contract.get("matrix_input_budget"), "Stage-4 matrix budget"
    )
    if budget.get("stable_power_constant_upper") is not None:
        raise ValueError("an unvalidated stable power constant was filled")
    if budget.get("validated_return_map_split_ball_radius_lower") is not None:
        raise ValueError("an unvalidated split return ball was filled")
    evaluation = _mapping(
        contract.get("matrix_evaluation"), "Stage-4 matrix evaluation"
    )
    expected_missing = {
        "stable_power_constant_upper",
        "validated_return_map_split_ball_radius_lower",
        *(f"hessian_blocks.{name}" for name in HESSIAN_FIELD_NAMES),
    }
    if (
        evaluation.get("input_complete") is not False
        or evaluation.get("graph_certificate_closes") is not False
        or set(evaluation.get("missing_inputs", ())) != expected_missing
    ):
        raise ValueError("the incomplete Stage-4 matrix evaluation was promoted")
    radius = _mapping(
        contract.get("radius_design_target"), "Stage-4 radius target"
    )
    if (
        radius.get("split_total_radius") != "0.0017"
        or radius.get("validated") is not False
        or radius.get("used_in_any_crossing_or_onset_claim") is not False
    ):
        raise ValueError("the Stage-4 design radius was promoted")
    interface = _mapping(
        contract.get("projected_propagator_certificate_interface"),
        "Stage-4 projected propagator interface",
    )
    outputs = str(interface.get("required_projected_outputs"))
    if outputs.count("D2P(") != 6:
        raise ValueError("the six projected Hessian outputs changed")
    return_event = _mapping(
        contract.get("return_event_contract"), "Stage-4 return event contract"
    )
    if "first positive physical return" not in str(
        return_event.get("return_orientation")
    ):
        raise ValueError("the physical first-return orientation changed")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "contract_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-4 manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "contract_sha256": canonical_sha256(contract),
        "parent_result_sha256": {
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        },
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4 manifest fixed data changed")
    repository = repository.resolve()
    source_hashes = _mapping(
        manifest.get("source_sha256"), "Stage-4 source manifest"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4 source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4 source changed: {relative}")
    for relative, digest in fixed["parent_result_sha256"].items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4 parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "HESSIAN_FIELD_NAMES",
    "MatrixLyapunovPerronEvaluation",
    "MatrixLyapunovPerronInputBudget",
    "NOTE_RELATIVE_PATH",
    "ProjectedReturnHessianBlockBudget",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "Stage4ProjectedReturnContract",
    "TRUE_FLAGS",
    "build_stage4_projected_return_contract",
    "build_stage4_projected_return_result",
    "canonical_sha256",
    "evaluate_matrix_lyapunov_perron_majorant",
    "validate_stage4_projected_return_result",
]
