"""Stage-3B frontier sweep across the first delayed-resolvent boundary.

For the theta band [-1e-3,0], this module treats both history-injection
branches s=theta+tau_j.  It tiles elapsed time up to tau_0, accumulates a
rigorous infinity logarithmic-norm bound for the homogeneous resolvent,
bridges the directed uncertainty in tau_0, and then validates one cell with
the genuinely nonzero forcing

    B_0(s+u) R(s+u-tau_0,s).

A tight interval-Picard sweep is attempted in parallel and stopped at the
first width threshold, which is recorded as a proof frontier together with a
mandatory dyadic refinement rule.  The coarse logarithmic-norm bridge makes
the delayed-boundary crossing rigorous but far too wide for a global return
contraction.  No shadow-transfer error is inferred.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import DirectedInterval, decimal_lower, decimal_upper
from canard_control.leaky_outer_continuous_kernel_stage3_shard import (
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    _build_leaky_base_sequences,
    _current_matrix,
    _delayed_injection_coefficient,
    _exact_voltage_box,
    _identity,
    _interval_record,
    _matvec,
    _matrix_inf_norm_upper,
    _matrix_multiply,
    _matrix_record,
    _symmetric,
    _vector_record,
    _zero,
    _zero_matrix,
    directed_picard_matrix_step,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)


SCHEMA_ID = "leaky-outer-continuous-kernel-stage3b-frontier-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_continuous_kernel_stage3b_frontier.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_continuous_kernel_stage3b_frontier.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_continuous_kernel_stage3b_frontier.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-continuous-kernel-stage3b-frontier.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_continuous_kernel_stage3b_frontier.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_continuous_kernel_stage3_shard.py",
    "src/canard_control/leaky_outer_high_resolution.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_continuous_kernel_stage3b_frontier.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR exact-orbit coefficient cells; infinity logarithmic "
    "norm accumulation; directed delay-uncertainty bridge; composable interval "
    "Picard cells with the first nonzero delayed-resolvent forcing; and exact "
    "source/parent binding"
)

STAGE3_RESULT_SHA256 = (
    "b8dc1027cdf3a952ee3bdef9605b4feab3c9188fee106d4e734733219de657fe"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
PRECISION_BITS = 160
PINNED_OPENBLAS_NUM_THREADS = "1"
EXACT_ORBIT_RADIUS = "1e-8"
THETA_LOWER = "-0.001"
THETA_UPPER = "0"
COARSE_ELAPSED_TILE_WIDTH = "0.5"
DELAY_CROSSING_TILE_WIDTH = "0.001"
TIGHT_ENDPOINT_NORM_LIMIT = "1000000"

TRUE_FLAGS = (
    "both_injection_branches_tiled_to_first_delay_boundary",
    "preboundary_logarithmic_norm_growth_validated",
    "directed_tau0_uncertainty_bridge_validated",
    "first_delayed_resolvent_forcing_enclosed_nonzero",
    "first_nonzero_delayed_forcing_picard_tile_validated",
    "uncorrected_per_branch_output_diagonal_tile_mass_upper_computed",
    "tight_picard_failure_frontier_registered",
    "adaptive_dyadic_subdivision_rule_registered",
    "remaining_tile_counts_registered",
)
FALSE_FLAGS = (
    "coarse_boundary_box_promoted_to_sharp_transfer_bound",
    "tight_picard_sweep_reaches_tau0_without_failure",
    "all_theta_bands_tiled",
    "all_elapsed_tiles_to_return_window_validated",
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


def _load_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a Stage-3B parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _matrix_width_upper(matrix: Any) -> gmpy2.mpfr:
    return max(value.width_upper() for row in matrix for value in row)


def _symmetric_matrix(radius: gmpy2.mpfr) -> Any:
    box = _symmetric(radius)
    return ((box, box), (box, box))


def _delayed_matrix(coefficient: DirectedInterval) -> Any:
    zero = _zero()
    return ((coefficient, zero), (zero, zero))


def _tile_digest(rows: Sequence[Mapping[str, str]]) -> str:
    return canonical_sha256(list(rows))


def _decimal_tile_bounds(index: int, width: Decimal, upper: Decimal) -> tuple[Decimal, Decimal]:
    lower = min(width * index, upper)
    finish = min(width * (index + 1), upper)
    return lower, finish


def _remaining_count(length: gmpy2.mpfr, width: Decimal) -> int:
    width_interval = DirectedInterval.from_decimal(str(width), PRECISION_BITS)
    if width_interval.lower <= 0:
        raise ValueError("a Stage-3B tile width must be positive")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        number = length / width_interval.lower
    return int(gmpy2.ceil(number))


def _nominal_global_remaining_tile_count(
    *,
    base: Any,
    exact_period: DirectedInterval,
    elapsed_frontier_upper: gmpy2.mpfr,
    total_theta_bands: int,
    preboundary_tile_count: int,
) -> int:
    """Count the fixed coarse queue before tau1 faces and adaptive children."""

    theta_width = Decimal("0.001")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        history_lower = -base.parameters["tau_1"].upper
    total = 0
    for theta_index in range(total_theta_bands):
        rational_lower = DirectedInterval.from_decimal(
            str(-theta_width * Decimal(theta_index + 1)), PRECISION_BITS
        ).lower
        theta_lower = max(history_lower, rational_lower)
        for delay_id in ("tau_0", "tau_1"):
            with gmpy2.context(
                precision=PRECISION_BITS, round=gmpy2.RoundDown
            ):
                injection_lower = (
                    theta_lower + base.parameters[delay_id].lower
                )
            with gmpy2.context(
                precision=PRECISION_BITS, round=gmpy2.RoundUp
            ):
                latest_elapsed = exact_period.upper - injection_lower
                post_length = max(
                    gmpy2.mpfr(0),
                    latest_elapsed - elapsed_frontier_upper,
                )
            post_count = _remaining_count(
                post_length, Decimal(COARSE_ELAPSED_TILE_WIDTH)
            )
            if theta_index == 0:
                total += post_count
            else:
                # Preboundary cells, one directed tau0 strip, and the first
                # nonzero-forcing crossing cell are all unvalidated.
                total += preboundary_tile_count + 2 + post_count
    return total


@dataclass(frozen=True)
class BranchFrontierSweep:
    injection_delay_id: str
    theta_band: dict[str, str]
    injection_time_band: dict[str, str]
    coarse_preboundary_tile_count: int
    coarse_tile_ledger_sha256: str
    accumulated_logarithmic_exponent_upper: str
    homogeneous_boundary_growth_upper: str
    tau0_uncertainty_width_upper: str
    uncertainty_predecessor_growth_upper: str
    uncertainty_bridge_growth_upper: str
    boundary_density_inf_norm_upper: str
    tight_picard_accepted_tile_count: int
    tight_picard_accepted_path_expansion_sum_upper: str
    tight_picard_failed_attempt_path_expansion_upper: str
    tight_picard_failure_tile_index: int
    tight_picard_failure_elapsed_cell: dict[str, str]
    tight_picard_failure_endpoint_norm_upper: str
    tight_picard_failure_endpoint_width_upper: str
    tight_picard_failure_coefficient_inf_norm_upper: str
    failure_step_norm_minimum_dyadic_depth: int
    failure_step_norm_child_width_upper: str
    first_delayed_crossing_elapsed_cell: dict[str, str]
    first_delayed_current_coefficient_matrix: Any
    first_delayed_coefficient_matrix: Any
    first_delayed_resolvent_path_matrix: Any
    first_delayed_forcing_matrix: Any
    first_delayed_forcing_inf_norm_lower_witness: str
    first_delayed_forcing_inf_norm_upper: str
    coarse_boundary_matrix: Any
    delayed_crossing_invariant_path_matrix: Any
    delayed_crossing_endpoint_matrix: Any
    delayed_crossing_path_expansion_upper: str
    delayed_crossing_endpoint_norm_upper: str
    delayed_crossing_endpoint_density_vector: Any
    delayed_crossing_endpoint_density_inf_norm_upper: str
    delayed_crossing_path_density_inf_norm_upper: str
    uncorrected_output_diagonal_tile_mass_upper: str
    elapsed_frontier_upper: str
    remaining_elapsed_tiles_to_latest_return: int
    first_nonzero_delayed_forcing_tile_validated: bool
    coarse_bridge_not_usable_as_shadow_transfer_error: bool


@dataclass(frozen=True)
class ContinuousKernelStage3BFrontier:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    binary_blas_thread_count: int
    parent_result_sha256: dict[str, str]
    exact_orbit_radius: str
    theta_band_width: str
    coarse_elapsed_tile_width: str
    delayed_crossing_tile_width: str
    branch_sweeps: tuple[BranchFrontierSweep, ...]
    adaptive_subdivision_rule: dict[str, Any]
    global_frontier: dict[str, Any]
    claim_status: dict[str, bool]
    conclusion: str


def _coefficient_cell(
    *,
    base: Any,
    exact_period: DirectedInterval,
    radius: DirectedInterval,
    physical_time: DirectedInterval,
) -> tuple[DirectedInterval, Any, gmpy2.mpfr, gmpy2.mpfr]:
    voltage = _exact_voltage_box(base, physical_time, exact_period, radius)
    matrix = _current_matrix(voltage, base.parameters)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        mu = max(matrix[0][0].upper + gmpy2.mpfr(1), gmpy2.mpfr(0))
    return voltage, matrix, mu, _matrix_inf_norm_upper(matrix)


def _build_branch_sweep(
    *,
    delay_id: str,
    injection_delay: DirectedInterval,
    theta: DirectedInterval,
    base: Any,
    exact_period: DirectedInterval,
    radius: DirectedInterval,
) -> BranchFrontierSweep:
    tau0 = base.parameters["tau_0"]
    coarse_width = Decimal(COARSE_ELAPSED_TILE_WIDTH)
    pre_upper = Decimal(str(tau0.lower))
    tile_count = _remaining_count(tau0.lower, coarse_width)
    injection_time = theta + injection_delay
    ledger: list[dict[str, str]] = []
    with gmpy2.context(precision=PRECISION_BITS):
        exponent = gmpy2.mpfr(0)
        limit = gmpy2.mpfr(TIGHT_ENDPOINT_NORM_LIMIT)
    tight_current = _identity()
    tight_accepted = 0
    tight_accepted_expansions: list[gmpy2.mpfr] = []
    tight_failure_expansion: gmpy2.mpfr | None = None
    failure_index: int | None = None
    failure_cell: DirectedInterval | None = None
    failure_norm: gmpy2.mpfr | None = None
    failure_width: gmpy2.mpfr | None = None
    failure_coefficient_norm: gmpy2.mpfr | None = None
    failure_step_upper: gmpy2.mpfr | None = None
    for index in range(tile_count):
        lower_decimal, upper_decimal = _decimal_tile_bounds(
            index, coarse_width, pre_upper
        )
        lower_point = DirectedInterval.from_decimal(
            str(lower_decimal), PRECISION_BITS
        )
        if index + 1 == tile_count:
            upper_point = DirectedInterval.from_bounds(
                tau0.lower, tau0.lower, PRECISION_BITS
            )
        else:
            upper_point = DirectedInterval.from_decimal(
                str(upper_decimal), PRECISION_BITS
            )
        elapsed_cell = DirectedInterval.from_bounds(
            lower_point.lower, upper_point.upper, PRECISION_BITS
        )
        step = upper_point - lower_point
        physical_time = injection_time + elapsed_cell
        _, coefficient, mu, coefficient_norm = _coefficient_cell(
            base=base,
            exact_period=exact_period,
            radius=radius,
            physical_time=physical_time,
        )
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            contribution = mu * step.upper
            exponent += contribution
        ledger.append(
            {
                "index": str(index),
                "elapsed_lower": decimal_lower(elapsed_cell.lower, 50),
                "elapsed_upper": decimal_upper(elapsed_cell.upper, 50),
                "mu_infinity_upper": decimal_upper(mu, 50),
                "coefficient_inf_norm_upper": decimal_upper(coefficient_norm, 50),
                "log_growth_contribution_upper": decimal_upper(contribution, 50),
            }
        )
        if failure_index is None:
            path, endpoint, expansion, endpoint_norm = directed_picard_matrix_step(
                current_matrix=tight_current,
                current_coefficient=coefficient,
                delayed_forcing=_zero_matrix(),
                step=step,
            )
            endpoint_width = _matrix_width_upper(endpoint)
            if endpoint_norm > limit or endpoint_width > limit:
                failure_index = index
                failure_cell = elapsed_cell
                failure_norm = endpoint_norm
                failure_width = endpoint_width
                failure_coefficient_norm = coefficient_norm
                failure_step_upper = step.upper
                tight_failure_expansion = expansion
            else:
                tight_current = endpoint
                tight_accepted += 1
                tight_accepted_expansions.append(expansion)
    if failure_index is None:
        raise AssertionError("the registered coarse tight-Picard frontier disappeared")
    assert (
        failure_cell is not None
        and failure_norm is not None
        and failure_width is not None
        and failure_coefficient_norm is not None
        and failure_step_upper is not None
        and tight_failure_expansion is not None
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        scaled_step_norm = (
            gmpy2.mpfr(32) * failure_step_upper * failure_coefficient_norm
        )
        dyadic_depth = 0
        while scaled_step_norm > 1:
            scaled_step_norm /= 2
            dyadic_depth += 1
        child_width = failure_step_upper / (gmpy2.mpfr(2) ** dyadic_depth)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        growth_to_lower = gmpy2.exp(exponent)
    delay_width = tau0.width_upper()
    # Across the tiny directed uncertainty strip some parameter realizations
    # have already activated B_0.  Bound that forcing by b_max*exp(mu*h).
    uncertainty_time = injection_time + DirectedInterval.from_bounds(
        tau0.lower, tau0.upper, PRECISION_BITS
    )
    _, _, uncertainty_mu, _ = _coefficient_cell(
        base=base,
        exact_period=exact_period,
        radius=radius,
        physical_time=uncertainty_time,
    )
    delayed_time_uncertainty = uncertainty_time - tau0
    delayed_voltage_uncertainty = _exact_voltage_box(
        base, delayed_time_uncertainty, exact_period, radius
    )
    b_uncertainty = _delayed_injection_coefficient(
        delayed_voltage_uncertainty, base.parameters
    )
    uncertainty_predecessor_elapsed = DirectedInterval.from_bounds(
        0, delay_width, PRECISION_BITS
    )
    uncertainty_predecessor_time = (
        injection_time + uncertainty_predecessor_elapsed
    )
    _, _, uncertainty_predecessor_mu, _ = _coefficient_cell(
        base=base,
        exact_period=exact_period,
        radius=radius,
        physical_time=uncertainty_predecessor_time,
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        uncertainty_predecessor_growth = gmpy2.exp(
            uncertainty_predecessor_mu * delay_width
        )
        bridge_growth = (
            growth_to_lower
            + delay_width
            * b_uncertainty.upper_abs()
            * uncertainty_predecessor_growth
        ) * gmpy2.exp(uncertainty_mu * delay_width)

    injection_voltage = _exact_voltage_box(base, theta, exact_period, radius)
    injection_coefficient = _delayed_injection_coefficient(
        injection_voltage, base.parameters
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        boundary_density = bridge_growth * injection_coefficient.upper_abs()

    crossing_width = DirectedInterval.from_decimal(
        DELAY_CROSSING_TILE_WIDTH, PRECISION_BITS
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        crossing_elapsed_upper = tau0.upper + crossing_width.upper
        early_elapsed_upper = crossing_width.upper + delay_width
    crossing_elapsed = DirectedInterval.from_bounds(
        tau0.upper, crossing_elapsed_upper, PRECISION_BITS
    )
    crossing_physical_time = injection_time + crossing_elapsed
    _, crossing_a, _, _ = _coefficient_cell(
        base=base,
        exact_period=exact_period,
        radius=radius,
        physical_time=crossing_physical_time,
    )
    delayed_physical_time = crossing_physical_time - tau0
    delayed_voltage = _exact_voltage_box(
        base, delayed_physical_time, exact_period, radius
    )
    delayed_coefficient = _delayed_injection_coefficient(
        delayed_voltage, base.parameters
    )
    b_matrix = _delayed_matrix(delayed_coefficient)

    early_elapsed = DirectedInterval.from_bounds(
        0, early_elapsed_upper, PRECISION_BITS
    )
    early_physical_time = injection_time + early_elapsed
    _, early_a, _, _ = _coefficient_cell(
        base=base,
        exact_period=exact_period,
        radius=radius,
        physical_time=early_physical_time,
    )
    early_path, _, _, _ = directed_picard_matrix_step(
        current_matrix=_identity(),
        current_coefficient=early_a,
        delayed_forcing=_zero_matrix(),
        step=early_elapsed,
    )
    forcing = _matrix_multiply(b_matrix, early_path)
    forcing_upper = _matrix_inf_norm_upper(forcing)
    forcing_lower_witness = forcing[0][0].lower_abs()
    if forcing_lower_witness <= 0:
        raise ArithmeticError("the first delayed forcing lost its nonzero witness")

    boundary_matrix = _symmetric_matrix(bridge_growth)
    crossing_path, crossing_endpoint, crossing_expansion, crossing_norm = (
        directed_picard_matrix_step(
            current_matrix=boundary_matrix,
            current_coefficient=crossing_a,
            delayed_forcing=forcing,
            step=crossing_width,
        )
    )
    endpoint_density = _matvec(
        crossing_endpoint, (injection_coefficient, _zero())
    )
    endpoint_density_norm = max(value.upper_abs() for value in endpoint_density)
    path_density = _matvec(
        crossing_path, (injection_coefficient, _zero())
    )
    path_density_norm = max(value.upper_abs() for value in path_density)
    theta_width = theta.width_upper()
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        theta_tv = theta_width * path_density_norm
        elapsed_frontier = tau0.upper + crossing_width.upper
        accepted_expansion_sum = gmpy2.mpfr(0)
        for expansion in tight_accepted_expansions:
            accepted_expansion_sum += expansion
        latest_elapsed = exact_period.upper - injection_time.lower
        remaining_length = max(latest_elapsed - elapsed_frontier, gmpy2.mpfr(0))
    return BranchFrontierSweep(
        injection_delay_id=delay_id,
        theta_band=_interval_record(theta),
        injection_time_band=_interval_record(injection_time),
        coarse_preboundary_tile_count=tile_count,
        coarse_tile_ledger_sha256=_tile_digest(ledger),
        accumulated_logarithmic_exponent_upper=decimal_upper(exponent, 60),
        homogeneous_boundary_growth_upper=decimal_upper(growth_to_lower, 60),
        tau0_uncertainty_width_upper=decimal_upper(delay_width, 60),
        uncertainty_predecessor_growth_upper=decimal_upper(
            uncertainty_predecessor_growth, 60
        ),
        uncertainty_bridge_growth_upper=decimal_upper(bridge_growth, 60),
        boundary_density_inf_norm_upper=decimal_upper(boundary_density, 60),
        tight_picard_accepted_tile_count=tight_accepted,
        tight_picard_accepted_path_expansion_sum_upper=decimal_upper(
            accepted_expansion_sum, 60
        ),
        tight_picard_failed_attempt_path_expansion_upper=decimal_upper(
            tight_failure_expansion, 60
        ),
        tight_picard_failure_tile_index=failure_index,
        tight_picard_failure_elapsed_cell=_interval_record(failure_cell),
        tight_picard_failure_endpoint_norm_upper=decimal_upper(failure_norm, 60),
        tight_picard_failure_endpoint_width_upper=decimal_upper(failure_width, 60),
        tight_picard_failure_coefficient_inf_norm_upper=decimal_upper(
            failure_coefficient_norm, 60
        ),
        failure_step_norm_minimum_dyadic_depth=dyadic_depth,
        failure_step_norm_child_width_upper=decimal_upper(child_width, 60),
        first_delayed_crossing_elapsed_cell=_interval_record(crossing_elapsed),
        first_delayed_current_coefficient_matrix=_matrix_record(crossing_a),
        first_delayed_coefficient_matrix=_matrix_record(b_matrix),
        first_delayed_resolvent_path_matrix=_matrix_record(early_path),
        first_delayed_forcing_matrix=_matrix_record(forcing),
        first_delayed_forcing_inf_norm_lower_witness=decimal_lower(
            forcing_lower_witness, 60
        ),
        first_delayed_forcing_inf_norm_upper=decimal_upper(forcing_upper, 60),
        coarse_boundary_matrix=_matrix_record(boundary_matrix),
        delayed_crossing_invariant_path_matrix=_matrix_record(crossing_path),
        delayed_crossing_endpoint_matrix=_matrix_record(crossing_endpoint),
        delayed_crossing_path_expansion_upper=decimal_upper(
            crossing_expansion, 60
        ),
        delayed_crossing_endpoint_norm_upper=decimal_upper(crossing_norm, 60),
        delayed_crossing_endpoint_density_vector=_vector_record(
            endpoint_density
        ),
        delayed_crossing_endpoint_density_inf_norm_upper=decimal_upper(
            endpoint_density_norm, 60
        ),
        delayed_crossing_path_density_inf_norm_upper=decimal_upper(
            path_density_norm, 60
        ),
        uncorrected_output_diagonal_tile_mass_upper=decimal_upper(theta_tv, 60),
        elapsed_frontier_upper=decimal_upper(elapsed_frontier, 60),
        remaining_elapsed_tiles_to_latest_return=_remaining_count(
            remaining_length, coarse_width
        ),
        first_nonzero_delayed_forcing_tile_validated=True,
        coarse_bridge_not_usable_as_shadow_transfer_error=True,
    )


def build_continuous_kernel_stage3b_frontier(
    repository: Path,
) -> ContinuousKernelStage3BFrontier:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3B requires OPENBLAS_NUM_THREADS=1")
    stage3 = _load_parent(
        repository, STAGE3_RESULT_RELATIVE_PATH, STAGE3_RESULT_SHA256
    )
    stage3_certificate = _mapping(stage3.get("certificate"), "Stage-3 certificate")
    if stage3_certificate.get("exact_orbit_radius") != EXACT_ORBIT_RADIUS:
        raise ValueError("the Stage-3 exact-orbit radius changed")
    if any(
        shard.get("interval_picard_endpoint_validated") is not True
        for shard in stage3_certificate.get("injection_shards", [])
    ):
        raise ValueError("a Stage-3 initial injection shard is absent")
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    radius = DirectedInterval.from_decimal(EXACT_ORBIT_RADIUS, PRECISION_BITS)
    exact_period = DirectedInterval.symmetric_radius(
        orbit.period, radius.upper, PRECISION_BITS
    )
    theta = DirectedInterval.from_bounds(THETA_LOWER, THETA_UPPER, PRECISION_BITS)
    branches = tuple(
        _build_branch_sweep(
            delay_id=delay_id,
            injection_delay=base.parameters[delay_id],
            theta=theta,
            base=base,
            exact_period=exact_period,
            radius=radius,
        )
        for delay_id in ("tau_0", "tau_1")
    )
    theta_width = theta.width_upper()
    total_theta_bands = _remaining_count(
        base.parameters["tau_1"].upper, Decimal("0.001")
    )
    crossing_width = DirectedInterval.from_decimal(
        DELAY_CROSSING_TILE_WIDTH, PRECISION_BITS
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        elapsed_frontier_upper = (
            base.parameters["tau_0"].upper + crossing_width.upper
        )
    nominal_remaining_tiles = _nominal_global_remaining_tile_count(
        base=base,
        exact_period=exact_period,
        elapsed_frontier_upper=elapsed_frontier_upper,
        total_theta_bands=total_theta_bands,
        preboundary_tile_count=branches[0].coarse_preboundary_tile_count,
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return ContinuousKernelStage3BFrontier(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=1,
        parent_result_sha256={
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        exact_orbit_radius=EXACT_ORBIT_RADIUS,
        theta_band_width=decimal_upper(theta_width, 60),
        coarse_elapsed_tile_width=COARSE_ELAPSED_TILE_WIDTH,
        delayed_crossing_tile_width=DELAY_CROSSING_TILE_WIDTH,
        branch_sweeps=branches,
        adaptive_subdivision_rule={
            "trigger": (
                "bisect a tile whenever endpoint inf norm or maximum entry "
                "width exceeds 1e6; a theorem-quality run must use a much "
                "smaller target tied to the remaining 0.873 linear margin"
            ),
            "coefficient_condition": "h*||A||_infinity <= 1/32",
            "path_condition": (
                "Picard path expansion <= max(1,||X_in||_infinity)/32"
            ),
            "theta_condition": (
                "bisect theta until the exact-voltage cell width is <=1e-3"
            ),
            "delay_alignment": (
                "force tile faces at u=tau0 and u=tau1; never let a cell "
                "straddle a newly active delayed predecessor without an "
                "explicit uncertainty bridge"
            ),
            "predecessor_rule": (
                "every nonzero delayed forcing may reference only an already "
                "validated shard digest at elapsed coordinate u-tau_j"
            ),
            "failure_is_not_rejection": (
                "the coarse box remains rigorous; failure means only that its "
                "width cannot contribute to E_voltage/E_recovery"
            ),
        },
        global_frontier={
            "validated_theta_band_count": 1,
            "total_theta_band_count_at_width_1e_minus_3": total_theta_bands,
            "remaining_theta_band_count": total_theta_bands - 1,
            "unstarted_branch_theta_chain_count": 2 * (total_theta_bands - 1),
            "current_band_remaining_elapsed_tile_count": sum(
                branch.remaining_elapsed_tiles_to_latest_return
                for branch in branches
            ),
            "nominal_coarse_remaining_2d_tile_count_before_tau1_alignment": (
                nominal_remaining_tiles
            ),
            "tau1_alignment_and_adaptive_child_tiles_not_in_nominal_count": True,
            "both_branches_cross_tau0": True,
            "returned_time_window_reached": False,
            "phase_subtracted_tv_complete": False,
            "voltage_shadow_transfer_error_upper": None,
            "recovery_shadow_transfer_error_upper": None,
            "phase_chart_shadow_transfer_error_upper": None,
            "stage2_linear_gate_re_evaluated": False,
            "single_remaining_linear_inequality": (
                "max(Qv_shadow+E_voltage,Qw_shadow+E_recovery)<1"
            ),
        },
        claim_status=claims,
        conclusion=(
            "both injection branches now cross the first delayed-resolvent "
            "boundary with a rigorously nonzero forcing tile; coarse growth "
            "boxes expose, rather than hide, the wrapping frontier, so global "
            "shadow-transfer errors and C0 contraction remain open"
        ),
    )


def build_continuous_kernel_stage3b_frontier_result(
    repository: Path,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_continuous_kernel_stage3b_frontier(repository)),
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


def validate_continuous_kernel_stage3b_frontier_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3B frontier schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3B certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3B manifest")
    if set(certificate) != {field.name for field in fields(ContinuousKernelStage3BFrontier)}:
        raise ValueError("the Stage-3B frontier fields changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3B frontier digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3B source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3B source set changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3B source changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "Stage-3B claim ledger")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the Stage-3B claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a validated Stage-3B frontier fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3B global claim was promoted")
    sweeps = certificate.get("branch_sweeps")
    if not isinstance(sweeps, list) or [row.get("injection_delay_id") for row in sweeps] != [
        "tau_0",
        "tau_1",
    ]:
        raise ValueError("the two Stage-3B branch sweeps changed")
    for sweep in sweeps:
        if sweep.get("first_nonzero_delayed_forcing_tile_validated") is not True:
            raise ValueError("a Stage-3B branch did not cross nonzero forcing")
        forcing_lower = gmpy2.mpq(
            str(sweep["first_delayed_forcing_inf_norm_lower_witness"])
        )
        forcing_upper = gmpy2.mpq(
            str(sweep["first_delayed_forcing_inf_norm_upper"])
        )
        if forcing_lower <= 0 or forcing_upper < forcing_lower:
            raise ValueError("a Stage-3B delayed forcing witness vanished")
        if sweep.get("coarse_bridge_not_usable_as_shadow_transfer_error") is not True:
            raise ValueError("a coarse Stage-3B bridge was promoted")
        failure_index = sweep.get("tight_picard_failure_tile_index")
        if failure_index < 0:
            raise ValueError("the Stage-3B tight frontier is absent")
        if sweep.get("tight_picard_accepted_tile_count") != failure_index:
            raise ValueError("the Stage-3B tight frontier is not contiguous")
        if sweep.get("failure_step_norm_minimum_dyadic_depth") < 1:
            raise ValueError("the Stage-3B adaptive split depth vanished")
        if gmpy2.mpq(
            str(sweep["uncertainty_predecessor_growth_upper"])
        ) < 1:
            raise ValueError("the Stage-3B uncertainty bridge is incomplete")
        if gmpy2.mpq(
            str(sweep["uncorrected_output_diagonal_tile_mass_upper"])
        ) <= 0:
            raise ValueError("the Stage-3B local density mass vanished")
        if sweep.get("remaining_elapsed_tiles_to_latest_return") <= 0:
            raise ValueError("the Stage-3B remaining elapsed frontier vanished")
    frontier = _mapping(certificate.get("global_frontier"), "Stage-3B global frontier")
    if frontier.get("both_branches_cross_tau0") is not True:
        raise ValueError("the Stage-3B delayed boundary crossing changed")
    if frontier.get("returned_time_window_reached") is not False:
        raise ValueError("the Stage-3B frontier was promoted to the return window")
    if frontier.get("remaining_theta_band_count") != 11180:
        raise ValueError("the Stage-3B remaining theta frontier changed")
    if frontier.get("unstarted_branch_theta_chain_count") != 22360:
        raise ValueError("the Stage-3B branch-theta queue changed")
    if frontier.get("current_band_remaining_elapsed_tile_count") != sum(
        sweep["remaining_elapsed_tiles_to_latest_return"] for sweep in sweeps
    ):
        raise ValueError("the Stage-3B current-band queue changed")
    if (
        frontier.get(
            "nominal_coarse_remaining_2d_tile_count_before_tau1_alignment"
        )
        <= frontier.get("unstarted_branch_theta_chain_count")
    ):
        raise ValueError("the Stage-3B nominal coarse queue vanished")
    if (
        frontier.get(
            "tau1_alignment_and_adaptive_child_tiles_not_in_nominal_count"
        )
        is not True
    ):
        raise ValueError("the Stage-3B refinement-count caveat vanished")
    if any(
        frontier.get(name) is not None
        for name in (
            "voltage_shadow_transfer_error_upper",
            "recovery_shadow_transfer_error_upper",
            "phase_chart_shadow_transfer_error_upper",
        )
    ):
        raise ValueError("a Stage-3B transfer error was invented")
    expected = json.loads(
        json.dumps(
            asdict(build_continuous_kernel_stage3b_frontier(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3B frontier differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_continuous_kernel_stage3b_frontier",
    "build_continuous_kernel_stage3b_frontier_result",
    "canonical_sha256",
    "validate_continuous_kernel_stage3b_frontier_result",
]
