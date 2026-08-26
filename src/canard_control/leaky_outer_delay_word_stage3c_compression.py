"""Stage-3C finite delay-word compression for the outer return kernel.

This module replaces the nominal two-dimensional method-of-steps queue by
the exact finite Volterra delay-word expansion on the one-return window.  It
proves the combinatorial truncation with outward MPFR arithmetic and records
binary64 low-rank/sign-front diagnostics from four independently rebuilt
finite sections.  The latter select a small Bernstein/Chebyshev proof
architecture; they are not promoted to continuous-history estimates.

No continuous path integral is enclosed here.  Consequently E_v, E_w and
E_phase remain null and every C0-contraction or attraction flag remains
false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import itertools
import json
import math
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
from canard_control.leaky_outer_continuous_kernel_stage3_shard import (
    _build_leaky_base_sequences,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_phase_fixed_return_stage1 import (
    _periodic_interpolator,
)
from canard_control.leaky_pulse_separator_candidate import finite_section


SCHEMA_ID = "leaky-outer-delay-word-stage3c-compression-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_delay_word_stage3c_compression.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_delay_word_stage3c_compression.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_delay_word_stage3c_compression.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-delay-word-stage3c-compression.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_delay_word_stage3c_compression.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_continuous_kernel_stage3_shard.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_phase_fixed_return_stage1.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_delay_word_stage3c_compression.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR delay, exact-period-ball, horizon and delay-word "
    "feasibility arithmetic; exact parent/source binding; binary64 finite-"
    "section SVD and sign-front calculations are diagnostics only"
)

STAGE2_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_signed_kernel_stage2.json"
)
STAGE2_RESULT_SHA256 = (
    "f4742db560c5de29072adfb0b963d5a21e993fed5a949a2180dcc6d0b355011f"
)
STAGE3B_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_continuous_kernel_stage3b_frontier.json"
)
STAGE3B_RESULT_SHA256 = (
    "9c87609472b6ba9149bf53a0c4917a4581cd535d22ea3536b16b070a81317855"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
PULSE_ATTACHMENT_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_outer_third_return_enclosure.json"
)
PULSE_ATTACHMENT_RESULT_SHA256 = (
    "7a01c2a8ec6b5421c090836f4962e595027d78be3381d490c4b6eb56d3beb13d"
)

PRECISION_BITS = 160
PINNED_OPENBLAS_NUM_THREADS = "1"
EXACT_ORBIT_RADIUS = "1e-8"
FINITE_SECTION_STEPS = (120, 180, 240, 360)
PHYSICAL_PADDING_CELL_COUNT = 4
SUPPORT_FACE_WINDOW = ("-9.2", "-8.45")
INTERIOR_ZERO_WINDOW = ("-1.2", "-0.85")

TRUE_FLAGS = (
    "stage2_signed_kernel_parent_validated",
    "stage3b_frontier_parent_validated",
    "exact_period_and_delay_intervals_rebuilt",
    "finite_volterra_delay_word_identity_registered",
    "all_globally_possible_history_delay_words_enumerated",
    "all_globally_possible_recovery_scalar_delay_words_enumerated",
    "all_omitted_longer_words_excluded_by_directed_delay_sum",
    "million_cell_queue_replaced_by_finite_word_proof_architecture",
    "phase_subtraction_prescribed_before_word_summation_and_total_variation",
    "duffy_simplex_parameterization_registered",
    "binary_resolution_ladder_low_rank_diagnostic_recomputed",
    "binary_resolution_ladder_sign_front_diagnostic_recomputed",
    "strict_remaining_linear_and_phase_error_budgets_computed",
    "minimal_remaining_directed_integral_gap_registered",
)
FALSE_FLAGS = (
    "binary_low_rank_pilot_promoted_to_continuous_kernel",
    "binary_sign_front_pilot_promoted_to_continuous_sign_theorem",
    "delay_word_path_integrals_directedly_enclosed",
    "continuous_density_total_variation_validated",
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
        raise ValueError(f"a Stage-3C parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _binary64_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("binary64 diagnostic must be finite")
    return {"binary64_hex": number.hex(), "decimal": format(number, ".17g")}


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower, 60),
        "upper": decimal_upper(value.upper, 60),
    }


def _word_id(word: Sequence[int]) -> str:
    return "empty" if not word else "".join(str(index) for index in word)


def _word_delay(
    word: Sequence[int], delays: Mapping[int, DirectedInterval]
) -> DirectedInterval:
    total = DirectedInterval.from_decimal(0, PRECISION_BITS)
    for index in word:
        total = total + delays[index]
    return total


def _possible_words(
    horizon: DirectedInterval, delays: Mapping[int, DirectedInterval]
) -> tuple[tuple[int, ...], ...]:
    """Enumerate every word not uniformly excluded on a horizon.

    A word can contribute only where its cumulative delay is strictly less
    than the elapsed horizon.  Inclusion uses the safe condition
    ``delay.lower < horizon.upper``; equality/uncertainty would retain rather
    than discard a word.
    """

    words: list[tuple[int, ...]] = []
    for length in range(3):
        for word in itertools.product((0, 1), repeat=length):
            delay = _word_delay(word, delays)
            if delay.lower < horizon.upper:
                words.append(word)
    return tuple(words)


@dataclass(frozen=True)
class DelayWordBranch:
    input_id: str
    maximum_elapsed_horizon: dict[str, str]
    possible_word_ids: tuple[str, ...]
    possible_word_delay_intervals: tuple[dict[str, str], ...]
    possible_word_count: int
    maximum_word_length: int
    three_minimum_delays_exceed_horizon_margin_lower: str
    complete_finite_word_list_validated: bool


@dataclass(frozen=True)
class ShadowCompressionDiagnostic:
    step_count: int
    physical_step_binary64: dict[str, str]
    physical_history_input_count: int
    returned_output_row_count: int
    largest_singular_value_binary64: dict[str, str]
    second_to_first_singular_ratio_binary64: dict[str, str]
    frobenius_tail_to_first_singular_ratio_binary64: dict[str, str]
    rank_one_max_row_l1_residual_binary64: dict[str, str]
    phase_fixed_max_row_l1_binary64: dict[str, str]
    rank_one_row_residual_ratio_binary64: dict[str, str]
    maximum_sign_change_count: int
    every_sign_change_inside_two_declared_windows: bool
    normalized_sign_template_on_three_safe_regions: tuple[int, int, int]
    normalized_sign_template_common_to_every_output_row: bool
    diagnostic_only: bool


@dataclass(frozen=True)
class OuterDelayWordStage3CCompression:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    binary_blas_thread_count: int
    parent_result_sha256: dict[str, str]
    exact_orbit_radius: str
    exact_period_interval: dict[str, str]
    exact_delay_intervals: dict[str, dict[str, str]]
    returned_output_window: dict[str, dict[str, str]]
    causal_volterra_identity: dict[str, str]
    history_density_word_branches: tuple[DelayWordBranch, ...]
    recovery_scalar_word_branch: DelayWordBranch
    history_density_word_term_count: int
    recovery_scalar_word_term_count: int
    total_phase_fixed_word_term_count: int
    stage3b_nominal_coarse_tile_count: int
    nominal_tile_to_word_term_ratio_lower: str
    phase_fixed_word_formula: dict[str, str]
    tensor_validation_contract: dict[str, Any]
    shadow_compression_diagnostics: tuple[ShadowCompressionDiagnostic, ...]
    shadow_sign_windows: dict[str, dict[str, str]]
    strict_transfer_error_budget: dict[str, str]
    minimum_remaining_gap: dict[str, Any]
    claim_status: dict[str, bool]
    conclusion: str


def _branch_record(
    input_id: str,
    horizon: DirectedInterval,
    delays: Mapping[int, DirectedInterval],
) -> DelayWordBranch:
    words = _possible_words(horizon, delays)
    three_tau0 = delays[0] * 3
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        margin = three_tau0.lower - horizon.upper
    if margin <= 0:
        raise ArithmeticError("three minimum delays do not exclude longer words")
    return DelayWordBranch(
        input_id=input_id,
        maximum_elapsed_horizon=_interval_record(horizon),
        possible_word_ids=tuple(_word_id(word) for word in words),
        possible_word_delay_intervals=tuple(
            _interval_record(_word_delay(word, delays)) for word in words
        ),
        possible_word_count=len(words),
        maximum_word_length=max(len(word) for word in words),
        three_minimum_delays_exceed_horizon_margin_lower=decimal_lower(margin, 60),
        complete_finite_word_list_validated=True,
    )


def _safe_region_signs(
    theta: np.ndarray, values: np.ndarray
) -> tuple[int, int, int]:
    support_lower, support_upper = map(float, SUPPORT_FACE_WINDOW)
    zero_lower, zero_upper = map(float, INTERIOR_ZERO_WINDOW)
    masks = (
        theta <= support_lower,
        (theta >= support_upper) & (theta <= zero_lower),
        theta >= zero_upper,
    )
    raw: list[int] = []
    for mask in masks:
        signs = np.unique(np.sign(values[mask]))
        signs = signs[signs != 0]
        if len(signs) != 1:
            raise ArithmeticError("a binary safe region lost sign coherence")
        raw.append(int(signs[0]))
    orientation = raw[0]
    return tuple(int(sign // orientation) for sign in raw)  # type: ignore[return-value]


def _shadow_diagnostic(orbit: Any, step_count: int) -> ShadowCompressionDiagnostic:
    section = finite_section(orbit, step_count)
    _, voltage_derivative = _periodic_interpolator(
        orbit.state[:, 0], orbit.period
    )
    _, recovery_derivative = _periodic_interpolator(
        orbit.state[:, 1], orbit.period
    )
    history_steps = section.history_steps
    tangent = np.asarray(
        [
            voltage_derivative((index - history_steps) * section.step)
            for index in range(history_steps + 1)
        ]
        + [recovery_derivative(0.0)],
        dtype=float,
    )
    phase_speed = float(tangent[history_steps])
    if not phase_speed > 0:
        raise ArithmeticError("the binary phase row lost transversality")
    phase_row = np.zeros(len(tangent), dtype=float)
    phase_row[history_steps] = 1.0 / phase_speed
    corrected = (
        np.eye(len(tangent), dtype=float) - np.outer(tangent, phase_row)
    ) @ section.matrix
    history_inputs = np.arange(PHYSICAL_PADDING_CELL_COUNT, history_steps)
    returned_outputs = np.r_[
        np.arange(PHYSICAL_PADDING_CELL_COUNT, history_steps),
        history_steps + 1,
    ]
    retained_inputs = np.r_[history_inputs, history_steps + 1]
    matrix = corrected[np.ix_(returned_outputs, retained_inputs)]
    left, singular_values, right = np.linalg.svd(matrix, full_matrices=False)
    rank_one = singular_values[0] * np.outer(left[:, 0], right[0])
    residual = matrix - rank_one
    row_residual = float(np.max(np.sum(np.abs(residual), axis=1)))
    row_norm = float(np.max(np.sum(np.abs(matrix), axis=1)))
    if not row_norm > 0:
        raise ArithmeticError("the binary corrected matrix vanished")

    theta = (history_inputs - history_steps) * section.step
    support_lower, support_upper = map(float, SUPPORT_FACE_WINDOW)
    zero_lower, zero_upper = map(float, INTERIOR_ZERO_WINDOW)
    templates: set[tuple[int, int, int]] = set()
    max_changes = 0
    all_changes_inside = True
    for output in returned_outputs:
        values = corrected[output, history_inputs]
        changes = np.flatnonzero(np.sign(values[1:]) != np.sign(values[:-1]))
        max_changes = max(max_changes, len(changes))
        change_theta = 0.5 * (theta[changes] + theta[changes + 1])
        for location in change_theta:
            inside = (
                support_lower <= location <= support_upper
                or zero_lower <= location <= zero_upper
            )
            all_changes_inside = bool(all_changes_inside and bool(inside))
        templates.add(_safe_region_signs(theta, values))
    if not all_changes_inside:
        raise ArithmeticError("a binary sign front escaped the declared windows")
    if templates != {(1, -1, 1)}:
        raise ArithmeticError("the binary normalized sign template changed")

    with np.errstate(over="raise", invalid="raise", divide="raise"):
        second_ratio = float(singular_values[1] / singular_values[0])
        frobenius_tail = float(
            np.linalg.norm(singular_values[1:]) / singular_values[0]
        )
        residual_ratio = row_residual / row_norm
    return ShadowCompressionDiagnostic(
        step_count=step_count,
        physical_step_binary64=_binary64_record(section.step),
        physical_history_input_count=len(history_inputs),
        returned_output_row_count=len(returned_outputs),
        largest_singular_value_binary64=_binary64_record(singular_values[0]),
        second_to_first_singular_ratio_binary64=_binary64_record(second_ratio),
        frobenius_tail_to_first_singular_ratio_binary64=_binary64_record(
            frobenius_tail
        ),
        rank_one_max_row_l1_residual_binary64=_binary64_record(row_residual),
        phase_fixed_max_row_l1_binary64=_binary64_record(row_norm),
        rank_one_row_residual_ratio_binary64=_binary64_record(residual_ratio),
        maximum_sign_change_count=max_changes,
        every_sign_change_inside_two_declared_windows=all_changes_inside,
        normalized_sign_template_on_three_safe_regions=(1, -1, 1),
        normalized_sign_template_common_to_every_output_row=True,
        diagnostic_only=True,
    )


def _strict_budget(
    stage2: Mapping[str, Any], attachment: Mapping[str, Any]
) -> dict[str, str]:
    stage2_certificate = _mapping(stage2.get("certificate"), "Stage-2 certificate")
    attach_certificate = _mapping(
        attachment.get("certificate"), "pulse attachment certificate"
    )
    qv = gmpy2.mpq(str(stage2_certificate["directed_voltage_shadow_norm_upper"]))
    qw = gmpy2.mpq(str(stage2_certificate["directed_recovery_shadow_norm_upper"]))
    qp = gmpy2.mpq(str(stage2_certificate["directed_phase_chart_shadow_norm_upper"]))
    history_ball = _mapping(
        attach_certificate.get("history_ball"), "pulse attachment history ball"
    )
    distance = gmpy2.mpq(str(history_ball["complete_history_distance_upper"]))
    section_radius = gmpy2.mpq("1/10000")
    voltage_slack = gmpy2.mpq(1) - qv
    recovery_slack = gmpy2.mpq(1) - qw
    phase_total_ceiling = section_radius / distance
    phase_error_slack = phase_total_ceiling - qp
    if min(voltage_slack, recovery_slack, phase_error_slack) <= 0:
        raise ArithmeticError("a strict Stage-3C transfer budget disappeared")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        voltage_slack_lower = gmpy2.mpfr(voltage_slack)
        recovery_slack_lower = gmpy2.mpfr(recovery_slack)
        phase_total_lower = gmpy2.mpfr(phase_total_ceiling)
        phase_error_lower = gmpy2.mpfr(phase_error_slack)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        distance_upper = gmpy2.mpfr(distance)
    return {
        "required_voltage_error_inequality": "E_voltage < 1-Qv_shadow",
        "voltage_error_strict_ceiling": decimal_lower(voltage_slack_lower, 60),
        "required_recovery_error_inequality": "E_recovery < 1-Qw_shadow",
        "recovery_error_strict_ceiling": decimal_lower(recovery_slack_lower, 60),
        "pulse_complete_history_distance_upper": decimal_upper(distance_upper, 60),
        "chosen_section_radius": "0.0001",
        "phase_chart_total_norm_strict_ceiling": decimal_lower(
            phase_total_lower, 60
        ),
        "required_phase_error_inequality": (
            "E_phase < r_section/d_pulse-Qphase_shadow"
        ),
        "phase_error_strict_ceiling": decimal_lower(phase_error_lower, 60),
    }


def build_outer_delay_word_stage3c_compression(
    repository: Path,
) -> OuterDelayWordStage3CCompression:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3C requires OPENBLAS_NUM_THREADS=1")
    stage2 = _load_parent(
        repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256
    )
    stage3b = _load_parent(
        repository, STAGE3B_RESULT_RELATIVE_PATH, STAGE3B_RESULT_SHA256
    )
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    attachment = _load_parent(
        repository,
        PULSE_ATTACHMENT_RESULT_RELATIVE_PATH,
        PULSE_ATTACHMENT_RESULT_SHA256,
    )
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    radius = DirectedInterval.from_decimal(EXACT_ORBIT_RADIUS, PRECISION_BITS)
    exact_period = DirectedInterval.symmetric_radius(
        orbit.period, radius.upper, PRECISION_BITS
    )
    tau0 = base.parameters["tau_0"]
    tau1 = base.parameters["tau_1"]
    delays = {0: tau0, 1: tau1}
    # The tau_j injection exists only for theta in [-tau_j,0].  Thus
    # s=theta+tau_j is nonnegative for both branches, and both maximum
    # elapsed horizons equal the return period.
    horizon_tau0 = exact_period
    horizon_tau1 = exact_period
    history_branches = (
        _branch_record("history_injection_tau_0", horizon_tau0, delays),
        _branch_record("history_injection_tau_1", horizon_tau1, delays),
    )
    scalar_branch = _branch_record(
        "initial_recovery_scalar_at_time_zero", exact_period, delays
    )
    expected_tau0 = ("empty", "0", "1", "00", "01", "10", "11")
    expected_tau1 = ("empty", "0", "1", "00", "01", "10", "11")
    if history_branches[0].possible_word_ids != expected_tau0:
        raise ArithmeticError("the tau0-injection delay-word list changed")
    if history_branches[1].possible_word_ids != expected_tau1:
        raise ArithmeticError("the tau1-injection delay-word list changed")
    if scalar_branch.possible_word_ids != expected_tau1:
        raise ArithmeticError("the recovery-scalar delay-word list changed")

    stage3b_certificate = _mapping(
        stage3b.get("certificate"), "Stage-3B certificate"
    )
    frontier = _mapping(
        stage3b_certificate.get("global_frontier"), "Stage-3B global frontier"
    )
    nominal_tiles = int(
        frontier["nominal_coarse_remaining_2d_tile_count_before_tau1_alignment"]
    )
    history_terms = sum(branch.possible_word_count for branch in history_branches)
    scalar_terms = scalar_branch.possible_word_count
    total_terms = history_terms + scalar_terms
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        compression_ratio = gmpy2.mpfr(nominal_tiles) / total_terms
    diagnostics = tuple(
        _shadow_diagnostic(orbit, step_count)
        for step_count in FINITE_SECTION_STEPS
    )
    budget = _strict_budget(stage2, attachment)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})

    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    returned_lower = exact_period - tau1
    return OuterDelayWordStage3CCompression(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=1,
        parent_result_sha256={
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            STAGE3B_RESULT_RELATIVE_PATH: STAGE3B_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
            PULSE_ATTACHMENT_RESULT_RELATIVE_PATH: (
                PULSE_ATTACHMENT_RESULT_SHA256
            ),
        },
        exact_orbit_radius=EXACT_ORBIT_RADIUS,
        exact_period_interval=_interval_record(exact_period),
        exact_delay_intervals={
            "tau_0": _interval_record(tau0),
            "tau_1": _interval_record(tau1),
        },
        returned_output_window={
            "lower": _interval_record(returned_lower),
            "upper": _interval_record(exact_period),
            "relative_lower": _interval_record(-tau1),
            "relative_upper": _interval_record(zero),
        },
        causal_volterra_identity={
            "current_fundamental_matrix": (
                "Phi_t=A(t)Phi, Phi(s,s)=I"
            ),
            "resolvent": (
                "R(t,s)=Phi(t,s)+sum_j integral_[s+tau_j,t] "
                "Phi(t,r) B_j(r) R(r-tau_j,s) dr"
            ),
            "truncation_reason": (
                "each history branch is supported only on theta>=-tau_j, so "
                "its injection time is nonnegative; every recursive delayed "
                "factor consumes at least tau_0 and three*tau_0 exceeds T"
            ),
        },
        history_density_word_branches=history_branches,
        recovery_scalar_word_branch=scalar_branch,
        history_density_word_term_count=history_terms,
        recovery_scalar_word_term_count=scalar_terms,
        total_phase_fixed_word_term_count=total_terms,
        stage3b_nominal_coarse_tile_count=nominal_tiles,
        nominal_tile_to_word_term_ratio_lower=decimal_lower(
            compression_ratio, 60
        ),
        phase_fixed_word_formula={
            "history_density": (
                "sum_j sum_word R_word(t,theta+tau_j) "
                "B_j(theta+tau_j)e_v"
            ),
            "voltage_phase_subtraction": (
                "apply e_v^T[R_word(T+sigma,s)-"
                "q_v(sigma)R_word(T,s)/q_v(0)] to every word, then sum"
            ),
            "recovery_phase_subtraction": (
                "apply e_w^T R_word(T,s)-"
                "q_w(0)e_v^T R_word(T,s)/q_v(0), then sum"
            ),
            "ordering_guard": (
                "sum signed branch/word contributions and perform phase "
                "subtraction before absolute value or total variation"
            ),
        },
        tensor_validation_contract={
            "path_domain": (
                "for word (j1,...,jm), nested ordered times obey "
                "s+sum(tau_jk)<=r_m<=...<=r_1<=t"
            ),
            "duffy_map": (
                "map each ordered simplex to [0,1]^m with a triangular "
                "Duffy transform; retain its polynomial Jacobian exactly"
            ),
            "coefficient_representation": (
                "evaluate exact Fourier orbit plus the 1e-8 Wiener ball; "
                "enclose Phi and every word integrand by directed "
                "Chebyshev-to-Bernstein coefficients"
            ),
            "activation_faces": (
                "split only at theta=-tau_0 and at affine faces "
                "t-(theta+tau_j)=sum(word delays); no uniform 1e-3 theta grid"
            ),
            "signed_tv_strategy": (
                "validate the normalized +,-,+ sign template outside the "
                "two registered zero windows; integrate signed polynomials "
                "there and pay absolute Bernstein mass only inside windows"
            ),
            "scalar_column": (
                "validate seven recovery-input word terms on the same output "
                "blocks; no theta dimension is present"
            ),
            "required_outputs": (
                "direct Q_v,Q_w,Q_phase bounds or directed quadrature errors "
                "E_voltage,E_recovery,E_phase satisfying the strict budget"
            ),
        },
        shadow_compression_diagnostics=diagnostics,
        shadow_sign_windows={
            "tau0_support_face_window": {
                "lower": SUPPORT_FACE_WINDOW[0],
                "upper": SUPPORT_FACE_WINDOW[1],
                "status": "binary guide only",
            },
            "interior_zero_window": {
                "lower": INTERIOR_ZERO_WINDOW[0],
                "upper": INTERIOR_ZERO_WINDOW[1],
                "status": "binary guide only",
            },
            "safe_region_normalized_template": {
                "left": "+1",
                "middle": "-1",
                "right": "+1",
                "status": "binary guide only",
            },
        },
        strict_transfer_error_budget=budget,
        minimum_remaining_gap={
            "single_mathematical_gap": (
                "a source-bound directed Bernstein enclosure of the 21 "
                "finite delay-word terms, with phase subtraction before "
                "absolute integration"
            ),
            "history_word_terms": history_terms,
            "recovery_scalar_word_terms": scalar_terms,
            "maximum_nested_integral_dimension": 2,
            "all_length_three_words_excluded": True,
            "binary_sign_statement_is_not_input": True,
            "continuous_sign_or_window_mass_still_required": True,
            "continuous_transfer_errors": {
                "E_voltage": None,
                "E_recovery": None,
                "E_phase": None,
            },
            "linear_gate_re_evaluated": False,
            "phase_entry_gate_re_evaluated": False,
        },
        claim_status=claims,
        conclusion=(
            "the million-cell frontier is not intrinsic: the exact one-return "
            "kernel has only 14 history delay-word terms and seven recovery-"
            "scalar terms, of nested dimension at most two; the remaining "
            "directed path-integral enclosure is finite but not yet supplied, "
            "so C0 contraction and outer attraction remain open"
        ),
    )


def build_outer_delay_word_stage3c_compression_result(
    repository: Path,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_delay_word_stage3c_compression(repository)),
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


def validate_outer_delay_word_stage3c_compression_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3C schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3C certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3C manifest")
    if set(certificate) != {
        field.name for field in fields(OuterDelayWordStage3CCompression)
    }:
        raise ValueError("the Stage-3C certificate fields changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the Stage-3C manifest schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the Stage-3C result path changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3C certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3C source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3C source set changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3C source changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "Stage-3C claim ledger")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the Stage-3C claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-3C fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3C claim was promoted")
    branches = certificate.get("history_density_word_branches")
    if not isinstance(branches, list) or len(branches) != 2:
        raise ValueError("the Stage-3C history branches changed")
    if branches[0].get("possible_word_ids") != [
        "empty", "0", "1", "00", "01", "10", "11"
    ]:
        raise ValueError("the tau0 history word list changed")
    if branches[1].get("possible_word_ids") != [
        "empty", "0", "1", "00", "01", "10", "11"
    ]:
        raise ValueError("the tau1 history word list changed")
    if certificate.get("history_density_word_term_count") != 14:
        raise ValueError("the Stage-3C history term count changed")
    if certificate.get("recovery_scalar_word_term_count") != 7:
        raise ValueError("the Stage-3C scalar term count changed")
    if certificate.get("total_phase_fixed_word_term_count") != 21:
        raise ValueError("the Stage-3C total term count changed")
    if gmpy2.mpq(str(certificate["nominal_tile_to_word_term_ratio_lower"])) <= 40000:
        raise ValueError("the Stage-3C analytic compression vanished")
    diagnostics = certificate.get("shadow_compression_diagnostics")
    if not isinstance(diagnostics, list) or [
        row.get("step_count") for row in diagnostics
    ] != list(FINITE_SECTION_STEPS):
        raise ValueError("the Stage-3C resolution ladder changed")
    for row in diagnostics:
        if row.get("diagnostic_only") is not True:
            raise ValueError("a binary Stage-3C guide was promoted")
        if row.get("every_sign_change_inside_two_declared_windows") is not True:
            raise ValueError("a binary Stage-3C sign front escaped")
        if row.get("normalized_sign_template_on_three_safe_regions") != [1, -1, 1]:
            raise ValueError("the binary Stage-3C sign template changed")
        ratio = float.fromhex(
            row["rank_one_row_residual_ratio_binary64"]["binary64_hex"]
        )
        if not 0 < ratio < 0.001:
            raise ValueError("the Stage-3C rank-one diagnostic changed")
    gap = _mapping(certificate.get("minimum_remaining_gap"), "Stage-3C gap")
    errors = _mapping(gap.get("continuous_transfer_errors"), "Stage-3C errors")
    if set(errors) != {"E_voltage", "E_recovery", "E_phase"}:
        raise ValueError("the Stage-3C transfer fields changed")
    if any(value is not None for value in errors.values()):
        raise ValueError("a Stage-3C continuous transfer error was invented")
    if gap.get("linear_gate_re_evaluated") is not False:
        raise ValueError("the Stage-3C linear gate was promoted")
    if gap.get("phase_entry_gate_re_evaluated") is not False:
        raise ValueError("the Stage-3C phase-entry gate was promoted")
    expected = json.loads(
        json.dumps(
            asdict(build_outer_delay_word_stage3c_compression(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3C certificate differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_outer_delay_word_stage3c_compression",
    "build_outer_delay_word_stage3c_compression_result",
    "canonical_sha256",
    "validate_outer_delay_word_stage3c_compression_result",
]
