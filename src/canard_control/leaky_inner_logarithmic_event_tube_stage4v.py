"""Stage-4V orbit-aware logarithmic-norm event-tube certificate.

The scalar Stage-4U comparison bounds the complete reduced-history
difference by a row-sum maximum over the whole two-period horizon.  This
module replaces that maximum by a time-dependent weighted-energy estimate.
For the current voltage/recovery difference ``(x,y)`` it uses

    z(t)^2 = x(t)^2 + y(t)^2 / epsilon.

The off-diagonal instantaneous terms cancel exactly in the derivative of
``z^2``.  The remaining linear envelope is therefore the orbit-aware
logarithmic rate

    r(t) = max(0, max(a(t),-epsilon) + |b_0(t)| + |b_1(t)|),

where ``a,b_0,b_1`` are the exact-orbit variational coefficients.  Stage-4I
Fourier/Taylor arithmetic is reused to enclose the one-period integral of
``r`` on all 1042 delay-aligned cells.  A first-exit argument adds the exact
polynomial Hessian remainder only as ``H_beta beta/2``.

The result is an explicit selected-event theorem on a scaled preferred
anisotropic ball.  It is not a theorem on the unscaled ball and proves no
self-map, event ordinal, Hessian block, graph, pulse crossing, or onset.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from functools import lru_cache
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    DELAY_GRID_DIVISOR,
    _centre_data,
    _complex_poly_bernstein_upper,
    _directed_taylor,
    _directed_taylor_tail_upper,
    _model_uncertainty,
    _real_part_bernstein_range,
    _validation_trim,
)


SCHEMA_ID = "leaky-inner-logarithmic-event-tube-stage4v-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_two_period_event"
STATUS = "PROVED_ORBIT_AWARE_SCALED_REDUCED_Y_EVENT_TUBE"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_logarithmic_event_tube_stage4v.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_logarithmic_event_tube_stage4v.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_logarithmic_event_tube_stage4v.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-logarithmic-event-tube-stage4v.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_logarithmic_event_tube_stage4v.py"
)

STAGE4S_A_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stage4s_event_tube.json"
)
STAGE4N_FEASIBILITY_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json"
)
STAGE4N_CONTRACT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json"
)
STAGE4M_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_enlarged_return_hessian_stage4m_contract.json"
)
STAGE4I_RELATIVE_PATH = (
    "experiments/results/leaky_inner_word_primitive_stage4i.json"
)
STAGE2_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
STAGE4R_RELATIVE_PATH = (
    "experiments/results/finite_delay_eventually_smooth_selected_return_stage4r.json"
)
STAGE4H_RELATIVE_PATH = (
    "experiments/results/leaky_inner_signed_stable_flow_stage4h.json"
)

PARENT_RESULT_SHA256 = {
    STAGE4S_A_RELATIVE_PATH: (
        "b552c5c6fc8afce53ed047ad8264a9d428351d9f031dc566af60969307a1d91f"
    ),
    STAGE4N_FEASIBILITY_RELATIVE_PATH: (
        "5e7214a2f5ba8ca22649c677a1d054b32342b5cc25966bd8e1da7600c605f1de"
    ),
    STAGE4N_CONTRACT_RELATIVE_PATH: (
        "b64f5230bb870b889fdc341d5d5139ea4ccac6faa7752ff2a5682eb0206cf160"
    ),
    STAGE4M_RELATIVE_PATH: (
        "1a7f89c4c61480a76149b88ae6a15fa40b11425f4d678615af3469b59f75100c"
    ),
    STAGE4I_RELATIVE_PATH: (
        "1248e9d95444f3cc12565c1e11b4bbeab3d4a9a7bb8922893e38b1ffa439f73e"
    ),
    STAGE2_RELATIVE_PATH: (
        "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
    ),
    STAGE4R_RELATIVE_PATH: (
        "4e68835bc3ba5fd44432d98a3b6b1d41506533d66f3353cd500df3e95da76418"
    ),
    STAGE4H_RELATIVE_PATH: (
        "6577a7fcba9888b5126adcd894a361c9436b29a6f619b04f3d54ce5c3218fc15"
    ),
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_shared_yqq_deflation_stage4e.py",
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/"
    "leaky_inner_logarithmic_event_tube_stage4v.py"
)
ARITHMETIC_SCOPE = (
    "exact-byte binding and semantic validation of Stages 4S-A, 4N, 4M, "
    "4I, 2, 4R, and the Stage-4H source-bound warning; 192-bit outward "
    "Taylor--Bernstein enclosure of the "
    "time-dependent weighted-energy logarithmic rate on every one of the "
    "1042 delay-aligned orbit cells; outward two-period plus event-window "
    "integration and exact polynomial Hessian bootstrap; explicit reduced-Y "
    "selected event and C2 hit on a scaled coordinate ball; no preferred "
    "lambda-one ball, self-map, ordinal, Hessian, graph, crossing, onset, "
    "routing, capture, safety, or general-network promotion"
)

PRECISION_BITS = 192
STABLE_RADIUS = "0.0097"
UNSTABLE_RADIUS = "0.00025"
SPLIT_RADIUS = "0.00995"
CERTIFIED_LAMBDA = "1.2e-8"
OPEN_DOMAIN_LAMBDA = "1.25e-8"
EPSILON = "0.2"
KAPPA_3 = "0.005"
EXPECTED_NUMERIC_CORE_SHA256 = (
    "7cda699176730596d1cfc0c1445b14d5f52840aa8a64b8e18d373618bd76ec4e"
)

TRUE_FLAGS = (
    "all_eight_parent_bytes_and_used_semantics_validated",
    "stage4i_delay_aligned_orbit_coefficient_cells_reused",
    "weighted_energy_cross_terms_cancel_exactly",
    "orbit_aware_logarithmic_rate_integral_enclosed_outward",
    "complete_initial_history_translation_retained",
    "polynomial_hessian_remainder_included",
    "first_exit_bootstrap_through_T_plus_validated",
    "explicit_lambda_lower_bound_validated",
    "scaled_ball_includes_arbitrary_continuous_reduced_y_stable_histories",
    "common_fixed_window_endpoint_signs_validated",
    "uniform_positive_event_speed_validated",
    "unique_selected_event_in_fixed_window_validated",
    "complete_returned_y_history_inside_local_patch_validated",
    "ambient_and_coordinate_selected_event_hit_C2_validated",
    "induced_local_section_return_validated",
)
FALSE_FLAGS = (
    "preferred_lambda_one_ball_validated",
    "unscaled_stage4n_nonlinear_tube_validated",
    "same_scaled_ball_self_map_validated",
    "full_x_sup_norm_tube_with_same_y_radius_validated",
    "event_ordinal_validated",
    "no_earlier_admissible_return_validated",
    "Q_equals_P2_validated",
    "six_projected_return_hessian_blocks_validated",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "biological_onset_or_control_validated",
    "two_sided_routing_validated",
    "outer_or_quiet_capture_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_validated",
    "general_network_canard_theorem_validated",
)


@dataclass(frozen=True)
class Stage4VCertificate:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    scaled_domain: dict[str, Any]
    weighted_energy_identity: dict[str, Any]
    directed_orbit_rate_integral: dict[str, Any]
    nonlinear_first_exit_bootstrap: dict[str, Any]
    common_event_and_patch: dict[str, Any]
    regularity_and_return: dict[str, Any]
    preferred_ball_feasibility: dict[str, Any]
    theorem_boundary: dict[str, Any]
    claim_status: dict[str, bool]


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is not a mapping")
    return value


def _point(value: object) -> DirectedInterval:
    return DirectedInterval.from_decimal(str(value), PRECISION_BITS)


def _mpfr_point(value: gmpy2.mpfr) -> DirectedInterval:
    return DirectedInterval.from_bounds(value, value, PRECISION_BITS)


def _exp(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval.from_bounds(lower, upper, PRECISION_BITS)


def _record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower, 80),
        "upper": decimal_upper(value.upper, 80),
    }


def _load_json(repository: Path, relative: str, digest: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != digest:
        raise ValueError(f"the Stage-4V parent bytes changed: {relative}")
    return _mapping(json.loads(path.read_text(encoding="utf-8")), relative)


def _load_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    return {
        relative: _load_json(repository, relative, digest)
        for relative, digest in PARENT_RESULT_SHA256.items()
    }


def _require_claim(
    payload: Mapping[str, Any], name: str, expected: bool, parent: str
) -> None:
    claims = _mapping(payload.get("claim_status"), f"{parent} claims")
    if claims.get(name) is not expected:
        raise ValueError(f"{parent} claim changed: {name}")


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "precision_bits": str(PRECISION_BITS),
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS", ""),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS", ""),
    }


def _numeric_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        name: certificate[name]
        for name in (
            "scaled_domain",
            "weighted_energy_identity",
            "directed_orbit_rate_integral",
            "nonlinear_first_exit_bootstrap",
            "common_event_and_patch",
            "preferred_ball_feasibility",
        )
    }


def _directed_logarithmic_rate_integral(
    repository: Path,
    *,
    true_period_lower: str,
    true_period_upper: str,
    tau_max_upper: str,
    orbit_history_speed_upper: str,
) -> dict[str, Any]:
    """Enclose one exact-orbit phase integral using Stage-4I arithmetic."""

    data = _centre_data(repository)
    precision = PRECISION_BITS
    period = DirectedInterval.from_float(float(data.period), precision)
    root = DirectedInterval.from_float(float(data.root), precision)
    regular_step = (
        DirectedInterval.from_float(float(data.tau0), precision)
        / DELAY_GRID_DIVISOR
    )
    cell_count = int(
        math.ceil(float(data.period) / (float(data.tau0) / DELAY_GRID_DIVISOR))
    )
    dictionaries = []
    for value in (data.current, data.delayed0, data.delayed1):
        dictionaries.append(
            _validation_trim(value, float(data.root), precision)
        )
    uncertainty = _model_uncertainty(data)
    current_error = gmpy2.mpfr(
        uncertainty["current_coefficient_error"], precision
    )
    inherited_delayed_error = gmpy2.mpfr(
        uncertainty["delayed_coefficient_each_error"], precision
    )
    epsilon = DirectedInterval.from_decimal(EPSILON, precision)
    minus_epsilon_upper = (-epsilon).upper
    kappa3 = DirectedInterval.from_decimal(KAPPA_3, precision)

    # The delayed Fourier dictionaries use the binary centre period and
    # binary delay centres.  The exact orbit is compared at the same current
    # phase, so a delayed argument also incurs the true-period/delay phase
    # drift below.  The 1e-8 algebra guard in _model_uncertainty controls
    # rounded dictionary algebra; it is not a substitute for this bridge.
    true_period = DirectedInterval.from_bounds(
        true_period_lower, true_period_upper, precision
    )
    period_drift = (true_period - period).upper_abs()
    tau_binary = (
        DirectedInterval.from_float(float(data.tau0), precision),
        DirectedInterval.from_float(float(data.tau1), precision),
    )
    sqrt_five = DirectedInterval.from_decimal(5, precision).sqrt()
    tau_exact = (4 * sqrt_five, 5 * sqrt_five)
    tau_center_drift = tuple(
        (exact - binary).upper_abs()
        for exact, binary in zip(tau_exact, tau_binary, strict=True)
    )
    maximum_tau_center_drift = max(tau_center_drift)
    tau_max = DirectedInterval.from_decimal(tau_max_upper, precision)
    p_lower = DirectedInterval.from_decimal(true_period_lower, precision)
    orbit_speed = DirectedInterval.from_decimal(
        orbit_history_speed_upper, precision
    )
    period_phase_time_drift = tau_max * _mpfr_point(period_drift) / p_lower
    total_argument_time_drift = (
        period_phase_time_drift + _mpfr_point(maximum_tau_center_drift)
    )
    orbit_voltage_error = DirectedInterval.from_float(
        float(uncertainty["orbit_error"]), precision
    )
    delayed_argument_voltage_error = (
        orbit_voltage_error + orbit_speed * total_argument_time_drift
    )
    voltage_bound = DirectedInterval.from_float(
        float(uncertainty["voltage_bound"]), precision
    )
    delayed_coefficient_slope = 3 * epsilon * kappa3 * (voltage_bound + 1)
    phase_voltage_error = orbit_speed * total_argument_time_drift
    phase_coefficient_error = delayed_coefficient_slope * phase_voltage_error
    delayed_error_interval = (
        DirectedInterval.from_float(float(inherited_delayed_error), precision)
        + phase_coefficient_error
    )
    delayed_error = delayed_error_interval.upper
    integral_upper = gmpy2.mpfr(0, precision)
    rate_maximum = gmpy2.mpfr(0, precision)
    current_upper_maximum = -gmpy2.inf()
    delayed_abs_maximum = [gmpy2.mpfr(0, precision), gmpy2.mpfr(0, precision)]
    tail_maximum = [gmpy2.mpfr(0, precision) for _ in range(3)]

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        for index in range(cell_count):
            left = regular_step * index
            step = (
                regular_step
                if index < cell_count - 1
                else period - left
            )
            cells = []
            for dictionary, omitted in dictionaries:
                polynomial = _directed_taylor(
                    dictionary, left, step, period, root
                )
                tail = (
                    _directed_taylor_tail_upper(
                        dictionary, step, period, root
                    )
                    + omitted
                )
                cells.append((polynomial, tail))
            for slot, (_, tail) in enumerate(cells):
                tail_maximum[slot] = max(tail_maximum[slot], tail)

            current_range = _real_part_bernstein_range(cells[0][0])
            current_upper = (
                current_range.upper + cells[0][1] + current_error
            )
            current_upper_maximum = max(current_upper_maximum, current_upper)
            delayed_upper = []
            for slot in (1, 2):
                value = (
                    _complex_poly_bernstein_upper(cells[slot][0])
                    + cells[slot][1]
                    + delayed_error
                )
                delayed_upper.append(value)
                delayed_abs_maximum[slot - 1] = max(
                    delayed_abs_maximum[slot - 1], value
                )
            mu_upper = max(current_upper, minus_epsilon_upper)
            rate_upper = max(
                gmpy2.mpfr(0, precision),
                mu_upper + delayed_upper[0] + delayed_upper[1],
            )
            integral_upper += step.upper * rate_upper
            rate_maximum = max(rate_maximum, rate_upper)

    if cell_count != 1042 or integral_upper <= 0 or rate_maximum <= 0:
        raise ArithmeticError("the Stage-4V orbit-rate enclosure failed")
    return {
        "binary_center_period_exact_float_interval": {
            "lower": decimal_lower(period.lower, 80),
            "upper": decimal_upper(period.upper, 80),
        },
        "regular_physical_step": format(
            float(data.tau0) / DELAY_GRID_DIVISOR, ".17g"
        ),
        "cell_count": cell_count,
        "tau0_aligned_cells": DELAY_GRID_DIVISOR,
        "tau1_aligned_cells": 640,
        "precision_bits": precision,
        "current_coefficient_model_error_upper": decimal_upper(
            current_error, 80
        ),
        "delayed_coefficient_each_model_error_upper": decimal_upper(
            delayed_error, 80
        ),
        "delayed_phase_bridge": {
            "true_period_interval": {
                "lower": true_period_lower,
                "upper": true_period_upper,
            },
            "binary_period_exact_float_interval": {
                "lower": decimal_lower(period.lower, 80),
                "upper": decimal_upper(period.upper, 80),
            },
            "period_center_drift_upper": decimal_upper(period_drift, 80),
            "tau0_exact_minus_binary_center_abs_upper": decimal_upper(
                tau_center_drift[0], 80
            ),
            "tau1_exact_minus_binary_center_abs_upper": decimal_upper(
                tau_center_drift[1], 80
            ),
            "period_induced_delay_time_drift_upper": _record(
                period_phase_time_drift
            ),
            "total_delay_argument_time_drift_upper": _record(
                total_argument_time_drift
            ),
            "orbit_history_speed_upper": orbit_history_speed_upper,
            "inherited_orbit_voltage_error_upper": _record(
                orbit_voltage_error
            ),
            "delayed_argument_voltage_error_upper": _record(
                delayed_argument_voltage_error
            ),
            "delayed_coefficient_slope_upper": _record(
                delayed_coefficient_slope
            ),
            "additional_phase_coefficient_error_upper": _record(
                phase_coefficient_error
            ),
            "inherited_delayed_coefficient_error_upper": decimal_upper(
                inherited_delayed_error, 80
            ),
            "total_delayed_coefficient_error_used_upper": decimal_upper(
                delayed_error, 80
            ),
            "formula": (
                "delta_v_delay<=orbit_voltage_error+vdot_upper*("
                "tau_max*|P-P_binary|/P_lower+"
                "|tau_exact-tau_binary|); the additional phase part is "
                "multiplied by 3*epsilon*kappa3*(V+1) and added to the "
                "inherited Stage-4I delayed coefficient error"
            ),
            "binary_algebra_guard_is_phase_bridge": False,
        },
        "maximum_taylor_tail_upper": {
            "current": decimal_upper(tail_maximum[0], 80),
            "delayed0": decimal_upper(tail_maximum[1], 80),
            "delayed1": decimal_upper(tail_maximum[2], 80),
        },
        "maximum_current_coefficient_upper": decimal_upper(
            current_upper_maximum, 80
        ),
        "maximum_delayed_abs_upper": {
            "delay0": decimal_upper(delayed_abs_maximum[0], 80),
            "delay1": decimal_upper(delayed_abs_maximum[1], 80),
        },
        "one_binary_period_rate_integral_upper": decimal_upper(
            integral_upper, 80
        ),
        "rate_maximum_upper": decimal_upper(rate_maximum, 80),
        "integrand": (
            "r(t)=max(0,max(a(t),-epsilon)+|b_0(t)|+|b_1(t)|)"
        ),
        "cell_rule": (
            "real-part Bernstein upper for a; complex-modulus Bernstein "
            "uppers for b_j; analytic Fourier tails and Stage-4I exact-orbit "
            "coefficient errors added before the monotone max and integral"
        ),
    }


@lru_cache(maxsize=4)
def build_stage4v_certificate(repository: Path) -> Stage4VCertificate:
    repository = repository.resolve()
    parents = _load_parents(repository)

    stage4s = _mapping(
        parents[STAGE4S_A_RELATIVE_PATH].get("certificate"), "Stage-4S-A"
    )
    if (
        stage4s.get("schema_id") != "leaky-inner-stage4s-event-tube-v2"
        or stage4s.get("status")
        != "PROVED_NUMERIC_CENTER_AND_QUALITATIVE_NONZERO_SCALED_FULL_BALL__PREFERRED_FULL_BALL_OPEN"
    ):
        raise ValueError("the Stage-4S-A theorem identity changed")
    center = _mapping(
        stage4s.get("exact_center_event_window"), "Stage-4S-A center window"
    )
    inputs = _mapping(stage4s.get("exact_inputs"), "Stage-4S-A inputs")
    bridge = _mapping(
        stage4s.get("reduced_history_bridge"), "Stage-4S-A bridge"
    )
    containment = _mapping(
        stage4s.get("return_domain_containment"), "Stage-4S-A containment"
    )
    _require_claim(
        stage4s,
        "qualitative_nonzero_scaled_full_ball_event_tube_proved",
        True,
        "Stage-4S-A",
    )
    _require_claim(
        stage4s,
        "numerical_lambda_star_lower_bound_validated",
        False,
        "Stage-4S-A",
    )

    feasibility = _mapping(
        parents[STAGE4N_FEASIBILITY_RELATIVE_PATH].get("pilot"),
        "Stage-4N feasibility",
    )
    sharp = _mapping(
        feasibility.get("stage4i_sharpened_generic_gronwall"),
        "Stage-4N corrected row",
    )
    if (
        sharp.get("exact_inner_voltage_bound_coordinate")
        != "centered z=v-1"
        or sharp.get("field_hessian_row_formula")
        != "2*(1+B+r)+12*epsilon*kappa3*(B+r), with B=sup|v_*-1|"
    ):
        raise ValueError("the centered-voltage Hessian semantics changed")

    stage4n = _mapping(
        parents[STAGE4N_CONTRACT_RELATIVE_PATH].get("contract"), "Stage-4N"
    )
    coordinates = _mapping(
        stage4n.get("coordinate_and_domain_registration"),
        "Stage-4N coordinates",
    )
    if "||q_hat||_Y=1" not in str(coordinates.get("fixed_unit_y_splitting")):
        raise ValueError("the unit-Y coordinate triangle changed")

    stage4m = _mapping(
        parents[STAGE4M_RELATIVE_PATH].get("contract"), "Stage-4M"
    )
    splitting = _mapping(
        stage4m.get("coordinate_registration"), "Stage-4M splitting"
    )
    if (
        splitting.get("normalization")
        != "||q_hat||_Y=1 and f_hat(q_hat)=1 exactly"
        or splitting.get("stable_space") != "E_s=ker(f_hat) in Sigma_0"
    ):
        raise ValueError("the exact Stage-4M splitting changed")

    stage4i = _mapping(
        parents[STAGE4I_RELATIVE_PATH].get("artifact"), "Stage-4I"
    )
    grid = _mapping(stage4i.get("guide_and_grid"), "Stage-4I grid")
    tubes = _mapping(
        stage4i.get("directed_primitive_error_tubes"), "Stage-4I tubes"
    )
    if (
        grid.get("full_cells_plus_final_short_cell") != 1042
        or grid.get("tau0_aligned_cell_count") != 512
        or grid.get("tau1_aligned_cell_count") != 640
        or tubes.get("primitive_error_tubes_propagated") is not True
    ):
        raise ValueError("the Stage-4I directed coefficient ingress changed")

    stage2 = _mapping(
        parents[STAGE2_RELATIVE_PATH].get("contract"), "Stage-2"
    )
    section = _mapping(
        stage2.get("explicit_voltage_section_audit"), "Stage-2 section"
    )
    if section.get("uniform_event_speed_on_declared_section_ball_validated") is not True:
        raise ValueError("the Stage-2 local event-speed theorem changed")

    stage4r = _mapping(
        parents[STAGE4R_RELATIVE_PATH].get("theorem"), "Stage-4R"
    )
    for claim in (
        "common_window_endpoint_signs_and_speed_imply_unique_selected_event",
        "strict_T_minus_greater_than_2_tau_star_is_C2_sufficient",
        "selected_event_time_and_complete_history_hit_Ck_proved",
        "open_event_domain_and_image_containment_registered",
    ):
        _require_claim(stage4r, claim, True, "Stage-4R")

    stage4h = _mapping(
        parents[STAGE4H_RELATIVE_PATH].get("artifact"), "Stage-4H"
    )
    stage4h_intermediate = _mapping(
        stage4h.get("intermediate_signed_flow_diagnostic"),
        "Stage-4H intermediate diagnostic",
    )
    sampled_current_state_row = str(
        stage4h_intermediate["sampled_current_state_maximum_binary64"]
    )
    if sampled_current_state_row != "0.037389500646448783":
        raise ValueError("the Stage-4H fixed-time warning changed")

    preferred = _mapping(
        inputs.get("preferred_unscaled_radii"), "Stage-4S-A preferred radii"
    )
    if (
        preferred.get("R_s") != STABLE_RADIUS
        or preferred.get("R_u_hat") != UNSTABLE_RADIUS
        or preferred.get("sum") != SPLIT_RADIUS
    ):
        raise ValueError("the preferred anisotropic radii changed")

    orbit_rate = _directed_logarithmic_rate_integral(
        repository,
        true_period_lower=str(center["period_lower"]),
        true_period_upper=str(center["period_upper"]),
        tau_max_upper=str(center["tau_max_upper"]),
        orbit_history_speed_upper=str(
            center["physical_orbit_history_speed_upper"]
        ),
    )
    one_period_integral = _point(
        orbit_rate["one_binary_period_rate_integral_upper"]
    )
    rate_maximum = _point(orbit_rate["rate_maximum_upper"])
    binary_period_record = _mapping(
        orbit_rate["binary_center_period_exact_float_interval"],
        "exact binary center period",
    )
    binary_period = DirectedInterval.from_bounds(
        binary_period_record["lower"],
        binary_period_record["upper"],
        PRECISION_BITS,
    )
    period_lower = _point(center["period_lower"])
    period_upper = _point(center["period_upper"])
    t_plus = _point(center["T_plus"])
    phase_offset = _point(center["maximum_center_phase_offset_upper"])
    center_gap = _point(center["center_left_endpoint_gap_lower"])
    beta = center_gap / 2
    epsilon = _point(EPSILON)
    energy_factor = (1 + 1 / epsilon).sqrt()

    centered_voltage = _point(
        sharp["exact_inner_centered_voltage_abs_upper"]
    )
    kappa3 = _point(KAPPA_3)
    hessian_beta = 2 * (1 + centered_voltage + beta) + (
        12 * epsilon * kappa3 * (centered_voltage + beta)
    )
    period_scale = period_upper / binary_period
    two_period_linear_exponent = (
        2 * one_period_integral * period_scale
        + rate_maximum * phase_offset
    )
    nonlinear_exponent = hessian_beta * beta * t_plus / 2
    total_exponent = two_period_linear_exponent + nonlinear_exponent
    gain = _exp(total_exponent)

    split_radius = _point(SPLIT_RADIUS)
    closed_lambda = _point(CERTIFIED_LAMBDA)
    open_lambda = _point(OPEN_DOMAIN_LAMBDA)
    closed_y_radius = split_radius * closed_lambda
    open_y_radius = split_radius * open_lambda
    open_energy_initial = energy_factor * open_y_radius
    open_flow_deviation = open_energy_initial * gain
    bootstrap_slack = beta - open_flow_deviation
    lambda_ceiling = beta / (energy_factor * split_radius * gain)
    if (
        open_lambda.lower <= closed_lambda.upper
        or lambda_ceiling.lower <= open_lambda.upper
        or bootstrap_slack.lower <= 0
    ):
        raise ArithmeticError("the Stage-4V weighted-energy bootstrap failed")

    center_displacement = _point(
        center["center_window_history_displacement_upper"]
    )
    section_radius = _point(center["declared_section_ball_radius"])
    window_radius = center_displacement + open_flow_deviation
    terminal_patch_margin = section_radius - window_radius
    endpoint_gap = center_gap - open_flow_deviation
    endpoint_half_slack = endpoint_gap - beta
    center_speed = _point(center["center_uniform_event_speed_lower"])
    field_lipschitz = _point(
        section["vector_field_lipschitz_upper_on_declared_section_ball"]
    )
    event_speed = center_speed - field_lipschitz * open_flow_deviation
    half_center_speed = center_speed / 2
    speed_half_slack = event_speed - half_center_speed
    if (
        endpoint_half_slack.lower <= 0
        or terminal_patch_margin.lower <= 0
        or event_speed.lower <= 0
        or speed_half_slack.lower <= 0
    ):
        raise ArithmeticError("a Stage-4V event/patch gate failed")

    preferred_initial_energy = energy_factor * split_radius
    preferred_initial_to_beta = preferred_initial_energy / beta
    preferred_formal_exponential_rhs = preferred_initial_energy * gain
    preferred_formal_rhs_to_beta = preferred_formal_exponential_rhs / beta

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4VCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        scaled_domain={
            "history_space": str(inputs["reduced_history_space"]),
            "coordinate_space": "M=E_s x R with E_s=ker(f_hat) in Sigma_0",
            "coordinate_injection": str(inputs["initial_coordinate_injection"]),
            "stable_radius_R_s": STABLE_RADIUS,
            "unit_unstable_radius_R_u_hat": UNSTABLE_RADIUS,
            "radius_sum": SPLIT_RADIUS,
            "certified_closed_lambda": CERTIFIED_LAMBDA,
            "strict_open_domain_lambda": OPEN_DOMAIN_LAMBDA,
            "closed_ball_y_radius_upper": _record(closed_y_radius),
            "open_history_y_radius": _record(open_y_radius),
            "open_history_energy_radius": _record(open_energy_initial),
            "closed_ball": str(inputs["scaled_closed_ball"]),
            "stable_history_quantifier": str(inputs["stable_history_quantifier"]),
            "unit_y_triangle": (
                "||x_s+q_hat*x_u||_Y<=||x_s||_Y+|x_u| because "
                "||q_hat||_Y=1 exactly"
            ),
        },
        weighted_energy_identity={
            "energy": "z(t)^2=x(t)^2+y(t)^2/epsilon",
            "variables": "x=eta_v(t), y=eta_w(t)",
            "instantaneous_matrix": "[[a(t),-1],[epsilon,-epsilon]]",
            "exact_derivative_identity": (
                "(1/2)d(z^2)/dt=a(t)x^2-y^2+"
                "sum_j b_j(t)x*x(t-tau_j)+x*N(t)"
            ),
            "cross_term_cancellation": "-x*y+y*x=0 exactly",
            "instantaneous_logarithmic_rate": "max(a(t),-epsilon)",
            "complete_history_envelope": (
                "Z(t)=max(sup_{theta in [-tau_max,0]}|eta_v(theta)|,"
                "sup_{0<=s<=t}z(s))"
            ),
            "initial_energy_factor": _record(energy_factor),
            "initial_bound": "Z(0)<=sqrt(1+1/epsilon)*rho_Y=sqrt(6)*rho_Y",
            "delay_activation_rule": (
                "before activation the delayed voltage is the exact initial-"
                "history translate; after activation it is a previous x(s); "
                "both are bounded by Z"
            ),
            "upper_dini_inequality": (
                "D^+Z<=[r(t)+(H_beta/2)Z]Z at every increasing-envelope time"
            ),
        },
        directed_orbit_rate_integral={
            **orbit_rate,
            "exact_period_rescaling": _record(period_scale),
            "two_period_plus_window_linear_exponent_upper": _record(
                two_period_linear_exponent
            ),
            "extension_rule": (
                "two exact periods use the one-binary-period integral times "
                "P_upper/P_binary_lower, where P_binary is the exact "
                "binary64 value enclosed directly by from_float (never a "
                "round-tripped display decimal); the remaining phase offset is bounded by "
                "the directed global rate maximum"
            ),
            "scalar_stage4u_row_sum_not_used": True,
        },
        nonlinear_first_exit_bootstrap={
            "bootstrap_radius_beta": _record(beta),
            "beta_choice": "one half of the certified center endpoint gap",
            "centered_voltage_bound": str(
                sharp["exact_inner_centered_voltage_abs_upper"]
            ),
            "hessian_row_formula": (
                "H_beta=2*(1+B+beta)+12*epsilon*kappa3*(B+beta)"
            ),
            "hessian_row_at_beta": _record(hessian_beta),
            "nonlinear_exponent_upper": _record(nonlinear_exponent),
            "total_comparison_exponent_upper": _record(total_exponent),
            "complete_history_energy_gain_upper": _record(gain),
            "open_domain_flow_deviation_upper": _record(open_flow_deviation),
            "bootstrap_slack": _record(bootstrap_slack),
            "construction_lambda_ceiling": _record(lambda_ceiling),
            "first_exit_argument": (
                "on Z<=beta, D^+Z<=[r(t)+H_beta*beta/2]Z; "
                "the outward exponential bound is strictly below beta, so a "
                "first exit through beta before T_plus is impossible"
            ),
            "continuation_argument": (
                "the polynomial reduced RFDE field is bounded on the closed "
                "orbit-centered beta tube, so the solution continues through "
                "T_plus"
            ),
        },
        common_event_and_patch={
            "common_window": (
                f"[{center['T_minus']},{center['T_plus']}] in physical time"
            ),
            "center_endpoint_gap_lower": str(
                center["center_left_endpoint_gap_lower"]
            ),
            "same_time_event_perturbation_upper": _record(open_flow_deviation),
            "endpoint_gap_lower": _record(endpoint_gap),
            "advertised_half_gap": _record(beta),
            "endpoint_margin_beyond_half_gap": _record(endpoint_half_slack),
            "window_y_radius_about_phase_zero_center": _record(window_radius),
            "declared_section_ball_radius": str(
                center["declared_section_ball_radius"]
            ),
            "terminal_patch_margin": _record(terminal_patch_margin),
            "uniform_event_speed_lower": _record(event_speed),
            "half_center_speed_target": _record(half_center_speed),
            "speed_margin_beyond_half_target": _record(speed_half_slack),
            "existence_uniqueness": (
                "strict endpoint signs give existence and the positive "
                "speed gives uniqueness in this fixed near-two-period window"
            ),
            "event_ordinal": None,
            "complete_returned_history_cover": (
                "the envelope covers every physical time in "
                "[T_minus-tau_max,T_plus], not only the current event value"
            ),
        },
        regularity_and_return={
            "full_reduced_bridge": str(bridge["reduced_C2_corollary"]),
            "selected_hit": str(bridge["reduced_hit"]),
            "initial_domain": (
                "W_V={y:||y-Y_*||_Y<0.00995*(1.25e-8)}; "
                "D_in=j^{-1}(W_V intersect Sigma_loc)"
            ),
            "terminal_domain": (
                "D_V=D_in intersect (R_Y o j)^{-1}(Sigma_loc); the explicit "
                "closed anisotropic ball lies in D_V by the strict initial "
                "and terminal bounds"
            ),
            "terminal_chart": str(containment["terminal_chart"]),
            "coordinate_output_domain": str(
                containment["terminal_chart_codomain"]
            ),
            "induced_return": str(containment["induced_return"]),
            "C2_scope": (
                "apply the Stage-4R theorem directly on the explicit W_V, "
                "using the Stage-4S-A exact full-X/reduced-Y bridge, the "
                "Stage-4V common solution domain, T_minus>2*tau_max, and the "
                "strict endpoint/speed bounds; this does not assume that the "
                "unspecified qualitative Stage-4S-A neighborhood contains W_V"
            ),
            "same_domain_self_map": False,
        },
        preferred_ball_feasibility={
            "preferred_lambda_one_proved": False,
            "preferred_initial_energy_radius": _record(
                preferred_initial_energy
            ),
            "preferred_initial_energy_to_beta_ratio": _record(
                preferred_initial_to_beta
            ),
            "formal_exponential_rhs_if_bootstrap_hypothesis_ignored": _record(
                preferred_formal_exponential_rhs
            ),
            "formal_rhs_to_beta_ratio": _record(preferred_formal_rhs_to_beta),
            "formal_rhs_is_validated_flow_bound": False,
            "interpretation": (
                "the orbit-aware logarithmic estimate improves the scalar "
                "Gronwall certified scale by about 22 decimal orders, but at "
                "lambda=1 its weighted initial energy already exceeds beta, "
                "so the beta-bootstrap hypothesis is inapplicable at t=0. "
                "The displayed exponential RHS is only the formal value "
                "obtained by ignoring that failed hypothesis; it is not a "
                "flow bound.  This is a no-go only for applicability of this "
                "sufficient construction, not a lower bound on the true flow"
            ),
            "next_required_ingress": (
                "separate a broad global boundedness tube from a terminal "
                "event-time tube; validate signed fixed-time event rows and "
                "the event-time second-variation kernel on a possibly wider "
                "center window, rather than requiring Z<=half-gap for all time"
            ),
            "fixed_plus_minus_1e3_window_excludes_preferred_ball_proved": False,
            "fixed_window_linear_warning": (
                "the Stage-4H source-bound sampled current-state row norm "
                f"{sampled_current_state_row} times R_s exceeds the center endpoint gap, but no "
                "directed lower witness is available, so exclusion is not "
                "promoted"
            ),
        },
        theorem_boundary={
            "proved_here": (
                "a closed scale lambda=1.2e-8 and a strictly larger open "
                "scale 1.25e-8 for arbitrary continuous reduced-Y stable "
                "histories; common existence through the fixed near-two-"
                "period window, endpoint signs, uniform positive speed, one "
                "unique selected event in that window, complete returned-Y "
                "patch containment, and the inherited C2 selected hit/return"
            ),
            "not_proved_here": (
                "lambda=1, fixed-window exclusion of lambda=1, a same-ball "
                "self-map, full-X same-radius tube, event ordinal, no-earlier "
                "return, Q=P^2, projected Hessians, stable graph, pulse-sheet "
                "crossing, biological onset/control, routing, capture, safety, "
                "or a general-network canard theorem"
            ),
            "stage4u_result_used_as_parent": False,
            "existing_artifacts_modified": False,
        },
        claim_status=claims,
    )


def build_stage4v_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_stage4v_certificate(repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "status": STATUS,
            "certificate_sha256": canonical_sha256(certificate),
            "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": _runtime_record(),
        },
    }


def validate_stage4v_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = True
) -> None:
    repository = repository.resolve()
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-4V result schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-4V certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-4V manifest")
    if set(certificate) != {field.name for field in fields(Stage4VCertificate)}:
        raise ValueError("the Stage-4V certificate schema changed")
    claims = _mapping(certificate.get("claim_status"), "Stage-4V claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4V claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4V gate was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4V gate was promoted")

    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "status": STATUS,
        "certificate_sha256": canonical_sha256(certificate),
        "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4V manifest fixed data changed")
    if manifest.get("numeric_core_sha256") != EXPECTED_NUMERIC_CORE_SHA256:
        raise ValueError("the frozen Stage-4V numeric core changed")
    source_hashes = _mapping(manifest.get("source_sha256"), "Stage-4V sources")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "Stage-4V dependencies"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4V source set changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4V dependency set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-4V source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-4V dependency changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"a Stage-4V parent changed: {relative}")
    runtime = _mapping(manifest.get("runtime"), "Stage-4V runtime")
    if runtime.get("precision_bits") != str(PRECISION_BITS):
        raise ValueError("the Stage-4V runtime precision changed")
    if recompute:
        expected = asdict(build_stage4v_certificate(repository))
        if certificate != expected:
            raise ValueError("the Stage-4V arithmetic differs from replay")


__all__ = [
    "CERTIFIED_LAMBDA",
    "EXPECTED_NUMERIC_CORE_SHA256",
    "FALSE_FLAGS",
    "OPEN_DOMAIN_LAMBDA",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "Stage4VCertificate",
    "TRUE_FLAGS",
    "_numeric_core",
    "build_stage4v_certificate",
    "build_stage4v_result",
    "canonical_sha256",
    "validate_stage4v_result",
]
