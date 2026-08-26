"""Stage-5G-a source-bound endpoint functional-coordinate certificate.

This module promotes the two endpoint computations from the former Stage-5G
feasibility pilot to a directed, source-bound theorem.  It evaluates the
complete Stage-5C selected-event histories at both exact pulse endpoints,
centres each history before taking a norm, and applies the same Stage-4D/4E
atom--density row and Stage-5E physical phase in numerator and denominator.

The result proves signs of ``f_phys(kappa(J_-))`` and
``f_phys(kappa(J_+))``.  It also records complete-history bounds for the two
stable projections and a *conditional* graph-height target.  It deliberately
does not claim a quantitative stable graph, stable-gap endpoint signs, a
stable-sheet crossing, biological onset, routing, capture, or safety.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_pulse_event_aligned_derivative_stage5d import (
    PRECISION_BITS,
    _event_time_polynomial,
    _fraction_interval,
    validate_stage5d_result,
)
from canard_control.leaky_pulse_oriented_adjoint_action_stage5e import (
    _CellLocator,
    _density_box,
    _directed_sum,
    _history_segments,
    _mapping,
    _q_phys_box,
    _serialized_phase_data,
    _state_component,
    _symmetric,
    validate_stage5e_result,
)
from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    build_coefficient_propagation,
    build_remainder_propagation,
    validate_directed_jet_result,
)
from canard_control.leaky_pulse_route_c_event_stage5c import (
    _power_range,
    validate_stage5c_result,
)
from canard_control.leaky_pulse_stable_gap_slope_bridge_stage5f import (
    validate_stage5f_result,
)
from canard_control.leaky_route_c_adjoint_stage4d import validate_stage4d_result
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    _adjoint_mode_rows,
    _centre_data,
    _guide_density_dictionary,
    _model_uncertainty,
    _row_tail_neumann,
    validate_stage4e_result,
)


SCHEMA_ID = "leaky-pulse-endpoint-functional-stage5ga-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_route_c_event"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_endpoint_functional_stage5ga.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_endpoint_functional_stage5ga.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_endpoint_functional_stage5ga.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-endpoint-functional-stage5ga.md"
CONTRACT_RELATIVE_PATH = "docs/leaky-pulse-centered-gap-stage5g-contract.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_endpoint_functional_stage5ga.py"
)

STAGE5B_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_parameter_jet_directed_enclosure.json"
)
STAGE3_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_projection_stage3.json"
)
STAGE4D_RELATIVE_PATH = "experiments/results/leaky_route_c_adjoint_stage4d.json"
STAGE4E_RELATIVE_PATH = (
    "experiments/results/leaky_shared_yqq_deflation_stage4e.json"
)
STAGE5C_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_route_c_event_stage5c.json"
)
STAGE5D_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_event_aligned_derivative_stage5d.json"
)
STAGE5E_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_oriented_adjoint_action_stage5e.json"
)
STAGE5F_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_stable_gap_slope_bridge_stage5f.json"
)

STAGE5B_SHA256 = "71276785fd803b663fc11de9489751ccd53dd8a408323a0bb140d0c9e7b7862b"
STAGE3_SHA256 = "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
STAGE4D_SHA256 = "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
STAGE4E_SHA256 = "ccdd6023f911e97785ec6f8be97b84d725d6af9f5051e1da602380d225e47acc"
STAGE5C_SHA256 = "f1f198d68cb736bc9b5a48a0bff3eb5a93d39ee3f0b8f7cb6f7e07779483128d"
STAGE5D_SHA256 = "e8be485b8b4711a0ae0b1f3ec875f704c509d9ba0abd5b2166a2384567ed654e"
STAGE5E_SHA256 = "187b8c6d614aa87c68442acb9f5d472233907c31f0df8a1c8d29dfc6941743be"
STAGE5F_SHA256 = "26acd6d9421a8bf60d5bb96fe4c68918b39f89a443973dd728fed17ccf48652b"

PARENT_SHA256 = {
    STAGE5B_RELATIVE_PATH: STAGE5B_SHA256,
    STAGE3_RELATIVE_PATH: STAGE3_SHA256,
    STAGE4D_RELATIVE_PATH: STAGE4D_SHA256,
    STAGE4E_RELATIVE_PATH: STAGE4E_SHA256,
    STAGE5C_RELATIVE_PATH: STAGE5C_SHA256,
    STAGE5D_RELATIVE_PATH: STAGE5D_SHA256,
    STAGE5E_RELATIVE_PATH: STAGE5E_SHA256,
    STAGE5F_RELATIVE_PATH: STAGE5F_SHA256,
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    CONTRACT_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_inner_stable_projection_stage3.py",
    "src/canard_control/leaky_route_c_adjoint_stage4d.py",
    "src/canard_control/leaky_shared_yqq_deflation_stage4e.py",
    "src/canard_control/leaky_pulse_parameter_jet_directed_enclosure.py",
    "src/canard_control/leaky_pulse_route_c_event_stage5c.py",
    "src/canard_control/leaky_pulse_event_aligned_derivative_stage5d.py",
    "src/canard_control/leaky_pulse_oriented_adjoint_action_stage5e.py",
    "src/canard_control/leaky_pulse_stable_gap_slope_bridge_stage5f.py",
)

EXPECTED_PYTHON_VERSION = "3.14.4"
EXPECTED_GMPY2_VERSION = "2.2.2"
EXPECTED_MPFR_VERSION = "MPFR 4.2.1"
EXPECTED_NUMPY_VERSION = "2.5.2"
EXPECTED_SCIPY_VERSION = "1.18.0"
EXPECTED_OPENBLAS_NUM_THREADS = "8"
EXPECTED_OMP_NUM_THREADS = "1"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 "
    "PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 "
    "experiments/leaky_pulse_endpoint_functional_stage5ga.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR; exact one-sided endpoint shards containing xi=-1 "
    "and xi=+1; Stage-5C fourth-order event graph with its full remainder; "
    "512 continuous-history cells over both delay pieces; exact residual "
    "centering before norms; the common Stage-4D/4E finite-plus-Neumann-tail "
    "atom-density row; Stage-5E physical phase; and a direct source-bound "
    "q_phys Y-norm checked below the registered Stage-5F Wiener bound"
)

J0 = Fraction(2409, 8000)
PARAMETER_HALF_WIDTH = Fraction(3, 40000)
PARAMETER_INTERVAL = (
    J0 - PARAMETER_HALF_WIDTH,
    J0 + PARAMETER_HALF_WIDTH,
)
ENDPOINT_WIDTH = Fraction(1, 2**30)
GRAPH_HEIGHT_TARGET = Fraction(1, 1_000)
ENDPOINT_CENTERS = {
    -1: "0.021366541445",
    1: "-0.016474080047",
}

HISTORY_SPACE = (
    "Y=C([-5*sqrt(5),0],R) x R with "
    "||(phi,w)||_Y=max(||phi||_infinity,|w|)"
)
SECTION_SPACE = (
    "Sigma={y in Y:y_v(0)=0}, with q_phys in Sigma and "
    "P_s=I-q_phys*f_phys"
)
PARAMETER_SCOPE = {
    "center_J0_exact": "2409/8000",
    "half_width_h_exact": "3/40000",
    "interval_exact": "I_J=[6021/20000,753/2500]",
    "normalized_parameter": "J=J0+h*xi with xi in [-1,1]",
    "endpoint_values_exact": {
        "minus": "6021/20000",
        "plus": "753/2500",
    },
}
COORDINATE_REGISTRATION = {
    "event_history": (
        "K(J) is the unique Stage-5C selected late-window Route-C "
        "event-aligned complete history"
    ),
    "reference_history": (
        "X_* is the exact inner periodic-orbit history at the identical "
        "Route-C phase-zero section"
    ),
    "centered_history": "kappa(J)=K(J)-X_* in Sigma",
    "physical_column": "q=q_phys=q_tilde/gamma",
    "physical_functional": "f=f_phys(y)=gamma*ell(y)/ell(q_tilde)",
    "normalization": "f_phys(q_phys)=1 exactly",
    "projection": "P_s=I-q_phys*f_phys on Sigma",
    "global_affine_section_splitting": (
        "C:Sigma->ker(f_phys)xR, C(kappa)=(P_s*kappa,f_phys(kappa))"
    ),
    "global_affine_section_splitting_inverse": "C^{-1}(z,u)=z+q_phys*u",
    "global_affine_section_splitting_is_bounded_linear_isomorphism": True,
    "ambient_chart_consequence": (
        "the registered affine coordinates are global on Sigma; evaluating "
        "the local stable gap only requires P_s*kappa to lie in dom(psi)"
    ),
    "endpoint_gap_not_yet_defined": (
        "H(J)=f_phys(kappa(J))-psi(P_s kappa(J)) requires a future "
        "quantitative graph psi"
    ),
}
BRANCH_REGULARITY = {
    "event_window": "the common late Route-C window registered by Stage 5C",
    "one_event_for_every_parameter": True,
    "event_switching_inside_window": False,
    "Y_valued_regularity": "K:I_J->Y is continuously differentiable",
    "source_split": (
        "Stage 5C proves one transverse event in the common window; Stage 5D "
        "proves the continuous Y-valued derivative of that event branch"
    ),
    "ordinal_third_crossing_validated": False,
}
ENDPOINT_EVALUATION_CONTRACT = {
    "endpoint_quantifier": (
        "for each sigma in {-1,+1}, every xi in the recorded one-sided "
        "positive-width shard is enclosed; in particular the exact xi=sigma "
        "endpoint is enclosed"
    ),
    "history_quantifier": (
        "for every theta in [-5*sqrt(5),0], the complete voltage history and "
        "the current recovery coordinate are enclosed"
    ),
    "endpoint_width_exact": "1/1073741824",
    "history_subdivision_count": 512,
    "history_subdivisions_per_delay_piece": 256,
    "delay_piece_count": 2,
    "density_dictionary_count": 4,
    "finite_parameter_sampling_used": False,
    "finite_history_sampling_used": False,
    "event_time_remainder_retained": True,
    "inner_orbit_uncertainty_retained": True,
    "recovery_atom_retained": True,
    "direct_and_omitted_density_dictionaries_kept_separate": True,
    "delay_and_history_seams_retained": True,
    "residual_formed_before_norm_or_absolute_value": True,
    "centers_are_exact_decimal_rationals": True,
    "binary64_midpoint_used_as_proof_data": False,
}
VOLTAGE_ATOM_ZERO_IDENTITY = {
    "pulse_section": "K_v(J,0)=V_true(0) exactly",
    "inner_section": "X_*v(0)=V_true(0) exactly",
    "unstable_column_section": "q_phys_v(0)=0 exactly",
    "residual_section": "r_sigma,v(0)=0 exactly",
    "voltage_current_atom_action": "0",
    "atom_v_omitted_only_by_these_exact_identities": True,
}
STAGE5F_BRIDGE_INTERFACE = {
    "same_history_space_and_projection": True,
    "conditional_derivative_interval_imported": {
        "lower": "-494.38777064344581684429268439849118579779001016259761314597835",
        "upper": "-9.61222935655418315570731560150881420220998983740238685418223374",
    },
    "derivative_status": (
        "conditional only: a quantitative graph, full-interval stable-coordinate "
        "graph-domain containment and sup||Dpsi||<=16 remain open"
    ),
}
THEOREM_STATEMENT = (
    "For the two exact endpoints of the Stage-5C selected late-window Route-C "
    "event branch, the complete centered histories satisfy the displayed "
    "source-bound intervals f_phys(kappa(J_-))>0 and "
    "f_phys(kappa(J_+))<0.  The displayed complete-history bounds on "
    "P_s kappa(J_-) and P_s kappa(J_+) use a direct 512-segment q_phys norm "
    "proved below the registered Stage-5F Wiener bound.  If a future graph in "
    "the identical normalization has endpoint height at most 10^-3, these "
    "functional signs imply opposite stable-gap endpoint signs.  No graph, "
    "stable-gap sign, stable-sheet crossing, onset, routing, capture, or "
    "safety conclusion is asserted here."
)

TRUE_FLAGS = (
    "stage5b_stage3_stage4d_stage4e_stage5c_stage5d_stage5e_stage5f_source_bound",
    "selected_event_is_one_C1_branch_without_window_switching",
    "exact_endpoint_shards_and_complete_histories_enclosed",
    "identical_physical_phase_and_same_adjoint_row_used",
    "recovery_atom_and_all_density_pieces_retained",
    "voltage_atom_zero_by_exact_section_identities",
    "endpoint_residuals_formed_before_norms",
    "direct_512_segment_q_phys_Y_norm_validated",
    "direct_q_norm_below_stage5f_registered_wiener_bound_validated",
    "endpoint_functional_intervals_validated",
    "endpoint_functional_signs_validated",
    "endpoint_stable_projection_norms_validated",
    "conditional_graph_height_target_admissible_validated",
    "stage5f_conditional_derivative_interval_imported_without_renormalization",
    "global_affine_route_c_section_splitting_validated",
    "finite_sampling_excluded_from_endpoint_proof",
)
FALSE_FLAGS = (
    "quantitative_inner_stable_graph_validated",
    "full_interval_stable_coordinate_graph_domain_containment_validated",
    "stable_gap_endpoint_signs_validated",
    "unconditional_stable_gap_derivative_excludes_zero_validated",
    "unique_selected_event_stable_sheet_crossing_validated",
    "interval_newton_strict_inclusion_validated",
    "ordinal_third_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_radius_validated",
)

if set(TRUE_FLAGS) & set(FALSE_FLAGS):
    raise RuntimeError("Stage-5G-a claim groups overlap")
if len(TRUE_FLAGS) != len(set(TRUE_FLAGS)) or len(FALSE_FLAGS) != len(set(FALSE_FLAGS)):
    raise RuntimeError("Stage-5G-a claim groups contain duplicates")

# Frozen after a cold source replay.  It binds all proof-bearing endpoint and
# common-row numerics independently of the top-level certificate digest.
EXPECTED_NUMERIC_CORE_SHA256 = (
    "06f1ae1018185b0b137695f8be90c8a614bd99b21464b789127b98bbb2323d12"
)


@dataclass(frozen=True)
class Stage5GAEndpointFunctionalCertificate:
    schema_id: str
    model_id: str
    branch: str
    history_space: str
    section_tangent_space: str
    parameter_scope: dict[str, Any]
    coordinate_registration: dict[str, Any]
    branch_regularity: dict[str, Any]
    endpoint_evaluation_contract: dict[str, Any]
    voltage_atom_zero_identity: dict[str, Any]
    common_row_and_q_ledger: dict[str, Any]
    endpoints: list[dict[str, Any]]
    conditional_graph_height_target: dict[str, Any]
    stage5f_bridge_interface: dict[str, Any]
    theorem_statement: str
    claim_status: dict[str, bool]


TOP_KEYS = ("certificate", "manifest")
CERTIFICATE_KEYS = tuple(
    field.name
    for field in Stage5GAEndpointFunctionalCertificate.__dataclass_fields__.values()
)
MANIFEST_KEYS = (
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "precision_bits",
    "python",
    "gmpy2",
    "mpfr",
    "numpy",
    "scipy",
    "openblas_num_threads",
    "omp_num_threads",
    "parent_sha256",
    "source_sha256",
    "dependency_source_sha256",
    "numeric_core_sha256",
    "certificate_sha256",
)
COMMON_LEDGER_KEYS = (
    "same_exact_row_in_residual_and_denominator",
    "same_physical_phase_as_stage5e_and_stage5f",
    "denominator_source",
    "denominator_modulus_lower",
    "stage4e_denominator_modulus_lower",
    "history_measure_difference_source",
    "history_measure_difference_upper",
    "direct_q_norm_method",
    "direct_q_phys_Y_norm_upper",
    "stage5f_registered_q_phys_Y_norm_upper",
    "direct_q_norm_below_stage5f_bound",
    "stable_projection_uses_q_norm",
    "physical_phase_gamma_box",
)
ENDPOINT_KEYS = (
    "name",
    "xi_endpoint_exact",
    "J_endpoint_exact",
    "one_sided_xi_interval_exact",
    "one_sided_width_exact",
    "exact_endpoint_included",
    "chosen_residual_center_exact",
    "event_time_interval",
    "residual_guide_action",
    "residual_Y_norm_upper",
    "common_measure_error_upper",
    "numerator_modulus_upper",
    "functional_radius_upper",
    "functional_interval",
    "functional_sign",
    "functional_sign_margin_lower",
    "stable_projection_identity",
    "stable_projection_Y_norm_upper",
)
INTERVAL_KEYS = ("lower", "upper")
COMPLEX_KEYS = ("real", "imag")
GRAPH_TARGET_KEYS = (
    "future_graph_height_hypothesis",
    "common_height_target_exact",
    "left_conditional_stable_gap_margin_lower",
    "right_conditional_stable_gap_margin_lower",
    "conditional_implication",
    "quantitative_graph_supplied_here",
    "stable_gap_endpoint_signs_claimed_here",
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


def _runtime_record() -> dict[str, str | None]:
    return {
        "python": platform.python_version(),
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
    }


def _require_runtime() -> dict[str, str]:
    expected = {
        "python": EXPECTED_PYTHON_VERSION,
        "gmpy2": EXPECTED_GMPY2_VERSION,
        "mpfr": EXPECTED_MPFR_VERSION,
        "numpy": EXPECTED_NUMPY_VERSION,
        "scipy": EXPECTED_SCIPY_VERSION,
        "openblas_num_threads": EXPECTED_OPENBLAS_NUM_THREADS,
        "omp_num_threads": EXPECTED_OMP_NUM_THREADS,
    }
    actual = _runtime_record()
    if actual != expected:
        raise RuntimeError(
            f"the Stage-5G-a replay environment changed: {actual} != {expected}"
        )
    return expected


def _exact_mapping(value: Any, name: str, keys: Sequence[str]) -> Mapping[str, Any]:
    mapped = _mapping(value, name)
    if set(mapped) != set(keys):
        raise ValueError(f"{name} keys changed")
    return mapped


def _load_bound_json(repository: Path, relative: str, expected_sha: str) -> dict[str, Any]:
    path = repository / relative
    actual = _sha256_path(path)
    if actual != expected_sha:
        raise ValueError(
            f"Stage-5G-a source-bound parent changed: {relative}: "
            f"{actual} != {expected_sha}"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Stage-5G-a parent {relative} is not a JSON object")
    return payload


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower),
        "upper": decimal_upper(value.upper),
    }


def _complex_record(value: DirectedComplexInterval) -> dict[str, dict[str, str]]:
    return {
        "real": _interval_record(value.real),
        "imag": _interval_record(value.imag),
    }


def _parse_interval(value: Any, name: str) -> DirectedInterval:
    record = _exact_mapping(value, name, INTERVAL_KEYS)
    result = DirectedInterval.from_bounds(
        str(record["lower"]), str(record["upper"]), PRECISION_BITS
    )
    if not gmpy2.is_finite(result.lower) or not gmpy2.is_finite(result.upper):
        raise ValueError(f"{name} must be finite")
    return result


def _parse_complex(value: Any, name: str) -> DirectedComplexInterval:
    record = _exact_mapping(value, name, COMPLEX_KEYS)
    return DirectedComplexInterval(
        _parse_interval(record["real"], f"{name} real"),
        _parse_interval(record["imag"], f"{name} imag"),
    )


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def _orbit_box(
    data: Any,
    uncertainty: Mapping[str, float],
    theta: DirectedInterval,
    *,
    voltage: bool,
) -> DirectedInterval:
    dictionary = data.orbit_v if voltage else data.orbit_w
    raw = _density_box((dictionary,), theta, data.period, data.root)
    error = DirectedInterval.from_decimal(
        str(uncertainty["orbit_error"]), PRECISION_BITS
    ).upper
    return raw.real + _symmetric(error)


def _endpoint_box(sign: int) -> tuple[DirectedInterval, DirectedInterval]:
    if sign == -1:
        return (
            _fraction_interval(Fraction(-1), PRECISION_BITS),
            _fraction_interval(Fraction(-1) + ENDPOINT_WIDTH, PRECISION_BITS),
        )
    if sign == 1:
        return (
            _fraction_interval(Fraction(1) - ENDPOINT_WIDTH, PRECISION_BITS),
            _fraction_interval(Fraction(1), PRECISION_BITS),
        )
    raise ValueError("Stage-5G-a endpoint sign must be -1 or +1")


def _validated_parent_ingress(repository: Path) -> dict[str, Mapping[str, Any]]:
    repository = Path(repository).resolve()
    parents = {
        "stage5b": _load_bound_json(repository, STAGE5B_RELATIVE_PATH, STAGE5B_SHA256),
        "stage3": _load_bound_json(repository, STAGE3_RELATIVE_PATH, STAGE3_SHA256),
        "stage4d": _load_bound_json(repository, STAGE4D_RELATIVE_PATH, STAGE4D_SHA256),
        "stage4e": _load_bound_json(repository, STAGE4E_RELATIVE_PATH, STAGE4E_SHA256),
        "stage5c": _load_bound_json(repository, STAGE5C_RELATIVE_PATH, STAGE5C_SHA256),
        "stage5d": _load_bound_json(repository, STAGE5D_RELATIVE_PATH, STAGE5D_SHA256),
        "stage5e": _load_bound_json(repository, STAGE5E_RELATIVE_PATH, STAGE5E_SHA256),
        "stage5f": _load_bound_json(repository, STAGE5F_RELATIVE_PATH, STAGE5F_SHA256),
    }
    validate_directed_jet_result(parents["stage5b"], repository)
    validate_stage3_stable_projection_result(parents["stage3"], repository)
    validate_stage4d_result(parents["stage4d"], repository)
    validate_stage4e_result(parents["stage4e"], repository)
    validate_stage5c_result(parents["stage5c"], repository)
    validate_stage5d_result(parents["stage5d"], repository)
    validate_stage5e_result(parents["stage5e"], repository)
    validate_stage5f_result(parents["stage5f"], repository)

    stage5b_claims = _mapping(
        parents["stage5b"]["certificate"]["claim_status"], "Stage-5B claims"
    )
    if stage5b_claims.get("fixed_time_wide_parameter_taylor_model_validated") is not True:
        raise ValueError("Stage-5B fixed-time family is unavailable")

    stage3_certificate = _mapping(parents["stage3"]["certificate"], "Stage-3 certificate")
    if stage3_certificate.get("section") != (
        "Sigma={phi_v(0)=0} at the exact Route-C phase-zero crossing"
    ):
        raise ValueError("Stage-3 Route-C section changed")

    stage4d_claims = _mapping(
        parents["stage4d"]["artifact"]["claim_status"], "Stage-4D claims"
    )
    if stage4d_claims.get("history_atom_density_measure_numeric_enclosed") is not True:
        raise ValueError("Stage-4D atom-density measure is unavailable")

    correlated = _mapping(
        parents["stage4e"]["artifact"]["continuous_history_correlated_deflation"],
        "Stage-4E correlated row",
    )
    if correlated.get("same_adjoint_coefficients_in_numerator_and_denominator") is not True:
        raise ValueError("Stage-4E same-row identity changed")

    stage5c_certificate = _mapping(parents["stage5c"]["certificate"], "Stage-5C certificate")
    stage5c_claims = _mapping(stage5c_certificate["claim_status"], "Stage-5C claims")
    for required in (
        "route_c_exact_phase_zero_level_source_bound",
        "one_and_only_one_route_c_event_in_declared_bracket_for_every_J_validated",
        "uniform_positive_event_speed_on_whole_event_bracket_validated",
        "common_event_complete_history_pullback_defined_in_Y",
        "common_event_complete_history_tube_validated",
    ):
        if stage5c_claims.get(required) is not True:
            raise ValueError(f"Stage-5C ingress omitted {required}")
    if stage5c_claims.get("declared_event_proved_to_be_the_third_post_release_crossing") is not False:
        raise ValueError("Stage-5C selected event was promoted to an ordinal crossing")
    route_section = _mapping(stage5c_certificate["route_c_section"], "Stage-5C section")
    if route_section.get("formula") != "h_C(phi)=phi_v(0)-V_true(0)":
        raise ValueError("Stage-5C exact Route-C section changed")

    stage5d_certificate = _mapping(parents["stage5d"]["certificate"], "Stage-5D certificate")
    stage5d_claims = _mapping(stage5d_certificate["claim_status"], "Stage-5D claims")
    for required in (
        "continuous_event_aligned_complete_history_J_derivative_enclosed_in_Y",
        "event_translation_term_retained_in_history_derivative",
        "section_current_voltage_J_derivative_is_exactly_zero",
    ):
        if stage5d_claims.get(required) is not True:
            raise ValueError(f"Stage-5D ingress omitted {required}")
    stage5d_history = _mapping(
        stage5d_certificate["continuous_Y_derivative"], "Stage-5D history derivative"
    )
    if stage5d_history.get("event_current_voltage_D_J_exact") != "0":
        raise ValueError("Stage-5D section derivative identity changed")
    if "continuously differentiable" not in str(stage5d_certificate.get("theorem_statement")):
        raise ValueError("Stage-5D no longer states a C1 Y-valued event branch")

    stage5e_certificate = _mapping(parents["stage5e"]["certificate"], "Stage-5E certificate")
    stage5e_claims = _mapping(stage5e_certificate["claim_status"], "Stage-5E claims")
    for required in (
        "physical_real_eigencolumn_phase_oriented",
        "same_adjoint_row_used_in_numerator_and_denominator",
        "recovery_atom_retained",
        "all_history_and_delay_seams_retained",
        "correlated_residual_formed_before_absolute_value",
    ):
        if stage5e_claims.get(required) is not True:
            raise ValueError(f"Stage-5E ingress omitted {required}")
    action = _mapping(
        stage5e_certificate["correlated_history_action"], "Stage-5E correlated action"
    )
    if action.get("voltage_current_atom_exactly_zero_after_section_and_q_section") is not True:
        raise ValueError("Stage-5E voltage-atom zero identity changed")
    identities = _mapping(action["exact_section_identities"], "Stage-5E section identities")
    if identities.get("q_phys_v_at_zero") != "0" or identities.get(
        "voltage_current_atom_action"
    ) != "0":
        raise ValueError("Stage-5E exact voltage-atom identities changed")

    stage5f_certificate = _mapping(parents["stage5f"]["certificate"], "Stage-5F certificate")
    stage5f_claims = _mapping(stage5f_certificate["claim_status"], "Stage-5F claims")
    if stage5f_claims.get("conditional_gap_derivative_strictly_negative_validated") is not True:
        raise ValueError("Stage-5F conditional derivative bridge is unavailable")
    if stage5f_claims.get("quantitative_inner_stable_graph_validated") is not False:
        raise ValueError("Stage-5F graph status was illicitly promoted")
    bridge = _mapping(
        stage5f_certificate["conditional_stable_gap_slope"], "Stage-5F bridge"
    )
    if dict(_mapping(bridge["conditional_gap_derivative_interval"], "Stage-5F interval")) != (
        STAGE5F_BRIDGE_INTERFACE["conditional_derivative_interval_imported"]
    ):
        raise ValueError("Stage-5F derivative interval changed")
    return parents


def _source_hashes(repository: Path, relatives: Sequence[str]) -> dict[str, str]:
    return {relative: _sha256_path(repository / relative) for relative in relatives}


def _public_endpoint_arithmetic(
    base: Mapping[str, Any], common: Mapping[str, Any]
) -> dict[str, Any]:
    residual_action = _parse_complex(base["residual_guide_action"], "residual action")
    residual_norm = DirectedInterval.from_decimal(
        str(base["residual_Y_norm_upper"]), PRECISION_BITS
    ).upper
    measure_difference = DirectedInterval.from_decimal(
        str(common["history_measure_difference_upper"]), PRECISION_BITS
    ).upper
    denominator = DirectedInterval.from_decimal(
        str(common["denominator_modulus_lower"]), PRECISION_BITS
    ).lower
    if denominator <= 0:
        raise ArithmeticError("Stage-5G-a denominator is not positive")
    direct_q_norm = DirectedInterval.from_decimal(
        str(common["direct_q_phys_Y_norm_upper"]), PRECISION_BITS
    ).upper
    center = DirectedInterval.from_decimal(
        str(base["chosen_residual_center_exact"]), PRECISION_BITS
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        measure_error = measure_difference * residual_norm
        numerator = residual_action.upper_abs() + measure_error
        radius = numerator / denominator
        stable_norm = residual_norm + direct_q_norm * radius
    radius_effective = DirectedInterval.from_decimal(
        decimal_upper(radius), PRECISION_BITS
    ).upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        functional_lower = center.lower - radius_effective
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        functional_upper = center.upper + radius_effective
    interval = DirectedInterval(functional_lower, functional_upper, PRECISION_BITS)
    if interval.lower > 0:
        sign = "positive"
        margin = interval.lower
    elif interval.upper < 0:
        sign = "negative"
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
            margin = -interval.upper
    else:
        sign = "contains_zero"
        margin = gmpy2.mpfr(0, PRECISION_BITS)
    return {
        "common_measure_error_upper": decimal_upper(measure_error),
        "numerator_modulus_upper": decimal_upper(numerator),
        "functional_radius_upper": decimal_upper(radius_effective),
        "functional_interval": _interval_record(interval),
        "functional_sign": sign,
        "functional_sign_margin_lower": decimal_lower(margin),
        "stable_projection_identity": (
            "P_s*kappa=r_sigma+q_phys*(c_sigma-f_phys(kappa))"
        ),
        "stable_projection_Y_norm_upper": decimal_upper(stable_norm),
    }


def _conditional_graph_height_record(
    endpoints: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if len(endpoints) != 2:
        raise ValueError("Stage-5G-a requires two endpoints")
    by_name = {str(endpoint["name"]): endpoint for endpoint in endpoints}
    left = _parse_interval(by_name["minus"]["functional_interval"], "minus functional")
    right = _parse_interval(by_name["plus"]["functional_interval"], "plus functional")
    target = _fraction_interval(GRAPH_HEIGHT_TARGET, PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        left_margin = left.lower - target.upper
        right_margin = -right.upper - target.upper
    if left_margin <= 0 or right_margin <= 0:
        raise ArithmeticError("the Stage-5G-a conditional graph-height target failed")
    return {
        "future_graph_height_hypothesis": (
            "if a future quantitative graph in the identical registered chart "
            "satisfies |psi(P_s*kappa(J_sigma))|<=eta_target at both endpoints"
        ),
        "common_height_target_exact": "1/1000",
        "left_conditional_stable_gap_margin_lower": decimal_lower(left_margin),
        "right_conditional_stable_gap_margin_lower": decimal_lower(right_margin),
        "conditional_implication": (
            "under that future graph-height hypothesis, "
            "H(J_-)>0>H(J_+)"
        ),
        "quantitative_graph_supplied_here": False,
        "stable_gap_endpoint_signs_claimed_here": False,
    }


def _numeric_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "common_row_and_q_ledger": certificate["common_row_and_q_ledger"],
        "endpoints": certificate["endpoints"],
        "conditional_graph_height_target": certificate[
            "conditional_graph_height_target"
        ],
    }


@lru_cache(maxsize=1)
def _source_bound_endpoint_records(
    repository_text: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    repository = Path(repository_text).resolve()
    parents = _validated_parent_ingress(repository)
    stage3 = parents["stage3"]
    stage4e = parents["stage4e"]
    stage5c = parents["stage5c"]
    stage5e = parents["stage5e"]
    stage5f = parents["stage5f"]

    coefficients = build_coefficient_propagation()
    remainder = build_remainder_propagation()
    if not coefficients.completed or not remainder.completed:
        raise ArithmeticError("Stage-5B coefficient or remainder propagation failed")
    locator = _CellLocator(coefficients)
    stage5c_certificate = _mapping(stage5c["certificate"], "Stage-5C certificate")
    event_polynomial = _event_time_polynomial(stage5c_certificate)

    data = _centre_data(repository)
    uncertainty = _model_uncertainty(data)
    phase, _, _, gamma_record = _serialized_phase_data(data, uncertainty, stage3)
    stage5e_phase = _mapping(stage5e["certificate"]["physical_phase_orientation"], "Stage-5E phase")
    if gamma_record != stage5e_phase.get("gamma_box"):
        raise ArithmeticError("the replayed physical phase differs from Stage 5E")

    tail_v, tail_w, _ = _row_tail_neumann(data)
    _, row_w = _adjoint_mode_rows(data, tail_v, tail_w)
    atom_w = _directed_sum(tuple(row_w.values()))
    densities: list[tuple[Mapping[tuple[int, int], complex], ...]] = []
    for delay, delayed_coefficient in (
        (data.tau0, data.delayed0),
        (data.tau1, data.delayed1),
    ):
        direct, omitted = _guide_density_dictionary(
            data, tail_v, tail_w, delay, delayed_coefficient
        )
        densities.append((direct, omitted))

    segments = _history_segments()
    if len(segments) != 512:
        raise ArithmeticError("Stage-5G-a history cover no longer has 512 cells")
    density_boxes: list[DirectedComplexInterval] = []
    q_voltage_boxes: list[DirectedInterval] = []
    for theta, active, _ in segments:
        active_densities = densities[1] if active == 1 else densities[0] + densities[1]
        density_boxes.append(_density_box(active_densities, theta, data.period, data.root))
        q_voltage_boxes.append(_q_phys_box(data, phase, theta, voltage=True))

    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    q_recovery = _q_phys_box(data, phase, zero, voltage=False)
    direct_q_norm = q_recovery.upper_abs()
    for q_voltage in q_voltage_boxes:
        direct_q_norm = max(direct_q_norm, q_voltage.upper_abs())
    direct_q_text = decimal_upper(direct_q_norm)

    stage5f_q = _mapping(
        stage5f["certificate"]["q_phys_norm_enclosure"], "Stage-5F q norm"
    )
    stage5f_q_text = str(stage5f_q["q_phys_history_norm_upper"])
    direct_q_effective = DirectedInterval.from_decimal(
        direct_q_text, PRECISION_BITS
    ).upper
    stage5f_q_effective = DirectedInterval.from_decimal(
        stage5f_q_text, PRECISION_BITS
    ).upper
    if direct_q_effective > stage5f_q_effective:
        raise ArithmeticError("the direct q norm exceeds the Stage-5F bound")

    correlated = _mapping(
        stage4e["artifact"]["continuous_history_correlated_deflation"],
        "Stage-4E correlated row",
    )
    oriented = _mapping(stage5e["certificate"]["oriented_action"], "Stage-5E oriented action")
    denominator_text = str(oriented["same_row_denominator_modulus_lower"])
    stage4e_denominator_text = str(correlated["f_q_modulus_lower"])
    denominator = DirectedInterval.from_decimal(denominator_text, PRECISION_BITS).lower
    stage4e_denominator = DirectedInterval.from_decimal(
        stage4e_denominator_text, PRECISION_BITS
    ).lower
    if denominator <= 0 or denominator > stage4e_denominator:
        raise ArithmeticError("the registered Stage-5E denominator is inconsistent")

    common = {
        "same_exact_row_in_residual_and_denominator": True,
        "same_physical_phase_as_stage5e_and_stage5f": True,
        "denominator_source": (
            "Stage-5E same-row lower bound; it is no larger than the "
            "Stage-4E correlated lower bound"
        ),
        "denominator_modulus_lower": denominator_text,
        "stage4e_denominator_modulus_lower": stage4e_denominator_text,
        "history_measure_difference_source": (
            "Stage-4E operator-norm difference between the exact complete "
            "measure and this same finite-plus-Neumann-tail guide"
        ),
        "history_measure_difference_upper": str(
            correlated["history_measure_difference_upper"]
        ),
        "direct_q_norm_method": (
            "192-bit termwise q_phys enclosure on all 512 history segments "
            "plus the current recovery coordinate"
        ),
        "direct_q_phys_Y_norm_upper": direct_q_text,
        "stage5f_registered_q_phys_Y_norm_upper": stage5f_q_text,
        "direct_q_norm_below_stage5f_bound": True,
        "stable_projection_uses_q_norm": "direct_q_phys_Y_norm_upper",
        "physical_phase_gamma_box": gamma_record,
    }

    endpoint_bases: list[dict[str, Any]] = []
    for sign in (-1, 1):
        parameter_lower, parameter_upper = _endpoint_box(sign)
        event_time = _power_range(
            event_polynomial, parameter_lower, parameter_upper
        )
        pulse_recovery = _state_component(
            locator,
            remainder,
            event_time,
            parameter_lower,
            parameter_upper,
            voltage=False,
        )
        orbit_recovery = _orbit_box(data, uncertainty, zero, voltage=False)
        kappa_recovery = pulse_recovery - orbit_recovery

        kappa_voltage_boxes: list[DirectedInterval] = []
        for theta, _, _ in segments:
            pulse_voltage = _state_component(
                locator,
                remainder,
                event_time + theta,
                parameter_lower,
                parameter_upper,
                voltage=True,
            )
            inner_voltage = _orbit_box(data, uncertainty, theta, voltage=True)
            kappa_voltage_boxes.append(pulse_voltage - inner_voltage)

        center_text = ENDPOINT_CENTERS[sign]
        center = DirectedInterval.from_decimal(center_text, PRECISION_BITS)
        residual_recovery = kappa_recovery - center * q_recovery
        residual_norm = residual_recovery.upper_abs()
        residual_action = atom_w * residual_recovery
        for (_, _, width), density, kappa_voltage, q_voltage in zip(
            segments,
            density_boxes,
            kappa_voltage_boxes,
            q_voltage_boxes,
            strict=True,
        ):
            residual_voltage = kappa_voltage - center * q_voltage
            residual_norm = max(residual_norm, residual_voltage.upper_abs())
            residual_action = residual_action + density * residual_voltage * width

        endpoint_j = PARAMETER_INTERVAL[0] if sign == -1 else PARAMETER_INTERVAL[1]
        one_sided_left = Fraction(-1) if sign == -1 else Fraction(1) - ENDPOINT_WIDTH
        one_sided_right = Fraction(-1) + ENDPOINT_WIDTH if sign == -1 else Fraction(1)
        base = {
            "name": "minus" if sign == -1 else "plus",
            "xi_endpoint_exact": str(sign),
            "J_endpoint_exact": _fraction_text(endpoint_j),
            "one_sided_xi_interval_exact": (
                f"[{_fraction_text(one_sided_left)},{_fraction_text(one_sided_right)}]"
            ),
            "one_sided_width_exact": "1/1073741824",
            "exact_endpoint_included": True,
            "chosen_residual_center_exact": center_text,
            "event_time_interval": _interval_record(event_time),
            "residual_guide_action": _complex_record(residual_action),
            "residual_Y_norm_upper": decimal_upper(residual_norm),
        }
        base.update(_public_endpoint_arithmetic(base, common))
        if base["functional_sign"] == "contains_zero":
            raise ArithmeticError("a Stage-5G-a endpoint functional interval contains zero")
        endpoint_bases.append(base)

    graph_target = _conditional_graph_height_record(endpoint_bases)
    return common, endpoint_bases, graph_target


def build_stage5ga_certificate(repository: Path) -> Stage5GAEndpointFunctionalCertificate:
    repository = Path(repository).resolve()
    _require_runtime()
    common, endpoints, graph_target = _source_bound_endpoint_records(
        str(repository)
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage5GAEndpointFunctionalCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        history_space=HISTORY_SPACE,
        section_tangent_space=SECTION_SPACE,
        parameter_scope=dict(PARAMETER_SCOPE),
        coordinate_registration=dict(COORDINATE_REGISTRATION),
        branch_regularity=dict(BRANCH_REGULARITY),
        endpoint_evaluation_contract=dict(ENDPOINT_EVALUATION_CONTRACT),
        voltage_atom_zero_identity=dict(VOLTAGE_ATOM_ZERO_IDENTITY),
        common_row_and_q_ledger=common,
        endpoints=endpoints,
        conditional_graph_height_target=graph_target,
        stage5f_bridge_interface=dict(STAGE5F_BRIDGE_INTERFACE),
        theorem_statement=THEOREM_STATEMENT,
        claim_status=claims,
    )


def build_stage5ga_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    runtime = _require_runtime()
    certificate = asdict(build_stage5ga_certificate(repository))
    numeric_hash = canonical_sha256(_numeric_core(certificate))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "precision_bits": PRECISION_BITS,
            **runtime,
            "parent_sha256": dict(PARENT_SHA256),
            "source_sha256": _source_hashes(repository, SOURCE_MANIFEST),
            "dependency_source_sha256": _source_hashes(
                repository, DEPENDENCY_SOURCE_MANIFEST
            ),
            "numeric_core_sha256": numeric_hash,
            "certificate_sha256": canonical_sha256(certificate),
        },
    }


def _clear_stage5ga_replay_caches() -> None:
    _source_bound_endpoint_records.cache_clear()
    build_coefficient_propagation.cache_clear()
    build_remainder_propagation.cache_clear()


def validate_stage5ga_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    repository = Path(repository).resolve()
    runtime = _require_runtime()
    result = _exact_mapping(payload, "Stage-5G-a result", TOP_KEYS)
    certificate = _exact_mapping(
        result["certificate"], "Stage-5G-a certificate", CERTIFICATE_KEYS
    )
    manifest = _exact_mapping(
        result["manifest"], "Stage-5G-a manifest", MANIFEST_KEYS
    )
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("Stage-5G-a schema changed")
    if certificate.get("model_id") != MODEL_ID or certificate.get("branch") != BRANCH:
        raise ValueError("Stage-5G-a model or branch changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("Stage-5G-a result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("Stage-5G-a command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("Stage-5G-a arithmetic scope changed")
    if manifest.get("precision_bits") != PRECISION_BITS:
        raise ValueError("Stage-5G-a precision changed")
    for key, expected in runtime.items():
        if manifest.get(key) != expected:
            raise ValueError(f"Stage-5G-a runtime ledger changed: {key}")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("Stage-5G-a certificate digest changed")

    constants = (
        ("history_space", HISTORY_SPACE),
        ("section_tangent_space", SECTION_SPACE),
        ("parameter_scope", PARAMETER_SCOPE),
        ("coordinate_registration", COORDINATE_REGISTRATION),
        ("branch_regularity", BRANCH_REGULARITY),
        ("endpoint_evaluation_contract", ENDPOINT_EVALUATION_CONTRACT),
        ("voltage_atom_zero_identity", VOLTAGE_ATOM_ZERO_IDENTITY),
        ("stage5f_bridge_interface", STAGE5F_BRIDGE_INTERFACE),
        ("theorem_statement", THEOREM_STATEMENT),
    )
    for key, expected in constants:
        value = certificate.get(key)
        if isinstance(expected, Mapping):
            if dict(_mapping(value, key)) != dict(expected):
                raise ValueError(f"Stage-5G-a registered {key} changed")
        elif value != expected:
            raise ValueError(f"Stage-5G-a registered {key} changed")

    claims = _mapping(certificate["claim_status"], "Stage-5G-a claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("Stage-5G-a claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved Stage-5G-a claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open Stage-5G-a claim was promoted: {name}")

    common = _exact_mapping(
        certificate["common_row_and_q_ledger"],
        "Stage-5G-a common row/q ledger",
        COMMON_LEDGER_KEYS,
    )
    if common.get("same_exact_row_in_residual_and_denominator") is not True:
        raise ValueError("Stage-5G-a same-row identity was removed")
    if common.get("same_physical_phase_as_stage5e_and_stage5f") is not True:
        raise ValueError("Stage-5G-a physical phase registration changed")
    if common.get("stable_projection_uses_q_norm") != "direct_q_phys_Y_norm_upper":
        raise ValueError("Stage-5G-a stable projection q norm changed")
    direct_q = DirectedInterval.from_decimal(
        str(common["direct_q_phys_Y_norm_upper"]), PRECISION_BITS
    ).upper
    stage5f_q = DirectedInterval.from_decimal(
        str(common["stage5f_registered_q_phys_Y_norm_upper"]), PRECISION_BITS
    ).upper
    if direct_q <= 0 or direct_q > stage5f_q:
        raise ValueError("Stage-5G-a direct q norm is not covered by Stage 5F")
    if common.get("direct_q_norm_below_stage5f_bound") is not True:
        raise ValueError("Stage-5G-a direct q comparison flag changed")
    _parse_complex(common["physical_phase_gamma_box"], "Stage-5G-a gamma")

    endpoints_value = certificate.get("endpoints")
    if not isinstance(endpoints_value, list) or len(endpoints_value) != 2:
        raise ValueError("Stage-5G-a requires exactly two endpoint records")
    endpoints: list[Mapping[str, Any]] = []
    for index, value in enumerate(endpoints_value):
        endpoint = _exact_mapping(value, f"Stage-5G-a endpoint {index}", ENDPOINT_KEYS)
        endpoints.append(endpoint)
    if [endpoint["name"] for endpoint in endpoints] != ["minus", "plus"]:
        raise ValueError("Stage-5G-a endpoint order changed")
    expected_static = (
        ("minus", "-1", "6021/20000", ENDPOINT_CENTERS[-1], "positive"),
        ("plus", "1", "753/2500", ENDPOINT_CENTERS[1], "negative"),
    )
    for endpoint, expected in zip(endpoints, expected_static, strict=True):
        name, xi, physical, center, sign = expected
        if (
            endpoint["name"] != name
            or endpoint["xi_endpoint_exact"] != xi
            or endpoint["J_endpoint_exact"] != physical
            or endpoint["chosen_residual_center_exact"] != center
            or endpoint["functional_sign"] != sign
            or endpoint["one_sided_width_exact"] != "1/1073741824"
            or endpoint["exact_endpoint_included"] is not True
        ):
            raise ValueError(f"Stage-5G-a {name} endpoint registration changed")
        _parse_interval(endpoint["event_time_interval"], f"{name} event time")
        _parse_complex(endpoint["residual_guide_action"], f"{name} residual action")
        expected_arithmetic = _public_endpoint_arithmetic(endpoint, common)
        for key, expected_value in expected_arithmetic.items():
            if endpoint.get(key) != expected_value:
                raise ValueError(f"Stage-5G-a {name} endpoint arithmetic changed: {key}")
        functional = _parse_interval(endpoint["functional_interval"], f"{name} functional")
        margin = DirectedInterval.from_decimal(
            str(endpoint["functional_sign_margin_lower"]), PRECISION_BITS
        ).lower
        stable_norm = DirectedInterval.from_decimal(
            str(endpoint["stable_projection_Y_norm_upper"]), PRECISION_BITS
        ).upper
        if margin <= 0 or stable_norm <= 0:
            raise ValueError(f"Stage-5G-a {name} endpoint lost a strict bound")
        if name == "minus" and functional.lower <= 0:
            raise ValueError("Stage-5G-a minus endpoint lost positivity")
        if name == "plus" and functional.upper >= 0:
            raise ValueError("Stage-5G-a plus endpoint lost negativity")

    graph_target = _exact_mapping(
        certificate["conditional_graph_height_target"],
        "Stage-5G-a graph-height target",
        GRAPH_TARGET_KEYS,
    )
    expected_graph_target = _conditional_graph_height_record(endpoints)
    if dict(graph_target) != expected_graph_target:
        raise ValueError("Stage-5G-a conditional graph-height arithmetic changed")
    if graph_target.get("quantitative_graph_supplied_here") is not False or graph_target.get(
        "stable_gap_endpoint_signs_claimed_here"
    ) is not False:
        raise ValueError("Stage-5G-a conditional graph target was promoted")

    numeric_hash = canonical_sha256(_numeric_core(certificate))
    if manifest.get("numeric_core_sha256") != numeric_hash:
        raise ValueError("Stage-5G-a numeric core manifest digest changed")
    if EXPECTED_NUMERIC_CORE_SHA256 == "TO_BE_FILLED_AFTER_COLD_REPLAY":
        raise ValueError("Stage-5G-a expected numeric core hash is not frozen")
    if numeric_hash != EXPECTED_NUMERIC_CORE_SHA256:
        raise ValueError("Stage-5G-a frozen numeric core changed")

    if dict(_mapping(manifest["parent_sha256"], "Stage-5G-a parent hashes")) != PARENT_SHA256:
        raise ValueError("Stage-5G-a parent hash manifest changed")
    for relative, expected in PARENT_SHA256.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"Stage-5G-a parent bytes changed: {relative}")
    source_hashes = _mapping(manifest["source_sha256"], "Stage-5G-a source hashes")
    dependency_hashes = _mapping(
        manifest["dependency_source_sha256"], "Stage-5G-a dependency hashes"
    )
    if dict(source_hashes) != _source_hashes(repository, SOURCE_MANIFEST):
        raise ValueError("Stage-5G-a source hash manifest is stale")
    if dict(dependency_hashes) != _source_hashes(repository, DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("Stage-5G-a dependency hash manifest is stale")

    parents = _validated_parent_ingress(repository)
    stage5e_phase = parents["stage5e"]["certificate"]["physical_phase_orientation"]
    if common["physical_phase_gamma_box"] != stage5e_phase["gamma_box"]:
        raise ValueError("Stage-5G-a gamma differs from Stage 5E")
    stage5f_q_record = parents["stage5f"]["certificate"]["q_phys_norm_enclosure"]
    if common["stage5f_registered_q_phys_Y_norm_upper"] != stage5f_q_record[
        "q_phys_history_norm_upper"
    ]:
        raise ValueError("Stage-5G-a registered q norm differs from Stage 5F")

    if recompute:
        _clear_stage5ga_replay_caches()
        rebuilt = asdict(build_stage5ga_certificate(repository))
        if canonical_sha256(rebuilt) != canonical_sha256(certificate):
            raise ValueError("Stage-5G-a certificate differs from a fresh replay")


__all__ = [
    "BRANCH",
    "CERTIFICATE_KEYS",
    "COORDINATE_REGISTRATION",
    "ENDPOINT_CENTERS",
    "ENDPOINT_EVALUATION_CONTRACT",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "HISTORY_SPACE",
    "MANIFEST_KEYS",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "PARAMETER_SCOPE",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SECTION_SPACE",
    "STAGE5F_BRIDGE_INTERFACE",
    "THEOREM_STATEMENT",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "VOLTAGE_ATOM_ZERO_IDENTITY",
    "_clear_stage5ga_replay_caches",
    "_conditional_graph_height_record",
    "_numeric_core",
    "_public_endpoint_arithmetic",
    "_runtime_record",
    "build_stage5ga_certificate",
    "build_stage5ga_result",
    "canonical_sha256",
    "validate_stage5ga_result",
]
