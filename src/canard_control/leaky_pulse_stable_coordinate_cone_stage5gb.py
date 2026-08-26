"""Stage-5G-b full-interval stable-coordinate cone certificate.

This stage does not construct a stable graph.  It combines four already
registered objects in the identical physical Grushin coordinates:

* the Stage-5D continuously differentiable selected event branch;
* the Stage-5E correlated derivative residual and functional radius;
* the Stage-5F projection identity; and
* the Stage-5G-a direct physical-column norm and two endpoint projections.

All displayed constants are imported from proof-bearing parent fields.  Exact
decimal strings are interpreted as rational upper bounds.  Exact rational
arithmetic first proves the sharp derivative bound and the two-ended cone
formula; 192-bit directed arithmetic independently serializes those values and
checks the strict meeting-point and radius margins.

The result proves only that ``P_s kappa(I_J)`` lies in the closed ``Y`` ball
of radius ``47/5000``.  A future graph must separately prove that its stable
domain contains that ball.  No graph, stable-gap sign, crossing, onset,
routing, capture, or safety conclusion is asserted here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
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
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_pulse_endpoint_functional_stage5ga import (
    validate_stage5ga_result,
)
from canard_control.leaky_pulse_event_aligned_derivative_stage5d import (
    PRECISION_BITS,
    validate_stage5d_result,
)
from canard_control.leaky_pulse_oriented_adjoint_action_stage5e import (
    validate_stage5e_result,
)
from canard_control.leaky_pulse_stable_gap_slope_bridge_stage5f import (
    validate_stage5f_result,
)


SCHEMA_ID = "leaky-pulse-stable-coordinate-cone-stage5gb-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_route_c_event"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_stable_coordinate_cone_stage5gb.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_stable_coordinate_cone_stage5gb.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_stable_coordinate_cone_stage5gb.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-stable-coordinate-cone-stage5gb.md"
CONTRACT_RELATIVE_PATH = (
    "docs/leaky-pulse-stable-coordinate-cone-stage5gb-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_stable_coordinate_cone_stage5gb.py"
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
STAGE5GA_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_endpoint_functional_stage5ga.json"
)

STAGE5D_SHA256 = "e8be485b8b4711a0ae0b1f3ec875f704c509d9ba0abd5b2166a2384567ed654e"
STAGE5E_SHA256 = "187b8c6d614aa87c68442acb9f5d472233907c31f0df8a1c8d29dfc6941743be"
STAGE5F_SHA256 = "26acd6d9421a8bf60d5bb96fe4c68918b39f89a443973dd728fed17ccf48652b"
STAGE5GA_SHA256 = "56e847fc804ced75e6c2fbf09ccbec1bdeabf505638e093c0939c2f2e584dd8c"

PARENT_SHA256 = {
    STAGE5D_RELATIVE_PATH: STAGE5D_SHA256,
    STAGE5E_RELATIVE_PATH: STAGE5E_SHA256,
    STAGE5F_RELATIVE_PATH: STAGE5F_SHA256,
    STAGE5GA_RELATIVE_PATH: STAGE5GA_SHA256,
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
    "src/canard_control/leaky_pulse_event_aligned_derivative_stage5d.py",
    "src/canard_control/leaky_pulse_oriented_adjoint_action_stage5e.py",
    "src/canard_control/leaky_pulse_stable_gap_slope_bridge_stage5f.py",
    "src/canard_control/leaky_pulse_endpoint_functional_stage5ga.py",
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
    "experiments/leaky_pulse_stable_coordinate_cone_stage5gb.py"
)
ARITHMETIC_SCOPE = (
    "exact rational arithmetic on the outward-decimal parent bounds; "
    "independent 192-bit directed serialization; the Stage-5E correlated "
    "complete-history residual and functional radius; the Stage-5G-a direct "
    "512-cell q_phys Y-norm and both endpoint stable projections; and the "
    "two-ended Banach-space fundamental-theorem-of-calculus cone on the full "
    "exact pulse interval; no parameter sampling, stable graph, graph-domain, "
    "stable-gap, crossing, onset, routing, capture, or safety promotion"
)

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
    "full_width_W_exact": "3/20000",
    "normalized_parameter": "J=J0+h*xi with xi in [-1,1]",
}
COORDINATE_REGISTRATION = {
    "event_history": (
        "K(J) is the unique Stage-5C selected late-window Route-C "
        "event-aligned complete history imported through Stage 5D"
    ),
    "reference_history": (
        "X_* is fixed while J varies and is the exact inner periodic-orbit "
        "history at the identical Route-C phase-zero section"
    ),
    "centered_history": "kappa(J)=K(J)-X_* in Sigma",
    "physical_column": "q=q_phys=q_tilde/gamma",
    "physical_functional": "f=f_phys(y)=gamma*ell(y)/ell(q_tilde)",
    "normalization": "f_phys(q_phys)=1 exactly",
    "projection": "P_s=I-q_phys*f_phys on Sigma",
    "stable_coordinate": "z(J)=P_s*kappa(J) in ker(f_phys)",
    "derivative_identity": "z'(J)=P_s*D_JK(J)",
}
PARENT_INGRESS = {
    "stage5d_C1_selected_event_branch": True,
    "stage5d_event_translation_retained": True,
    "stage5e_same_physical_normalization": True,
    "stage5e_correlated_residual_formed_before_norm": True,
    "stage5f_projection_identity_imported_without_renormalization": True,
    "stage5ga_direct_q_norm_and_both_endpoint_projections_imported": True,
}
CONDITIONAL_GRAPH_INTERFACE = {
    "proved_ball": (
        "P_s*kappa(I_J) is contained in the closed inherited-Y ball in "
        "ker(f_phys) of radius 47/5000"
    ),
    "conditional_implication": (
        "if a future quantitative stable graph in the identical coordinates "
        "has a stable domain containing that closed ball, then its full-"
        "interval stable-coordinate domain premise is satisfied"
    ),
    "quantitative_graph_supplied_here": False,
    "future_graph_domain_contains_ball_validated": False,
    "stable_gap_endpoint_signs_claimed_here": False,
    "selected_crossing_claimed_here": False,
}
THEOREM_STATEMENT = (
    "For the single Stage-5D continuously differentiable selected Route-C "
    "event branch, in the identical Stage-5E/5F/5G-a physical Grushin "
    "coordinates and complete-history norm, the stable coordinate "
    "P_s(K(J)-X_*) lies in the closed Y-ball of radius 47/5000 for every J "
    "in I_J.  This uses the exact two-ended cone and the Stage-5G-a direct "
    "q_phys norm, not sampled interpolation.  The same arithmetic proves the "
    "conditional implication that a future graph with sup||Dpsi||<=16 has "
    "the displayed strictly negative stable-gap derivative interval.  A future "
    "graph must separately exist, contain the ball, and satisfy that derivative "
    "bound; no unconditional stable-gap sign or derivative, stable-sheet "
    "crossing, onset, routing, capture, or safety conclusion is asserted here."
)

TRUE_FLAGS = (
    "stage5d_stage5e_stage5f_stage5ga_parent_bytes_source_bound",
    "selected_event_is_one_C1_branch_on_full_interval",
    "event_translation_retained_in_derivative_parent",
    "identical_physical_grushin_normalization_validated",
    "correlated_derivative_residual_and_functional_radius_imported",
    "direct_complete_history_q_phys_norm_imported",
    "both_endpoint_stable_projection_norms_imported",
    "sharp_stable_projection_derivative_norm_validated",
    "two_ended_cone_meeting_point_strictly_inside_interval_validated",
    "full_interval_stable_coordinate_radius_47_over_5000_validated",
    "banach_fundamental_theorem_argument_used_without_parameter_sampling",
    "conditional_gap_derivative_interval_with_Lpsi_16_arithmetic_validated",
    "conditional_maximum_admissible_graph_derivative_arithmetic_validated",
)
FALSE_FLAGS = (
    "quantitative_inner_stable_graph_validated",
    "future_graph_domain_contains_radius_47_over_5000_ball_validated",
    "full_interval_stable_coordinate_in_future_graph_domain_validated",
    "graph_derivative_norm_16_validated",
    "graph_height_endpoint_bounds_validated",
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
    raise RuntimeError("Stage-5G-b claim groups overlap")
if len(TRUE_FLAGS) != len(set(TRUE_FLAGS)) or len(FALSE_FLAGS) != len(set(FALSE_FLAGS)):
    raise RuntimeError("Stage-5G-b claim groups contain duplicates")

# Frozen only after Stage 5G-a and the Stage-5G-b exact arithmetic are replayed.
EXPECTED_NUMERIC_CORE_SHA256 = (
    "acdf92f82b51866b89536fb45c4632f8da11f4ac54eabbffcdcc6c284ef741e5"
)


@dataclass(frozen=True)
class Stage5GBStableCoordinateConeCertificate:
    schema_id: str
    model_id: str
    branch: str
    history_space: str
    section_tangent_space: str
    parameter_scope: dict[str, Any]
    coordinate_registration: dict[str, Any]
    parent_ingress: dict[str, bool]
    derivative_ledger: dict[str, Any]
    endpoints: list[dict[str, Any]]
    two_ended_cone: dict[str, Any]
    conditional_stable_gap_slope: dict[str, Any]
    conditional_graph_interface: dict[str, Any]
    theorem_statement: str
    claim_status: dict[str, bool]


TOP_KEYS = ("certificate", "manifest")
CERTIFICATE_KEYS = tuple(
    field.name
    for field in Stage5GBStableCoordinateConeCertificate.__dataclass_fields__.values()
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
DERIVATIVE_KEYS = (
    "projection_identity",
    "residual_center_exact",
    "correlated_residual_Y_norm_upper",
    "functional_deviation_from_center_upper",
    "q_norm_source",
    "direct_q_phys_Y_norm_upper",
    "stage5f_coarse_q_phys_Y_norm_upper",
    "direct_q_norm_strictly_below_stage5f_coarse_bound",
    "bound_formula",
    "stable_projection_derivative_norm_exact_fraction",
    "stable_projection_derivative_norm_directed_interval",
    "stable_projection_derivative_norm_upper",
)
ENDPOINT_KEYS = (
    "name",
    "J_endpoint_exact",
    "stable_projection_Y_norm_upper",
)
CONE_KEYS = (
    "argument",
    "finite_parameter_sampling_used",
    "interval_width_W_exact",
    "left_cone",
    "right_cone",
    "meeting_point_formula",
    "meeting_point_exact_fraction",
    "meeting_point_directed_interval",
    "left_meeting_margin_lower",
    "right_meeting_margin_lower",
    "meeting_point_strictly_inside_interval",
    "cone_radius_formula",
    "cone_radius_exact_fraction",
    "cone_radius_directed_interval",
    "cone_radius_upper",
    "target_radius_exact",
    "target_margin_lower",
    "cone_radius_strictly_below_target",
    "full_interval_conclusion",
)
CONDITIONAL_SLOPE_KEYS = (
    "derivative_identity",
    "parent_functional_action_interval",
    "graph_derivative_norm_hypothesis_exact",
    "graph_correction_norm_exact_fraction",
    "conditional_gap_derivative_exact_interval",
    "conditional_gap_derivative_directed_interval",
    "conditional_negative_margin_lower",
    "maximum_admissible_graph_derivative_norm_exact_fraction",
    "maximum_admissible_graph_derivative_norm_directed_interval",
    "maximum_admissible_graph_derivative_norm_lower",
    "conditional_implication",
    "quantitative_graph_supplied_here",
    "graph_derivative_norm_hypothesis_validated_here",
    "unconditional_gap_derivative_claimed_here",
)
INTERVAL_KEYS = ("lower", "upper")


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
            f"the Stage-5G-b replay environment changed: {actual} != {expected}"
        )
    return expected


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _exact_mapping(value: Any, name: str, keys: Sequence[str]) -> Mapping[str, Any]:
    mapped = _mapping(value, name)
    if set(mapped) != set(keys):
        raise ValueError(f"{name} keys changed")
    return mapped


def _load_bound_json(repository: Path, relative: str, expected_sha: str) -> dict[str, Any]:
    if expected_sha.startswith("TO_BE_FILLED"):
        raise RuntimeError("the Stage-5G-a parent hash has not been frozen")
    path = repository / relative
    actual = _sha256_path(path)
    if actual != expected_sha:
        raise ValueError(
            f"Stage-5G-b source-bound parent changed: {relative}: "
            f"{actual} != {expected_sha}"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Stage-5G-b parent {relative} is not a JSON object")
    return payload


def _source_hashes(repository: Path, relatives: Sequence[str]) -> dict[str, str]:
    return {relative: _sha256_path(repository / relative) for relative in relatives}


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _fraction_interval(value: Fraction) -> DirectedInterval:
    numerator = DirectedInterval.from_decimal(value.numerator, PRECISION_BITS)
    denominator = DirectedInterval.from_decimal(value.denominator, PRECISION_BITS)
    return numerator / denominator


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower),
        "upper": decimal_upper(value.upper),
    }


def _parse_interval(value: Any, name: str) -> DirectedInterval:
    record = _exact_mapping(value, name, INTERVAL_KEYS)
    interval = DirectedInterval.from_bounds(
        str(record["lower"]), str(record["upper"]), PRECISION_BITS
    )
    if not gmpy2.is_finite(interval.lower) or not gmpy2.is_finite(interval.upper):
        raise ValueError(f"{name} must be finite")
    return interval


def _positive_decimal_fraction(value: Any, name: str) -> Fraction:
    try:
        result = Fraction(str(value))
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{name} is not an exact decimal rational") from error
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _decimal_fraction(value: Any, name: str) -> Fraction:
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{name} is not an exact decimal rational") from error


def _validated_parent_ingress(repository: Path) -> dict[str, Mapping[str, Any]]:
    repository = Path(repository).resolve()
    parents = {
        "stage5d": _load_bound_json(repository, STAGE5D_RELATIVE_PATH, STAGE5D_SHA256),
        "stage5e": _load_bound_json(repository, STAGE5E_RELATIVE_PATH, STAGE5E_SHA256),
        "stage5f": _load_bound_json(repository, STAGE5F_RELATIVE_PATH, STAGE5F_SHA256),
        "stage5ga": _load_bound_json(
            repository, STAGE5GA_RELATIVE_PATH, STAGE5GA_SHA256
        ),
    }
    validate_stage5d_result(parents["stage5d"], repository)
    validate_stage5e_result(parents["stage5e"], repository)
    validate_stage5f_result(parents["stage5f"], repository)
    validate_stage5ga_result(parents["stage5ga"], repository)

    stage5d_certificate = _mapping(
        parents["stage5d"]["certificate"], "Stage-5D certificate"
    )
    stage5d_claims = _mapping(stage5d_certificate["claim_status"], "Stage-5D claims")
    for required in (
        "continuous_event_aligned_complete_history_J_derivative_enclosed_in_Y",
        "event_translation_term_retained_in_history_derivative",
        "finite_parameter_sampling_excluded_from_proof",
    ):
        if stage5d_claims.get(required) is not True:
            raise ValueError(f"Stage-5D ingress omitted {required}")
    stage5d_history = _mapping(
        stage5d_certificate["continuous_Y_derivative"], "Stage-5D history derivative"
    )
    if stage5d_history.get("phase_space") != "Y=C([-5*sqrt(5),0],R)xR":
        raise ValueError("Stage-5D history space changed")
    if stage5d_history.get("exact_chain_rule") != (
        "D_J K=(partial_J z+z_t*T_J) on the voltage history and current recovery coordinate"
    ):
        raise ValueError("Stage-5D event translation identity changed")

    stage5e_certificate = _mapping(
        parents["stage5e"]["certificate"], "Stage-5E certificate"
    )
    stage5e_claims = _mapping(stage5e_certificate["claim_status"], "Stage-5E claims")
    for required in (
        "physical_real_eigencolumn_phase_oriented",
        "same_adjoint_row_used_in_numerator_and_denominator",
        "stage5d_event_translation_retained",
        "correlated_residual_formed_before_absolute_value",
    ):
        if stage5e_claims.get(required) is not True:
            raise ValueError(f"Stage-5E ingress omitted {required}")
    phase = _mapping(
        stage5e_certificate["physical_phase_orientation"], "Stage-5E phase"
    )
    if (
        phase.get("q_phys_definition") != "q_phys=q_tilde/gamma"
        or phase.get("f_phys_definition")
        != "f_phys(y)=gamma*ell(y)/ell(q_tilde)"
        or phase.get("projection_identity")
        != "q_phys*f_phys(y)=q_tilde*ell(y)/ell(q_tilde)"
    ):
        raise ValueError("Stage-5E physical normalization changed")
    correlated = _mapping(
        stage5e_certificate["correlated_history_action"], "Stage-5E residual"
    )
    if (
        correlated.get("center_c_star_exact") != "-252"
        or correlated.get("residual") != "Y_*(J)=D_JK(J)-c_*q_phys"
        or correlated.get("event_translation_retained") is not True
    ):
        raise ValueError("Stage-5E derivative residual changed")

    stage5f_certificate = _mapping(
        parents["stage5f"]["certificate"], "Stage-5F certificate"
    )
    if stage5f_certificate.get("history_space") != (
        "Y=C([-tau_max,0],R) x R with "
        "||(phi,w)||_Y=max(||phi||_infinity,|w|)"
    ):
        raise ValueError("Stage-5F history norm changed")
    compatibility = _mapping(
        stage5f_certificate["coordinate_compatibility"], "Stage-5F coordinates"
    )
    if (
        compatibility.get("normalization") != "f_phys(q_phys)=1 exactly"
        or compatibility.get("projection") != "P_s=I-q_phys f_phys on Sigma"
    ):
        raise ValueError("Stage-5F projection normalization changed")
    if stage5f_certificate.get("projection_identity") != (
        "P_s D_Jkappa=P_sD_JK=Y_*+q_phys(c_*-f_phys(D_JK)), where "
        "P_s=I-q_phys f_phys on Sigma, D_Jkappa=D_JK, and "
        "Y_*=D_JK-c_*q_phys"
    ):
        raise ValueError("Stage-5F projection identity changed")
    stage5f_scope = _mapping(
        stage5f_certificate["parameter_scope"], "Stage-5F parameter scope"
    )
    if stage5f_scope.get("interval_exact") != "I_J=[6021/20000,753/2500]":
        raise ValueError("Stage-5F pulse interval changed")

    stage5ga_certificate = _mapping(
        parents["stage5ga"]["certificate"], "Stage-5G-a certificate"
    )
    if (
        stage5ga_certificate.get("history_space") != HISTORY_SPACE
        or stage5ga_certificate.get("section_tangent_space") != SECTION_SPACE
    ):
        raise ValueError("Stage-5G-a history or section space changed")
    ga_coordinates = _mapping(
        stage5ga_certificate["coordinate_registration"], "Stage-5G-a coordinates"
    )
    for key, expected in (
        ("centered_history", "kappa(J)=K(J)-X_* in Sigma"),
        ("physical_column", "q=q_phys=q_tilde/gamma"),
        ("physical_functional", "f=f_phys(y)=gamma*ell(y)/ell(q_tilde)"),
        ("normalization", "f_phys(q_phys)=1 exactly"),
        ("projection", "P_s=I-q_phys*f_phys on Sigma"),
    ):
        if ga_coordinates.get(key) != expected:
            raise ValueError(f"Stage-5G-a coordinate changed: {key}")
    ga_regularity = _mapping(
        stage5ga_certificate["branch_regularity"], "Stage-5G-a branch"
    )
    if (
        ga_regularity.get("one_event_for_every_parameter") is not True
        or ga_regularity.get("event_switching_inside_window") is not False
        or ga_regularity.get("Y_valued_regularity")
        != "K:I_J->Y is continuously differentiable"
    ):
        raise ValueError("Stage-5G-a selected branch regularity changed")
    ga_claims = _mapping(stage5ga_certificate["claim_status"], "Stage-5G-a claims")
    for required in (
        "direct_512_segment_q_phys_Y_norm_validated",
        "direct_q_norm_below_stage5f_registered_wiener_bound_validated",
        "endpoint_stable_projection_norms_validated",
    ):
        if ga_claims.get(required) is not True:
            raise ValueError(f"Stage-5G-a ingress omitted {required}")
    for required_open in (
        "quantitative_inner_stable_graph_validated",
        "full_interval_stable_coordinate_graph_domain_containment_validated",
        "stable_gap_endpoint_signs_validated",
        "unique_selected_event_stable_sheet_crossing_validated",
    ):
        if ga_claims.get(required_open) is not False:
            raise ValueError(f"Stage-5G-a open claim was promoted: {required_open}")
    return parents


def _parent_numeric_inputs(
    parents: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    stage5e = _mapping(parents["stage5e"]["certificate"], "Stage-5E certificate")
    correlated = _mapping(stage5e["correlated_history_action"], "Stage-5E residual")
    oriented = _mapping(stage5e["oriented_action"], "Stage-5E action")
    stage5f = _mapping(parents["stage5f"]["certificate"], "Stage-5F certificate")
    coarse_q = _mapping(stage5f["q_phys_norm_enclosure"], "Stage-5F q norm")
    stage5ga = _mapping(parents["stage5ga"]["certificate"], "Stage-5G-a certificate")
    direct_q = _mapping(stage5ga["common_row_and_q_ledger"], "Stage-5G-a q norm")
    endpoint_values = stage5ga.get("endpoints")
    if not isinstance(endpoint_values, list) or len(endpoint_values) != 2:
        raise ValueError("Stage-5G-a must supply exactly two endpoints")
    endpoints = {
        str(_mapping(row, "Stage-5G-a endpoint")["name"]): _mapping(
            row, "Stage-5G-a endpoint"
        )
        for row in endpoint_values
    }
    if set(endpoints) != {"minus", "plus"}:
        raise ValueError("Stage-5G-a endpoint names changed")
    return {
        "residual_Y_norm_upper": str(
            correlated["maximum_correlated_residual_Y_norm_upper"]
        ),
        "functional_deviation_upper": str(oriented["quotient_radius_upper"]),
        "functional_action_lower": str(oriented["physical_real_interval"]["lower"]),
        "functional_action_upper": str(oriented["physical_real_interval"]["upper"]),
        "direct_q_norm_upper": str(direct_q["direct_q_phys_Y_norm_upper"]),
        "coarse_q_norm_upper": str(
            coarse_q["q_phys_history_norm_upper"]
        ),
        "endpoint_minus_J": str(endpoints["minus"]["J_endpoint_exact"]),
        "endpoint_plus_J": str(endpoints["plus"]["J_endpoint_exact"]),
        "endpoint_minus_norm_upper": str(
            endpoints["minus"]["stable_projection_Y_norm_upper"]
        ),
        "endpoint_plus_norm_upper": str(
            endpoints["plus"]["stable_projection_Y_norm_upper"]
        ),
    }


def _arithmetic_records(inputs: Mapping[str, Any]) -> tuple[
    dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]
]:
    residual = _positive_decimal_fraction(
        inputs["residual_Y_norm_upper"], "Stage-5E residual norm"
    )
    deviation = _positive_decimal_fraction(
        inputs["functional_deviation_upper"], "Stage-5E functional deviation"
    )
    direct_q = _positive_decimal_fraction(
        inputs["direct_q_norm_upper"], "Stage-5G-a direct q norm"
    )
    coarse_q = _positive_decimal_fraction(
        inputs["coarse_q_norm_upper"], "Stage-5F coarse q norm"
    )
    endpoint_minus = _positive_decimal_fraction(
        inputs["endpoint_minus_norm_upper"], "Stage-5G-a minus endpoint norm"
    )
    endpoint_plus = _positive_decimal_fraction(
        inputs["endpoint_plus_norm_upper"], "Stage-5G-a plus endpoint norm"
    )
    action_lower = _decimal_fraction(
        inputs["functional_action_lower"], "Stage-5E functional action lower"
    )
    action_upper = _decimal_fraction(
        inputs["functional_action_upper"], "Stage-5E functional action upper"
    )
    if not action_lower <= action_upper < 0:
        raise ValueError("Stage-5E physical functional action is not strictly negative")
    if inputs["endpoint_minus_J"] != "6021/20000" or inputs[
        "endpoint_plus_J"
    ] != "753/2500":
        raise ValueError("Stage-5G-a exact endpoint registration changed")
    if direct_q >= coarse_q:
        raise ArithmeticError("the Stage-5G-a direct q norm is not sharper")

    width = Fraction(3, 20_000)
    target = Fraction(47, 5_000)
    derivative_bound = residual + direct_q * deviation
    if derivative_bound <= 0:
        raise ArithmeticError("the sharp stable derivative bound is not positive")
    meeting = (
        endpoint_plus - endpoint_minus + derivative_bound * width
    ) / (2 * derivative_bound)
    cone_radius = (
        endpoint_minus + endpoint_plus + derivative_bound * width
    ) / 2
    graph_derivative_target = Fraction(16)
    graph_correction = graph_derivative_target * derivative_bound
    conditional_slope_lower = action_lower - graph_correction
    conditional_slope_upper = action_upper + graph_correction
    maximum_graph_derivative = -action_upper / derivative_bound
    if not (Fraction(0) < meeting < width):
        raise ArithmeticError("the two endpoint cones do not meet inside I_J")
    if not cone_radius < target:
        raise ArithmeticError("the two-ended cone did not close below 47/5000")
    if not conditional_slope_lower <= conditional_slope_upper < 0:
        raise ArithmeticError("the sharp conditional stable-gap slope includes zero")
    if maximum_graph_derivative <= graph_derivative_target:
        raise ArithmeticError("the admissible graph derivative did not exceed 16")

    residual_box = _fraction_interval(residual)
    deviation_box = _fraction_interval(deviation)
    direct_q_box = _fraction_interval(direct_q)
    endpoint_minus_box = _fraction_interval(endpoint_minus)
    endpoint_plus_box = _fraction_interval(endpoint_plus)
    width_box = _fraction_interval(width)
    target_box = _fraction_interval(target)
    action_lower_box = _fraction_interval(action_lower)
    action_upper_box = _fraction_interval(action_upper)
    derivative_box = residual_box + direct_q_box * deviation_box
    meeting_box = (
        endpoint_plus_box - endpoint_minus_box + derivative_box * width_box
    ) / (2 * derivative_box)
    cone_box = (
        endpoint_minus_box + endpoint_plus_box + derivative_box * width_box
    ) / 2
    left_margin_box = meeting_box
    right_margin_box = width_box - meeting_box
    target_margin_box = target_box - cone_box
    graph_correction_box = 16 * derivative_box
    conditional_slope_box = DirectedInterval(
        (action_lower_box - graph_correction_box).lower,
        (action_upper_box + graph_correction_box).upper,
        PRECISION_BITS,
    )
    maximum_graph_derivative_box = (-action_upper_box) / derivative_box
    if meeting_box.lower <= 0 or right_margin_box.lower <= 0:
        raise ArithmeticError("directed arithmetic lost the strict cone intersection")
    if target_margin_box.lower <= 0:
        raise ArithmeticError("directed arithmetic lost the strict radius margin")
    if conditional_slope_box.upper >= 0:
        raise ArithmeticError("directed arithmetic lost the conditional slope sign")
    if maximum_graph_derivative_box.lower <= 16:
        raise ArithmeticError("directed arithmetic lost the admissible slope margin")

    derivative = {
        "projection_identity": (
            "P_sD_JK=Y_*+q_phys*(c_*-f_phys(D_JK))"
        ),
        "residual_center_exact": "-252",
        "correlated_residual_Y_norm_upper": str(inputs["residual_Y_norm_upper"]),
        "functional_deviation_from_center_upper": str(
            inputs["functional_deviation_upper"]
        ),
        "q_norm_source": (
            "Stage-5G-a direct 512-continuous-history-cell q_phys Y-norm"
        ),
        "direct_q_phys_Y_norm_upper": str(inputs["direct_q_norm_upper"]),
        "stage5f_coarse_q_phys_Y_norm_upper": str(inputs["coarse_q_norm_upper"]),
        "direct_q_norm_strictly_below_stage5f_coarse_bound": True,
        "bound_formula": "L_s=R_*+Q_*delta_f",
        "stable_projection_derivative_norm_exact_fraction": _fraction_text(
            derivative_bound
        ),
        "stable_projection_derivative_norm_directed_interval": _interval_record(
            derivative_box
        ),
        "stable_projection_derivative_norm_upper": decimal_upper(
            derivative_box.upper
        ),
    }
    endpoints = [
        {
            "name": "minus",
            "J_endpoint_exact": "6021/20000",
            "stable_projection_Y_norm_upper": str(
                inputs["endpoint_minus_norm_upper"]
            ),
        },
        {
            "name": "plus",
            "J_endpoint_exact": "753/2500",
            "stable_projection_Y_norm_upper": str(
                inputs["endpoint_plus_norm_upper"]
            ),
        },
    ]
    cone = {
        "argument": (
            "two-ended Banach-space fundamental theorem of calculus in the "
            "continuous complete-history Y norm"
        ),
        "finite_parameter_sampling_used": False,
        "interval_width_W_exact": "3/20000",
        "left_cone": "||z(J)||_Y<=E_-+L_s*(J-J_-)",
        "right_cone": "||z(J)||_Y<=E_++L_s*(J_+-J)",
        "meeting_point_formula": "x_*=(E_+-E_-+L_s*W)/(2*L_s)",
        "meeting_point_exact_fraction": _fraction_text(meeting),
        "meeting_point_directed_interval": _interval_record(meeting_box),
        "left_meeting_margin_lower": decimal_lower(left_margin_box.lower),
        "right_meeting_margin_lower": decimal_lower(right_margin_box.lower),
        "meeting_point_strictly_inside_interval": True,
        "cone_radius_formula": "E_cone=(E_-+E_++L_s*W)/2",
        "cone_radius_exact_fraction": _fraction_text(cone_radius),
        "cone_radius_directed_interval": _interval_record(cone_box),
        "cone_radius_upper": decimal_upper(cone_box.upper),
        "target_radius_exact": "47/5000",
        "target_margin_lower": decimal_lower(target_margin_box.lower),
        "cone_radius_strictly_below_target": True,
        "full_interval_conclusion": (
            "P_s*kappa(I_J) subset closed_B_Y(0,47/5000) intersect ker(f_phys)"
        ),
    }
    conditional_slope = {
        "derivative_identity": (
            "H'(J)=f_phys(D_JK)-Dpsi(P_s*kappa)[P_sD_JK]"
        ),
        "parent_functional_action_interval": {
            "lower": str(inputs["functional_action_lower"]),
            "upper": str(inputs["functional_action_upper"]),
        },
        "graph_derivative_norm_hypothesis_exact": "16",
        "graph_correction_norm_exact_fraction": _fraction_text(graph_correction),
        "conditional_gap_derivative_exact_interval": {
            "lower": _fraction_text(conditional_slope_lower),
            "upper": _fraction_text(conditional_slope_upper),
        },
        "conditional_gap_derivative_directed_interval": _interval_record(
            conditional_slope_box
        ),
        "conditional_negative_margin_lower": decimal_lower(
            (-conditional_slope_box).lower
        ),
        "maximum_admissible_graph_derivative_norm_exact_fraction": _fraction_text(
            maximum_graph_derivative
        ),
        "maximum_admissible_graph_derivative_norm_directed_interval": _interval_record(
            maximum_graph_derivative_box
        ),
        "maximum_admissible_graph_derivative_norm_lower": decimal_lower(
            maximum_graph_derivative_box.lower
        ),
        "conditional_implication": (
            "if a future quantitative graph in the identical coordinates is "
            "defined on P_s*kappa(I_J) and satisfies sup||Dpsi||<=16, then "
            "H'(J) lies in the displayed negative interval for every J in I_J"
        ),
        "quantitative_graph_supplied_here": False,
        "graph_derivative_norm_hypothesis_validated_here": False,
        "unconditional_gap_derivative_claimed_here": False,
    }
    return derivative, endpoints, cone, conditional_slope


def _numeric_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "derivative_ledger": certificate["derivative_ledger"],
        "endpoints": certificate["endpoints"],
        "two_ended_cone": certificate["two_ended_cone"],
        "conditional_stable_gap_slope": certificate[
            "conditional_stable_gap_slope"
        ],
    }


def build_stage5gb_certificate(
    repository: Path,
) -> Stage5GBStableCoordinateConeCertificate:
    repository = Path(repository).resolve()
    _require_runtime()
    parents = _validated_parent_ingress(repository)
    derivative, endpoints, cone, conditional_slope = _arithmetic_records(
        _parent_numeric_inputs(parents)
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage5GBStableCoordinateConeCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        history_space=HISTORY_SPACE,
        section_tangent_space=SECTION_SPACE,
        parameter_scope=dict(PARAMETER_SCOPE),
        coordinate_registration=dict(COORDINATE_REGISTRATION),
        parent_ingress=dict(PARENT_INGRESS),
        derivative_ledger=derivative,
        endpoints=endpoints,
        two_ended_cone=cone,
        conditional_stable_gap_slope=conditional_slope,
        conditional_graph_interface=dict(CONDITIONAL_GRAPH_INTERFACE),
        theorem_statement=THEOREM_STATEMENT,
        claim_status=claims,
    )


def build_stage5gb_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    runtime = _require_runtime()
    certificate = asdict(build_stage5gb_certificate(repository))
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
            "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
            "certificate_sha256": canonical_sha256(certificate),
        },
    }


def validate_stage5gb_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    repository = Path(repository).resolve()
    runtime = _require_runtime()
    result = _exact_mapping(payload, "Stage-5G-b result", TOP_KEYS)
    certificate = _exact_mapping(
        result["certificate"], "Stage-5G-b certificate", CERTIFICATE_KEYS
    )
    manifest = _exact_mapping(
        result["manifest"], "Stage-5G-b manifest", MANIFEST_KEYS
    )
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("Stage-5G-b schema changed")
    if certificate.get("model_id") != MODEL_ID or certificate.get("branch") != BRANCH:
        raise ValueError("Stage-5G-b model or branch changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("Stage-5G-b result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("Stage-5G-b command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("Stage-5G-b arithmetic scope changed")
    if manifest.get("precision_bits") != PRECISION_BITS:
        raise ValueError("Stage-5G-b precision changed")
    for key, expected in runtime.items():
        if manifest.get(key) != expected:
            raise ValueError(f"Stage-5G-b runtime ledger changed: {key}")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("Stage-5G-b certificate digest changed")

    constants = (
        ("history_space", HISTORY_SPACE),
        ("section_tangent_space", SECTION_SPACE),
        ("parameter_scope", PARAMETER_SCOPE),
        ("coordinate_registration", COORDINATE_REGISTRATION),
        ("parent_ingress", PARENT_INGRESS),
        ("conditional_graph_interface", CONDITIONAL_GRAPH_INTERFACE),
        ("theorem_statement", THEOREM_STATEMENT),
    )
    for key, expected in constants:
        value = certificate.get(key)
        if isinstance(expected, Mapping):
            if dict(_mapping(value, key)) != dict(expected):
                raise ValueError(f"Stage-5G-b registered {key} changed")
        elif value != expected:
            raise ValueError(f"Stage-5G-b registered {key} changed")

    claims = _mapping(certificate["claim_status"], "Stage-5G-b claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("Stage-5G-b claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved Stage-5G-b claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open Stage-5G-b claim was promoted: {name}")

    parents = _validated_parent_ingress(repository)
    (
        expected_derivative,
        expected_endpoints,
        expected_cone,
        expected_conditional_slope,
    ) = _arithmetic_records(_parent_numeric_inputs(parents))
    derivative = _exact_mapping(
        certificate["derivative_ledger"], "Stage-5G-b derivative", DERIVATIVE_KEYS
    )
    if dict(derivative) != expected_derivative:
        raise ValueError("Stage-5G-b derivative arithmetic changed")
    _parse_interval(
        derivative["stable_projection_derivative_norm_directed_interval"],
        "Stage-5G-b derivative interval",
    )
    endpoint_values = certificate.get("endpoints")
    if not isinstance(endpoint_values, list) or len(endpoint_values) != 2:
        raise ValueError("Stage-5G-b requires both endpoint norms")
    endpoints = [
        _exact_mapping(value, f"Stage-5G-b endpoint {index}", ENDPOINT_KEYS)
        for index, value in enumerate(endpoint_values)
    ]
    if [dict(endpoint) for endpoint in endpoints] != expected_endpoints:
        raise ValueError("Stage-5G-b endpoint arithmetic changed")
    cone = _exact_mapping(certificate["two_ended_cone"], "Stage-5G-b cone", CONE_KEYS)
    if dict(cone) != expected_cone:
        raise ValueError("Stage-5G-b cone arithmetic changed")
    meeting_interval = _parse_interval(
        cone["meeting_point_directed_interval"], "Stage-5G-b meeting point"
    )
    cone_interval = _parse_interval(
        cone["cone_radius_directed_interval"], "Stage-5G-b cone radius"
    )
    width_interval = _fraction_interval(Fraction(3, 20_000))
    target_interval = _fraction_interval(Fraction(47, 5_000))
    if meeting_interval.lower <= 0 or meeting_interval.upper >= width_interval.lower:
        raise ValueError("Stage-5G-b meeting point is not strictly inside I_J")
    if cone_interval.upper >= target_interval.lower:
        raise ValueError("Stage-5G-b cone radius is not strictly below 47/5000")
    if cone.get("finite_parameter_sampling_used") is not False:
        raise ValueError("Stage-5G-b sampled interpolation was promoted to proof")
    conditional_slope = _exact_mapping(
        certificate["conditional_stable_gap_slope"],
        "Stage-5G-b conditional slope",
        CONDITIONAL_SLOPE_KEYS,
    )
    if dict(conditional_slope) != expected_conditional_slope:
        raise ValueError("Stage-5G-b conditional slope arithmetic changed")
    conditional_interval = _parse_interval(
        conditional_slope["conditional_gap_derivative_directed_interval"],
        "Stage-5G-b conditional gap derivative",
    )
    admissible_interval = _parse_interval(
        conditional_slope[
            "maximum_admissible_graph_derivative_norm_directed_interval"
        ],
        "Stage-5G-b maximum graph derivative",
    )
    if conditional_interval.upper >= 0:
        raise ValueError("Stage-5G-b conditional gap derivative includes zero")
    if admissible_interval.lower <= 16:
        raise ValueError("Stage-5G-b maximum graph derivative lost its margin")
    if (
        conditional_slope.get("quantitative_graph_supplied_here") is not False
        or conditional_slope.get("graph_derivative_norm_hypothesis_validated_here")
        is not False
        or conditional_slope.get("unconditional_gap_derivative_claimed_here")
        is not False
    ):
        raise ValueError("Stage-5G-b conditional slope was promoted")

    numeric_hash = canonical_sha256(_numeric_core(certificate))
    if manifest.get("numeric_core_sha256") != numeric_hash:
        raise ValueError("Stage-5G-b numeric core manifest digest changed")
    if EXPECTED_NUMERIC_CORE_SHA256.startswith("TO_BE_FILLED"):
        raise ValueError("Stage-5G-b expected numeric core hash is not frozen")
    if numeric_hash != EXPECTED_NUMERIC_CORE_SHA256:
        raise ValueError("Stage-5G-b frozen numeric core changed")

    if dict(_mapping(manifest["parent_sha256"], "Stage-5G-b parent hashes")) != PARENT_SHA256:
        raise ValueError("Stage-5G-b parent hash manifest changed")
    for relative, expected in PARENT_SHA256.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"Stage-5G-b parent bytes changed: {relative}")
    source_hashes = _mapping(manifest["source_sha256"], "Stage-5G-b source hashes")
    dependency_hashes = _mapping(
        manifest["dependency_source_sha256"], "Stage-5G-b dependency hashes"
    )
    if dict(source_hashes) != _source_hashes(repository, SOURCE_MANIFEST):
        raise ValueError("Stage-5G-b source hash manifest is stale")
    if dict(dependency_hashes) != _source_hashes(repository, DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("Stage-5G-b dependency hash manifest is stale")

    if recompute:
        rebuilt = asdict(build_stage5gb_certificate(repository))
        if canonical_sha256(rebuilt) != canonical_sha256(certificate):
            raise ValueError("Stage-5G-b certificate differs from a fresh replay")


__all__ = [
    "BRANCH",
    "CERTIFICATE_KEYS",
    "CONDITIONAL_GRAPH_INTERFACE",
    "COORDINATE_REGISTRATION",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "HISTORY_SPACE",
    "MANIFEST_KEYS",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "PARAMETER_SCOPE",
    "PARENT_INGRESS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SECTION_SPACE",
    "THEOREM_STATEMENT",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "_arithmetic_records",
    "_numeric_core",
    "_parent_numeric_inputs",
    "_runtime_record",
    "build_stage5gb_certificate",
    "build_stage5gb_result",
    "canonical_sha256",
    "validate_stage5gb_result",
]
