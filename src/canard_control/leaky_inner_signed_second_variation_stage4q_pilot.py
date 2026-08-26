"""Stage-4Q signed event-aligned second-variation pilot.

The primary row is the selected near-two-period Route-C event branch.  A
near-one-period row is retained only to expose why it is not a full-history
``C^2`` object: ``P-tau_max < tau_max``.  At two periods the corresponding
smoothing inequality is satisfied at the centre, but every numerical value
below remains a finite-section, binary floating-point diagnostic.

For each mesh this module propagates the physical first and second
variations through two periods, forms the moving-event correction and the
entire translated returned history, applies one fixed discretization of the
Stage-4L/Stage-4D Grushin pair, and only then takes norms.  It also compares
the direct two-period tensor with the discrete composition identity

    D2(P o P)[h,k] = D2P[DP h, DP k] + DP D2P[h,k].

No outward rounding, continuous-history discretization estimate, nonlinear
return tube, selected-first-return theorem, Hessian bound, stable graph, or
biological routing statement is made here.  In particular every field in
``claim_status`` is deliberately false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import numpy as np
from scipy.optimize import minimize_scalar

from canard_control.leaky_inner_enlarged_return_hessian_stage4m_contract import (
    RESULT_RELATIVE_PATH as STAGE4M_RESULT_RELATIVE_PATH,
    validate_stage4m_result,
)
from canard_control.leaky_inner_graph_closure_arithmetic_stage4p import (
    RESULT_RELATIVE_PATH as STAGE4P_RESULT_RELATIVE_PATH,
    validate_stage4p_result,
)
from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility import (
    RESULT_RELATIVE_PATH as STAGE4N_RESULT_RELATIVE_PATH,
    validate_stage4n_feasibility_result,
)
from canard_control.leaky_inner_signed_stable_flow_stage4h import (
    QUADRATURE_MAX_PANEL,
    _FourWordDiagnostic,
)
from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    RESULT_RELATIVE_PATH as STAGE4L_RESULT_RELATIVE_PATH,
    validate_stage4l_result,
)
from canard_control.leaky_inner_word_primitive_stage4i import (
    RESULT_RELATIVE_PATH as STAGE4I_RESULT_RELATIVE_PATH,
    validate_stage4i_result,
)
from canard_control.leaky_periodic_branch_artifact import (
    validate_leaky_periodic_branch_artifact,
)
from canard_control.leaky_projected_return_hessian_stage4a_pilot import (
    INNER_ORBIT_RESULT_RELATIVE_PATH,
    _LongDoubleFourierOrbit,
    _Model,
    _base_second_derivative,
    _cubic_weights,
    _field,
    _hessian_coefficients,
    _linear_coefficients,
    _model_from_payload,
    _dominant_split,
)


SCHEMA_ID = "leaky-inner-signed-second-variation-stage4q-pilot-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_two_period_event"
STATUS = "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_signed_second_variation_stage4q_pilot.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_signed_second_variation_stage4q_pilot.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_signed_second_variation_stage4q_pilot.json"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-inner-signed-second-variation-stage4q-pilot.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_signed_second_variation_stage4q_pilot.py"
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/leaky_projected_return_hessian_stage4a_pilot.py",
    "src/canard_control/leaky_inner_signed_stable_flow_stage4h.py",
    "src/canard_control/leaky_inner_word_primitive_stage4i.py",
    "src/canard_control/leaky_inner_terminal_stable_row_stage4l.py",
    "src/canard_control/leaky_inner_enlarged_return_hessian_stage4m_contract.py",
    "src/canard_control/leaky_inner_graph_closure_arithmetic_stage4p.py",
    "src/canard_control/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py",
)

INNER_ORBIT_RESULT_SHA256 = (
    "bee1da065d213c3c33d724ced1dba37c5914934515c1128588919bed34abe69b"
)
STAGE4I_RESULT_SHA256 = (
    "1248e9d95444f3cc12565c1e11b4bbeab3d4a9a7bb8922893e38b1ffa439f73e"
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
STAGE4P_RESULT_SHA256 = (
    "860a51d51648919f74bd7bd4e8230a629f7864b2bdcccf490aab5ff9e8e6b542"
)
PARENT_RESULT_SHA256 = {
    INNER_ORBIT_RESULT_RELATIVE_PATH: INNER_ORBIT_RESULT_SHA256,
    STAGE4I_RESULT_RELATIVE_PATH: STAGE4I_RESULT_SHA256,
    STAGE4L_RESULT_RELATIVE_PATH: STAGE4L_RESULT_SHA256,
    STAGE4M_RESULT_RELATIVE_PATH: STAGE4M_RESULT_SHA256,
    STAGE4N_RESULT_RELATIVE_PATH: STAGE4N_RESULT_SHA256,
    STAGE4P_RESULT_RELATIVE_PATH: STAGE4P_RESULT_SHA256,
}

PINNED_OPENBLAS_NUM_THREADS = "8"
PINNED_OMP_NUM_THREADS = "1"
DEFAULT_PERIOD_STEP_COUNTS = (120, 180, 240)
PRIMARY_RETURN_PERIODS = 2
Q_NORM_SAMPLE_COUNT = 4097
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 "
    "experiments/leaky_inner_signed_second_variation_stage4q_pilot.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-result and source-byte binding; numpy.longdouble fixed-step "
    "RK4 first/second physical variational equations with cubic delayed "
    "interpolation; fixed physical phase of the Stage-4L Grushin q,f pair; "
    "near-one- versus near-two-period full-history smoothing gate; Stage-4P "
    "two-return simultaneous design box and conditional K_ret target; signed "
    "moving-event correction and complete returned-history translation before "
    "fixed input/output projections and norms; direct two-period versus "
    "discrete composition oracle; no outward rounding, continuous-history "
    "operator error, uniform nonlinear tube, selected first return, certified "
    "Hessian block, graph, crossing, onset, routing, capture, or safety claim"
)

BLOCK_NAMES = (
    "stable_output_ss_upper",
    "stable_output_su_upper",
    "stable_output_uu_upper",
    "unstable_output_ss_upper",
    "unstable_output_su_upper",
    "unstable_output_uu_upper",
)
FORMATION_ORDER = (
    "propagate_signed_physical_first_and_second_variations",
    "form_terminal_moving_event_time_derivatives",
    "translate_every_returned_history_coordinate_at_the_common_event",
    "contract_inputs_with_fixed_Ps_or_qhat",
    "apply_fixed_fhat_to_each_correlated_output_sector",
    "subtract_qhat_times_the_same_unstable_output_sector",
    "take_finite_section_linf_and_l1_tensor_norms",
)
THEOREM_FLAGS = (
    "binary_floating_rows_are_outward_rounded",
    "one_period_map_is_c2_on_the_full_history_space",
    "two_period_finite_section_tensor_is_a_continuous_history_operator_bound",
    "two_period_selected_event_branch_exists_uniformly_on_a_ball",
    "two_period_event_is_the_second_positive_oriented_hit",
    "no_earlier_section_hit_is_validated",
    "uniform_event_speed_lower_bound_is_validated",
    "complete_returned_history_tube_is_validated",
    "fixed_unit_y_grushin_discretization_error_is_validated",
    "actual_signed_event_aligned_kret_upper_is_validated",
    "six_projected_hessian_blocks_are_validated",
    "all_stage4m_strict_caps_are_proved",
    "nonlinear_selected_return_tube_is_validated",
    "quantitative_inner_stable_graph_is_validated",
    "pulse_sheet_crossing_is_validated",
    "unique_physical_pulse_onset_is_validated",
    "two_sided_basin_routing_is_validated",
    "biological_capture_is_validated",
    "network_safety_is_validated",
)


@dataclass(frozen=True)
class Stage4QPilot:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    selected_branch_and_smoothing: dict[str, Any]
    fixed_grushin_coordinate: dict[str, Any]
    signed_formation_order: dict[str, Any]
    mesh_rows: tuple[dict[str, Any], ...]
    refinement_and_acceptance: dict[str, Any]
    diagnostic_checks: dict[str, bool]
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


def _format(value: Any) -> str:
    return format(np.longdouble(value), ".21g")


def _require_runtime() -> None:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-4Q requires OPENBLAS_NUM_THREADS=8")
    if os.environ.get("OMP_NUM_THREADS") != PINNED_OMP_NUM_THREADS:
        raise RuntimeError("Stage-4Q requires OMP_NUM_THREADS=1")


def _load_json(repository: Path, relative: str, digest: str) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError(f"the Stage-4Q parent changed: {relative}")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the Stage-4Q parent is malformed: {relative}")
    return payload


def _load_and_validate_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    parents = {
        relative: _load_json(repository, relative, digest)
        for relative, digest in PARENT_RESULT_SHA256.items()
    }
    validate_leaky_periodic_branch_artifact(
        parents[INNER_ORBIT_RESULT_RELATIVE_PATH], repository
    )
    validate_stage4i_result(parents[STAGE4I_RESULT_RELATIVE_PATH], repository)
    validate_stage4l_result(
        parents[STAGE4L_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    validate_stage4m_result(
        parents[STAGE4M_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    validate_stage4n_feasibility_result(
        parents[STAGE4N_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    validate_stage4p_result(
        parents[STAGE4P_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    return parents


def _stage4m_caps(payload: Mapping[str, Any]) -> dict[str, str]:
    contract = _mapping(payload.get("contract"), "Stage-4M contract")
    ledger = _mapping(contract.get("common_cap_ledger"), "Stage-4M cap ledger")
    records = ledger.get("records")
    if not isinstance(records, list):
        raise ValueError("the Stage-4M cap records are malformed")
    caps = {
        str(record["block"]): str(record["strict_cap_decimal_exact"])
        for record in records
    }
    if set(caps) != set(BLOCK_NAMES):
        raise ValueError("the Stage-4M six-cap set changed")
    return caps


def _stage4n_kret_target(payload: Mapping[str, Any]) -> str:
    pilot = _mapping(payload.get("pilot"), "Stage-4N feasibility pilot")
    target = _mapping(
        pilot.get("conditional_terminal_kernel_target"),
        "Stage-4N kernel target",
    )
    return str(target["strict_kernel_target_lower"])


def _stage4p_two_return_design(
    payload: Mapping[str, Any]
) -> tuple[dict[str, str], str, dict[str, Any]]:
    design = _mapping(payload.get("design"), "Stage-4P design")
    two = _mapping(design.get("two_return_design"), "Stage-4P two-return design")
    wide = _mapping(
        two.get("recommended_wide_proof_box"), "Stage-4P wide proof box"
    )
    blocks = {
        str(name): str(value)
        for name, value in _mapping(wide.get("blocks"), "Stage-4P wide blocks").items()
    }
    if set(blocks) != set(BLOCK_NAMES):
        raise ValueError("the Stage-4P two-return block set changed")
    if (
        wide.get("raw_graph_arithmetic_closes") is not True
        or wide.get("entered_into_strict_numeric_ingress") is not False
        or wide.get("blocks_are_source_bound_continuous_history_bounds") is not False
    ):
        raise ValueError("the Stage-4P wide-box claim boundary changed")
    target = str(wide["conditional_kret_target_lower"])
    coupling = _mapping(design.get("kret_coupling"), "Stage-4P Kret coupling")
    metadata = {
        "result_path": STAGE4P_RESULT_RELATIVE_PATH,
        "result_sha256": STAGE4P_RESULT_SHA256,
        "box_label": str(wide["label"]),
        "simultaneous_box_graph_arithmetic_closes_conditionally": True,
        "box_is_a_directed_hessian_bound": False,
        "box_entered_into_strict_numeric_ingress": False,
        "pair_sum_implies_conditional_kret_target": bool(
            wide["pair_sum_implies_conditional_kret_target"]
        ),
        "kret_is_required_by_matrix_lyapunov_perron_arithmetic": bool(
            coupling["kret_is_required_by_matrix_lyapunov_perron_arithmetic"]
        ),
        "scalar_kret_is_only_a_sufficient_return_domain_route": True,
    }
    return blocks, target, metadata


def _physical_grushin_data(
    diagnostic: _FourWordDiagnostic,
) -> tuple[complex, np.longdouble, list[tuple[float, complex]], dict[str, Any]]:
    q_w_zero = diagnostic.evaluate(diagnostic.data.qsection_w, 0.0)
    if abs(q_w_zero) <= 1.0e-14:
        raise ArithmeticError("the Grushin phase anchor vanished")
    phase = q_w_zero / abs(q_w_zero)

    sample_times = np.linspace(-diagnostic.tau1, 0.0, Q_NORM_SAMPLE_COUNT)
    q_samples = np.asarray(
        [
            (diagnostic.evaluate(diagnostic.data.qsection_v, float(time)) / phase).real
            for time in sample_times
        ],
        dtype=float,
    )
    absolute = np.abs(q_samples)
    candidate_indices = np.argpartition(absolute, -8)[-8:]
    candidates = [float(absolute[index]) for index in candidate_indices]
    refined_locations: list[float] = []
    for index in candidate_indices:
        left = float(sample_times[max(0, index - 1)])
        right = float(sample_times[min(len(sample_times) - 1, index + 1)])
        if right <= left:
            continue
        result = minimize_scalar(
            lambda time: -abs(
                diagnostic.evaluate(diagnostic.data.qsection_v, time) / phase
            ),
            bounds=(left, right),
            method="bounded",
            options={"xatol": 1.0e-14},
        )
        candidates.append(float(-result.fun))
        refined_locations.append(float(result.x))
    q_recovery = abs((q_w_zero / phase).real)
    q_norm = np.longdouble(max([q_recovery, *candidates]))

    quadrature_samples: list[tuple[float, complex]] = []
    breaks = diagnostic.integration_breaks()
    for left, right in zip(breaks[:-1], breaks[1:], strict=True):
        panel_count = max(
            1, int(math.ceil((right - left) / QUADRATURE_MAX_PANEL))
        )
        edges = np.linspace(left, right, panel_count + 1)
        for panel_left, panel_right in zip(edges[:-1], edges[1:], strict=True):
            points = (
                0.5 * (panel_left + panel_right)
                + 0.5 * (panel_right - panel_left) * diagnostic.nodes
            )
            factor = 0.5 * (panel_right - panel_left)
            for weight, point in zip(diagnostic.weights, points, strict=True):
                normalized_density = (
                    phase * diagnostic.f_density(float(point)) / diagnostic.fq
                )
                quadrature_samples.append(
                    (float(point), complex(factor * weight * normalized_density))
                )

    max_q_imag = 0.0
    max_f_imag = 0.0
    for time in np.linspace(-diagnostic.tau1, 0.0, 257):
        max_q_imag = max(
            max_q_imag,
            abs(
                (
                    diagnostic.evaluate(diagnostic.data.qsection_v, float(time))
                    / phase
                ).imag
            ),
        )
        max_f_imag = max(
            max_f_imag,
            abs(
                (
                    phase
                    * diagnostic.f_density(float(time))
                    / diagnostic.fq
                ).imag
            ),
        )
    recovery_functional = phase * diagnostic.f_recovery_atom / diagnostic.fq
    max_f_imag = max(max_f_imag, abs(recovery_functional.imag))
    metadata = {
        "physical_phase_anchor": "q_w(0) is positive real",
        "complex_phase_real": _format(phase.real),
        "complex_phase_imag": _format(phase.imag),
        "continuous_q_norm_finite_sample_candidate": _format(q_norm),
        "q_norm_sample_count": Q_NORM_SAMPLE_COUNT,
        "q_norm_refined_local_maximizers": len(refined_locations),
        "sampled_rotated_q_max_imaginary_residual": _format(max_q_imag),
        "sampled_rotated_f_max_imaginary_residual": _format(max_f_imag),
        "normalized_recovery_functional_real": _format(
            recovery_functional.real
        ),
        "normalized_recovery_functional_imag": _format(
            recovery_functional.imag
        ),
        "quadrature_node_count": len(quadrature_samples),
        "continuous_q_norm_is_validated": False,
        "continuous_f_discretization_is_validated": False,
    }
    return phase, q_norm, quadrature_samples, metadata


def _discrete_grushin_pair(
    diagnostic: _FourWordDiagnostic,
    phase: complex,
    q_norm: np.longdouble,
    quadrature_samples: list[tuple[float, complex]],
    step: np.longdouble,
    history_steps: int,
    *,
    boundary_mode: str = "one_sided_four_node",
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    dimension = history_steps + 1
    qhat_complex = np.zeros(dimension, dtype=np.clongdouble)
    for index in range(-history_steps, 0):
        qhat_complex[index + history_steps] = (
            diagnostic.evaluate(
                diagnostic.data.qsection_v,
                float(np.longdouble(index) * step),
            )
            / phase
            / q_norm
        )
    qhat_complex[-1] = (
        diagnostic.evaluate(diagnostic.data.qsection_w, 0.0)
        / phase
        / q_norm
    )

    fhat_complex = np.zeros(dimension, dtype=np.clongdouble)
    for point, weighted_density in quadrature_samples:
        location = np.longdouble(point) / step
        left = int(np.floor(location))
        if boundary_mode == "one_sided_four_node":
            start = min(left - 1, -3)
            start = max(start, -history_steps)
            nodes = tuple(range(start, start + 4))
            weights_list: list[np.longdouble] = []
            for node in nodes:
                weight = np.longdouble(1)
                for other in nodes:
                    if other != node:
                        weight *= (location - np.longdouble(other)) / np.longdouble(
                            node - other
                        )
                weights_list.append(weight)
            weights = tuple(weights_list)
        elif boundary_mode == "discarded_zero_nonsection_stencil":
            fraction = location - np.longdouble(left)
            weights = _cubic_weights(fraction)
            nodes = (left - 1, left, left + 1, left + 2)
        else:
            raise ValueError("unknown Stage-4Q Grushin boundary adapter")
        for weight, node in zip(weights, nodes, strict=True):
            if -history_steps <= node <= -1:
                fhat_complex[node + history_steps] += (
                    np.clongdouble(q_norm)
                    * np.clongdouble(weighted_density)
                    * np.clongdouble(weight)
                )
            elif node >= 0:
                # This branch is reachable only for the explicitly discarded
                # symmetric-stencil audit.  The primary one-sided adapter uses
                # nodes -3,-2,-1,0 and the section value at node 0 is zero.
                continue
            elif node < -history_steps:
                raise ArithmeticError("the Grushin quadrature escaped the grid")
    fhat_complex[-1] += (
        np.clongdouble(q_norm)
        * np.clongdouble(phase)
        * np.clongdouble(diagnostic.f_recovery_atom)
        / np.clongdouble(diagnostic.fq)
    )

    qhat = np.asarray(qhat_complex.real, dtype=np.longdouble)
    fhat = np.asarray(fhat_complex.real, dtype=np.longdouble)
    pairing_before = fhat @ qhat
    if abs(pairing_before) <= np.longdouble("0.5"):
        raise ArithmeticError("the discrete Grushin pairing collapsed")
    fhat /= pairing_before
    pairing_after = fhat @ qhat
    metadata = {
        "section_dimension": dimension,
        "qhat_nodal_linf": _format(np.max(np.abs(qhat))),
        "fhat_nodal_l1": _format(np.sum(np.abs(fhat))),
        "pairing_before_discrete_correction": _format(pairing_before),
        "pairing_after_discrete_correction": _format(pairing_after),
        "relative_discrete_pairing_correction": _format(
            abs(np.longdouble(1) / pairing_before - np.longdouble(1))
        ),
        "qhat_max_imaginary_discarded": _format(
            np.max(np.abs(qhat_complex.imag))
        ),
        "fhat_max_imaginary_discarded": _format(
            np.max(np.abs(fhat_complex.imag))
        ),
        "boundary_interpolation": boundary_mode,
        "current_voltage_node_zero_on_sigma0": True,
        "positive_time_nodes_used": False,
        "pairing_identity_enforced_in_finite_section": True,
        "finite_section_adapter_validated": False,
    }
    return qhat, fhat, metadata


def _propagate_two_period_variations(
    orbit: _LongDoubleFourierOrbit,
    model: _Model,
    period_step_count: int,
) -> tuple[
    tuple[np.ndarray, np.ndarray, dict[str, Any]],
    tuple[np.ndarray, np.ndarray, dict[str, Any]],
    dict[str, Any],
]:
    period = orbit.period
    step = period / np.longdouble(period_step_count)
    history_steps = int(np.ceil(model.tau_1 / step)) + 3
    dimension = history_steps + 1
    final_step_count = 2 * period_step_count
    storage = history_steps + final_step_count + 1
    u_voltage: list[np.ndarray | None] = [None] * storage
    v_voltage: list[np.ndarray | None] = [None] * storage
    u_recovery: list[np.ndarray | None] = [None] * storage
    v_recovery: list[np.ndarray | None] = [None] * storage

    for index in range(-history_steps, 0):
        basis = np.zeros(dimension, dtype=np.longdouble)
        basis[index + history_steps] = 1
        u_voltage[index + history_steps] = basis
        v_voltage[index + history_steps] = np.zeros(
            (dimension, dimension), dtype=np.longdouble
        )
    u_voltage[history_steps] = np.zeros(dimension, dtype=np.longdouble)
    v_voltage[history_steps] = np.zeros(
        (dimension, dimension), dtype=np.longdouble
    )
    recovery_basis = np.zeros(dimension, dtype=np.longdouble)
    recovery_basis[-1] = 1
    u_recovery[history_steps] = recovery_basis
    v_recovery[history_steps] = np.zeros(
        (dimension, dimension), dtype=np.longdouble
    )

    def stored(values: list[np.ndarray | None], index: int) -> np.ndarray:
        value = values[index + history_steps]
        if value is None:
            raise ArithmeticError("the Stage-4Q grid requested unavailable data")
        return value

    def delayed(
        values: list[np.ndarray | None], location: np.longdouble
    ) -> np.ndarray:
        left = int(np.floor(location))
        fraction = location - np.longdouble(left)
        weights = _cubic_weights(fraction)
        return sum(
            (
                weight * stored(values, node)
                for weight, node in zip(
                    weights,
                    (left - 1, left, left + 1, left + 2),
                    strict=True,
                )
            ),
            np.zeros_like(stored(values, left)),
        )

    def rhs(
        time: np.longdouble,
        uv: np.ndarray,
        uw: np.ndarray,
        vv: np.ndarray,
        vw: np.ndarray,
        grid_index: int,
        stage: np.longdouble,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        current, coefficient_0, coefficient_1 = _linear_coefficients(
            orbit, model, time
        )
        h_current, h_0, h_1 = _hessian_coefficients(orbit, model, time)
        location_0 = np.longdouble(grid_index) + stage - model.tau_0 / step
        location_1 = np.longdouble(grid_index) + stage - model.tau_1 / step
        uv_0 = delayed(u_voltage, location_0)
        uv_1 = delayed(u_voltage, location_1)
        vv_0 = delayed(v_voltage, location_0)
        vv_1 = delayed(v_voltage, location_1)
        duv = current * uv - uw + coefficient_0 * uv_0 + coefficient_1 * uv_1
        duw = model.epsilon * (uv - uw)
        dvv = (
            current * vv
            - vw
            + coefficient_0 * vv_0
            + coefficient_1 * vv_1
            + h_current * np.outer(uv, uv)
            + h_0 * np.outer(uv_0, uv_0)
            + h_1 * np.outer(uv_1, uv_1)
        )
        dvw = model.epsilon * (vv - vw)
        return duv, duw, dvv, dvw

    half = np.longdouble("0.5")
    one = np.longdouble(1)
    for grid_index in range(final_step_count):
        uv = stored(u_voltage, grid_index)
        uw = stored(u_recovery, grid_index)
        vv = stored(v_voltage, grid_index)
        vw = stored(v_recovery, grid_index)
        time = np.longdouble(grid_index) * step
        k1 = rhs(time, uv, uw, vv, vw, grid_index, np.longdouble(0))
        k2 = rhs(
            time + half * step,
            uv + half * step * k1[0],
            uw + half * step * k1[1],
            vv + half * step * k1[2],
            vw + half * step * k1[3],
            grid_index,
            half,
        )
        k3 = rhs(
            time + half * step,
            uv + half * step * k2[0],
            uw + half * step * k2[1],
            vv + half * step * k2[2],
            vw + half * step * k2[3],
            grid_index,
            half,
        )
        k4 = rhs(
            time + step,
            uv + step * k3[0],
            uw + step * k3[1],
            vv + step * k3[2],
            vw + step * k3[3],
            grid_index,
            one,
        )
        index = grid_index + 1
        u_voltage[index + history_steps] = uv + step * (
            k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]
        ) / 6
        u_recovery[index + history_steps] = uw + step * (
            k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]
        ) / 6
        v_voltage[index + history_steps] = vv + step * (
            k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]
        ) / 6
        v_recovery[index + history_steps] = vw + step * (
            k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]
        ) / 6

    def event_map(
        horizon_steps: int, return_periods: int
    ) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
        horizon = np.longdouble(return_periods) * period
        final_uv = stored(u_voltage, horizon_steps)
        final_uw = stored(u_recovery, horizon_steps)
        final_vv = stored(v_voltage, horizon_steps)
        final_vw = stored(v_recovery, horizon_steps)
        final_rhs = rhs(
            horizon,
            final_uv,
            final_uw,
            final_vv,
            final_vw,
            horizon_steps,
            np.longdouble(0),
        )
        event_speed = _field(orbit, model, horizon)[0]
        if event_speed <= 0:
            raise ArithmeticError("the Stage-4Q event has wrong orientation")
        tau_one = -final_uv / event_speed
        second_base = _base_second_derivative(orbit, model, horizon)
        event_core = (
            final_vv
            + np.outer(final_rhs[0], tau_one)
            + np.outer(tau_one, final_rhs[0])
            + second_base[0] * np.outer(tau_one, tau_one)
        )
        tau_two = -event_core / event_speed

        jacobian_rows: list[np.ndarray] = []
        hessian_rows: list[np.ndarray] = []
        for index in range(horizon_steps - history_steps, horizon_steps):
            uv = stored(u_voltage, index)
            uw = stored(u_recovery, index)
            vv = stored(v_voltage, index)
            vw = stored(v_recovery, index)
            derivative = rhs(
                np.longdouble(index) * step,
                uv,
                uw,
                vv,
                vw,
                index,
                np.longdouble(0),
            )
            velocity = _field(orbit, model, np.longdouble(index) * step)[0]
            acceleration = _base_second_derivative(
                orbit, model, np.longdouble(index) * step
            )[0]
            jacobian_rows.append(uv + velocity * tau_one)
            hessian_rows.append(
                vv
                + np.outer(derivative[0], tau_one)
                + np.outer(tau_one, derivative[0])
                + acceleration * np.outer(tau_one, tau_one)
                + velocity * tau_two
            )
        recovery_velocity = _field(orbit, model, horizon)[1]
        recovery_acceleration = second_base[1]
        jacobian_rows.append(final_uw + recovery_velocity * tau_one)
        hessian_rows.append(
            final_vw
            + np.outer(final_rhs[1], tau_one)
            + np.outer(tau_one, final_rhs[1])
            + recovery_acceleration * np.outer(tau_one, tau_one)
            + recovery_velocity * tau_two
        )
        jacobian = np.asarray(jacobian_rows, dtype=np.longdouble)
        hessian = np.asarray(hessian_rows, dtype=np.longdouble)
        current_section_jacobian = final_uv + event_speed * tau_one
        current_section_hessian = event_core + event_speed * tau_two
        diagnostics = {
            "return_periods": return_periods,
            "selected_event_target_time": _format(horizon),
            "base_event_speed": _format(event_speed),
            "base_orbit_field_vs_fourier_tangent_inf": _format(
                np.max(
                    np.abs(
                        _field(orbit, model, horizon)
                        - orbit.evaluate(horizon, 1)
                    )
                )
            ),
            "first_event_identity_defect_inf": _format(
                np.max(np.abs(current_section_jacobian))
            ),
            "second_event_identity_defect_inf": _format(
                np.max(np.abs(current_section_hessian))
            ),
            "return_hessian_symmetry_defect_inf": _format(
                np.max(np.abs(hessian - np.swapaxes(hessian, 1, 2)))
            ),
            "return_time_d1_ambient_linf_operator_norm": _format(
                np.sum(np.abs(tau_one))
            ),
            "return_time_d2_ambient_linf_bilinear_upper": _format(
                np.sum(np.abs(tau_two))
            ),
            "positive_orientation_at_base": True,
            "selected_event_exists_uniformly": False,
            "no_earlier_hit_validated": False,
        }
        return jacobian, hessian, diagnostics

    common = {
        "period_step_count": period_step_count,
        "total_two_period_step_count": final_step_count,
        "step_size": _format(step),
        "history_padding_steps": history_steps,
        "section_dimension": dimension,
        "integrator": "fixed-step classical RK4",
        "delay_interpolation": "four-node cubic Lagrange",
        "state_arithmetic": "numpy.longdouble",
    }
    return (
        event_map(period_step_count, 1),
        event_map(final_step_count, 2),
        common,
    )


def _block_diagnostics(
    hessian: np.ndarray, qhat: np.ndarray, fhat: np.ndarray
) -> dict[str, Any]:
    h_q = np.einsum("oij,j->oi", hessian, qhat, optimize=True)
    h_qq = np.einsum("oi,i->o", h_q, qhat, optimize=True)
    h_ss = (
        hessian
        - fhat[None, :, None] * h_q[:, None, :]
        - h_q[:, :, None] * fhat[None, None, :]
        + h_qq[:, None, None] * fhat[None, :, None] * fhat[None, None, :]
    )
    h_su = h_q - h_qq[:, None] * fhat[None, :]
    unstable_ss = np.einsum("o,oij->ij", fhat, h_ss, optimize=True)
    unstable_su = np.einsum("o,oi->i", fhat, h_su, optimize=True)
    unstable_uu = fhat @ h_qq
    stable_ss = h_ss - qhat[:, None, None] * unstable_ss[None, :, :]
    stable_su = h_su - qhat[:, None] * unstable_su[None, :]
    stable_uu = h_qq - qhat * unstable_uu

    raw_sector = {
        "ss": np.max(np.sum(np.abs(h_ss), axis=(1, 2))),
        "su": np.max(np.sum(np.abs(h_su), axis=1)),
        "uu": np.max(np.abs(h_qq)),
    }
    unstable_sector = {
        "ss": np.sum(np.abs(unstable_ss)),
        "su": np.sum(np.abs(unstable_su)),
        "uu": abs(unstable_uu),
    }
    stable_sector = {
        "ss": np.max(np.sum(np.abs(stable_ss), axis=(1, 2))),
        "su": np.max(np.sum(np.abs(stable_su), axis=1)),
        "uu": np.max(np.abs(stable_uu)),
    }
    blocks = {
        "stable_output_ss_upper": _format(stable_sector["ss"]),
        "stable_output_su_upper": _format(stable_sector["su"]),
        "stable_output_uu_upper": _format(stable_sector["uu"]),
        "unstable_output_ss_upper": _format(unstable_sector["ss"]),
        "unstable_output_su_upper": _format(unstable_sector["su"]),
        "unstable_output_uu_upper": _format(unstable_sector["uu"]),
    }
    cancellation: dict[str, Any] = {}
    for sector in ("ss", "su", "uu"):
        correlated = stable_sector[sector]
        separate = raw_sector[sector] + unstable_sector[sector]
        cancellation[sector] = {
            "pre_output_deflation_sector_norm": _format(raw_sector[sector]),
            "separately_triangularized_upper": _format(separate),
            "correlated_stable_output_norm": _format(correlated),
            "separate_triangle_to_correlated_ratio": (
                None if correlated == 0 else _format(separate / correlated)
            ),
        }
    ambient = np.max(np.sum(np.abs(hessian), axis=(1, 2)))
    return {
        "projected_hessian_blocks": blocks,
        "signed_event_aligned_ambient_kret_candidate": _format(ambient),
        "output_deflation_cancellation": cancellation,
        "all_linear_combinations_formed_before_norm": True,
        "finite_section_only": True,
    }


def _composition_oracle(
    one_jacobian: np.ndarray,
    one_hessian: np.ndarray,
    two_jacobian: np.ndarray,
    two_hessian: np.ndarray,
    qhat: np.ndarray,
    fhat: np.ndarray,
) -> dict[str, Any]:
    composed_jacobian = one_jacobian @ one_jacobian
    composed_hessian = np.einsum(
        "oab,ai,bj->oij",
        one_hessian,
        one_jacobian,
        one_jacobian,
        optimize=True,
    ) + np.einsum(
        "oa,aij->oij", one_jacobian, one_hessian, optimize=True
    )
    direct_blocks = _block_diagnostics(two_hessian, qhat, fhat)
    composed_blocks = _block_diagnostics(composed_hessian, qhat, fhat)
    block_relative_defects: dict[str, str] = {}
    for name in BLOCK_NAMES:
        direct = np.longdouble(
            direct_blocks["projected_hessian_blocks"][name]
        )
        composed = np.longdouble(
            composed_blocks["projected_hessian_blocks"][name]
        )
        denominator = max(abs(direct), abs(composed), np.longdouble("1e-30"))
        block_relative_defects[name] = _format(abs(direct - composed) / denominator)
    return {
        "identity": "H2=H1[A1*.,A1*.]+A1*H1",
        "two_period_jacobian_direct_vs_composed_max_abs": _format(
            np.max(np.abs(two_jacobian - composed_jacobian))
        ),
        "two_period_hessian_direct_vs_composed_max_abs": _format(
            np.max(np.abs(two_hessian - composed_hessian))
        ),
        "two_period_hessian_direct_vs_composed_linf_bilinear": _format(
            np.max(
                np.sum(
                    np.abs(two_hessian - composed_hessian), axis=(1, 2)
                )
            )
        ),
        "projected_block_relative_defects": block_relative_defects,
        "composed_two_period_summary": composed_blocks,
        "oracle_is_directed_error_bound": False,
    }


def _mesh_row(
    orbit: _LongDoubleFourierOrbit,
    model: _Model,
    diagnostic: _FourWordDiagnostic,
    phase: complex,
    q_norm: np.longdouble,
    quadrature_samples: list[tuple[float, complex]],
    period_step_count: int,
) -> dict[str, Any]:
    one, two, common = _propagate_two_period_variations(
        orbit, model, period_step_count
    )
    one_jacobian, one_hessian, one_event = one
    two_jacobian, two_hessian, two_event = two
    step = orbit.period / np.longdouble(period_step_count)
    qhat, fhat, coordinate = _discrete_grushin_pair(
        diagnostic,
        phase,
        q_norm,
        quadrature_samples,
        step,
        int(common["history_padding_steps"]),
        boundary_mode="one_sided_four_node",
    )
    discarded_qhat, discarded_fhat, discarded_coordinate = _discrete_grushin_pair(
        diagnostic,
        phase,
        q_norm,
        quadrature_samples,
        step,
        int(common["history_padding_steps"]),
        boundary_mode="discarded_zero_nonsection_stencil",
    )
    one_blocks = _block_diagnostics(one_hessian, qhat, fhat)
    two_blocks = _block_diagnostics(two_hessian, qhat, fhat)
    discarded_two_blocks = _block_diagnostics(
        two_hessian, discarded_qhat, discarded_fhat
    )
    _, finite_qhat, finite_fhat, finite_split = _dominant_split(one_jacobian)
    finite_one_blocks = _block_diagnostics(
        one_hessian, finite_qhat, finite_fhat
    )
    finite_two_blocks = _block_diagnostics(
        two_hessian, finite_qhat, finite_fhat
    )
    if qhat @ finite_qhat < 0:
        finite_qhat = -finite_qhat
        finite_fhat = -finite_fhat
    fixed_projector = np.outer(qhat, fhat)
    finite_projector = np.outer(finite_qhat, finite_fhat)
    coordinate_comparison = {
        "fixed_qhat_vs_finite_eigen_qhat_linf": _format(
            np.max(np.abs(qhat - finite_qhat))
        ),
        "fixed_fhat_vs_finite_eigen_fhat_l1": _format(
            np.sum(np.abs(fhat - finite_fhat))
        ),
        "fixed_vs_finite_unstable_projector_linf": _format(
            np.max(np.sum(np.abs(fixed_projector - finite_projector), axis=1))
        ),
        "finite_eigensplit_replaces_stage4l_coordinate": False,
    }
    composition = _composition_oracle(
        one_jacobian,
        one_hessian,
        two_jacobian,
        two_hessian,
        qhat,
        fhat,
    )
    return {
        **common,
        "fixed_grushin_discretization": coordinate,
        "discarded_zero_nonsection_stencil_adapter_audit": {
            "coordinate": discarded_coordinate,
            "two_period_kernel_and_blocks": discarded_two_blocks,
            "used_for_primary_acceptance": False,
            "reason_discarded": (
                "a symmetric cubic stencil near theta=0 formally touches "
                "positive-time nodes that are not section-history coordinates"
            ),
        },
        "self_consistent_finite_eigensplit_oracle": {
            "one_period_eigensplit": finite_split,
            "coordinate_difference_from_fixed_stage4l_adapter": (
                coordinate_comparison
            ),
            "one_period_kernel_and_blocks": finite_one_blocks,
            "two_period_kernel_and_blocks": finite_two_blocks,
            "used_for_primary_acceptance": False,
            "eigensplit_is_continuous_history_grushin_pair": False,
        },
        "one_period_formal_diagnostic": {
            "event": one_event,
            "kernel_and_blocks": one_blocks,
            "full_history_c2_smoothing_gate": False,
            "eligible_for_full_history_c2_claim": False,
            "evidence_status": (
                "FORMAL_FINITE_SECTION_ONLY; P-tau_max<tau_max"
            ),
        },
        "two_period_primary_diagnostic": {
            "event": two_event,
            "kernel_and_blocks": two_blocks,
            "full_history_c2_smoothing_gate_at_center": True,
            "continuous_history_c2_bound": False,
            "evidence_status": (
                "FINITE_SECTION_DIAGNOSTIC; centre smoothing gate only"
            ),
        },
        "direct_two_period_vs_discrete_composition": composition,
    }


def _refinement_and_acceptance(
    rows: list[dict[str, Any]],
    stage4p_caps: Mapping[str, str],
    stage4m_caps: Mapping[str, str],
    stage4p_kret_target: str,
    stage4n_kret_target: str,
    stage4p_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    if len(rows) < 2:
        raise ValueError("Stage-4Q needs at least two meshes")
    previous = rows[-2]["two_period_primary_diagnostic"]["kernel_and_blocks"]
    final = rows[-1]["two_period_primary_diagnostic"]["kernel_and_blocks"]
    envelope_blocks: dict[str, str] = {}
    changes: dict[str, str] = {}
    strict_cap_tests: dict[str, bool] = {}
    ratios: dict[str, str] = {}
    stage4m_legacy_tests: dict[str, bool] = {}
    stage4m_legacy_ratios: dict[str, str] = {}
    for name in BLOCK_NAMES:
        old = np.longdouble(previous["projected_hessian_blocks"][name])
        new = np.longdouble(final["projected_hessian_blocks"][name])
        change = abs(new - old)
        envelope = max(old, new) + 2 * change + np.longdouble("1e-18")
        envelope_blocks[name] = _format(envelope)
        changes[name] = _format(change)
        strict_cap_tests[name] = bool(
            envelope < np.longdouble(stage4p_caps[name])
        )
        ratios[name] = _format(envelope / np.longdouble(stage4p_caps[name]))
        stage4m_legacy_tests[name] = bool(
            envelope < np.longdouble(stage4m_caps[name])
        )
        stage4m_legacy_ratios[name] = _format(
            envelope / np.longdouble(stage4m_caps[name])
        )
    old_kret = np.longdouble(previous["signed_event_aligned_ambient_kret_candidate"])
    new_kret = np.longdouble(final["signed_event_aligned_ambient_kret_candidate"])
    kret_change = abs(new_kret - old_kret)
    kret_envelope = max(old_kret, new_kret) + 2 * kret_change + np.longdouble(
        "1e-18"
    )
    kret_passes = bool(kret_envelope < np.longdouble(stage4p_kret_target))
    legacy_kret_passes = bool(
        kret_envelope < np.longdouble(stage4n_kret_target)
    )
    exceeded = [name for name in BLOCK_NAMES if not strict_cap_tests[name]]
    if not kret_passes:
        exceeded.append("signed_event_aligned_ambient_K_ret")
    first_exceeded = max(
        (
            ({"name": name, "ratio": np.longdouble(ratios[name])})
            for name in BLOCK_NAMES
            if not strict_cap_tests[name]
        ),
        key=lambda item: item["ratio"],
        default=None,
    )
    kret_ratio = kret_envelope / np.longdouble(stage4p_kret_target)
    legacy_kret_ratio = kret_envelope / np.longdouble(stage4n_kret_target)
    if not kret_passes and (
        first_exceeded is None or kret_ratio > first_exceeded["ratio"]
    ):
        first_exceeded = {
            "name": "signed_event_aligned_ambient_K_ret",
            "ratio": kret_ratio,
        }
    coordinate_trends: dict[str, Any] = {}
    for name in BLOCK_NAMES:
        fixed_series = [
            row["two_period_primary_diagnostic"]["kernel_and_blocks"][
                "projected_hessian_blocks"
            ][name]
            for row in rows
        ]
        finite_series = [
            row["self_consistent_finite_eigensplit_oracle"][
                "two_period_kernel_and_blocks"
            ]["projected_hessian_blocks"][name]
            for row in rows
        ]
        discarded_series = [
            row["discarded_zero_nonsection_stencil_adapter_audit"][
                "two_period_kernel_and_blocks"
            ]["projected_hessian_blocks"][name]
            for row in rows
        ]
        fixed_final = np.longdouble(fixed_series[-1])
        finite_final = np.longdouble(finite_series[-1])
        coordinate_trends[name] = {
            "fixed_stage4l_adapter_mesh_series": fixed_series,
            "self_consistent_finite_eigensplit_mesh_series": finite_series,
            "discarded_zero_nonsection_adapter_mesh_series": discarded_series,
            "final_fixed_minus_finite_absolute": _format(
                abs(fixed_final - finite_final)
            ),
            "finite_eigensplit_used_for_acceptance": False,
        }
    return {
        "construction": (
            "max(last two meshes)+2*absolute last-mesh change+1e-18; "
            "heuristic only, not directed error"
        ),
        "cap_source": STAGE4P_RESULT_RELATIVE_PATH,
        "stage4p_two_return_design": dict(stage4p_metadata),
        "stage4p_recommended_wide_simultaneous_box": dict(stage4p_caps),
        "stage4m_legacy_strict_caps": dict(stage4m_caps),
        "last_mesh_absolute_block_changes": changes,
        "two_period_projected_block_heuristic_envelope": envelope_blocks,
        "envelope_to_cap_ratios": ratios,
        "strict_six_block_diagnostic_tests": strict_cap_tests,
        "all_six_block_diagnostic_tests_pass": all(strict_cap_tests.values()),
        "stage4m_legacy_six_block_diagnostic_tests": stage4m_legacy_tests,
        "stage4m_legacy_envelope_to_cap_ratios": stage4m_legacy_ratios,
        "stage4m_legacy_all_six_tests_pass": all(
            stage4m_legacy_tests.values()
        ),
        "kret_target_from_stage4p_two_return_conditional_lower": (
            stage4p_kret_target
        ),
        "legacy_one_return_kret_target_from_stage4n": stage4n_kret_target,
        "last_mesh_absolute_kret_change": _format(kret_change),
        "two_period_ambient_kret_heuristic_envelope": _format(kret_envelope),
        "kret_envelope_to_target_ratio": _format(kret_ratio),
        "kret_diagnostic_test_passes": kret_passes,
        "legacy_stage4n_kret_envelope_to_target_ratio": _format(
            legacy_kret_ratio
        ),
        "legacy_stage4n_kret_diagnostic_test_passes": legacy_kret_passes,
        "ambient_kret_is_required_for_stage4p_graph_arithmetic": False,
        "exceeded_diagnostic_targets": exceeded,
        "largest_exceeded_target": (
            None
            if first_exceeded is None
            else {
                "name": first_exceeded["name"],
                "ratio": _format(first_exceeded["ratio"]),
            }
        ),
        "coordinate_oracle_mesh_trends": coordinate_trends,
        "any_diagnostic_test_is_a_theorem": False,
    }


def _numeric_core(pilot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "selected_branch_and_smoothing": pilot["selected_branch_and_smoothing"],
        "fixed_grushin_coordinate": pilot["fixed_grushin_coordinate"],
        "mesh_rows": pilot["mesh_rows"],
        "refinement_and_acceptance": pilot["refinement_and_acceptance"],
    }


def build_stage4q_pilot(repository: Path) -> Stage4QPilot:
    _require_runtime()
    repository = repository.resolve()
    parents = _load_and_validate_parents(repository)
    orbit_payload = parents[INNER_ORBIT_RESULT_RELATIVE_PATH]
    orbit_candidate = validate_leaky_periodic_branch_artifact(
        orbit_payload, repository
    )
    orbit = _LongDoubleFourierOrbit(
        np.asarray(orbit_candidate.state, dtype=np.longdouble),
        orbit_candidate.period,
    )
    model = _model_from_payload(orbit_payload)
    diagnostic = _FourWordDiagnostic(repository)
    phase, q_norm, quadrature_samples, grushin_metadata = _physical_grushin_data(
        diagnostic
    )
    rows = [
        _mesh_row(
            orbit,
            model,
            diagnostic,
            phase,
            q_norm,
            quadrature_samples,
            step_count,
        )
        for step_count in DEFAULT_PERIOD_STEP_COUNTS
    ]
    stage4m_caps = _stage4m_caps(parents[STAGE4M_RESULT_RELATIVE_PATH])
    stage4n_kret_target = _stage4n_kret_target(
        parents[STAGE4N_RESULT_RELATIVE_PATH]
    )
    stage4p_caps, stage4p_kret_target, stage4p_metadata = (
        _stage4p_two_return_design(parents[STAGE4P_RESULT_RELATIVE_PATH])
    )
    refinement = _refinement_and_acceptance(
        rows,
        stage4p_caps,
        stage4m_caps,
        stage4p_kret_target,
        stage4n_kret_target,
        stage4p_metadata,
    )

    period = np.longdouble(orbit.period)
    tau_max = np.longdouble(model.tau_1)
    one_margin = period - 2 * tau_max
    two_margin = 2 * period - 2 * tau_max
    if not one_margin < 0 or not two_margin > 0:
        raise ArithmeticError("the one-versus-two-period smoothing gate changed")
    claims = {name: False for name in THEOREM_FLAGS}
    return Stage4QPilot(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        selected_branch_and_smoothing={
            "tau_max": _format(tau_max),
            "centre_period": _format(period),
            "one_period_target": _format(period),
            "two_period_target": _format(2 * period),
            "full_history_c2_smoothing_condition": "T-tau_max>tau_max",
            "one_period_smoothing_margin_P_minus_2tau_max": _format(one_margin),
            "one_period_gate_passes": False,
            "one_period_usage": "formal finite-section diagnostic only",
            "two_period_smoothing_margin_2P_minus_2tau_max": _format(two_margin),
            "two_period_center_gate_passes": True,
            "primary_selected_branch": "near-two-period positive-oriented event",
            "primary_branch_is_proved_selected_second_hit": False,
            "smoothing_gate_is_operator_error_bound": False,
        },
        fixed_grushin_coordinate={
            **grushin_metadata,
            "source": (
                "same Stage-4L/Stage-4D q,f on the phase-zero Route-C section"
            ),
            "physical_pair": "q_phys=q/phase, f_phys=phase*f with f_phys(q_phys)=1",
            "unit_pair": "qhat=q_phys/||q_phys||_Y, fhat=||q_phys||_Y*f_phys",
            "fixed_projection": "Ps=I-qhat*fhat=I-q*f",
            "same_pair_used_for_every_mesh_and_both_return_horizons": True,
            "q_norm_candidate_is_not_certified": True,
        },
        signed_formation_order={
            "order": list(FORMATION_ORDER),
            "moving_event_history_formula": (
                "V(T+theta)+dotU(T+theta)T_h+dotU(T+theta)T_k+"
                "ddotX(T+theta)T_hT_k+dotX(T+theta)T_hk"
            ),
            "input_stable_deflation": "H[Ps*.,Ps*.]",
            "unstable_action": "fhat applied to the already correlated sector",
            "stable_output": "sector-qhat*fhat(sector)",
            "norm_before_all_signed_combinations": False,
            "finite_section_norm_only": True,
        },
        mesh_rows=tuple(rows),
        refinement_and_acceptance=refinement,
        diagnostic_checks={
            "parent_bytes_validated": True,
            "stage4p_two_return_wide_box_bound_and_used": True,
            "physical_grushin_phase_fixed": True,
            "finite_section_pairing_identity_enforced": True,
            "one_period_smoothing_gate_fails": True,
            "two_period_center_smoothing_gate_passes": True,
            "direct_two_period_event_tensor_computed": True,
            "two_period_composition_oracle_computed": True,
            "six_projected_blocks_computed_after_correlated_deflation": True,
            "one_sided_endpoint_adapter_used_for_primary_blocks": True,
            "discarded_endpoint_adapter_retained_only_as_audit": True,
            "self_consistent_finite_eigensplit_retained_only_as_oracle": True,
            "heuristic_refinement_envelope_computed": True,
        },
        theorem_boundary={
            "result_status": STATUS,
            "one_period_row": (
                "not a C2 map on the full history space because P-tau_max<tau_max"
            ),
            "two_period_row": (
                "centre smoothing gate passes, but the finite-section tensor has "
                "no outward integration, interpolation, orbit, q/f, or history "
                "truncation error bound"
            ),
            "event_boundary": (
                "no common event window, uniform speed lower bound, or no-earlier-"
                "hit proof is supplied"
            ),
            "domain_boundary": (
                "centre orbit only; no supremum over the Stage-4M anisotropic ball"
            ),
            "biological_boundary": (
                "no pulse capture, routing, onset, or network conclusion follows"
            ),
        },
        claim_status=claims,
    )


def build_stage4q_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    pilot = asdict(build_stage4q_pilot(repository))
    return {
        "pilot": pilot,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "proof_status": STATUS,
            "pilot_sha256": canonical_sha256(pilot),
            "numeric_core_sha256": canonical_sha256(_numeric_core(pilot)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "longdouble_bits": int(np.finfo(np.longdouble).bits),
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
                "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
            },
        },
    }


def validate_stage4q_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = False
) -> None:
    _require_runtime()
    repository = repository.resolve()
    if not isinstance(payload, Mapping) or set(payload) != {"pilot", "manifest"}:
        raise ValueError("the Stage-4Q outer schema changed")
    pilot = _mapping(payload.get("pilot"), "Stage-4Q pilot")
    manifest = _mapping(payload.get("manifest"), "Stage-4Q manifest")
    if set(pilot) != {field.name for field in fields(Stage4QPilot)}:
        raise ValueError("the Stage-4Q pilot schema changed")
    if (
        pilot.get("schema_id") != SCHEMA_ID
        or pilot.get("model_id") != MODEL_ID
        or pilot.get("branch") != BRANCH
        or pilot.get("status") != STATUS
        or pilot.get("parent_result_sha256") != PARENT_RESULT_SHA256
    ):
        raise ValueError("the Stage-4Q identity changed")

    claims = _mapping(pilot.get("claim_status"), "Stage-4Q claim ledger")
    if set(claims) != set(THEOREM_FLAGS):
        raise ValueError("the Stage-4Q theorem flag set changed")
    if any(claims.get(name) is not False for name in THEOREM_FLAGS):
        raise ValueError("a Stage-4Q diagnostic was promoted to theorem")

    smoothing = _mapping(
        pilot.get("selected_branch_and_smoothing"), "Stage-4Q smoothing ledger"
    )
    if (
        Decimal(str(smoothing["one_period_smoothing_margin_P_minus_2tau_max"]))
        >= 0
        or smoothing.get("one_period_gate_passes") is not False
        or Decimal(
            str(smoothing["two_period_smoothing_margin_2P_minus_2tau_max"])
        )
        <= 0
        or smoothing.get("two_period_center_gate_passes") is not True
        or smoothing.get("primary_branch_is_proved_selected_second_hit") is not False
        or smoothing.get("smoothing_gate_is_operator_error_bound") is not False
    ):
        raise ValueError("the Stage-4Q smoothing boundary changed")

    order = _mapping(
        pilot.get("signed_formation_order"), "Stage-4Q formation order"
    )
    if (
        order.get("order") != list(FORMATION_ORDER)
        or order.get("norm_before_all_signed_combinations") is not False
        or order.get("finite_section_norm_only") is not True
    ):
        raise ValueError("the Stage-4Q signed formation order changed")

    rows = pilot.get("mesh_rows")
    if not isinstance(rows, (list, tuple)) or [
        row.get("period_step_count") for row in rows
    ] != list(DEFAULT_PERIOD_STEP_COUNTS):
        raise ValueError("the Stage-4Q mesh ladder changed")
    for row in rows:
        coordinate = _mapping(
            row.get("fixed_grushin_discretization"), "Stage-4Q discrete pair"
        )
        if (
            coordinate.get("pairing_identity_enforced_in_finite_section")
            is not True
            or abs(Decimal(str(coordinate["pairing_after_discrete_correction"])) - 1)
            > Decimal("1e-15")
            or coordinate.get("finite_section_adapter_validated") is not False
            or coordinate.get("boundary_interpolation")
            != "one_sided_four_node"
            or coordinate.get("positive_time_nodes_used") is not False
        ):
            raise ValueError("the Stage-4Q finite-section Grushin pair changed")
        discarded = _mapping(
            row.get("discarded_zero_nonsection_stencil_adapter_audit"),
            "Stage-4Q discarded adapter",
        )
        if (
            discarded.get("used_for_primary_acceptance") is not False
            or _mapping(discarded.get("coordinate"), "discarded coordinate").get(
                "boundary_interpolation"
            )
            != "discarded_zero_nonsection_stencil"
        ):
            raise ValueError("the discarded Stage-4Q adapter was promoted")
        finite_oracle = _mapping(
            row.get("self_consistent_finite_eigensplit_oracle"),
            "Stage-4Q finite eigensplit oracle",
        )
        coordinate_difference = _mapping(
            finite_oracle.get("coordinate_difference_from_fixed_stage4l_adapter"),
            "Stage-4Q coordinate comparison",
        )
        if (
            finite_oracle.get("used_for_primary_acceptance") is not False
            or finite_oracle.get("eigensplit_is_continuous_history_grushin_pair")
            is not False
            or coordinate_difference.get(
                "finite_eigensplit_replaces_stage4l_coordinate"
            )
            is not False
        ):
            raise ValueError("the finite Stage-4Q eigensplit was promoted")
        one = _mapping(
            row.get("one_period_formal_diagnostic"), "Stage-4Q one-period row"
        )
        two = _mapping(
            row.get("two_period_primary_diagnostic"), "Stage-4Q two-period row"
        )
        if (
            one.get("full_history_c2_smoothing_gate") is not False
            or one.get("eligible_for_full_history_c2_claim") is not False
            or two.get("full_history_c2_smoothing_gate_at_center") is not True
            or two.get("continuous_history_c2_bound") is not False
        ):
            raise ValueError("a Stage-4Q horizon was misclassified")
        for branch in (one, two):
            blocks = _mapping(
                _mapping(branch.get("kernel_and_blocks"), "kernel row").get(
                    "projected_hessian_blocks"
                ),
                "six projected blocks",
            )
            if set(blocks) != set(BLOCK_NAMES) or any(
                Decimal(str(blocks[name])) < 0 for name in BLOCK_NAMES
            ):
                raise ValueError("a Stage-4Q projected block changed")
            if branch["kernel_and_blocks"].get("finite_section_only") is not True:
                raise ValueError("a Stage-4Q finite tensor was promoted")
        composition = _mapping(
            row.get("direct_two_period_vs_discrete_composition"),
            "Stage-4Q composition oracle",
        )
        if (
            composition.get("identity") != "H2=H1[A1*.,A1*.]+A1*H1"
            or composition.get("oracle_is_directed_error_bound") is not False
        ):
            raise ValueError("the Stage-4Q composition oracle changed")

    refinement = _mapping(
        pilot.get("refinement_and_acceptance"), "Stage-4Q refinement"
    )
    if (
        refinement.get("cap_source") != STAGE4P_RESULT_RELATIVE_PATH
        or set(
            _mapping(
                refinement.get("stage4p_recommended_wide_simultaneous_box"),
                "Stage-4Q Stage-4P cap row",
            )
        )
        != set(BLOCK_NAMES)
        or set(
            _mapping(
                refinement.get("stage4m_legacy_strict_caps"),
                "Stage-4Q legacy Stage-4M cap row",
            )
        )
        != set(BLOCK_NAMES)
        or refinement.get("any_diagnostic_test_is_a_theorem") is not False
        or set(
            _mapping(
                refinement.get("coordinate_oracle_mesh_trends"),
                "Stage-4Q coordinate trends",
            )
        )
        != set(BLOCK_NAMES)
    ):
        raise ValueError("the Stage-4Q cap boundary changed")
    stage4p_design = _mapping(
        refinement.get("stage4p_two_return_design"),
        "Stage-4Q Stage-4P design metadata",
    )
    if (
        stage4p_design.get("result_sha256") != STAGE4P_RESULT_SHA256
        or stage4p_design.get(
            "simultaneous_box_graph_arithmetic_closes_conditionally"
        )
        is not True
        or stage4p_design.get("box_is_a_directed_hessian_bound") is not False
        or stage4p_design.get("box_entered_into_strict_numeric_ingress")
        is not False
        or stage4p_design.get(
            "kret_is_required_by_matrix_lyapunov_perron_arithmetic"
        )
        is not False
        or refinement.get("ambient_kret_is_required_for_stage4p_graph_arithmetic")
        is not False
    ):
        raise ValueError("the Stage-4Q Stage-4P boundary changed")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "proof_status",
        "pilot_sha256",
        "numeric_core_sha256",
        "source_sha256",
        "dependency_source_sha256",
        "parent_result_sha256",
        "runtime",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-4Q manifest schema changed")
    fixed_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "proof_status": STATUS,
        "pilot_sha256": canonical_sha256(pilot),
        "numeric_core_sha256": canonical_sha256(_numeric_core(pilot)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
    }
    if any(manifest.get(name) != value for name, value in fixed_manifest.items()):
        raise ValueError("the Stage-4Q fixed manifest data changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-4Q sources")
    dependencies = _mapping(
        manifest.get("dependency_source_sha256"), "Stage-4Q dependencies"
    )
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4Q source set changed")
    if set(dependencies) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4Q dependency set changed")
    for relative, digest in {**sources, **dependencies}.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4Q source changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4Q parent changed: {relative}")
    runtime = _mapping(manifest.get("runtime"), "Stage-4Q runtime")
    if (
        runtime.get("openblas_num_threads") != PINNED_OPENBLAS_NUM_THREADS
        or runtime.get("omp_num_threads") != PINNED_OMP_NUM_THREADS
    ):
        raise ValueError("the Stage-4Q runtime changed")
    if recompute:
        expected = build_stage4q_result(repository)
        if canonical_sha256(expected["pilot"]) != canonical_sha256(pilot):
            raise ValueError("the Stage-4Q fresh replay changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BLOCK_NAMES",
    "DEFAULT_COMMAND",
    "DEFAULT_PERIOD_STEP_COUNTS",
    "DEPENDENCY_SOURCE_MANIFEST",
    "FORMATION_ORDER",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATUS",
    "Stage4QPilot",
    "TEST_RELATIVE_PATH",
    "THEOREM_FLAGS",
    "_numeric_core",
    "build_stage4q_pilot",
    "build_stage4q_result",
    "canonical_sha256",
    "validate_stage4q_result",
]
