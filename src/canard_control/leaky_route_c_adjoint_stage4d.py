"""Stage-4D Fourier-to-history adjoint bridge for the inner Route-C map.

Stage 4C enclosed a nonzero bottom row of the full Fourier Grushin inverse
but deliberately stopped before calling that row a continuous-history
adjoint measure.  This module closes that bridge in three pieces:

* the bilinear Fourier transpose uses mode reversal, not Hermitian
  conjugation, and is exactly the advanced RFDE adjoint equation;
* a separate row-sum tail contraction proves that the exact cokernel row is
  absolutely summable, hence reconstructs a continuous periodic adjoint;
* the Grushin derivative identity and the parent Rouché comparison give a
  directed nonzero interval for the history pairing ``f(q)``.

A source-bound finite-section pilot then evaluates ``Y_qq-q*f(Y_qq)`` as one
expression before taking its norm.  The pilot is not a directed enclosure of
the physical-return ``Y_qq``.  Thus ``C_s^{uu}<12`` and every stable-graph or
onset claim remain false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    upward_sum,
)
from canard_control.leaky_floquet_inner_unstable_root import (
    PRECISION_BITS,
    RESULT_RELATIVE_PATH as ROOT_RESULT_RELATIVE_PATH,
    ROOT_DISK_RADIUS,
    _complex_abs_upper,
    _dependency_fingerprint,
    _prepare_cached,
    _split_upper,
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
from canard_control.leaky_route_c_adjoint_stage4c import (
    RESULT_RELATIVE_PATH as STAGE4C_RESULT_RELATIVE_PATH,
    ROOT_REPLAY_CENTER,
    ROOT_REPLAY_NEIGHBORHOOD,
    _directed_grushin_left_row,
    validate_stage4c_result,
)


SCHEMA_ID = "leaky-route-c-adjoint-stage4d-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_route_c_adjoint_stage4d.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_route_c_adjoint_stage4d.py"
RESULT_RELATIVE_PATH = "experiments/results/leaky_route_c_adjoint_stage4d.json"
NOTE_RELATIVE_PATH = "docs/leaky-route-c-adjoint-stage4d.md"
TEST_RELATIVE_PATH = "tests/test_leaky_route_c_adjoint_stage4d.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_route_c_adjoint_stage4d.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source binding; 160-bit outward MPFR row-sum "
    "tail contraction and Wiener-l1 reconstruction from the Stage-4C full "
    "Grushin row; analytic bilinear Fourier reversal, advanced-adjoint, "
    "Grushin derivative, and averaged RFDE history-pairing identities; a "
    "Cauchy derivative estimate from the validated Rouché boundary error; "
    "plus a source-bound long-double shared-deflation pilot in a fresh "
    "one-thread OpenBLAS subprocess; no directed physical Y_qq, return tube, "
    "stable-output uu bound, graph, separator, or onset theorem"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

ROOT_RESULT_SHA256 = (
    "ab2876efc8a26df544f56257ab00b9fde0fea4ba043f4500f1450e0d0885fa2c"
)
STAGE3_RESULT_SHA256 = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)
STAGE4A_RESULT_SHA256 = (
    "b9308d01137559f5b88e42f7120b6eb01490aaa6bda3ac7b6eed2fd2ce5421c7"
)
STAGE4C_RESULT_SHA256 = (
    "5ddd440449e0405bab4ca33818174a8e214d85fa695f603ea45ddef051ceaa29"
)
INNER_ORBIT_RESULT_SHA256 = (
    "bee1da065d213c3c33d724ced1dba37c5914934515c1128588919bed34abe69b"
)

PINNED_GRUSHIN_OPENBLAS_THREADS = "8"
PINNED_PILOT_OPENBLAS_THREADS = "1"
PILOT_STEP_COUNTS = (120, 180, 240)

TRUE_FLAGS = (
    "bilinear_fourier_mode_reversal_identity_proved",
    "hermitian_conjugation_rejected",
    "advanced_rfde_adjoint_recovered_from_fourier_row",
    "adjoint_fourier_tail_wiener_l1_summable_validated",
    "continuous_periodic_adjoint_reconstructed",
    "history_atom_density_measure_numeric_enclosed",
    "grushin_border_normalization_identity_proved",
    "directed_f_of_q_modulus_lower_validated",
    "nonzero_recovery_history_action_shard_validated",
    "shared_y_qq_deflation_pilot_computed",
)
FALSE_FLAGS = (
    "mesh_refinement_is_interval_error",
    "directed_shared_action_on_physical_y_qq_available",
    "stable_output_uu_below_twelve_validated",
    "six_projected_return_hessian_blocks_validated",
    "stage4b_strict_certificate_closes",
    "inner_local_stable_graph_quantitatively_validated",
    "graph_radius_1p7e_minus_3_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage4DArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    fourier_reversal_and_advanced_adjoint: dict[str, Any]
    summable_adjoint_tail_certificate: dict[str, Any]
    grushin_border_normalization: dict[str, Any]
    continuous_history_measure_enclosure: dict[str, Any]
    shared_y_qq_deflation_pilot: dict[str, Any]
    directed_shared_y_qq_contract: dict[str, Any]
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


def fourier_reversal_oracle() -> dict[str, str]:
    """Check the bilinear reversal and separate a Hermitian mutation."""

    modes = np.arange(-3, 4, dtype=int)
    s = 0.31
    alpha = 0.27
    coefficients = {
        -1: 0.13 - 0.04j,
        0: -0.21 + 0.03j,
        1: 0.08 + 0.07j,
    }
    p = np.zeros(len(modes), dtype=complex)
    r = np.zeros(len(modes), dtype=complex)
    for mode, value in ((-1, 0.17 + 0.06j), (0, -0.11), (1, 0.04 - 0.09j)):
        p[mode + 3] = value
    for mode, value in ((-1, -0.03 + 0.12j), (0, 0.19), (1, 0.07 + 0.02j)):
        r[mode + 3] = value
    convolution = np.asarray(
        [
            [coefficients.get(int(k - m), 0.0) for m in modes]
            for k in modes
        ],
        dtype=complex,
    )
    output_rotation = np.diag(
        np.exp(-(s + 2.0j * np.pi * modes) * alpha)
    )
    row = np.asarray([r[-mode + 3] for mode in modes], dtype=complex)
    forward_fourier = complex(row @ (output_rotation @ convolution @ p))

    grid = np.arange(4096, dtype=float) / 4096.0
    exponential = np.exp(2.0j * np.pi * modes[:, None] * grid[None, :])
    p_grid = p @ exponential
    r_grid = r @ exponential
    b_grid = sum(
        value * np.exp(2.0j * np.pi * mode * grid)
        for mode, value in coefficients.items()
    )
    shifted_grid = (grid - alpha) % 1.0
    shifted_exponential = np.exp(
        2.0j * np.pi * modes[:, None] * shifted_grid[None, :]
    )
    p_shifted = p @ shifted_exponential
    b_shifted = sum(
        value * np.exp(2.0j * np.pi * mode * shifted_grid)
        for mode, value in coefficients.items()
    )
    forward_grid = np.mean(
        r_grid * np.exp(-s * alpha) * b_shifted * p_shifted
    )
    advanced_grid = np.mean(
        np.exp(-s * alpha)
        * b_grid
        * (r @ np.exp(
            2.0j * np.pi * modes[:, None] * ((grid + alpha) % 1.0)[None, :]
        ))
        * p_grid
    )
    hermitian_mutation = np.mean(
        np.conjugate(r_grid)
        * np.exp(-s * alpha)
        * b_shifted
        * p_shifted
    )
    return {
        "fourier_vs_physical_bilinear_error_binary64": format(
            abs(forward_fourier - forward_grid), ".17g"
        ),
        "forward_vs_advanced_change_of_variables_error_binary64": format(
            abs(forward_grid - advanced_grid), ".17g"
        ),
        "hermitian_mutation_separation_binary64": format(
            abs(forward_grid - hermitian_mutation), ".17g"
        ),
    }


def _binary_complex_sum_box(
    values: np.ndarray, precision: int
) -> DirectedComplexInterval:
    real = DirectedInterval.from_decimal(0, precision)
    imaginary = DirectedInterval.from_decimal(0, precision)
    for value in np.asarray(values, dtype=complex):
        real = real + DirectedInterval.from_float(float(value.real), precision)
        imaginary = imaginary + DirectedInterval.from_float(
            float(value.imag), precision
        )
    return DirectedComplexInterval(real, imaginary)


def _pairing_derivative_bounds(
    root_certificate: Mapping[str, Any],
    stage3_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    precision = PRECISION_BITS
    bracket = _mapping(stage3_certificate.get("root_bracket"), "root bracket")
    radius = DirectedInterval.from_decimal(ROOT_DISK_RADIUS, precision)
    center = DirectedInterval.from_float(
        float(root_certificate["root_disk_center_binary64"]), precision
    )
    lower = DirectedInterval.from_decimal(bracket["root_real_lower"], precision)
    upper = DirectedInterval.from_decimal(bracket["root_real_upper"], precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        root_offset = max(
            abs(lower.lower - center.upper), abs(upper.upper - center.lower)
        )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        cauchy_radius = radius.lower - root_offset
    comparison = DirectedInterval.from_decimal(
        root_certificate["maximum_boundary_comparison_error_upper"], precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        derivative_error = comparison / cauchy_radius
    reference = DirectedComplexInterval(
        DirectedInterval.from_float(
            float(root_certificate["reference_effective_slope_real_binary64"]),
            precision,
        ),
        DirectedInterval.from_float(
            float(root_certificate["reference_effective_slope_imag_binary64"]),
            precision,
        ),
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        pairing_lower = reference.lower_abs() - derivative_error
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        pairing_upper = reference.upper_abs() + derivative_error
    if pairing_lower <= 0:
        raise ArithmeticError("the Stage-4D history pairing lower bound vanished")
    return {
        "root_offset_from_rouche_center_upper": decimal_upper(root_offset),
        "cauchy_interior_radius_lower": decimal_lower(cauchy_radius),
        "boundary_affine_comparison_upper": decimal_upper(comparison),
        "effective_derivative_difference_upper": decimal_upper(derivative_error),
        "f_of_q_modulus_lower": decimal_lower(pairing_lower),
        "f_of_q_modulus_upper": decimal_upper(pairing_upper),
        "normalization_reciprocal_upper": decimal_upper(1 / pairing_lower),
    }


def _directed_fourier_history_bridge(
    repository: Path,
    root_certificate: Mapping[str, Any],
    stage3_certificate: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_GRUSHIN_OPENBLAS_THREADS:
        raise RuntimeError(
            "the Stage-4D bridge replay requires OPENBLAS_NUM_THREADS="
            + PINNED_GRUSHIN_OPENBLAS_THREADS
        )
    grushin = _directed_grushin_left_row(repository)
    prepared, _ = _prepare_cached(
        str(repository), _dependency_fingerprint(repository)
    )
    precision = PRECISION_BITS
    row_error = DirectedInterval.from_decimal(
        grushin["exact_bottom_row_distance_dual_upper"], precision
    ).upper
    coefficients = np.asarray(
        [
            complex(
                float(item["real_binary64"]),
                float(item["imag_binary64"]),
            )
            for item in grushin["finite_row_coefficients"]
        ],
        dtype=complex,
    )
    if len(coefficients) != 258:
        raise ValueError("the Stage-4C finite Grushin row changed dimension")
    finite_binary_l1 = upward_sum(
        tuple(_split_upper(value, precision) for value in coefficients),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_exact_l1 = finite_binary_l1 + len(coefficients) * row_error
        period_upper = prepared.base.period.upper + prepared.period_radius
        epsilon_upper = prepared.base.parameters["epsilon"].upper
        coefficient_sum = (
            prepared.current_binary_norm
            + 2 * prepared.delayed_binary_norm
            + prepared.current_total_variation
            + prepared.delayed_total_variation
        )
    fast_inverse = DirectedInterval.from_decimal(
        grushin["fast_tail_preconditioner_norm_upper"], precision
    ).upper
    slow_inverse = DirectedInterval.from_decimal(
        grushin["slow_tail_preconditioner_norm_upper"], precision
    ).upper
    neighborhood = DirectedInterval.from_decimal(
        ROOT_REPLAY_NEIGHBORHOOD, precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        fast_row = fast_inverse * (
            neighborhood + period_upper * (coefficient_sum + 1)
        )
        slow_row = slow_inverse * (
            period_upper * epsilon_upper
            + neighborhood
            + epsilon_upper * prepared.period_radius
        )
        tail_row_contraction = max(fast_row, slow_row)
    if not 0 < tail_row_contraction < 1:
        raise ArithmeticError("the Stage-4D adjoint row tail did not contract")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_to_tail_row = period_upper * coefficient_sum
        tail_inverse_row = max(fast_inverse, slow_inverse) / (
            1 - tail_row_contraction
        )
        tail_gain = finite_to_tail_row * tail_inverse_row
        total_tail_l1 = finite_exact_l1 * tail_gain
        recovery_from_voltage_tail = period_upper * slow_inverse
        recovery_tail_l1 = recovery_from_voltage_tail * total_tail_l1

    voltage = coefficients[:129]
    recovery = coefficients[129:]
    voltage_binary_l1 = upward_sum(
        tuple(_split_upper(value, precision) for value in voltage), precision
    )
    recovery_binary_l1 = upward_sum(
        tuple(_split_upper(value, precision) for value in recovery), precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage_finite_l1 = voltage_binary_l1 + len(voltage) * row_error
        recovery_finite_l1 = recovery_binary_l1 + len(recovery) * row_error
        voltage_total_l1 = voltage_finite_l1 + total_tail_l1
        recovery_total_l1 = recovery_finite_l1 + recovery_tail_l1
        total_adjoint_l1 = finite_exact_l1 + total_tail_l1

    recovery_sum = _binary_complex_sum_box(recovery, precision)
    voltage_sum = _binary_complex_sum_box(voltage, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        recovery_atom_lower = (
            recovery_sum.lower_abs()
            - len(recovery) * row_error
            - recovery_tail_l1
        )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        recovery_atom_upper = (
            recovery_sum.upper_abs()
            + len(recovery) * row_error
            + recovery_tail_l1
        )
        voltage_atom_upper = (
            voltage_sum.upper_abs()
            + len(voltage) * row_error
            + total_tail_l1
        )
    if recovery_atom_lower <= 0:
        raise ArithmeticError("the Stage-4D recovery action shard vanished")

    delayed_slot = (
        prepared.delayed_binary_norm + prepared.delayed_total_variation
    )
    tau_sum = upward_sum(
        (
            prepared.base.parameters["tau_0"].upper,
            prepared.base.parameters["tau_1"].upper,
        ),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        density_total_variation = (
            tau_sum * voltage_total_l1 * delayed_slot
        )
        history_measure_norm = (
            voltage_atom_upper
            + recovery_atom_upper
            + density_total_variation
        )

    pairing = _pairing_derivative_bounds(root_certificate, stage3_certificate)
    pairing_lower = DirectedInterval.from_decimal(
        pairing["f_of_q_modulus_lower"], precision
    ).lower
    pairing_upper = DirectedInterval.from_decimal(
        pairing["f_of_q_modulus_upper"], precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        normalized_measure_norm = history_measure_norm / pairing_lower
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        normalized_recovery_shard_lower = recovery_atom_lower / pairing_upper

    tail = {
        "finite_row_split_l1_upper": decimal_upper(finite_exact_l1),
        "exact_coefficient_sum_wiener_upper": decimal_upper(coefficient_sum),
        "tail_row_fast_contraction_upper": decimal_upper(fast_row),
        "tail_row_slow_contraction_upper": decimal_upper(slow_row),
        "tail_row_contraction_upper": decimal_upper(tail_row_contraction),
        "finite_to_tail_row_sum_upper": decimal_upper(finite_to_tail_row),
        "tail_inverse_row_sum_upper": decimal_upper(tail_inverse_row),
        "tail_l1_gain_from_finite_upper": decimal_upper(tail_gain),
        "full_tail_split_l1_upper": decimal_upper(total_tail_l1),
        "recovery_tail_from_voltage_factor_upper": decimal_upper(
            recovery_from_voltage_tail
        ),
        "recovery_tail_split_l1_upper": decimal_upper(recovery_tail_l1),
        "complete_adjoint_split_wiener_l1_upper": decimal_upper(
            total_adjoint_l1
        ),
        "tail_summability_validated": True,
        "tail_space": (
            "row l1 under the matrix row-sum norm; the parent l-infinity "
            "cokernel solution agrees by uniqueness of the tail solve"
        ),
    }
    measure = {
        "fourier_reconstruction": (
            "r_hat[n]=E_minus_state[-n] with no complex conjugation; "
            "z(T*theta)=exp(-s*theta)*r(theta)"
        ),
        "voltage_adjoint_wiener_l1_upper": decimal_upper(voltage_total_l1),
        "recovery_adjoint_wiener_l1_upper": decimal_upper(recovery_total_l1),
        "current_voltage_atom_modulus_upper": decimal_upper(voltage_atom_upper),
        "current_recovery_atom_modulus_lower": decimal_lower(
            recovery_atom_lower
        ),
        "current_recovery_atom_modulus_upper": decimal_upper(
            recovery_atom_upper
        ),
        "voltage_history_density_total_variation_upper": decimal_upper(
            density_total_variation
        ),
        "unnormalized_history_measure_norm_upper": decimal_upper(
            history_measure_norm
        ),
        "normalized_history_measure_norm_upper": decimal_upper(
            normalized_measure_norm
        ),
        "normalized_recovery_only_history_action_modulus_lower": decimal_lower(
            normalized_recovery_shard_lower
        ),
        "recovery_only_history_shard": (
            "phi_v(theta)=0 and phi_w(0)=1, so f(phi) is exactly the "
            "current-recovery atom"
        ),
        "continuous_atom_density_measure_numeric_enclosed": True,
    }
    return tail, pairing, measure


def _build_shared_yqq_pilot(repository: Path) -> dict[str, Any]:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_PILOT_OPENBLAS_THREADS:
        raise RuntimeError(
            "the Stage-4D Y_qq pilot requires OPENBLAS_NUM_THREADS="
            + PINNED_PILOT_OPENBLAS_THREADS
        )
    orbit_payload = _load_parent(
        repository,
        INNER_ORBIT_RESULT_RELATIVE_PATH,
        INNER_ORBIT_RESULT_SHA256,
        "inner orbit",
    )
    candidate = validate_leaky_periodic_branch_artifact(
        orbit_payload, repository
    )
    orbit = _LongDoubleFourierOrbit(
        np.asarray(candidate.state, dtype=np.longdouble), candidate.period
    )
    model = _model_from_payload(orbit_payload)
    rows: list[dict[str, Any]] = []
    for step_count in PILOT_STEP_COUNTS:
        jacobian, hessian, diagnostics = _finite_section_variations(
            orbit, model, step_count
        )
        _, right, left, split = _dominant_split(jacobian)
        y_qq = np.einsum(
            "oij,i,j->o", hessian, right, right, optimize=True
        )
        scalar = left @ y_qq
        unstable_reconstruction = right * scalar
        stable_output = y_qq - unstable_reconstruction
        raw_norm = np.max(np.abs(y_qq))
        reconstruction_norm = np.max(np.abs(unstable_reconstruction))
        stable_norm = np.max(np.abs(stable_output))
        rows.append(
            {
                "step_count": step_count,
                "section_dimension": diagnostics["section_dimension"],
                "unstable_scalar_f_n_y_qq": _format(scalar),
                "raw_y_qq_linf": _format(raw_norm),
                "unstable_reconstruction_linf": _format(
                    reconstruction_norm
                ),
                "separate_triangle_upper": _format(
                    raw_norm + reconstruction_norm
                ),
                "correlated_stable_output_linf": _format(stable_norm),
                "raw_to_correlated_ratio": _format(raw_norm / stable_norm),
                "triangle_to_correlated_ratio": _format(
                    (raw_norm + reconstruction_norm) / stable_norm
                ),
                "left_action_of_deflated_output_abs": _format(
                    abs(left @ stable_output)
                ),
                "evaluation_order": (
                    "form y_qq-right*(left@y_qq) first, then take l-infinity"
                ),
                "left_eigen_residual_inf": split[
                    "unstable_left_residual_inf"
                ],
                "evidence_status": (
                    "source-bound long-double finite-section pilot; not a "
                    "directed continuous-history Y_qq enclosure"
                ),
            }
        )
    return {
        "mesh_rows": rows,
        "last_two_mesh_stable_output_change": _format(
            abs(
                np.longdouble(rows[-1]["correlated_stable_output_linf"])
                - np.longdouble(rows[-2]["correlated_stable_output_linf"])
            )
        ),
        "mesh_change_is_interval_error": False,
        "pilot_promoted_to_directed_y_qq_action": False,
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
        "from canard_control.leaky_route_c_adjoint_stage4d import "
        "_build_shared_yqq_pilot; "
        "print(json.dumps(_build_shared_yqq_pilot(Path(sys.argv[1])),"
        "sort_keys=True,separators=(',',':'),allow_nan=False))"
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
            "the Stage-4D one-thread Y_qq subprocess failed: "
            + completed.stderr.strip()
        )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("the Stage-4D Y_qq subprocess returned no mapping")
    return value


def build_stage4d_artifact(repository: Path) -> Stage4DArtifact:
    repository = repository.resolve()
    root = _load_parent(
        repository, ROOT_RESULT_RELATIVE_PATH, ROOT_RESULT_SHA256, "inner root"
    )
    stage3 = _load_parent(
        repository, STAGE3_RESULT_RELATIVE_PATH, STAGE3_RESULT_SHA256, "Stage-3"
    )
    stage4a = _load_parent(
        repository, STAGE4A_RESULT_RELATIVE_PATH, STAGE4A_RESULT_SHA256, "Stage-4A"
    )
    stage4c = _load_parent(
        repository, STAGE4C_RESULT_RELATIVE_PATH, STAGE4C_RESULT_SHA256, "Stage-4C"
    )
    validate_stage3_stable_projection_result(stage3, repository)
    validate_stage4a_pilot_result(stage4a, repository)
    validate_stage4c_result(stage4c, repository)
    root_certificate = _mapping(root.get("certificate"), "root certificate")
    stage3_certificate = _mapping(stage3.get("certificate"), "Stage-3 certificate")
    tail, pairing, measure = _directed_fourier_history_bridge(
        repository, root_certificate, stage3_certificate
    )
    oracle = fourier_reversal_oracle()
    if (
        float(oracle["fourier_vs_physical_bilinear_error_binary64"]) > 1e-14
        or float(
            oracle["forward_vs_advanced_change_of_variables_error_binary64"]
        ) > 1e-14
        or float(oracle["hermitian_mutation_separation_binary64"]) < 1e-4
    ):
        raise ArithmeticError("the Stage-4D Fourier reversal oracle failed")
    pilot = _pilot_subprocess(repository)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4DArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            ROOT_RESULT_RELATIVE_PATH: ROOT_RESULT_SHA256,
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
            STAGE4C_RESULT_RELATIVE_PATH: STAGE4C_RESULT_SHA256,
        },
        fourier_reversal_and_advanced_adjoint={
            "bilinear_pairing": (
                "integral_0^1 r(theta)^T g(theta)dtheta="
                "sum_k r_hat[-k]^T g_hat[k]"
            ),
            "row_to_adjoint_coefficients": "r_hat[n]=E_minus_state[-n]",
            "complex_conjugation_used": False,
            "forward_delayed_operator": (
                "exp(-(D+s)alpha_j) applied after multiplication by the "
                "unshifted delayed coefficient b_j"
            ),
            "bilinear_transpose_delayed_operator": (
                "multiplication by b_j followed by exp(-s alpha_j) and "
                "the advanced shift r(theta+alpha_j)"
            ),
            "advanced_physical_adjoint": (
                "-z'(t)=A_0(t)^Tz(t)+sum_j A_j(t+tau_j)^Tz(t+tau_j)"
            ),
            "oracle": oracle,
            "identity_status": "analytic coefficient identity; binary oracle diagnostic",
        },
        summable_adjoint_tail_certificate=tail,
        grushin_border_normalization={
            "grushin_inverse_blocks": (
                "[[E,E_plus],[E_minus,E_minus_plus]]"
            ),
            "root_kernel_normalization": "R_plus E_plus=1",
            "root_cokernel_normalization": "E_minus R_minus=1",
            "effective_hamiltonian_derivative": (
                "E_minus_plus'(s_star)=-E_minus L'(s_star) E_plus"
            ),
            "averaged_history_pairing_identity": (
                "E_minus L'(s_star) E_plus equals the phase average of "
                "the invariant RFDE bilinear history pairing, hence f(q)"
            ),
            "cauchy_argument": (
                "the Rouché boundary comparison bounds the analytic remainder; "
                "Cauchy's estimate on the root-centered interior disk bounds "
                "the derivative remainder"
            ),
            **pairing,
            "directed_numeric_normalization_available": True,
        },
        continuous_history_measure_enclosure=measure,
        shared_y_qq_deflation_pilot=pilot,
        directed_shared_y_qq_contract={
            "required_input": (
                "one shared outward interval-polynomial enclosure of q, the "
                "physical-time event-corrected Y_qq history, and the adjoint "
                "atoms/densities on every history cell"
            ),
            "required_scalar_action": (
                "integrate the same Y_qq enclosure against the normalized "
                "atom-plus-density measure without decorrelating symbols"
            ),
            "required_output_expression": (
                "Y_qq-q*f(Y_qq), evaluated cellwise before any absolute value "
                "or history sup norm"
            ),
            "global_projection_norm_transfer_allowed": False,
            "separate_triangle_bound_allowed": False,
            "physical_return_y_qq_directed_enclosure": None,
            "normalized_adjoint_action_on_y_qq_directed_enclosure": None,
            "correlated_stable_output_uu_upper": None,
            "contract_closes": False,
        },
        stage4b_ingress_update={
            "continuous_history_measure_action_gate_closed": True,
            "directed_normalization_gate_closed": True,
            "nonzero_history_action_shard_closed": True,
            "action_on_actual_shared_y_qq_gate_closed": False,
            "stable_output_uu_directed_upper": None,
            "stable_output_uu_design_target": "12",
            "stage4a_heuristic_envelope": "7.94681563672845125978",
            "structural_obstruction_found": False,
            "minimal_remaining_gate": (
                "propagate the physical event-corrected Y_qq in the same "
                "interval-polynomial history representation and perform the "
                "normalized adjoint subtraction before taking the norm"
            ),
        },
        claim_status=claims,
    )


def build_stage4d_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = asdict(build_stage4d_artifact(repository))
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


def validate_stage4d_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("the Stage-4D result has the wrong outer schema")
    artifact = _mapping(payload.get("artifact"), "Stage-4D artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4D manifest")
    if set(artifact) != {field.name for field in fields(Stage4DArtifact)}:
        raise ValueError("the Stage-4D artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4D identity changed")
    claims = _mapping(artifact.get("claim_status"), "Stage-4D claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4D claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4D statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4D theorem gate was promoted")
    tail = _mapping(
        artifact.get("summable_adjoint_tail_certificate"), "Stage-4D tail"
    )
    if (
        tail.get("tail_summability_validated") is not True
        or gmpy2.mpq(tail["tail_row_contraction_upper"]) >= gmpy2.mpq("0.105")
        or gmpy2.mpq(tail["full_tail_split_l1_upper"]) >= gmpy2.mpq("0.012")
    ):
        raise ValueError("the Stage-4D summable tail changed")
    normalization = _mapping(
        artifact.get("grushin_border_normalization"),
        "Stage-4D normalization",
    )
    if (
        normalization.get("directed_numeric_normalization_available") is not True
        or gmpy2.mpq(normalization["f_of_q_modulus_lower"])
        <= gmpy2.mpq("0.0003")
    ):
        raise ValueError("the Stage-4D pairing normalization changed")
    measure = _mapping(
        artifact.get("continuous_history_measure_enclosure"),
        "Stage-4D history measure",
    )
    if (
        measure.get("continuous_atom_density_measure_numeric_enclosed") is not True
        or gmpy2.mpq(measure["current_recovery_atom_modulus_lower"]) <= 0
        or gmpy2.mpq(
            measure["normalized_recovery_only_history_action_modulus_lower"]
        ) <= 0
    ):
        raise ValueError("the Stage-4D history measure changed")
    pilot = _mapping(
        artifact.get("shared_y_qq_deflation_pilot"), "Stage-4D Y_qq pilot"
    )
    rows = pilot.get("mesh_rows")
    if (
        not isinstance(rows, list)
        or [row.get("step_count") for row in rows] != list(PILOT_STEP_COUNTS)
        or pilot.get("mesh_change_is_interval_error") is not False
        or pilot.get("pilot_promoted_to_directed_y_qq_action") is not False
    ):
        raise ValueError("the Stage-4D Y_qq pilot changed")
    contract = _mapping(
        artifact.get("directed_shared_y_qq_contract"),
        "Stage-4D shared Y_qq contract",
    )
    if (
        contract.get("physical_return_y_qq_directed_enclosure") is not None
        or contract.get("normalized_adjoint_action_on_y_qq_directed_enclosure")
        is not None
        or contract.get("correlated_stable_output_uu_upper") is not None
        or contract.get("contract_closes") is not False
        or contract.get("global_projection_norm_transfer_allowed") is not False
    ):
        raise ValueError("an open Stage-4D shared action was promoted")
    ingress = _mapping(
        artifact.get("stage4b_ingress_update"), "Stage-4D ingress update"
    )
    if (
        ingress.get("continuous_history_measure_action_gate_closed") is not True
        or ingress.get("directed_normalization_gate_closed") is not True
        or ingress.get("action_on_actual_shared_y_qq_gate_closed") is not False
        or ingress.get("stable_output_uu_directed_upper") is not None
        or ingress.get("structural_obstruction_found") is not False
    ):
        raise ValueError("the Stage-4D ingress status changed")

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
        raise ValueError("the Stage-4D manifest schema changed")
    parents = {
        ROOT_RESULT_RELATIVE_PATH: ROOT_RESULT_SHA256,
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
        STAGE4C_RESULT_RELATIVE_PATH: STAGE4C_RESULT_SHA256,
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
        raise ValueError("the Stage-4D manifest fixed data changed")
    repository = repository.resolve()
    sources = _mapping(manifest.get("source_sha256"), "Stage-4D sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4D source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4D source changed: {relative}")
    for relative, digest in parents.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4D parent changed: {relative}")


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
    "Stage4DArtifact",
    "TRUE_FLAGS",
    "build_stage4d_artifact",
    "build_stage4d_result",
    "canonical_sha256",
    "fourier_reversal_oracle",
    "validate_stage4d_result",
]
