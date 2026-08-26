"""Stage-5F bridge from the physical pulse action to a stable-gap slope.

Stage 5E proves a nonzero, physically oriented unstable action but deliberately
does not promote it to a derivative of the nonlinear stable-sheet gap.  This
module closes the missing *linear-algebra bridge* on the Route-C section
tangent space.  It gives a source-bound upper bound for
``||(I-q f) D_J K||`` and proves a quantitative conditional implication: a
centered Route-C stable graph with the stated chart containment and
``||D psi|| <= 16`` in the identical Grushin normalization has a strictly
negative pulse-gap derivative.

The quantitative graph certificate in this registered normalization and its
chart/domain containment remain open.  Consequently this module does not
claim a quantitative stable-sheet enclosure, endpoint signs, an
interval-Newton root, pulse onset, routing, capture, or network safety.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, localcontext
from functools import lru_cache
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_pulse_oriented_adjoint_action_stage5e import (
    validate_stage5e_result,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    PRECISION_BITS,
    SCALAR_TRANSCRIPTION_GUARD,
    _centre_data,
    _dictionary_l1_directed_upper,
    _model_uncertainty,
    validate_stage4e_result,
)


SCHEMA_ID = "leaky-pulse-stable-gap-slope-bridge-stage5f-v2"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_route_c"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_stable_gap_slope_bridge_stage5f.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_stable_gap_slope_bridge_stage5f.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_stable_gap_slope_bridge_stage5f.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-stable-gap-slope-bridge-stage5f.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_stable_gap_slope_bridge_stage5f.py"
)

STAGE5E_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_oriented_adjoint_action_stage5e.json"
)
STAGE4E_RELATIVE_PATH = (
    "experiments/results/leaky_shared_yqq_deflation_stage4e.json"
)
STAGE5E_SHA256 = (
    "187b8c6d614aa87c68442acb9f5d472233907c31f0df8a1c8d29dfc6941743be"
)
STAGE4E_SHA256 = (
    "ccdd6023f911e97785ec6f8be97b84d725d6af9f5051e1da602380d225e47acc"
)

SELECTED_GRAPH_DERIVATIVE_TARGET = "16"
EXTRA_Q_NORM_GUARD = SCALAR_TRANSCRIPTION_GUARD
EXPECTED_PYTHON_VERSION = "3.14.4"
EXPECTED_GMPY2_VERSION = "2.2.2"
EXPECTED_MPFR_VERSION = "MPFR 4.2.1"
EXPECTED_NUMPY_VERSION = "2.5.2"
EXPECTED_SCIPY_VERSION = "1.18.0"
EXPECTED_OPENBLAS_NUM_THREADS = "8"
EXPECTED_OMP_NUM_THREADS = "1"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 "
    "experiments/leaky_pulse_stable_gap_slope_bridge_stage5f.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR replay of the source-bound Route-C section "
    "eigencolumn Wiener majorant, followed by outward interval evaluation "
    "of the exact rank-one projection identity and stable-gap slope gate"
)

HISTORY_SPACE = (
    "Y=C([-tau_max,0],R) x R with "
    "||(phi,w)||_Y=max(||phi||_infinity,|w|)"
)
SECTION_TANGENT_SPACE = (
    "Sigma={y in Y:y_v(0)=0}, equipped with the inherited Y max norm; "
    "q_phys, D_JK and Y_* all belong to Sigma"
)
PROJECTION_IDENTITY = (
    "P_s D_Jkappa=P_sD_JK=Y_*+q_phys(c_*-f_phys(D_JK)), "
    "where P_s=I-q_phys f_phys on Sigma, D_Jkappa=D_JK, "
    "and Y_*=D_JK-c_*q_phys"
)
THEOREM_STATEMENT = (
    "For the selected Stage-5C late-window Route-C event and the identical "
    "Stage-3/4D/5E Grushin pair on Sigma, the displayed source-bound norm "
    "implies that if the ambient chart contains kappa(I_J), the centered C1 "
    "stable graph is defined on P_s kappa(I_J), and sup||Dpsi||<=16, then "
    "H'(J)<0 on I_J.  A quantitative centered graph in this registered "
    "chart/normalization, chart/domain containment, event ordinal, endpoint "
    "signs, Newton root, onset and routing remain open."
)

CENTERED_CHART = {
    "reference_history": (
        "X_* is the exact validated inner periodic-orbit history at the "
        "Route-C phase-zero section"
    ),
    "event_history": (
        "K(J) is the Stage-5C selected late-window event-aligned reduced "
        "history on the Route-C section"
    ),
    "centered_pulse_history": "kappa(J)=K(J)-X_* in Sigma",
    "derivative_identity": "D_Jkappa(J)=D_JK(J)",
    "stable_sheet_gap": (
        "H(J):=f_phys(kappa(J))-psi(P_s kappa(J)); the centered local "
        "stable sheet is H=0"
    ),
}

PARAMETER_SCOPE = {
    "center_J0_exact": "2409/8000",
    "half_width_h_exact": "3/40000",
    "interval_exact": "I_J=[6021/20000,753/2500]",
    "normalized_parameter": "J=J0+h*xi with xi in [-1,1]",
    "parent_chain": (
        "the interval is inherited from the pinned Stage-5B->Stage-5C->"
        "Stage-5D->Stage-5E chain"
    ),
}

COORDINATE_COMPATIBILITY = {
    "normalization": "f_phys(q_phys)=1 exactly",
    "pair": (
        "q_phys and f_phys are the same Stage-3/4D Grushin right/left pair "
        "with the Stage-5E physical phase orientation"
    ),
    "projection": "P_s=I-q_phys f_phys on Sigma",
    "graph_derivative_norm": (
        "||Dpsi|| is the operator norm from (P_s Sigma, inherited Y max "
        "norm) to the scalar coordinate defined by this same f_phys"
    ),
    "phase_norm_invariance": (
        "q_phys=q_tilde/gamma and |gamma|=1, so the physical phase rotation "
        "does not change the exact Y norm"
    ),
    "forbidden_transfer": (
        "the Lpsi=16 gate cannot be imported from a finite left row, a "
        "different scaling of q, or a different history norm"
    ),
    "future_stage4_binding": (
        "a future Stage-4 graph certificate must byte-bind this Grushin "
        "normalization, Sigma, P_s and the continuous Y norm"
    ),
}

SELECTED_EVENT_SCOPE = {
    "event": (
        "the unique Route-C crossing in the late time window selected and "
        "validated by Stage 5C"
    ),
    "local_graph_relation": (
        "the event may be evaluated in the inner local Poincare graph only "
        "after kappa is proved to lie in the ambient chart and P_s kappa is "
        "proved to lie in the domain of psi"
    ),
    "ordinal_third_crossing_validated": False,
    "finite_third_return_pilot_role": (
        "the binary64 180-step third-return coordinate and its derivative "
        "use an unvalidated finite left row and are not evidence for this gate"
    ),
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_shared_yqq_deflation_stage4e.py",
    "src/canard_control/leaky_pulse_oriented_adjoint_action_stage5e.py",
)

TRUE_FLAGS = (
    "physical_phase_preserves_q_norm_validated",
    "route_c_q_phys_history_norm_upper_validated",
    "stable_projection_pulse_derivative_norm_upper_validated",
    "conditional_graph_slope_gate_with_Lpsi_16_validated",
    "conditional_gap_derivative_strictly_negative_validated",
)

FALSE_FLAGS = (
    "quantitative_inner_stable_graph_validated",
    "pulse_curve_contained_in_stable_graph_chart_validated",
    "unconditional_stable_gap_derivative_excludes_zero_validated",
    "stable_gap_endpoint_signs_validated",
    "interval_newton_strict_inclusion_validated",
    "unique_stable_sheet_pulse_parameter_Jc_validated",
    "unique_physical_pulse_onset_validated",
    "ordinal_third_crossing_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "asynchronous_network_safety_radius_validated",
    "frequency_amplitude_safety_radius_validated",
)

_FLAG_GROUPS = (TRUE_FLAGS, FALSE_FLAGS)
if any(len(group) != len(set(group)) for group in _FLAG_GROUPS):
    raise RuntimeError("Stage-5F claim flag groups must each be unique")
if set(TRUE_FLAGS) & set(FALSE_FLAGS):
    raise RuntimeError("Stage-5F claim flag groups must be disjoint")

EXPECTED_Q_NUMERIC_RECORDS = {
    "voltage_section_guide_wiener_upper": (
        "1.38298040920189145714386502363387765260102557004375432630050963"
    ),
    "recovery_section_guide_wiener_upper": (
        "0.517259064904607257427559143320394872096900221871823688930646296"
    ),
    "maximum_section_guide_wiener_upper": (
        "1.38298040920189145714386502363387765260102557004375432630050963"
    ),
    "section_column_error_upper": (
        "1.9449956486127083780035204596536857479804893955588340759281142e-07"
    ),
    "additional_transcription_guard_upper": (
        "9.99999999999999979886647629255615367252843506129522666015253543e-13"
    ),
    "q_phys_history_norm_upper": (
        "1.38298060370245631841470282396581026559885598345994672569132122"
    ),
}


@dataclass(frozen=True)
class Stage5FStableGapSlopeBridgeCertificate:
    schema_id: str
    model_id: str
    branch: str
    history_space: str
    section_tangent_space: str
    centered_chart: dict[str, Any]
    coordinate_compatibility: dict[str, Any]
    projection_identity: str
    selected_event_scope: dict[str, Any]
    parameter_scope: dict[str, Any]
    parent_action: dict[str, Any]
    q_phys_norm_enclosure: dict[str, Any]
    stable_projection_derivative: dict[str, Any]
    conditional_stable_gap_slope: dict[str, Any]
    theorem_statement: str
    claim_status: dict[str, bool]


TOP_KEYS = ("certificate", "manifest")
CERTIFICATE_KEYS = tuple(
    field.name for field in Stage5FStableGapSlopeBridgeCertificate.__dataclass_fields__.values()
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
    "certificate_sha256",
)
PARENT_ACTION_KEYS = (
    "center_c_star",
    "action_lower",
    "action_upper",
    "action_radius_upper",
    "correlated_residual_Y_norm_upper",
)
Q_NORM_KEYS = (
    *EXPECTED_Q_NUMERIC_RECORDS.keys(),
    "phase_rotation",
    "norm_transfer_reason",
    "positive_phase_wiener_guard_retained",
)
STABLE_DERIVATIVE_KEYS = (
    "formula",
    "correlated_residual_Y_norm_upper",
    "q_phys_history_norm_upper",
    "action_deviation_from_c_star_upper",
    "stable_projection_pulse_derivative_norm_upper",
)
GATE_KEYS = (
    "stable_sheet_chart",
    "derivative_identity",
    "open_antecedents",
    "selected_graph_derivative_norm_upper",
    "graph_correction_norm_upper",
    "conditional_gap_derivative_interval",
    "conditional_negative_margin_lower",
    "maximum_admissible_graph_derivative_norm_lower",
    "conditional_implication",
    "theorem_status",
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
            f"the Stage-5F replay environment changed: {actual} != {expected}"
        )
    return expected


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _exact_mapping(
    value: object, name: str, keys: tuple[str, ...]
) -> Mapping[str, Any]:
    mapped = _mapping(value, name)
    if set(mapped) != set(keys):
        raise ValueError(f"{name} keys changed")
    return mapped


def _load_bound_json(repository: Path, relative: str, expected_sha: str) -> dict[str, Any]:
    path = repository / relative
    actual = _sha256_path(path)
    if actual != expected_sha:
        raise ValueError(
            f"source-bound parent {relative} changed: {actual} != {expected_sha}"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"parent {relative} must contain a JSON object")
    return payload


def _point(value: str | int | gmpy2.mpfr) -> DirectedInterval:
    if isinstance(value, str) or isinstance(value, int):
        return DirectedInterval.from_decimal(value, PRECISION_BITS)
    return DirectedInterval.from_bounds(value, value, PRECISION_BITS)


@lru_cache(maxsize=1)
def _source_bound_q_norm_records(repository_text: str) -> dict[str, str]:
    """Replay a conservative ``Y``-norm bound for the physical eigencolumn.

    The stored complex-gauge section column is bounded before phase rotation.
    Since the physical rotation has unit modulus, the same upper bound applies
    to ``q_phys``.  The default positive-phase Wiener guard is intentionally
    retained even though the Route-C history interval is nonpositive.
    """

    repository = Path(repository_text).resolve()
    data = _centre_data(repository)
    uncertainty = _model_uncertainty(data)
    voltage_guide = _dictionary_l1_directed_upper(
        data.qsection_v, data.root, precision=PRECISION_BITS
    )
    recovery_guide = _dictionary_l1_directed_upper(
        data.qsection_w, data.root, precision=PRECISION_BITS
    )
    guide = max(voltage_guide, recovery_guide)
    q_error = DirectedInterval.from_bounds(
        0, uncertainty["qsection_error"], PRECISION_BITS
    )
    extra_guard = DirectedInterval.from_bounds(
        0, EXTRA_Q_NORM_GUARD, PRECISION_BITS
    )
    # Form the final sum from the *serialized outward upper endpoints* that
    # appear in the result.  This makes the public arithmetic ledger itself
    # composable: summing its displayed named terms cannot exceed the
    # displayed total merely because each Decimal rendering rounded upward.
    voltage_text = decimal_upper(voltage_guide)
    recovery_text = decimal_upper(recovery_guide)
    guide_text = decimal_upper(guide)
    q_error_text = decimal_upper(q_error.upper)
    extra_guard_text = decimal_upper(extra_guard.upper)
    q_upper = (
        _point(guide_text)
        + _point(q_error_text)
        + _point(extra_guard_text)
    )
    return {
        "voltage_section_guide_wiener_upper": voltage_text,
        "recovery_section_guide_wiener_upper": recovery_text,
        "maximum_section_guide_wiener_upper": guide_text,
        "section_column_error_upper": q_error_text,
        "additional_transcription_guard_upper": extra_guard_text,
        "q_phys_history_norm_upper": decimal_upper(q_upper.upper),
    }


def _parent_action_records(stage5e: Mapping[str, Any]) -> dict[str, str]:
    certificate = _mapping(stage5e.get("certificate"), "Stage-5E certificate")
    action = _mapping(certificate.get("oriented_action"), "Stage-5E action")
    residual = _mapping(
        certificate.get("correlated_history_action"),
        "Stage-5E correlated action",
    )
    interval = _mapping(action.get("physical_real_interval"), "physical action interval")
    return {
        "center_c_star": str(residual["center_c_star_exact"]),
        "action_lower": str(interval["lower"]),
        "action_upper": str(interval["upper"]),
        "action_radius_upper": str(action["quotient_radius_upper"]),
        "correlated_residual_Y_norm_upper": str(
            residual["maximum_correlated_residual_Y_norm_upper"]
        ),
    }


def _q_record_from_numeric(numeric: Mapping[str, Any]) -> dict[str, Any]:
    numeric_record = _exact_mapping(
        numeric,
        "Stage-5F q numeric record",
        tuple(EXPECTED_Q_NUMERIC_RECORDS),
    )
    return {
        **{key: str(numeric_record[key]) for key in EXPECTED_Q_NUMERIC_RECORDS},
        "phase_rotation": "q_phys=q_tilde/gamma with |gamma|=1",
        "norm_transfer_reason": (
            "unit-modulus phase rotation preserves the exact pointwise "
            "modulus; the common section-column error and an additional "
            "transcription guard are added before the norm bound"
        ),
        "positive_phase_wiener_guard_retained": True,
    }


def _derive_bridge_records(
    parent_action: Mapping[str, Any],
    q_record: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Derive every public Stage-5F inequality from serialized endpoints."""

    parent = _exact_mapping(
        parent_action, "Stage-5F parent action", PARENT_ACTION_KEYS
    )
    q = _exact_mapping(q_record, "Stage-5F q record", Q_NORM_KEYS)
    q_upper = _point(str(q["q_phys_history_norm_upper"]))
    residual_upper = _point(str(parent["correlated_residual_Y_norm_upper"]))
    action_radius = _point(str(parent["action_radius_upper"]))
    stable_upper = residual_upper + q_upper * action_radius
    stable_upper_text = decimal_upper(stable_upper.upper)

    # Downstream products start at the displayed outward endpoint, so the
    # public JSON ledger reproduces the proof without hidden extra precision.
    public_stable_upper = _point(stable_upper_text)
    action_lower = _point(str(parent["action_lower"]))
    action_upper = _point(str(parent["action_upper"]))
    graph_target = _point(SELECTED_GRAPH_DERIVATIVE_TARGET)
    graph_correction = graph_target * public_stable_upper
    derivative_lower = action_lower - graph_correction
    derivative_upper = action_upper + graph_correction
    if derivative_upper.upper >= 0:
        raise ArithmeticError("the selected conditional graph-slope gate did not close")

    zero = _point(0)
    maximum_admissible = (zero - action_upper) / public_stable_upper
    negative_margin = zero - derivative_upper
    stable = {
        "formula": (
            "||P_sD_Jkappa||_Y=||P_sD_JK||_Y <= ||Y_*||_Y + "
            "||q_phys||_Y |c_*-f_phys(D_JK)|"
        ),
        "correlated_residual_Y_norm_upper": str(
            parent["correlated_residual_Y_norm_upper"]
        ),
        "q_phys_history_norm_upper": str(q["q_phys_history_norm_upper"]),
        "action_deviation_from_c_star_upper": str(parent["action_radius_upper"]),
        "stable_projection_pulse_derivative_norm_upper": stable_upper_text,
    }
    gate = {
        "stable_sheet_chart": CENTERED_CHART["stable_sheet_gap"],
        "derivative_identity": (
            "H'(J)=f_phys(D_Jkappa)-Dpsi(P_s kappa)[P_sD_Jkappa]="
            "f_phys(D_JK)-Dpsi(P_s kappa)[P_sD_JK]"
        ),
        "open_antecedents": [
            (
                "a quantitative centered C1 stable graph psi exists in the "
                "identical Route-C chart and Grushin normalization"
            ),
            (
                "the ambient chart contains kappa(I_J) and the domain of psi "
                "contains P_s kappa(I_J)"
            ),
            (
                "sup_{J in I_J} ||Dpsi(P_s kappa(J))||, in the registered "
                "operator norm, is at most 16"
            ),
        ],
        "selected_graph_derivative_norm_upper": SELECTED_GRAPH_DERIVATIVE_TARGET,
        "graph_correction_norm_upper": decimal_upper(graph_correction.upper),
        "conditional_gap_derivative_interval": {
            "lower": decimal_lower(derivative_lower.lower),
            "upper": decimal_upper(derivative_upper.upper),
        },
        "conditional_negative_margin_lower": decimal_lower(negative_margin.lower),
        "maximum_admissible_graph_derivative_norm_lower": decimal_lower(
            maximum_admissible.lower
        ),
        "conditional_implication": (
            "if every open antecedent holds for the selected Stage-5C event, "
            "then H'(J)<0 throughout the full physical pulse interval"
        ),
        "theorem_status": (
            "PROVED conditional implication; a quantitative centered graph in "
            "this registered chart/normalization, chart/domain containment and "
            "its derivative bound remain OPEN"
        ),
    }
    return stable, gate


