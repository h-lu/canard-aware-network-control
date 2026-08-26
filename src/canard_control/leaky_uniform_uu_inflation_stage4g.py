"""Stage-4G audit of the radius-0.0017 ``C_s^{uu}`` inflation gate.

Stage 4E proves the correlated stable-output bound only at the periodic base
orbit.  This module asks the next logically smaller question: can that bound
be inflated over the proposed split ball by a direct complete-history
mean-flow majorant?

The answer for the scalar ``P``-logarithmic-norm route is no.  The calculation
below is nevertheless directed and useful: it propagates the difference of
two exact RFDE solutions on the same 1042-cell physical-time grid as Stage 4E,
uses the exact delay translations by 512 and 640 cells, and solves the
current-cell radius inequality self-consistently.  It records the first cell
on which this majorant no longer fits the validated local section ball.  No
mesh spread is used as an error estimate.

This is a *route-failure certificate*, not a proof that a sharper signed
propagator cannot close.  In particular it does not provide the third
variation, event-time jet, moving eigencovector, or a uniform ``C_s^{uu}``
bound.  Those claims stay false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from fractions import Fraction
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Iterable, Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.floquet_cover_arithmetic import _box_distance_split_upper
from canard_control.leaky_floquet_inner_unstable_root import (
    _dependency_fingerprint,
    _prepare_cached,
)
from canard_control.leaky_pulse_quiet_capture import (
    _current_log_norm_upper,
    _delayed_forcing_upper,
    _gronwall_endpoint,
    _p_box_norm_upper,
    _p_constants,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    DELAY_GRID_DIVISOR,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH as STAGE4E_RESULT_RELATIVE_PATH,
    SCALAR_TRANSCRIPTION_GUARD,
    _delay,
    _directed_taylor,
    _directed_taylor_tail_upper,
    _enlarge_real,
    _orbit_dictionary,
    _real_part_bernstein_range,
    _validation_trim,
    canonical_sha256,
    validate_stage4e_result,
)


SCHEMA_ID = "leaky-uniform-uu-inflation-stage4g-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_uniform_uu_inflation_stage4g.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_uniform_uu_inflation_stage4g.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_uniform_uu_inflation_stage4g.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-uniform-uu-inflation-stage4g.md"
TEST_RELATIVE_PATH = "tests/test_leaky_uniform_uu_inflation_stage4g.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_uniform_uu_inflation_stage4g.py"
)
ARITHMETIC_SCOPE = (
    "exact Stage-4E parent-byte binding; exact-rational target-budget "
    "arithmetic; 192-bit outward MPFR complete-history RFDE mean-flow "
    "majorant on the Stage-4E 1042-cell physical grid; exact 512/640-cell "
    "delay translations; self-consistent current-cell P-radius closure; "
    "route-failure only, with no third-variation, event-jet, moving q/f, "
    "uniform Hessian block, stable graph, separator, or onset promotion"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/floquet_cover_arithmetic.py",
    "src/canard_control/leaky_floquet_inner_unstable_root.py",
    "src/canard_control/leaky_pulse_quiet_capture.py",
    "src/canard_control/leaky_quiet_history_basin.py",
    "src/canard_control/leaky_shared_yqq_deflation_stage4e.py",
)

STAGE4E_RESULT_SHA256 = (
    "ccdd6023f911e97785ec6f8be97b84d725d6af9f5051e1da602380d225e47acc"
)
TARGET = Fraction(12, 1)
SPLIT_RADIUS = Fraction(17, 10_000)
LOCAL_SECTION_RADIUS = Fraction(1, 100)
CURRENT_CELL_INFLATION = Fraction(1_000_000_000_001, 1_000_000_000_000)

TRUE_FLAGS = (
    "stage4e_base_orbit_bound_source_bound",
    "exact_uniform_inflation_budget_computed",
    "full_history_lipschitz_error_decomposition_registered",
    "directed_scalar_mean_flow_attempt_completed",
    "both_physical_delays_cell_aligned",
    "self_consistent_current_cell_radius_validated",
    "scalar_route_first_failure_frozen",
    "signed_finite_delay_word_replacement_identified",
)
FALSE_FLAGS = (
    "scalar_p_log_norm_route_closes_local_return_tube",
    "complete_history_base_state_small_tube_validated",
    "third_variation_correlated_p_tube_validated",
    "uniform_uq_vqq_variation_validated",
    "uniform_event_time_variation_validated",
    "moving_q_covector_variation_validated",
    "moving_f_covector_variation_validated",
    "moving_fq_normalization_excludes_zero_validated",
    "uniform_split_ball_stable_output_uu_below_twelve_validated",
    "other_five_projected_return_hessian_blocks_validated",
    "six_projected_return_hessian_blocks_validated",
    "stable_power_constant_numeric_upper_validated",
    "split_return_tube_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "graph_radius_1p7e_minus_3_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage4GArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    exact_radius_budget: dict[str, object]
    full_history_lipschitz_decomposition: dict[str, object]
    directed_scalar_mean_flow_attempt: dict[str, object]
    frozen_minimal_failure: dict[str, object]
    downstream_status: dict[str, object]
    claim_status: dict[str, bool]


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _lower_text(value: gmpy2.mpfr, digits: int = 64) -> str:
    return decimal_lower(value, digits)


def _upper_text(value: gmpy2.mpfr, digits: int = 64) -> str:
    return decimal_upper(value, digits)


def _fraction_interval(value: Fraction) -> DirectedInterval:
    return (
        DirectedInterval.from_decimal(value.numerator, PRECISION_BITS)
        / value.denominator
    )


def _load_stage4e(repository: Path) -> Mapping[str, object]:
    path = repository / STAGE4E_RESULT_RELATIVE_PATH
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != STAGE4E_RESULT_SHA256:
        raise ValueError("the bound Stage-4E result changed")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError("the Stage-4E parent is malformed")
    validate_stage4e_result(payload, repository)
    return payload


def _exact_budget(stage4e: Mapping[str, object]) -> dict[str, object]:
    artifact = stage4e.get("artifact")
    if not isinstance(artifact, Mapping):
        raise ValueError("the Stage-4E artifact is missing")
    base = artifact.get("base_orbit_stable_output_uu")
    if not isinstance(base, Mapping):
        raise ValueError("the Stage-4E base bound is missing")
    base_text = str(base.get("normalized_stable_output_uu_upper"))
    base_upper = Fraction(base_text)
    if base_upper >= TARGET:
        raise ArithmeticError("the Stage-4E base upper no longer leaves a budget")
    increment = TARGET - base_upper
    cap = increment / SPLIT_RADIUS
    cap_interval = _fraction_interval(cap)
    increment_interval = _fraction_interval(increment)
    return {
        "stage4e_base_orbit_stable_output_uu_upper": base_text,
        "uniform_target": str(TARGET),
        "split_ball_radius": "0.0017",
        "guaranteed_increment_budget_lower": _lower_text(
            increment_interval.lower
        ),
        "required_lipschitz_cap_exact_fraction": (
            f"{cap.numerator}/{cap.denominator}"
        ),
        "required_lipschitz_cap_lower": _lower_text(cap_interval.lower),
        "required_lipschitz_cap_upper": _upper_text(cap_interval.upper),
        "sufficient_gate": (
            "if sup_{||x||_split<=0.0017} Lip_x(C_s^uu) is strictly "
            "below the registered cap, then "
            "C_s^uu(x)<=C_s,base^uu+0.0017*Lip_x(C_s^uu)<12"
        ),
        "cap_is_a_sufficient_threshold_not_a_validated_bound": True,
    }


def _orbit_error_upper(prepared: object, orbit_v: Mapping[tuple[int, int], complex]) -> float:
    total = 0.0
    for mode, interval in prepared.base.voltage.items():
        total += float(
            _box_distance_split_upper(
                interval, orbit_v.get((0, int(mode)), 0.0j)
            )
        )
    return (
        total
        + float(prepared.period_radius)
        + SCALAR_TRANSCRIPTION_GUARD
    )


def _directed_rows_digest(rows: Iterable[Mapping[str, object]]) -> str:
    serial: list[dict[str, object]] = []
    for row in rows:
        converted: dict[str, object] = {}
        for key, value in sorted(row.items()):
            if isinstance(value, gmpy2.mpfr):
                converted[key] = _upper_text(value)
            else:
                converted[key] = value
        serial.append(converted)
    return canonical_sha256(serial)


def _base_orbit_ranges(
    orbit_v: Mapping[tuple[int, int], complex],
    period_value: float,
    tau0_value: float,
    tau1_value: float,
    root_value: float,
    orbit_error: gmpy2.mpfr,
) -> tuple[
    tuple[tuple[DirectedInterval, DirectedInterval, DirectedInterval], ...],
    DirectedInterval,
    int,
]:
    precision = PRECISION_BITS
    period = DirectedInterval.from_float(period_value, precision)
    root = DirectedInterval.from_float(root_value, precision)
    regular_step = (
        DirectedInterval.from_float(tau0_value, precision)
        / DELAY_GRID_DIVISOR
    )
    regular_step_float = tau0_value / DELAY_GRID_DIVISOR
    full_count = int(math.floor(period_value / regular_step_float))
    if not full_count * regular_step_float < period_value:
        raise ArithmeticError("the Stage-4G final short cell disappeared")
    cell_count = full_count + 1
    dictionaries = (
        orbit_v,
        _delay(orbit_v, tau0_value, period_value, root_value),
        _delay(orbit_v, tau1_value, period_value, root_value),
    )
    trimmed = tuple(
        _validation_trim(dictionary, root_value, precision)
        for dictionary in dictionaries
    )
    rows: list[tuple[DirectedInterval, DirectedInterval, DirectedInterval]] = []
    for index in range(cell_count):
        left = regular_step * index
        local_step = (
            regular_step if index < cell_count - 1 else period - left
        )
        ranges: list[DirectedInterval] = []
        for dictionary, omitted in trimmed:
            polynomial = _directed_taylor(
                dictionary, left, local_step, period, root
            )
            value_range = _real_part_bernstein_range(polynomial)
            analytic_tail = _directed_taylor_tail_upper(
                dictionary, local_step, period, root
            )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                radius = orbit_error + analytic_tail + omitted
            ranges.append(_enlarge_real(value_range, radius))
        rows.append((ranges[0], ranges[1], ranges[2]))
    return tuple(rows), regular_step, cell_count


def _directed_scalar_mean_flow(repository: Path) -> dict[str, object]:
    """Propagate the direct nonlinear mean-flow ``P`` majorant.

    If ``e=X-X_0``, the cubic RFDE difference is written exactly as a
    mean-value linear equation along ``X_0+s e``.  The current coefficient is
    enclosed on the base-orbit voltage range enlarged by the current-cell
    voltage radius.  Each delayed coefficient is enclosed on its delayed
    base-orbit range enlarged by the already available source-cell voltage
    radius.  Thus the only fixed point is the current-cell maximum radius.
    """

    repository = repository.resolve()
    prepared, _ = _prepare_cached(
        str(repository), _dependency_fingerprint(repository)
    )
    period_value = float(prepared.orbit.period)
    # Every orbit dictionary key has growth index zero.  Hence the real
    # Floquet exponent is algebraically absent from all range evaluations;
    # passing zero makes that independence explicit.
    root_value = 0.0
    tau0_value, tau1_value = (
        float(value) for value in prepared.orbit.parameters.physical_delays
    )
    regular_step_float = tau0_value / DELAY_GRID_DIVISOR
    if tau1_value != regular_step_float * 640:
        raise ArithmeticError("the tau1=640h binary alignment changed")
    if tau0_value != regular_step_float * 512:
        raise ArithmeticError("the tau0=512h binary alignment changed")

    orbit_v = _orbit_dictionary(prepared.orbit.state, 0)
    orbit_error = gmpy2.mpfr(
        _orbit_error_upper(prepared, orbit_v), PRECISION_BITS
    )
    base_ranges, regular_step, cell_count = _base_orbit_ranges(
        orbit_v,
        period_value,
        tau0_value,
        tau1_value,
        root_value,
        orbit_error,
    )
    radius_y = _fraction_interval(SPLIT_RADIUS).upper
    initial_p_radius = _p_box_norm_upper(
        radius_y, radius_y, PRECISION_BITS
    )
    voltage_coordinate_factor = _p_constants(PRECISION_BITS)[0]
    local_ball = _fraction_interval(LOCAL_SECTION_RADIUS).lower
    inflation = _fraction_interval(CURRENT_CELL_INFLATION).upper
    period = DirectedInterval.from_float(period_value, PRECISION_BITS)

    rows: list[dict[str, object]] = []
    previous_endpoint = initial_p_radius
    first_local_ball_failure: dict[str, object] | None = None
    maximum_fixed_point_iterations = 0
    for index in range(cell_count):
        left = regular_step * index
        local_step = (
            regular_step if index < cell_count - 1 else period - left
        )
        source0_voltage = (
            radius_y
            if index < 512
            else voltage_coordinate_factor
            * rows[index - 512]["maximum_p_radius_upper"]
        )
        source1_voltage = (
            radius_y
            if index < 640
            else voltage_coordinate_factor
            * rows[index - 640]["maximum_p_radius_upper"]
        )
        if not isinstance(source0_voltage, gmpy2.mpfr) or not isinstance(
            source1_voltage, gmpy2.mpfr
        ):
            raise TypeError("a delayed mean-flow source lost its MPFR radius")
        current_base, delayed0_base, delayed1_base = base_ranges[index]
        delayed0_range = _enlarge_real(delayed0_base, source0_voltage)
        delayed1_range = _enlarge_real(delayed1_base, source1_voltage)
        delay0_gain = _delayed_forcing_upper(
            delayed0_range, PRECISION_BITS
        )
        delay1_gain = _delayed_forcing_upper(
            delayed1_range, PRECISION_BITS
        )
        with gmpy2.context(
            precision=PRECISION_BITS, round=gmpy2.RoundUp
        ):
            forcing = (
                delay0_gain * source0_voltage
                + delay1_gain * source1_voltage
            )

        candidate = previous_endpoint
        endpoint = previous_endpoint
        logarithmic_norm = gmpy2.mpfr(0, PRECISION_BITS)
        for iteration in range(1, 201):
            current_voltage_radius = voltage_coordinate_factor * candidate
            current_range = _enlarge_real(
                current_base, current_voltage_radius
            )
            logarithmic_norm = _current_log_norm_upper(
                current_range, PRECISION_BITS
            )
            endpoint = _gronwall_endpoint(
                previous_endpoint,
                forcing,
                logarithmic_norm,
                local_step.upper,
                PRECISION_BITS,
            )
            new_candidate = max(previous_endpoint, endpoint)
            if new_candidate <= candidate:
                maximum_fixed_point_iterations = max(
                    maximum_fixed_point_iterations, iteration
                )
                break
            with gmpy2.context(
                precision=PRECISION_BITS, round=gmpy2.RoundUp
            ):
                candidate = new_candidate * inflation
        else:
            raise ArithmeticError(
                f"the scalar mean-flow cell {index} did not self-close"
            )
        if endpoint > candidate:
            raise ArithmeticError("a scalar mean-flow cell lost closure")
        voltage_radius = voltage_coordinate_factor * candidate
        row: dict[str, object] = {
            "cell_index": index,
            "start_p_radius_upper": previous_endpoint,
            "endpoint_p_radius_upper": endpoint,
            "maximum_p_radius_upper": candidate,
            "voltage_coordinate_radius_upper": voltage_radius,
            "source0_voltage_radius_upper": source0_voltage,
            "source1_voltage_radius_upper": source1_voltage,
            "delay0_gain_upper": delay0_gain,
            "delay1_gain_upper": delay1_gain,
            "logarithmic_norm_upper": logarithmic_norm,
            "current_cell_self_closes": True,
        }
        rows.append(row)
        if first_local_ball_failure is None and voltage_radius >= local_ball:
            first_local_ball_failure = {
                "cell_index": index,
                "left_time_lower": _lower_text(left.lower),
                "right_time_upper": _upper_text((left + local_step).upper),
                "voltage_coordinate_radius_upper": _upper_text(
                    voltage_radius
                ),
                "local_section_ball_radius": "0.01",
                "interpretation": (
                    "the scalar upper bound, not the exact trajectory, first "
                    "ceases to certify containment in the local ball"
                ),
            }
        previous_endpoint = endpoint

    if first_local_ball_failure is None:
        raise ArithmeticError(
            "the expected scalar-route local-ball failure disappeared"
        )
    worst = max(rows, key=lambda row: row["maximum_p_radius_upper"])
    retained_left = period - DirectedInterval.from_float(
        tau1_value, PRECISION_BITS
    )
    retained_rows = [
        row
        for row in rows
        if (regular_step * (int(row["cell_index"]) + 1)).upper
        >= retained_left.lower
    ]
    retained_maximum = max(
        row["voltage_coordinate_radius_upper"] for row in retained_rows
    )
    return {
        "history_space": "Y=C([-tau_max,0],R) x R",
        "input_relation": "||delta phi||_Y <= ||delta phi||_split <= 0.0017",
        "mean_equation": (
            "dot e=A_bar(t,e)e+B0_bar(t,e_tau0)e_v(t-tau0)"
            "+B1_bar(t,e_tau1)e_v(t-tau1), with each bar the exact "
            "segment mean between the base and perturbed histories"
        ),
        "norm": "P norm on current (voltage,recovery); voltage sup on delayed history",
        "interval_precision_bits": PRECISION_BITS,
        "taylor_degree_inherited_from_stage4e": 24,
        "cell_count": cell_count,
        "tau0_aligned_cell_count": 512,
        "tau1_aligned_cell_count": 640,
        "regular_step_binary64": format(regular_step_float, ".17g"),
        "period_binary64": format(period_value, ".17g"),
        "initial_p_radius_upper": _upper_text(initial_p_radius),
        "p_to_voltage_coordinate_factor_upper": _upper_text(
            voltage_coordinate_factor
        ),
        "orbit_fourier_coefficient_error_upper": _upper_text(orbit_error),
        "all_current_cells_self_closed": True,
        "maximum_fixed_point_iterations": maximum_fixed_point_iterations,
        "maximum_p_radius_upper": _upper_text(
            worst["maximum_p_radius_upper"]
        ),
        "maximum_p_radius_cell_index": int(worst["cell_index"]),
        "maximum_voltage_coordinate_radius_upper": _upper_text(
            worst["voltage_coordinate_radius_upper"]
        ),
        "returned_history_voltage_radius_upper": _upper_text(
            retained_maximum
        ),
        "first_local_ball_failure": first_local_ball_failure,
        "local_return_tube_gate_closes": False,
        "row_digest_sha256": _directed_rows_digest(rows),
        "mesh_spread_used_as_error": False,
    }


def _decomposition() -> dict[str, object]:
    return {
        "objects": {
            "stable_block": (
                "C_s^uu(x)=||G(x)||_Y/||q(x)||_Y^2"
            ),
            "deflated_history": (
                "G(x)=Y_qq(x)-q(x)*alpha(x)"
            ),
            "quotient": (
                "alpha(x)=f_x(Y_qq(x))/f_x(q(x))"
            ),
            "event_corrected_second_history": (
                "Y_qq=V_qq+2*dot(U_q)*tau_q+ddot(X)*tau_q^2"
                "+dot(X)*tau_qq, evaluated on every returned-history theta"
            ),
        },
        "exact_first_difference_identity": (
            "D_x G[h]=D_x Y_qq[h]-D_x q[h]*alpha-q*D_x alpha[h]"
        ),
        "exact_quotient_derivative": (
            "D_x alpha[h]=((D_x f[h])(Y_qq)+f(D_x Y_qq[h]))/f(q)"
            "-f(Y_qq)*((D_x f[h])(q)+f(D_x q[h]))/f(q)^2"
        ),
        "required_lipschitz_pieces": {
            "L_base_flow": (
                "complete-history mean-flow tube for X_x-X_0 on [0,T]"
            ),
            "L_UV": (
                "correlated tubes for D_x U_q[h], D_x V_qq[h], hence the "
                "third variation W_hqq, including moving q inputs"
            ),
            "L_event": (
                "physical-time derivatives D_x tau_q[h] and D_x tau_qq[h] "
                "with a uniform positive event-speed denominator"
            ),
            "L_q": "moving normalized Route-C right history D_x q[h]",
            "L_f": (
                "moving atom-plus-density left covector D_x f[h] in total variation"
            ),
            "L_normalization": (
                "uniform lower bound for |f_x(q(x))| and variation of ||q(x)||_Y^-2"
            ),
        },
        "required_evaluation_order": (
            "form D_x(Y_qq-q*f(Y_qq)/f(q))[h] with shared symbols on every "
            "history cell before taking total variation or a history norm"
        ),
        "independent_triangle_bounds_on_quotient_terms_allowed": False,
        "stage4b_design_targets_used_as_bounds": False,
    }


def build_stage4g_artifact(repository: Path) -> Stage4GArtifact:
    repository = repository.resolve()
    stage4e = _load_stage4e(repository)
    budget = _exact_budget(stage4e)
    mean_flow = _directed_scalar_mean_flow(repository)
    if mean_flow["local_return_tube_gate_closes"] is not False:
        raise ArithmeticError("the Stage-4G route-failure status changed")
    first_failure = mean_flow["first_local_ball_failure"]
    if not isinstance(first_failure, Mapping):
        raise ArithmeticError("the Stage-4G first failure is missing")
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4GArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            STAGE4E_RESULT_RELATIVE_PATH: STAGE4E_RESULT_SHA256
        },
        exact_radius_budget=budget,
        full_history_lipschitz_decomposition=_decomposition(),
        directed_scalar_mean_flow_attempt=mean_flow,
        frozen_minimal_failure={
            "first_unclosed_ingress": (
                "complete-history base-state mean-flow tube inside the "
                "validated radius-0.01 local return domain"
            ),
            "failure_cell_index": first_failure["cell_index"],
            "failure_reason": (
                "the direct scalar P-log-norm majorant loses the local "
                "return-history ball before event and third-variation "
                "denominators can be invoked"
            ),
            "this_does_not_disprove_a_sharper_signed_bound": True,
            "minimal_replacement": (
                "construct the signed current-ODE fundamental propagator and "
                "the finite Volterra delay words, form U(t)P_s and the "
                "unstable contribution with shared q/f symbols, and take "
                "total variation only after the signed sums"
            ),
            "nonzero_forward_delay_words_over_one_period": (
                "empty, (tau0), (tau1), (tau0,tau0)"
            ),
            "word_depth_reason": (
                "2*tau0<T<tau0+tau1<3*tau0, so all other depth-two and "
                "all depth-three delay words vanish on [0,T]"
            ),
            "required_signed_ingress_parent": None,
        },
        downstream_status={
            "validated_complete_history_lipschitz_upper": None,
            "required_lipschitz_cap": budget[
                "required_lipschitz_cap_upper"
            ],
            "uniform_stable_output_uu_upper": None,
            "uniform_stable_output_uu_strictly_below_twelve": False,
            "third_variation_correlated_p_tube": None,
            "uniform_event_speed_lower": None,
            "moving_q_variation_upper": None,
            "moving_f_total_variation_upper": None,
            "moving_fq_modulus_lower": None,
            "other_five_hessian_blocks": None,
            "stable_power_constant_upper": None,
            "split_return_tube_history_radius_upper": None,
            "quantitative_stable_graph": False,
            "physical_pulse_onset": False,
        },
        claim_status=claims,
    )


def build_stage4g_result(repository: Path) -> dict[str, object]:
    repository = repository.resolve()
    artifact = asdict(build_stage4g_artifact(repository))
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
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(
                artifact["parent_result_sha256"]
            ),
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "gmpy2": gmpy2.version(),
                "mpfr": gmpy2.mpfr_version(),
                "mpfr_precision_bits": PRECISION_BITS,
                "openblas_num_threads": os.environ.get(
                    "OPENBLAS_NUM_THREADS"
                ),
                "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
            },
        },
    }


def validate_stage4g_result(
    payload: Mapping[str, object], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "artifact",
        "manifest",
    }:
        raise ValueError("the Stage-4G result has the wrong outer schema")
    artifact = payload.get("artifact")
    manifest = payload.get("manifest")
    if not isinstance(artifact, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the Stage-4G artifact or manifest is missing")
    if set(artifact) != {field.name for field in fields(Stage4GArtifact)}:
        raise ValueError("the Stage-4G artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4G identity changed")
    claims = artifact.get("claim_status")
    if not isinstance(claims, Mapping):
        raise ValueError("the Stage-4G claim ledger is missing")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4G claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4G audit statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4G theorem gate was promoted")

    budget = artifact.get("exact_radius_budget")
    decomposition = artifact.get("full_history_lipschitz_decomposition")
    attempt = artifact.get("directed_scalar_mean_flow_attempt")
    failure = artifact.get("frozen_minimal_failure")
    downstream = artifact.get("downstream_status")
    if not all(
        isinstance(value, Mapping)
        for value in (budget, decomposition, attempt, failure, downstream)
    ):
        raise ValueError("a Stage-4G proof block is missing")
    cap_lower = gmpy2.mpq(str(budget.get("required_lipschitz_cap_lower")))
    cap_upper = gmpy2.mpq(str(budget.get("required_lipschitz_cap_upper")))
    if not gmpy2.mpq(2408) < cap_lower <= cap_upper < gmpy2.mpq(2409):
        raise ValueError("the exact Stage-4G Lipschitz cap changed")
    if (
        decomposition.get("stage4b_design_targets_used_as_bounds") is not False
        or decomposition.get(
            "independent_triangle_bounds_on_quotient_terms_allowed"
        )
        is not False
    ):
        raise ValueError("the Stage-4G correlated decomposition changed")
    if (
        attempt.get("cell_count") != 1042
        or attempt.get("tau0_aligned_cell_count") != 512
        or attempt.get("tau1_aligned_cell_count") != 640
        or attempt.get("all_current_cells_self_closed") is not True
        or attempt.get("mesh_spread_used_as_error") is not False
        or attempt.get("local_return_tube_gate_closes") is not False
    ):
        raise ValueError("the Stage-4G scalar mean-flow audit changed")
    first = attempt.get("first_local_ball_failure")
    if not isinstance(first, Mapping) or int(first.get("cell_index", -1)) < 0:
        raise ValueError("the Stage-4G first failure disappeared")
    if gmpy2.mpq(
        str(first.get("voltage_coordinate_radius_upper"))
    ) <= gmpy2.mpq("0.01"):
        raise ValueError("the Stage-4G local-ball failure is not strict")
    if (
        failure.get("this_does_not_disprove_a_sharper_signed_bound")
        is not True
        or failure.get("required_signed_ingress_parent") is not None
    ):
        raise ValueError("the Stage-4G minimal failure was overclaimed")
    if (
        downstream.get("validated_complete_history_lipschitz_upper")
        is not None
        or downstream.get("uniform_stable_output_uu_upper") is not None
        or downstream.get(
            "uniform_stable_output_uu_strictly_below_twelve"
        )
        is not False
        or downstream.get("quantitative_stable_graph") is not False
        or downstream.get("physical_pulse_onset") is not False
    ):
        raise ValueError("an open Stage-4G downstream gate was promoted")

    expected_parents = {
        STAGE4E_RESULT_RELATIVE_PATH: STAGE4E_RESULT_SHA256
    }
    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "dependency_source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-4G manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": expected_parents,
    }
    if any(manifest.get(key) != value for key, value in fixed.items()):
        raise ValueError("the Stage-4G manifest fixed data changed")
    if artifact.get("parent_result_sha256") != expected_parents:
        raise ValueError("the Stage-4G artifact parent binding changed")
    repository = repository.resolve()
    sources = manifest.get("source_sha256")
    dependencies = manifest.get("dependency_source_sha256")
    if not isinstance(sources, Mapping) or set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4G source set changed")
    if not isinstance(dependencies, Mapping) or set(dependencies) != set(
        DEPENDENCY_SOURCE_MANIFEST
    ):
        raise ValueError("the Stage-4G dependency source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4G source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependencies.get(relative) != _sha256_path(repository / relative):
            raise ValueError(
                f"the Stage-4G dependency source changed: {relative}"
            )
    for relative, digest in expected_parents.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4G parent changed: {relative}")
    _load_stage4e(repository)


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "Stage4GArtifact",
    "TRUE_FLAGS",
    "build_stage4g_artifact",
    "build_stage4g_result",
    "validate_stage4g_result",
]
