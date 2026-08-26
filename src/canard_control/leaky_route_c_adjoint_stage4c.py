"""Stage-4C left-adjoint and correlated-deflation certificate.

The inner unstable Floquet multiplier is algebraically simple.  This gives a
nonzero monodromy adjoint functional and, because the multiplier is not one,
that functional annihilates the neutral flow tangent.  Hence restricting the
unstable eigenhistory and the adjoint to the affine Route-C section does not
change their pairing.

This module also encloses the bottom row of the full Fourier Grushin inverse
near the refined unstable root.  That row is a rigorous cokernel functional
for the periodic characteristic pencil in the declared Wiener primal/dual
pairing.  A separate three-mesh long-double pilot supplies an executable
finite-section history action and correlated deflation.

The missing bridge is stated explicitly: the Fourier cokernel row has not yet
been converted, with a directed normalization and a summable tail, into the
atom-plus-density adjoint measure on the continuous Route-C history space.
Consequently the pilot action on ``Y_qq`` and the target ``C_s^{uu}<12`` are
not theorem statements.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np

from canard_control.directed_interval import decimal_lower, decimal_upper
from canard_control.leaky_floquet_inner_unstable_root import (
    PRECISION_BITS,
    RESULT_RELATIVE_PATH as ROOT_RESULT_RELATIVE_PATH,
    _augment_finite,
    _complex_abs_lower,
    _dependency_fingerprint,
    _evaluate_prepared,
    _grushin_block_bounds,
    _prepare_cached,
    _up,
)
from canard_control.leaky_inner_stable_manifold_stage2_contract import (
    RESULT_RELATIVE_PATH as STAGE2_RESULT_RELATIVE_PATH,
    validate_stage2_stable_manifold_result,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_periodic_branch_artifact import (
    validate_leaky_periodic_branch_artifact,
)
from canard_control.leaky_projected_return_hessian_stage4a_pilot import (
    INNER_ORBIT_RESULT_RELATIVE_PATH,
    RESULT_RELATIVE_PATH as STAGE4A_RESULT_RELATIVE_PATH,
    _LongDoubleFourierOrbit,
    _dominant_split,
    _finite_section_variations,
    _format,
    _model_from_payload,
    validate_stage4a_pilot_result,
)
from canard_control.leaky_stable_output_uu_stage4b_contract import (
    RESULT_RELATIVE_PATH as STAGE4B_RESULT_RELATIVE_PATH,
    validate_stage4b_contract_result,
)


SCHEMA_ID = "leaky-route-c-adjoint-stage4c-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_route_c_adjoint_stage4c.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_route_c_adjoint_stage4c.py"
RESULT_RELATIVE_PATH = "experiments/results/leaky_route_c_adjoint_stage4c.json"
NOTE_RELATIVE_PATH = "docs/leaky-route-c-adjoint-stage4c.md"
TEST_RELATIVE_PATH = "tests/test_leaky_route_c_adjoint_stage4c.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_route_c_adjoint_stage4c.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source binding; 160-bit outward MPFR enclosure "
    "of the full cutoff-64 plus infinite-tail Grushin bottom row on the "
    "refined real-root neighborhood; analytic compact-Fredholm pairing and "
    "RFDE bilinear-form identities; plus a source-bound three-mesh "
    "numpy.longdouble finite-section adjoint pilot in a fresh one-thread "
    "OpenBLAS subprocess; no directed history-measure normalization, "
    "continuous-history action on Y_qq, return tube, Hessian block, graph, "
    "separator, or onset theorem"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

ROOT_RESULT_SHA256 = (
    "ab2876efc8a26df544f56257ab00b9fde0fea4ba043f4500f1450e0d0885fa2c"
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
STAGE4B_RESULT_SHA256 = (
    "a310e4c1dba96961cc6fe7f70e4ee978f3b25a46956f9bcdde9f31286b40f7f7"
)
INNER_ORBIT_RESULT_SHA256 = (
    "bee1da065d213c3c33d724ced1dba37c5914934515c1128588919bed34abe69b"
)

PINNED_GRUSHIN_OPENBLAS_THREADS = "8"
PINNED_PILOT_OPENBLAS_THREADS = "1"
ROOT_REPLAY_CENTER = 0.69836042
ROOT_REPLAY_NEIGHBORHOOD = "1.1e-8"
PILOT_STEP_COUNTS = (120, 180, 240)

TRUE_FLAGS = (
    "unstable_multiplier_algebraically_simple_validated",
    "nonzero_adjoint_pairing_f_of_q_validated",
    "rfde_adjoint_atom_density_identity_proved",
    "nonneutral_adjoint_annihilates_flow_tangent_proved",
    "route_c_section_restriction_preserves_adjoint_pairing_proved",
    "full_infinite_fourier_grushin_cokernel_row_enclosed",
    "fourier_cokernel_row_nonzero_validated",
    "finite_section_history_action_pilot_computed",
    "discrete_correlated_deflation_operator_executable",
)
FALSE_FLAGS = (
    "fourier_cokernel_identified_with_history_adjoint_measure",
    "adjoint_history_measure_numeric_enclosed",
    "directed_normalization_f_of_q_equals_one_available",
    "directed_adjoint_action_on_y_qq_available",
    "stable_output_uu_below_twelve_validated",
    "stage4b_stable_deflation_ingress_closed",
    "inner_local_stable_graph_quantitatively_validated",
    "graph_radius_1p7e_minus_3_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage4CArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    simple_multiplier_and_pairing_theorem: dict[str, Any]
    rfde_adjoint_history_measure_identity: dict[str, Any]
    directed_fourier_grushin_left_row: dict[str, Any]
    finite_section_history_action_pilot: dict[str, Any]
    correlated_deflation_interface: dict[str, Any]
    stage4b_ingress_update: dict[str, Any]
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


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} is missing")
    return value


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


def apply_discrete_normalized_deflation(
    history: Sequence[Any],
    right_eigenvector: Sequence[Any],
    left_covector: Sequence[Any],
) -> tuple[np.ndarray, np.longdouble]:
    """Apply the finite-section pilot deflation as one correlated expression.

    This routine is deliberately numerical, not interval-valued.  A strict
    implementation must use a shared outward interval/Taylor representation
    for ``history``, the scalar action, and the subtraction.
    """

    value = np.asarray(history, dtype=np.longdouble)
    right = np.asarray(right_eigenvector, dtype=np.longdouble)
    left = np.asarray(left_covector, dtype=np.longdouble)
    if value.ndim != 1 or right.shape != value.shape or left.shape != value.shape:
        raise ValueError("the discrete deflation vectors must have one shape")
    denominator = left @ right
    if abs(denominator) <= np.longdouble("1e-18"):
        raise ArithmeticError("the discrete adjoint pairing vanished")
    coefficient = (left @ value) / denominator
    return value - right * coefficient, coefficient


def _directed_grushin_left_row(repository: Path) -> dict[str, Any]:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_GRUSHIN_OPENBLAS_THREADS:
        raise RuntimeError(
            "the Stage-4C Grushin replay requires OPENBLAS_NUM_THREADS="
            + PINNED_GRUSHIN_OPENBLAS_THREADS
        )
    prepared, _ = _prepare_cached(
        str(repository), _dependency_fingerprint(repository)
    )
    spectral_center = complex(ROOT_REPLAY_CENTER, 0.0)
    (
        finite,
        first,
        second,
        finite_tail,
        finite_tail_first,
        tail_finite,
        errors,
    ) = _evaluate_prepared(prepared, spectral_center)
    del first, second
    grushin = _augment_finite(
        finite, prepared.right_border, prepared.left_border
    )
    inverse = np.linalg.inv(grushin)
    block = _grushin_block_bounds(
        prepared,
        s=spectral_center,
        neighborhood=_up(ROOT_REPLAY_NEIGHBORHOOD),
        inverse=inverse,
        finite=finite,
        finite_tail=finite_tail,
        finite_tail_first=finite_tail_first,
        tail_finite=tail_finite,
        errors=errors,
        include_disk_s_variation=True,
    )
    contraction = block["contraction"]
    if not 0 < contraction < 1:
        raise ArithmeticError("the Stage-4C full Grushin row did not contract")
    preconditioner_norm = max(
        block["inverse_norm"],
        block["fast_tail_inverse"],
        block["slow_tail_inverse"],
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        exact_row_distance = (
            block["bottom_row"]
            * preconditioner_norm
            / (1 - contraction)
        )
    finite_row = np.asarray(inverse[-1, :-1], dtype=complex)
    largest_index = int(np.argmax(np.abs(finite_row)))
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        largest_exact_component = (
            _complex_abs_lower(finite_row[largest_index], PRECISION_BITS)
            - exact_row_distance
        )
    if largest_exact_component <= 0:
        raise ArithmeticError("the enclosed Fourier cokernel row could vanish")
    mode_count = 2 * 64 + 1
    component = "voltage" if largest_index < mode_count else "recovery"
    mode_index = largest_index if largest_index < mode_count else (
        largest_index - mode_count
    )
    mode = mode_index - 64
    coefficients = [
        {
            "real_binary64": format(value.real, ".17g"),
            "imag_binary64": format(value.imag, ".17g"),
        }
        for value in finite_row
    ]
    return {
        "spectral_center_binary64": format(ROOT_REPLAY_CENTER, ".17g"),
        "spectral_neighborhood_radius": ROOT_REPLAY_NEIGHBORHOOD,
        "root_bracket_contained_in_neighborhood": True,
        "norm_pairing": (
            "complex Wiener l1 primal against coefficientwise l-infinity dual"
        ),
        "finite_state_dimension": len(finite_row),
        "finite_ordering": (
            "voltage Fourier modes -64,...,64, then recovery modes -64,...,64"
        ),
        "finite_bordered_inverse_norm_upper": decimal_upper(
            block["inverse_norm"]
        ),
        "fast_tail_preconditioner_norm_upper": decimal_upper(
            block["fast_tail_inverse"]
        ),
        "slow_tail_preconditioner_norm_upper": decimal_upper(
            block["slow_tail_inverse"]
        ),
        "full_grushin_contraction_upper": decimal_upper(contraction),
        "bottom_row_residual_dual_upper": decimal_upper(block["bottom_row"]),
        "exact_bottom_row_distance_dual_upper": decimal_upper(
            exact_row_distance
        ),
        "approximate_finite_row_dual_upper": decimal_upper(block["row_norm"]),
        "largest_component": {
            "flat_index": largest_index,
            "state_component": component,
            "fourier_mode": mode,
            "approximate_real_binary64": format(
                finite_row[largest_index].real, ".17g"
            ),
            "approximate_imag_binary64": format(
                finite_row[largest_index].imag, ".17g"
            ),
            "exact_modulus_lower": decimal_lower(largest_exact_component),
        },
        "finite_row_coefficients": coefficients,
        "finite_row_complex128_bytes_sha256": sha256(
            np.asarray(finite_row, dtype=np.complex128).tobytes()
        ).hexdigest(),
        "full_infinite_fourier_cokernel_row_enclosed": True,
        "fourier_cokernel_row_nonzero": True,
        "history_adjoint_measure_identification_validated": False,
        "missing_identification": (
            "prove the Fourier reversal/conjugation convention, obtain a "
            "summable directed adjoint tail, and match the Grushin border "
            "scale to the RFDE bilinear history functional"
        ),
    }


def _build_discrete_history_action_pilot(repository: Path) -> dict[str, Any]:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_PILOT_OPENBLAS_THREADS:
        raise RuntimeError(
            "the Stage-4C finite-section pilot requires OPENBLAS_NUM_THREADS="
            + PINNED_PILOT_OPENBLAS_THREADS
        )
    orbit_payload = _load_parent(
        repository,
        INNER_ORBIT_RESULT_RELATIVE_PATH,
        INNER_ORBIT_RESULT_SHA256,
        "inner orbit",
    )
    orbit_candidate = validate_leaky_periodic_branch_artifact(
        orbit_payload, repository
    )
    orbit = _LongDoubleFourierOrbit(
        np.asarray(orbit_candidate.state, dtype=np.longdouble),
        orbit_candidate.period,
    )
    model = _model_from_payload(orbit_payload)
    rows: list[dict[str, Any]] = []
    finest_vectors: dict[str, Any] | None = None
    for step_count in PILOT_STEP_COUNTS:
        jacobian, hessian, diagnostics = _finite_section_variations(
            orbit, model, step_count
        )
        del hessian
        multiplier, right, left, split = _dominant_split(jacobian)
        step = np.longdouble(diagnostics["step_size"])
        history_steps = int(diagnostics["history_padding_steps"])
        theta = np.arange(-history_steps, 0, dtype=np.longdouble) * step
        pairing = left @ right
        deflated_q, q_coordinate = apply_discrete_normalized_deflation(
            right, right, left
        )
        moments = {
            str(order): _format(np.sum(left[:-1] * theta**order))
            for order in range(4)
        }
        row = {
            "step_count": step_count,
            "step_size": diagnostics["step_size"],
            "history_padding_steps": history_steps,
            "section_dimension": len(left),
            "unstable_multiplier": _format(multiplier),
            "normalized_pairing_left_right": _format(pairing),
            "left_eigen_residual_inf": split["unstable_left_residual_inf"],
            "right_eigen_residual_inf": split["unstable_right_residual_inf"],
            "recovery_atom_weight": _format(left[-1]),
            "history_voltage_weight_sum": _format(np.sum(left[:-1])),
            "history_voltage_total_variation_discrete": _format(
                np.sum(np.abs(left[:-1]))
            ),
            "full_covector_l1_norm": _format(np.sum(np.abs(left))),
            "history_weight_moments": moments,
            "deflation_of_q_coordinate": _format(q_coordinate),
            "deflation_of_q_residual_inf": _format(
                np.max(np.abs(deflated_q))
            ),
            "evidence_status": (
                "long-double nodal pilot; not an interval or continuous-history "
                "adjoint measure"
            ),
        }
        rows.append(row)
        if step_count == PILOT_STEP_COUNTS[-1]:
            finest_vectors = {
                "step_count": step_count,
                "theta_voltage_nodes": [_format(value) for value in theta],
                "left_voltage_history_weights": [
                    _format(value) for value in left[:-1]
                ],
                "left_current_recovery_atom": _format(left[-1]),
                "right_voltage_history_values": [
                    _format(value) for value in right[:-1]
                ],
                "right_current_recovery_value": _format(right[-1]),
                "input_coordinate_ordering": (
                    "voltage values at theta nodes followed by current recovery; "
                    "current voltage is fixed by the Route-C section"
                ),
                "action_formula": (
                    "f_N(y)=sum_i left_weight_i*y_v(theta_i)+"
                    "left_recovery_atom*y_w(0)"
                ),
                "normalization": "f_N(q_N)=1 in long-double arithmetic",
            }
    if finest_vectors is None:
        raise AssertionError("the Stage-4C pilot produced no finest mesh")
    previous, final = rows[-2], rows[-1]
    weak_changes = {
        f"moment_{order}": _format(
            abs(
                np.longdouble(final["history_weight_moments"][str(order)])
                - np.longdouble(previous["history_weight_moments"][str(order)])
            )
        )
        for order in range(4)
    }
    weak_changes["recovery_atom"] = _format(
        abs(
            np.longdouble(final["recovery_atom_weight"])
            - np.longdouble(previous["recovery_atom_weight"])
        )
    )
    return {
        "mesh_rows": rows,
        "finest_discrete_action_operator": finest_vectors,
        "last_two_mesh_weak_action_changes": weak_changes,
        "mesh_changes_are_interval_errors": False,
        "pilot_promoted_to_history_measure": False,
    }


def _pilot_subprocess(repository: Path) -> dict[str, Any]:
    environment = dict(os.environ)
    environment["OPENBLAS_NUM_THREADS"] = PINNED_PILOT_OPENBLAS_THREADS
    environment["OMP_NUM_THREADS"] = "1"
    source = str(repository / "src")
    inherited = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = source if not inherited else source + os.pathsep + inherited
    program = (
        "import json,sys; from pathlib import Path; "
        "from canard_control.leaky_route_c_adjoint_stage4c import "
        "_build_discrete_history_action_pilot; "
        "print(json.dumps(_build_discrete_history_action_pilot("
        "Path(sys.argv[1])),sort_keys=True,separators=(',',':'),allow_nan=False))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", program, str(repository)],
        cwd=repository,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "the Stage-4C one-thread pilot subprocess failed: "
            + completed.stderr.strip()
        )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("the Stage-4C pilot subprocess returned no mapping")
    return value


def build_stage4c_artifact(repository: Path) -> Stage4CArtifact:
    repository = repository.resolve()
    root = _load_parent(
        repository, ROOT_RESULT_RELATIVE_PATH, ROOT_RESULT_SHA256, "inner root"
    )
    stage2 = _load_parent(
        repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256, "Stage-2"
    )
    stage3 = _load_parent(
        repository, STAGE3_RESULT_RELATIVE_PATH, STAGE3_RESULT_SHA256, "Stage-3"
    )
    stage4a = _load_parent(
        repository, STAGE4A_RESULT_RELATIVE_PATH, STAGE4A_RESULT_SHA256, "Stage-4A"
    )
    stage4b = _load_parent(
        repository, STAGE4B_RESULT_RELATIVE_PATH, STAGE4B_RESULT_SHA256, "Stage-4B"
    )
    validate_stage2_stable_manifold_result(stage2, repository)
    validate_stage3_stable_projection_result(stage3, repository)
    validate_stage4a_pilot_result(stage4a, repository)
    validate_stage4b_contract_result(stage4b, repository)

    root_certificate = _mapping(root.get("certificate"), "root certificate")
    stage2_contract = _mapping(stage2.get("contract"), "Stage-2 contract")
    stage2_spectral = _mapping(
        stage2_contract.get("strengthened_gamma01_spectral_ingress"),
        "Stage-2 spectral ingress",
    )
    stage3_certificate = _mapping(
        stage3.get("certificate"), "Stage-3 certificate"
    )
    root_bracket = _mapping(
        stage3_certificate.get("root_bracket"), "Stage-3 root bracket"
    )
    if root_certificate.get("root_analytic_algebraic_multiplicity_one") is not True:
        raise ValueError("the unstable characteristic root lost simplicity")
    if stage2_spectral.get("unstable_restriction_dimension") != 1:
        raise ValueError("the unstable monodromy restriction is no longer one-dimensional")
    if root_bracket.get("parent_disk_contains_exactly_one_real_simple_root") is not True:
        raise ValueError("the refined root bracket lost its simple root")

    grushin = _directed_grushin_left_row(repository)
    pilot = _pilot_subprocess(repository)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4CArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            ROOT_RESULT_RELATIVE_PATH: ROOT_RESULT_SHA256,
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
            STAGE4B_RESULT_RELATIVE_PATH: STAGE4B_RESULT_SHA256,
        },
        simple_multiplier_and_pairing_theorem={
            "unstable_restriction_dimension": 1,
            "characteristic_root_algebraic_multiplicity": 1,
            "refined_root_real_lower": root_bracket["root_real_lower"],
            "refined_root_real_upper": root_bracket["root_real_upper"],
            "multiplier_is_nonneutral": True,
            "fredholm_range_identity": (
                "Range(M-lambda I)=ker(f) for the codimension-one range of "
                "the algebraically simple compact monodromy eigenvalue"
            ),
            "nonzero_pairing_proof": (
                "if f(q)=0 then q lies in Range(M-lambda I), so "
                "q=(M-lambda I)y and y is a generalized eigenvector, "
                "contradicting algebraic simplicity"
            ),
            "f_of_q_nonzero_validated": True,
            "qualitative_rescaling_f_of_q_equals_one_allowed": True,
            "directed_numeric_rescaling_available": False,
            "root_effective_hamiltonian_slope_modulus_lower": (
                root_certificate["reference_effective_slope_modulus_lower"]
            ),
            "slope_is_not_identified_with_f_of_q": True,
        },
        rfde_adjoint_history_measure_identity={
            "forward_equation": (
                "x'(t)=A_0(t)x(t)+sum_j A_j(t)x(t-tau_j)"
            ),
            "advanced_adjoint_equation": (
                "-z'(t)=A_0(t)^T z(t)+sum_j A_j(t+tau_j)^T z(t+tau_j)"
            ),
            "adjoint_floquet_condition": "z(t+T)=lambda^(-1)z(t)",
            "history_functional": (
                "f_t(phi)=z(t)^T phi(0)+sum_j integral_{-tau_j}^0 "
                "z(t+theta+tau_j)^T A_j(t+theta+tau_j) phi(theta) dtheta"
            ),
            "model_atoms": (
                "current-voltage atom z_v(t) and current-recovery atom z_w(t)"
            ),
            "model_voltage_density_each_delay": (
                "z_v(t+theta+tau_j)*b_j(t+theta+tau_j), where "
                "b_j(s)=epsilon/2*(kappa_1+3*kappa_3*(v(s-tau_j)-1)^2)"
            ),
            "pairing_invariance": "d/dt f_t(x_t)=0",
            "left_monodromy_action": "f_0(M phi)=lambda*f_0(phi)",
            "flow_tangent_annihilation": (
                "f(p)=0 because Mp=p and fM=lambda*f with lambda!=1"
            ),
            "route_c_section_consequence": (
                "for Q=I-p*h_C/h_C(p), f(Qy)=f(y); hence f(q^Sigma)=f(q)"
            ),
            "analytic_identity_proved": True,
            "atoms_and_density_numerically_enclosed": False,
        },
        directed_fourier_grushin_left_row=grushin,
        finite_section_history_action_pilot=pilot,
        correlated_deflation_interface={
            "normalized_formula": "Pi_s Y=Y-q*f(Y) after choosing f(q)=1",
            "unscaled_formula": "Pi_s Y=Y-q*f(Y)/f(q)",
            "required_evaluation_order": (
                "evaluate f(Y_qq) and subtract q times that same shared "
                "scalar inside one outward interval/Taylor object; take the "
                "history sup norm only afterward"
            ),
            "pilot_python_entry_point": (
                "canard_control.leaky_route_c_adjoint_stage4c."
                "apply_discrete_normalized_deflation"
            ),
            "pilot_entry_point_is_directed": False,
            "strict_input_type": (
                "shared-noise outward interval polynomial histories for "
                "q, Y_qq, and the adjoint action"
            ),
            "global_projection_norm_transfer_allowed": False,
            "separate_absolute_triangle_bound_allowed": False,
        },
        stage4b_ingress_update={
            "qualitative_f_of_q_nonzero_gate_closed": True,
            "fourier_pencil_left_row_gate_closed": True,
            "continuous_history_measure_action_gate_closed": False,
            "action_on_actual_y_qq_gate_closed": False,
            "stable_output_uu_directed_upper": None,
            "stable_output_uu_design_target": "12",
            "stage4a_heuristic_envelope": "7.94681563672845125978",
            "isolated_pilot_failure_ceiling": "13.91505697189666824171448158",
            "structural_obstruction_found": False,
            "minimal_remaining_gate": (
                "turn the enclosed Fourier cokernel row into a directed "
                "normalized Route-C history action, then apply it directly "
                "to a shared enclosure of the physical-return Y_qq"
            ),
        },
        claim_status=claims,
    )


def build_stage4c_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = asdict(build_stage4c_artifact(repository))
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
            "parent_result_sha256": dict(artifact["parent_result_sha256"]),
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "grushin_openblas_num_threads": os.environ.get(
                    "OPENBLAS_NUM_THREADS"
                ),
                "pilot_openblas_num_threads": PINNED_PILOT_OPENBLAS_THREADS,
                "mpfr_precision_bits": PRECISION_BITS,
            },
        },
    }


def validate_stage4c_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("the Stage-4C result has the wrong outer schema")
    artifact = _mapping(payload.get("artifact"), "Stage-4C artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4C manifest")
    if set(artifact) != {field.name for field in fields(Stage4CArtifact)}:
        raise ValueError("the Stage-4C artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4C identity changed")
    claims = _mapping(artifact.get("claim_status"), "Stage-4C claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4C claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4C statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4C theorem gate was promoted")
    theorem = _mapping(
        artifact.get("simple_multiplier_and_pairing_theorem"),
        "Stage-4C pairing theorem",
    )
    if (
        theorem.get("f_of_q_nonzero_validated") is not True
        or theorem.get("directed_numeric_rescaling_available") is not False
    ):
        raise ValueError("the Stage-4C pairing status changed")
    grushin = _mapping(
        artifact.get("directed_fourier_grushin_left_row"),
        "Stage-4C Grushin row",
    )
    if (
        grushin.get("full_infinite_fourier_cokernel_row_enclosed") is not True
        or grushin.get("fourier_cokernel_row_nonzero") is not True
        or grushin.get("history_adjoint_measure_identification_validated") is not False
        or gmpy2.mpq(grushin["exact_bottom_row_distance_dual_upper"])
        >= gmpy2.mpq("1.18e-9")
        or gmpy2.mpq(grushin["largest_component"]["exact_modulus_lower"])
        <= gmpy2.mpq("0.0296")
    ):
        raise ValueError("the directed Stage-4C Fourier row changed")
    pilot = _mapping(
        artifact.get("finite_section_history_action_pilot"),
        "Stage-4C history pilot",
    )
    rows = pilot.get("mesh_rows")
    if (
        not isinstance(rows, list)
        or [row.get("step_count") for row in rows] != list(PILOT_STEP_COUNTS)
        or pilot.get("mesh_changes_are_interval_errors") is not False
        or pilot.get("pilot_promoted_to_history_measure") is not False
    ):
        raise ValueError("the Stage-4C finite-section pilot changed")
    ingress = _mapping(
        artifact.get("stage4b_ingress_update"), "Stage-4B ingress update"
    )
    if (
        ingress.get("qualitative_f_of_q_nonzero_gate_closed") is not True
        or ingress.get("continuous_history_measure_action_gate_closed") is not False
        or ingress.get("action_on_actual_y_qq_gate_closed") is not False
        or ingress.get("stable_output_uu_directed_upper") is not None
        or ingress.get("structural_obstruction_found") is not False
    ):
        raise ValueError("an open Stage-4C ingress was promoted")

    expected_manifest = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest:
        raise ValueError("the Stage-4C manifest schema changed")
    parents = {
        ROOT_RESULT_RELATIVE_PATH: ROOT_RESULT_SHA256,
        STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
        STAGE4B_RESULT_RELATIVE_PATH: STAGE4B_RESULT_SHA256,
    }
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": parents,
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4C manifest fixed data changed")
    repository = repository.resolve()
    sources = _mapping(manifest.get("source_sha256"), "Stage-4C sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4C source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4C source changed: {relative}")
    for relative, digest in parents.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4C parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "PILOT_STEP_COUNTS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "Stage4CArtifact",
    "TRUE_FLAGS",
    "apply_discrete_normalized_deflation",
    "build_stage4c_artifact",
    "build_stage4c_result",
    "canonical_sha256",
    "validate_stage4c_result",
]