def build_stage5f_bridge_certificate(repository: Path) -> Stage5FStableGapSlopeBridgeCertificate:
    repository = Path(repository).resolve()
    _require_runtime()
    stage5e = _load_bound_json(repository, STAGE5E_RELATIVE_PATH, STAGE5E_SHA256)
    stage4e = _load_bound_json(repository, STAGE4E_RELATIVE_PATH, STAGE4E_SHA256)
    validate_stage5e_result(stage5e, repository)
    validate_stage4e_result(stage4e, repository)

    parent = _parent_action_records(stage5e)
    if Decimal(parent["action_upper"]) >= 0:
        raise ArithmeticError("the Stage-5E oriented action no longer excludes zero")

    q_numeric = _source_bound_q_norm_records(str(repository))
    if q_numeric != EXPECTED_Q_NUMERIC_RECORDS:
        raise ArithmeticError("the source-bound q-norm replay changed")
    q_records = _q_record_from_numeric(q_numeric)
    stable, gate = _derive_bridge_records(parent, q_records)

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage5FStableGapSlopeBridgeCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        history_space=HISTORY_SPACE,
        section_tangent_space=SECTION_TANGENT_SPACE,
        centered_chart=dict(CENTERED_CHART),
        coordinate_compatibility=dict(COORDINATE_COMPATIBILITY),
        projection_identity=PROJECTION_IDENTITY,
        selected_event_scope=dict(SELECTED_EVENT_SCOPE),
        parameter_scope=dict(PARAMETER_SCOPE),
        parent_action=parent,
        q_phys_norm_enclosure=q_records,
        stable_projection_derivative=stable,
        conditional_stable_gap_slope=gate,
        theorem_statement=THEOREM_STATEMENT,
        claim_status=claims,
    )


