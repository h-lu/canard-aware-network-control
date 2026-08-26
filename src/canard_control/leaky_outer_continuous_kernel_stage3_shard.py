"""Composable Stage-3 shard for the exact outer continuous kernel.

The shard validates the first short propagation cell of each delayed-history
injection contributing to the absolutely continuous kernel.  For
theta in [-1e-3,0] and s=theta+tau_j, it encloses

    dR/du = A(s+u) R,  R(0)=I,  0<=u<=1e-3,

because this elapsed-time cell is strictly shorter than the minimum delay and
there is no delayed resolvent feedback yet.  The coefficient enclosure uses
the exact directed Fourier polynomial plus the validated 1e-8 orbit/period
ball.  An invariant-path Gronwall box and an outward interval Picard integral
give a rigorous endpoint matrix.  Multiplication by the exact delayed
injection coefficient yields one rigorous absolutely continuous density box
for each delay.

This is a composable local proof shard.  It does not propagate to the returned
history, integrate total variation, or provide the global shadow-transfer
errors E_v and E_w.  Those fields remain null and no C0 contraction is
claimed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
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
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.leaky_floquet_outer_grushin_stage1 import (
    RESULT_RELATIVE_PATH as GRUSHIN_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_signed_kernel_stage2 import (
    RESULT_RELATIVE_PATH as STAGE2_RESULT_RELATIVE_PATH,
    validate_outer_signed_kernel_stage2_result,
)
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences


SCHEMA_ID = "leaky-outer-continuous-kernel-stage3-shard-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_continuous_kernel_stage3_shard.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_continuous_kernel_stage3_shard.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_continuous_kernel_stage3_shard.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-continuous-kernel-stage3-shard.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_continuous_kernel_stage3_shard.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_signed_kernel_stage2.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/leaky_outer_high_resolution.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_continuous_kernel_stage3_shard.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR Fourier-phase, exact-orbit/period ball, coefficient, "
    "Gronwall invariant-path, interval Picard integral, and Volterra density "
    "injection arithmetic; exact source and parent binding"
)

OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
GRUSHIN_RESULT_SHA256 = (
    "5ca82a8c3e25ef0749e29142e9e19f49f21d219794b881ad3c9fb9011de0e524"
)
STAGE2_RESULT_SHA256 = (
    "f4742db560c5de29072adfb0b963d5a21e993fed5a949a2180dcc6d0b355011f"
)
PRECISION_BITS = 160
PINNED_OPENBLAS_NUM_THREADS = "1"
EXACT_ORBIT_RADIUS = "1e-8"
THETA_CELL_LOWER = "-0.001"
THETA_CELL_UPPER = "0"
LOCAL_ELAPSED_TIME = "0.001"

TRUE_FLAGS = (
    "nested_exact_outer_orbit_radius_parent_validated",
    "exact_period_uncertainty_included",
    "exact_voltage_wiener_evaluation_error_included",
    "physical_unshifted_variational_coefficient_enclosed",
    "minimum_delay_exceeds_local_elapsed_cell",
    "delayed_resolvent_feedback_exactly_zero_on_initial_cell",
    "gronwall_invariant_path_box_validated",
    "interval_picard_endpoint_matrix_validated",
    "two_delay_ac_density_injection_boxes_validated",
    "stage3_shard_is_composable",
)
FALSE_FLAGS = (
    "initial_shard_promoted_to_full_period_kernel",
    "all_theta_cells_continuously_propagated",
    "all_method_of_steps_depths_continuously_propagated",
    "returned_phase_subtracted_density_tv_validated",
    "voltage_shadow_transfer_error_validated",
    "recovery_shadow_transfer_error_validated",
    "phase_chart_shadow_transfer_error_validated",
    "arbitrary_c0_linear_return_contraction_validated",
    "outer_nonlinear_return_contraction_validated",
    "outer_quantitative_attracting_tube_validated",
    "outer_pulse_capture_validated",
    "physical_pulse_onset_validated",
)


IntervalMatrix = tuple[
    tuple[DirectedInterval, DirectedInterval],
    tuple[DirectedInterval, DirectedInterval],
]


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
        raise ValueError(f"{name} must be a mapping")
    return value


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower, 60),
        "upper": decimal_upper(value.upper, 60),
    }


def _matrix_record(matrix: IntervalMatrix) -> tuple[tuple[dict[str, str], ...], ...]:
    return tuple(tuple(_interval_record(value) for value in row) for row in matrix)


def _vector_record(vector: Sequence[DirectedInterval]) -> tuple[dict[str, str], ...]:
    return tuple(_interval_record(value) for value in vector)


def _zero() -> DirectedInterval:
    return DirectedInterval.from_decimal(0, PRECISION_BITS)


def _one() -> DirectedInterval:
    return DirectedInterval.from_decimal(1, PRECISION_BITS)


def _symmetric(radius: gmpy2.mpfr) -> DirectedInterval:
    return DirectedInterval.from_bounds(-radius, radius, PRECISION_BITS)


def _identity() -> IntervalMatrix:
    return ((_one(), _zero()), (_zero(), _one()))


def _zero_matrix() -> IntervalMatrix:
    return ((_zero(), _zero()), (_zero(), _zero()))


def _matrix_add(left: IntervalMatrix, right: IntervalMatrix) -> IntervalMatrix:
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def _matrix_multiply(left: IntervalMatrix, right: IntervalMatrix) -> IntervalMatrix:
    return tuple(
        tuple(
            left[i][0] * right[0][j] + left[i][1] * right[1][j]
            for j in range(2)
        )
        for i in range(2)
    )  # type: ignore[return-value]


def _matrix_scale(matrix: IntervalMatrix, scalar: DirectedInterval) -> IntervalMatrix:
    return tuple(
        tuple(value * scalar for value in row) for row in matrix
    )  # type: ignore[return-value]


def _matrix_inf_norm_upper(matrix: IntervalMatrix) -> gmpy2.mpfr:
    rows: list[gmpy2.mpfr] = []
    for row in matrix:
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            rows.append(row[0].upper_abs() + row[1].upper_abs())
    return max(rows)


def _matrix_expand(matrix: IntervalMatrix, radius: gmpy2.mpfr) -> IntervalMatrix:
    error = _symmetric(radius)
    return tuple(
        tuple(value + error for value in row) for row in matrix
    )  # type: ignore[return-value]


def _matvec(matrix: IntervalMatrix, vector: Sequence[DirectedInterval]) -> tuple[DirectedInterval, DirectedInterval]:
    if len(vector) != 2:
        raise ValueError("the Stage-3 shard requires a two-vector")
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def directed_picard_matrix_step(
    *,
    current_matrix: IntervalMatrix,
    current_coefficient: IntervalMatrix,
    delayed_forcing: IntervalMatrix,
    step: DirectedInterval,
) -> tuple[IntervalMatrix, IntervalMatrix, gmpy2.mpfr, gmpy2.mpfr]:
    """Validate one composable interval-Picard matrix step.

    ``current_coefficient`` and ``delayed_forcing`` must enclose their values
    throughout the cell.  The return values are the invariant path box, the
    endpoint box, the path-expansion radius, and the endpoint norm upper.
    """

    if step.lower < 0:
        raise ValueError("the Picard step must be nonnegative")
    coefficient_norm = _matrix_inf_norm_upper(current_coefficient)
    initial_norm = _matrix_inf_norm_upper(current_matrix)
    forcing_norm = _matrix_inf_norm_upper(delayed_forcing)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        h = step.upper
        growth = gmpy2.exp(coefficient_norm * h)
        path_norm = (initial_norm + h * forcing_norm) * growth
        expansion = h * (coefficient_norm * path_norm + forcing_norm)
    path_box = _matrix_expand(current_matrix, expansion)
    derivative_box = _matrix_add(
        _matrix_multiply(current_coefficient, path_box), delayed_forcing
    )
    endpoint = _matrix_add(
        current_matrix, _matrix_scale(derivative_box, step)
    )
    return path_box, endpoint, expansion, _matrix_inf_norm_upper(endpoint)


def _series_real_box(
    coefficients: Mapping[int, DirectedComplexInterval],
    phase: DirectedInterval,
) -> DirectedInterval:
    zero = _zero()
    total = DirectedComplexInterval(zero, zero)
    pi = pi_interval(PRECISION_BITS)
    for mode, coefficient in coefficients.items():
        angle = pi * (2 * int(mode)) * phase
        total = total + coefficient * complex_unit_interval(angle)
    return total.real


def _exact_voltage_box(
    base: Any,
    physical_time: DirectedInterval,
    exact_period: DirectedInterval,
    radius: DirectedInterval,
) -> DirectedInterval:
    phase = physical_time / exact_period
    return _series_real_box(base.voltage, phase) + DirectedInterval.from_bounds(
        -radius.upper, radius.upper, PRECISION_BITS
    )


def _current_matrix(voltage: DirectedInterval, parameters: Mapping[str, DirectedInterval]) -> IntervalMatrix:
    epsilon = parameters["epsilon"]
    kappa_1 = parameters["kappa_1"]
    kappa_3 = parameters["kappa_3"]
    centered = voltage - 1
    fast_voltage = 1 - voltage**2 - epsilon * (
        kappa_1 + 3 * kappa_3 * centered**2
    )
    return (
        (fast_voltage, DirectedInterval.from_decimal(-1, PRECISION_BITS)),
        (epsilon, -epsilon),
    )


def _delayed_injection_coefficient(
    delayed_voltage: DirectedInterval,
    parameters: Mapping[str, DirectedInterval],
) -> DirectedInterval:
    epsilon = parameters["epsilon"]
    centered = delayed_voltage - 1
    return (epsilon / 2) * (
        parameters["kappa_1"]
        + 3 * parameters["kappa_3"] * centered**2
    )


@dataclass(frozen=True)
class InjectionShard:
    delay_id: str
    delay_interval: dict[str, str]
    theta_cell: dict[str, str]
    injection_time_cell: dict[str, str]
    propagated_time_cell: dict[str, str]
    normalized_phase_cell: dict[str, str]
    exact_voltage_cell: dict[str, str]
    current_coefficient_matrix: tuple[tuple[dict[str, str], ...], ...]
    delayed_injection_coefficient: dict[str, str]
    delayed_resolvent_feedback_matrix: tuple[tuple[dict[str, str], ...], ...]
    invariant_path_matrix: tuple[tuple[dict[str, str], ...], ...]
    endpoint_resolvent_matrix: tuple[tuple[dict[str, str], ...], ...]
    endpoint_density_vector: tuple[dict[str, str], ...]
    path_expansion_radius_upper: str
    endpoint_resolvent_inf_norm_upper: str
    endpoint_density_inf_norm_upper: str
    minimum_delay_minus_elapsed_lower: str
    initial_dirac_jump_is_identity: bool
    delayed_feedback_zero_on_cell: bool
    interval_picard_endpoint_validated: bool
    exact_ac_density_injection_validated: bool
    composable_endpoint_interface_validated: bool


@dataclass(frozen=True)
class ContinuousKernelStage3Shard:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    binary_blas_thread_count: int
    parent_result_sha256: dict[str, str]
    exact_orbit_radius: str
    stored_period_interval: dict[str, str]
    exact_period_interval: dict[str, str]
    theta_cell: dict[str, str]
    local_elapsed_time: str
    injection_shards: tuple[InjectionShard, ...]
    composition_contract: dict[str, Any]
    global_transfer_budget: dict[str, Any]
    claim_status: dict[str, bool]
    conclusion: str


def _load_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a continuous-kernel shard parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _build_injection_shard(
    *,
    delay_id: str,
    delay: DirectedInterval,
    minimum_delay: DirectedInterval,
    theta: DirectedInterval,
    elapsed: DirectedInterval,
    base: Any,
    exact_period: DirectedInterval,
    radius: DirectedInterval,
) -> InjectionShard:
    injection_time = theta + delay
    propagated_time = injection_time + DirectedInterval.from_bounds(
        0, elapsed.upper, PRECISION_BITS
    )
    phase = propagated_time / exact_period
    voltage = _exact_voltage_box(base, propagated_time, exact_period, radius)
    coefficient = _current_matrix(voltage, base.parameters)
    delayed_voltage = _exact_voltage_box(base, theta, exact_period, radius)
    injection = _delayed_injection_coefficient(
        delayed_voltage, base.parameters
    )
    zero_forcing = _zero_matrix()
    path, endpoint, expansion, endpoint_norm = directed_picard_matrix_step(
        current_matrix=_identity(),
        current_coefficient=coefficient,
        delayed_forcing=zero_forcing,
        step=elapsed,
    )
    density = _matvec(endpoint, (injection, _zero()))
    density_norm = max(value.upper_abs() for value in density)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        no_delay_margin = minimum_delay.lower - elapsed.upper
    if no_delay_margin <= 0:
        raise ArithmeticError("the initial shard reaches delayed feedback")
    return InjectionShard(
        delay_id=delay_id,
        delay_interval=_interval_record(delay),
        theta_cell=_interval_record(theta),
        injection_time_cell=_interval_record(injection_time),
        propagated_time_cell=_interval_record(propagated_time),
        normalized_phase_cell=_interval_record(phase),
        exact_voltage_cell=_interval_record(voltage),
        current_coefficient_matrix=_matrix_record(coefficient),
        delayed_injection_coefficient=_interval_record(injection),
        delayed_resolvent_feedback_matrix=_matrix_record(zero_forcing),
        invariant_path_matrix=_matrix_record(path),
        endpoint_resolvent_matrix=_matrix_record(endpoint),
        endpoint_density_vector=_vector_record(density),
        path_expansion_radius_upper=decimal_upper(expansion, 60),
        endpoint_resolvent_inf_norm_upper=decimal_upper(endpoint_norm, 60),
        endpoint_density_inf_norm_upper=decimal_upper(density_norm, 60),
        minimum_delay_minus_elapsed_lower=decimal_lower(no_delay_margin, 60),
        initial_dirac_jump_is_identity=True,
        delayed_feedback_zero_on_cell=True,
        interval_picard_endpoint_validated=True,
        exact_ac_density_injection_validated=True,
        composable_endpoint_interface_validated=True,
    )


def build_continuous_kernel_stage3_shard(
    repository: Path,
) -> ContinuousKernelStage3Shard:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3 shard requires OPENBLAS_NUM_THREADS=1")
    stage2 = _load_parent(
        repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256
    )
    validate_outer_signed_kernel_stage2_result(stage2, repository)
    grushin = _load_parent(
        repository, GRUSHIN_RESULT_RELATIVE_PATH, GRUSHIN_RESULT_SHA256
    )
    grushin_certificate = _mapping(
        grushin.get("certificate"), "outer Grushin certificate"
    )
    if grushin_certificate.get("nested_correction_radius") != EXACT_ORBIT_RADIUS:
        raise ValueError("the exact nested outer-orbit radius changed")
    if gmpy2.mpq(str(grushin_certificate["nested_radii_margin_lower"])) <= 0:
        raise ValueError("the exact nested outer-orbit radius lost its proof margin")
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    radius = DirectedInterval.from_decimal(EXACT_ORBIT_RADIUS, PRECISION_BITS)
    exact_period = DirectedInterval.symmetric_radius(
        orbit.period, radius.upper, PRECISION_BITS
    )
    theta = DirectedInterval.from_bounds(
        THETA_CELL_LOWER, THETA_CELL_UPPER, PRECISION_BITS
    )
    elapsed = DirectedInterval.from_decimal(
        LOCAL_ELAPSED_TIME, PRECISION_BITS
    )
    delays = (
        ("tau_0", base.parameters["tau_0"]),
        ("tau_1", base.parameters["tau_1"]),
    )
    minimum_delay = min(
        (delay for _, delay in delays), key=lambda value: value.lower
    )
    shards = tuple(
        _build_injection_shard(
            delay_id=delay_id,
            delay=delay,
            minimum_delay=minimum_delay,
            theta=theta,
            elapsed=elapsed,
            base=base,
            exact_period=exact_period,
            radius=radius,
        )
        for delay_id, delay in delays
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return ContinuousKernelStage3Shard(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=1,
        parent_result_sha256={
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            GRUSHIN_RESULT_RELATIVE_PATH: GRUSHIN_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        exact_orbit_radius=EXACT_ORBIT_RADIUS,
        stored_period_interval=_interval_record(base.period),
        exact_period_interval=_interval_record(exact_period),
        theta_cell=_interval_record(theta),
        local_elapsed_time=LOCAL_ELAPSED_TIME,
        injection_shards=shards,
        composition_contract={
            "state": (
                "a 2x2 endpoint resolvent interval box for each injection "
                "parameter cell, plus delayed endpoint boxes addressed by tau_j"
            ),
            "next_cell_current_term": "A(t)*R(t,s)",
            "next_cell_delayed_forcing": (
                "sum_j B_j(t)*R(t-tau_j,s), using already validated earlier cells"
            ),
            "step_evaluator": (
                "directed_picard_matrix_step(current_matrix,A_box,forcing_box,h)"
            ),
            "method_of_steps_rule": (
                "a delayed forcing is exactly zero before t-s reaches its delay; "
                "afterward it must be read only from validated predecessor shards"
            ),
            "density_injection_rule": (
                "multiply the resolvent shard by B_j(s)e_v, retaining the "
                "theta-cell parameter enclosure"
            ),
            "phase_subtraction_rule": (
                "after propagation to returned time, subtract signed q-row "
                "kernels cellwise before absolute-value integration"
            ),
            "shard_digest_requirement": (
                "every shard records exact parameter/time cells, coefficient "
                "boxes, predecessor ids, endpoint boxes, and source hashes"
            ),
        },
        global_transfer_budget={
            "voltage_shadow_transfer_error_upper": None,
            "recovery_shadow_transfer_error_upper": None,
            "phase_chart_shadow_transfer_error_upper": None,
            "validated_theta_cell_count": 1,
            "required_theta_domain": "[-5*sqrt(5),0]",
            "validated_elapsed_time_upper": LOCAL_ELAPSED_TIME,
            "required_returned_time_domain": "[T-5*sqrt(5),T]",
            "full_period_density_propagation_complete": False,
            "returned_total_variation_accumulation_complete": False,
            "stage2_linear_gate_re_evaluated": False,
            "single_remaining_linear_inequality": (
                "max(Qv_shadow+E_voltage,Qw_shadow+E_recovery)<1"
            ),
        },
        claim_status=claims,
        conclusion=(
            "two exact continuous AC-density injection shards now close with "
            "directed orbit/period uncertainty and composable endpoint boxes; "
            "the global returned kernel and E_voltage/E_recovery remain open"
        ),
    )


def build_continuous_kernel_stage3_shard_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_continuous_kernel_stage3_shard(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
            },
        },
    }


def validate_continuous_kernel_stage3_shard_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the continuous-kernel Stage-3 shard schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3 certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3 manifest")
    if set(certificate) != {field.name for field in fields(ContinuousKernelStage3Shard)}:
        raise ValueError("the continuous-kernel Stage-3 fields changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the continuous-kernel Stage-3 digest changed")
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the continuous-kernel Stage-3 schema id changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3 source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the continuous-kernel Stage-3 source set changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a continuous-kernel Stage-3 source changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "Stage-3 claim ledger")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the continuous-kernel Stage-3 claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a validated local continuous-kernel fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open global continuous-kernel claim was promoted")
    shards = certificate.get("injection_shards")
    if not isinstance(shards, list) or [row.get("delay_id") for row in shards] != [
        "tau_0",
        "tau_1",
    ]:
        raise ValueError("the two continuous injection shards changed")
    for shard in shards:
        if not all(
            shard.get(name) is True
            for name in (
                "initial_dirac_jump_is_identity",
                "delayed_feedback_zero_on_cell",
                "interval_picard_endpoint_validated",
                "exact_ac_density_injection_validated",
                "composable_endpoint_interface_validated",
            )
        ):
            raise ValueError("a continuous injection shard lost validation")
        if gmpy2.mpq(str(shard["minimum_delay_minus_elapsed_lower"])) <= 0:
            raise ValueError("a continuous injection shard reaches delayed feedback")
    budget = _mapping(certificate.get("global_transfer_budget"), "Stage-3 global budget")
    if budget.get("full_period_density_propagation_complete") is not False:
        raise ValueError("the local shard was promoted to a full-period kernel")
    if any(
        budget.get(name) is not None
        for name in (
            "voltage_shadow_transfer_error_upper",
            "recovery_shadow_transfer_error_upper",
            "phase_chart_shadow_transfer_error_upper",
        )
    ):
        raise ValueError("a global transfer error was invented from a local shard")
    expected = json.loads(
        json.dumps(
            asdict(build_continuous_kernel_stage3_shard(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the continuous-kernel Stage-3 shard differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_continuous_kernel_stage3_shard",
    "build_continuous_kernel_stage3_shard_result",
    "canonical_sha256",
    "directed_picard_matrix_step",
    "validate_continuous_kernel_stage3_shard_result",
]