def _source_hashes(repository: Path) -> dict[str, str]:
    return {relative: _sha256_path(repository / relative) for relative in SOURCE_MANIFEST}


def build_stage5f_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    runtime = _require_runtime()
    certificate = asdict(build_stage5f_bridge_certificate(repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "precision_bits": PRECISION_BITS,
            **runtime,
            "parent_sha256": {
                STAGE5E_RELATIVE_PATH: STAGE5E_SHA256,
                STAGE4E_RELATIVE_PATH: STAGE4E_SHA256,
            },
            "source_sha256": _source_hashes(repository),
            "certificate_sha256": canonical_sha256(certificate),
        },
    }


def _clear_stage5f_replay_caches() -> None:
    _source_bound_q_norm_records.cache_clear()


def validate_stage5f_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = False
) -> None:
    repository = Path(repository).resolve()
    runtime = _require_runtime()
    result = _exact_mapping(payload, "Stage-5F result", TOP_KEYS)
    certificate = _exact_mapping(
        result.get("certificate"), "Stage-5F certificate", CERTIFICATE_KEYS
    )
    manifest = _exact_mapping(
        result.get("manifest"), "Stage-5F manifest", MANIFEST_KEYS
    )
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the Stage-5F schema id changed")
    if certificate.get("model_id") != MODEL_ID or certificate.get("branch") != BRANCH:
        raise ValueError("the Stage-5F model or branch changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the Stage-5F result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("the Stage-5F replay command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("the Stage-5F arithmetic scope changed")
    if manifest.get("precision_bits") != PRECISION_BITS:
        raise ValueError("the Stage-5F precision changed")
    for key, expected in runtime.items():
        if manifest.get(key) != expected:
            raise ValueError(f"the Stage-5F {key} replay ledger changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the Stage-5F certificate digest changed")
    if certificate.get("history_space") != HISTORY_SPACE:
        raise ValueError("the Stage-5F history space changed")
    if certificate.get("section_tangent_space") != SECTION_TANGENT_SPACE:
        raise ValueError("the Stage-5F section tangent space changed")
    if dict(_mapping(certificate.get("centered_chart"), "centered chart")) != CENTERED_CHART:
        raise ValueError("the Stage-5F centered chart changed")
    if dict(
        _mapping(
            certificate.get("coordinate_compatibility"),
            "coordinate compatibility",
        )
    ) != COORDINATE_COMPATIBILITY:
        raise ValueError("the Stage-5F coordinate compatibility changed")
    if certificate.get("projection_identity") != PROJECTION_IDENTITY:
        raise ValueError("the Stage-5F projection identity changed")
    if dict(
        _mapping(certificate.get("selected_event_scope"), "selected event scope")
    ) != SELECTED_EVENT_SCOPE:
        raise ValueError("the Stage-5F selected event scope changed")
    if dict(
        _mapping(certificate.get("parameter_scope"), "parameter scope")
    ) != PARAMETER_SCOPE:
        raise ValueError("the Stage-5F parameter scope changed")
    if certificate.get("theorem_statement") != THEOREM_STATEMENT:
        raise ValueError("the Stage-5F theorem statement changed")

    parent_hashes = _mapping(manifest.get("parent_sha256"), "parent hashes")
    expected_parents = {
        STAGE5E_RELATIVE_PATH: STAGE5E_SHA256,
        STAGE4E_RELATIVE_PATH: STAGE4E_SHA256,
    }
    if dict(parent_hashes) != expected_parents:
        raise ValueError("the Stage-5F parent hash manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"the Stage-5F parent bytes changed: {relative}")
    if dict(_mapping(manifest.get("source_sha256"), "source hashes")) != _source_hashes(repository):
        raise ValueError("the Stage-5F source hash manifest is stale")

    # Parent validation is part of every ingress: matching hashes alone are
    # insufficient evidence that the parents retain their theorem boundary.
    stage5e = _load_bound_json(repository, STAGE5E_RELATIVE_PATH, STAGE5E_SHA256)
    stage4e = _load_bound_json(repository, STAGE4E_RELATIVE_PATH, STAGE4E_SHA256)
    validate_stage5e_result(stage5e, repository)
    validate_stage4e_result(stage4e, repository)

    parent_action = _exact_mapping(
        certificate.get("parent_action"), "parent action", PARENT_ACTION_KEYS
    )
    if dict(parent_action) != _parent_action_records(stage5e):
        raise ValueError("the Stage-5F parent action differs from Stage 5E")
    q_record = _exact_mapping(
        certificate.get("q_phys_norm_enclosure"), "q norm", Q_NORM_KEYS
    )
    expected_q = _q_record_from_numeric(EXPECTED_Q_NUMERIC_RECORDS)
    if dict(q_record) != expected_q:
        raise ValueError("the Stage-5F q-norm record changed")
    stable = _exact_mapping(
        certificate.get("stable_projection_derivative"),
        "stable projection derivative",
        STABLE_DERIVATIVE_KEYS,
    )
    gate = _exact_mapping(
        certificate.get("conditional_stable_gap_slope"),
        "conditional stable-gap slope",
        GATE_KEYS,
    )
    interval = _exact_mapping(
        gate.get("conditional_gap_derivative_interval"),
        "conditional derivative interval",
        INTERVAL_KEYS,
    )
    expected_stable, expected_gate = _derive_bridge_records(parent_action, q_record)
    if dict(stable) != expected_stable:
        raise ValueError("the Stage-5F stable derivative ledger changed")
    if dict(gate) != expected_gate:
        raise ValueError("the Stage-5F graph-slope gate changed")

    # The public endpoints carry roughly 60 decimal digits.  Do not let the
    # Decimal module's default 28-digit context introduce a second, unrelated
    # rounding layer into this independently recomputable ledger.
    with localcontext() as context:
        context.prec = 200
        q_sum = (
            Decimal(q_record["maximum_section_guide_wiener_upper"])
            + Decimal(q_record["section_column_error_upper"])
            + Decimal(q_record["additional_transcription_guard_upper"])
        )
        if Decimal(q_record["q_phys_history_norm_upper"]) < q_sum:
            raise ValueError("the registered q norm does not cover its named terms")
        stable_sum = (
            Decimal(parent_action["correlated_residual_Y_norm_upper"])
            + Decimal(q_record["q_phys_history_norm_upper"])
            * Decimal(parent_action["action_radius_upper"])
        )
        if Decimal(stable["stable_projection_pulse_derivative_norm_upper"]) < stable_sum:
            raise ValueError("the stable-projection derivative bound is too small")
        graph_target = Decimal(gate["selected_graph_derivative_norm_upper"])
        correction = graph_target * Decimal(
            stable["stable_projection_pulse_derivative_norm_upper"]
        )
        if Decimal(gate["graph_correction_norm_upper"]) < correction:
            raise ValueError("the registered graph correction is too small")
        if Decimal(interval["upper"]) >= 0:
            raise ValueError("the conditional gap derivative no longer excludes zero")
        if Decimal(gate["conditional_negative_margin_lower"]) <= 0:
            raise ValueError("the conditional negative margin vanished")
        if Decimal(gate["maximum_admissible_graph_derivative_norm_lower"]) <= graph_target:
            raise ValueError("the selected graph target is not strictly admissible")

    claims = _mapping(certificate.get("claim_status"), "Stage-5F claim status")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-5F claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved conditional bridge flag is not true: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open downstream claim was promoted: {name}")

    if recompute:
        _clear_stage5f_replay_caches()
        expected = asdict(build_stage5f_bridge_certificate(repository))
        if dict(certificate) != expected:
            raise ValueError("the Stage-5F certificate differs from a fresh replay")
