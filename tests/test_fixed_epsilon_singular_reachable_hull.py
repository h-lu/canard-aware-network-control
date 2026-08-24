"""Hostile tests for the singular reachable-hull geometry certificate."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

import gmpy2
import mpmath as mp
import pytest
import sympy as sp

import canard_control.fixed_epsilon_singular_reachable_hull as geometry
from canard_control.directed_interval import DirectedInterval
from canard_control.fixed_epsilon_singular_reachable_hull import (
    MANIFEST_ARITHMETIC,
    OPEN_FLAGS,
    PRECISION_BITS,
    PROVED_FLAGS,
    backward_moving_tube_face_margin,
    backward_normal_boundary_velocity,
    backward_normal_variation,
    backward_static_barrier_margin,
    build_reference_certificate,
    causal_backward_crossing_time_bound,
    causal_slab_inverse_gain,
    curved_barrier_lie_derivative,
    flow_time_integrand_diagnostic,
    json_ready_singular_reachable_hull_audit,
    level_normals_diagnostic,
    log_first_integral,
    normal_level_sensitivity,
    perturbed_coordinate_rhs,
    perturbed_first_integral_drift,
    positive_level_turning_phase,
    singular_coordinate_rhs,
    smooth_first_integral,
    smooth_first_integral_gradient,
    validate_singular_reachable_hull_audit,
    validate_singular_reachable_hull_result,
)
REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_singular_reachable_hull.py"
)
GENERATOR = (
    REPOSITORY / "experiments/fixed_epsilon_singular_reachable_hull.py"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_singular_reachable_hull.json"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-singular-reachable-hull.md"
README = REPOSITORY / "README.md"

EXPECTED_SOURCE_SHA256 = (
    "7a36ae725ffbe4a067991646eff59a503e9302e199aee4e7aa3b49db5cfe9989"
)
EXPECTED_GENERATOR_SHA256 = (
    "c401e406d1cf53f5bda7fdcbb86b3d74367dc62b71bb9e87cb5323d5247b15a7"
)
EXPECTED_RESULT_SHA256 = (
    "0bf501b77fa43761e34a8ad084b7630912bf56850f43e5c094e17dbc08a78431"
)
EXPECTED_NOTE_SHA256 = (
    "9a34e223a3cbe3aeb0984aec78adad820c2a5db6ee85553a365099c9b3762dce"
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _interval(record: object) -> DirectedInterval:
    assert isinstance(record, dict)
    return DirectedInterval.from_bounds(
        record["lower"], record["upper"], PRECISION_BITS
    )


def _independent_theta_bounds() -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    precision = PRECISION_BITS
    parent = json.loads(
        (
            REPOSITORY
            / "experiments/results/fixed_window_prepared_gap_seed.json"
        ).read_text(encoding="utf-8")
    )["audit"]["certificate"]["period"]
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        period_lower = gmpy2.mpfr(parent["lower"])
        sqrt_five_lower = gmpy2.sqrt(gmpy2.mpfr(5))
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        period_upper = gmpy2.mpfr(parent["upper"])
        sqrt_five_upper = gmpy2.sqrt(gmpy2.mpfr(5))
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower = period_lower / sqrt_five_upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        upper = period_upper / sqrt_five_lower
    return lower, upper


def test_coordinate_dynamics_and_first_integral_are_symbolically_exact() -> None:
    sigma, normal = sp.symbols("sigma normal", real=True)
    x = -sigma / 2
    y = sigma**2 / 4 - sp.Rational(1, 2) + normal
    x_dot = y - x**2
    y_dot = -x
    sigma_dot = sp.simplify(-2 * x_dot)
    normal_dot = sp.simplify(y_dot - 2 * x * x_dot)
    assert sigma_dot == 1 - 2 * normal
    assert normal_dot == sigma * normal

    first_integral = normal * sp.exp(-2 * normal - sigma**2 / 2)
    lie = sp.simplify(
        sp.diff(first_integral, sigma) * sigma_dot
        + sp.diff(first_integral, normal) * normal_dot
    )
    assert lie == 0

    canonical_h = sp.Rational(1, 2) * sp.exp(-2 * y) * normal
    assert sp.simplify(canonical_h - sp.E * first_integral / 2) == 0

    assert singular_coordinate_rhs((1.25, -0.4)) == pytest.approx(
        (1.8, -0.5)
    )
    assert smooth_first_integral((0.0, 0.0)) == 0.0
    assert smooth_first_integral_gradient((0.0, 0.0)) == (0.0, 1.0)
    with pytest.raises(ValueError, match="undefined"):
        log_first_integral((0.0, 0.0))
    assert log_first_integral((1.5, -0.2)) == pytest.approx(
        math.log(0.2) + 0.4 - 1.5**2 / 2
    )


def test_cartesian_perturbation_j_drift_has_the_exact_signs() -> None:
    sigma, normal, delta_x, delta_y = sp.symbols(
        "sigma normal delta_x delta_y", real=True
    )
    weight = sp.exp(-2 * normal - sigma**2 / 2)
    first_integral = normal * weight
    sigma_dot = 1 - 2 * normal - 2 * delta_x
    normal_dot = sigma * normal + sigma * delta_x + delta_y
    actual = sp.simplify(
        sp.diff(first_integral, sigma) * sigma_dot
        + sp.diff(first_integral, normal) * normal_dot
    )
    expected = weight * (sigma * delta_x + (1 - 2 * normal) * delta_y)
    assert sp.simplify(actual - expected) == 0

    cases = (
        ((1.0, 0.25), (1.0, 0.0), 1),
        ((-1.0, 0.25), (1.0, 0.0), -1),
        ((0.0, 0.25), (0.0, 1.0), 1),
        ((0.0, 0.75), (0.0, 1.0), -1),
    )
    for state, perturbation, sign in cases:
        value = perturbed_first_integral_drift(state, perturbation)
        assert math.copysign(1.0, value) == float(sign)

    state = (0.7, -0.15)
    perturbation = (0.2, -0.4)
    gradient = smooth_first_integral_gradient(state)
    coordinate_rhs = perturbed_coordinate_rhs(state, perturbation)
    dot_product = sum(a * b for a, b in zip(gradient, coordinate_rhs))
    assert dot_product == pytest.approx(
        perturbed_first_integral_drift(state, perturbation)
    )


def test_lambert_branches_reconstruct_levels_and_enforce_domains() -> None:
    with mp.workdps(80):
        negative = level_normals_diagnostic(1, mp.mpf("-0.1"))
        assert len(negative) == 1 and negative[0] < 0
        assert mp.almosteq(
            negative[0] * mp.exp(-2 * negative[0] - mp.mpf("0.5")),
            mp.mpf("-0.1"),
        )

        positive = level_normals_diagnostic(0, mp.mpf(1) / 8)
        assert len(positive) == 2
        assert 0 < positive[0] < mp.mpf("0.5") < positive[1]
        for normal in positive:
            assert mp.almosteq(normal * mp.exp(-2 * normal), mp.mpf(1) / 8)

        assert level_normals_diagnostic(0, mp.mpf(1) / 4) == ()
        assert len(level_normals_diagnostic(2, mp.mpf("0.01"))) == 2
        assert level_normals_diagnostic(3, mp.mpf("0.01")) == ()
        assert level_normals_diagnostic(2, mp.mpf("0.01")) == (
            level_normals_diagnostic(-2, mp.mpf("0.01"))
        )
        assert level_normals_diagnostic(100, 0) == (mp.mpf("0"),)

        level = mp.mpf("0.01")
        turning = positive_level_turning_phase(level)
        assert mp.almosteq(2 * level * mp.exp(turning**2 / 2), 1 / mp.e)
        lower_integrand = flow_time_integrand_diagnostic(0, level, branch=0)
        upper_integrand = flow_time_integrand_diagnostic(0, level, branch=-1)
        assert lower_integrand > 0 and upper_integrand < 0
        level_normals = level_normals_diagnostic(0, level)
        assert mp.almosteq((1 - 2 * level_normals[0]) * lower_integrand, 1)
        assert mp.almosteq((1 - 2 * level_normals[1]) * upper_integrand, 1)
        maximum = mp.exp(-1) / 2
        assert level_normals_diagnostic(0, maximum) == (mp.mpf("0.5"),)
        for branch in (0, -1):
            with pytest.raises(ValueError, match="singular"):
                flow_time_integrand_diagnostic(0, maximum, branch=branch)
        with pytest.raises(ValueError, match="not a finite branch"):
            flow_time_integrand_diagnostic(2, 0, branch=-1)

    for invalid_branch in (False, 0.0, -1.0, 1):
        with pytest.raises(ValueError, match="branch"):
            flow_time_integrand_diagnostic(0, "0.01", branch=invalid_branch)
    for function, arguments in (
        (level_normals_diagnostic, (0, "0.01")),
        (positive_level_turning_phase, ("0.01",)),
        (flow_time_integrand_diagnostic, (0, "0.01")),
    ):
        with pytest.raises(ValueError, match="decimal_digits"):
            function(*arguments, decimal_digits=80.0)
    with pytest.raises(ValueError, match="singular"):
        normal_level_sensitivity(0.0, 0.5)


def test_lambert_turning_topology_uses_strict_high_precision_order() -> None:
    with mp.workdps(220):
        maximum = mp.exp(-1) / 2
        below = mp.nstr(maximum * (1 - mp.mpf("1e-120")), 210)
        above = mp.nstr(maximum * (1 + mp.mpf("1e-120")), 210)
        exact = maximum

    lower, upper = level_normals_diagnostic(
        0, below, decimal_digits=200
    )
    assert lower < mp.mpf("0.5") < upper
    assert level_normals_diagnostic(0, above, decimal_digits=200) == ()
    for branch in (0, -1):
        value = flow_time_integrand_diagnostic(
            0, below, branch=branch, decimal_digits=200
        )
        assert mp.isfinite(value)
        with pytest.raises(ValueError, match="nonreal"):
            flow_time_integrand_diagnostic(
                0, above, branch=branch, decimal_digits=200
            )
        with pytest.raises(ValueError, match="singular"):
            flow_time_integrand_diagnostic(
                0, exact, branch=branch, decimal_digits=200
            )


def test_constant_width_strip_and_normal_multiplier_are_refused_exactly() -> None:
    for radius in (1e-8, 0.25, 3.0):
        assert backward_normal_boundary_velocity(-2.0, radius) > 0
        assert backward_normal_boundary_velocity(-2.0, -radius) < 0
    for sigma, delay in ((0.0, 2.0), (-5.0, 1.7), (3.0, 4.0)):
        assert backward_normal_variation(sigma, delay) == pytest.approx(
            math.exp(-sigma * delay + delay**2 / 2)
        )
    assert normal_level_sensitivity(20.0, 0.0) == pytest.approx(math.exp(200))


def test_curved_and_static_backward_barrier_signs_are_not_reversed() -> None:
    state = (0.8, 0.2)
    perturbation = (0.07, -0.03)
    slope = -0.11
    sigma_dot = perturbed_coordinate_rhs(state, perturbation)[0]
    expected = (
        perturbed_first_integral_drift(state, perturbation) - slope * sigma_dot
    )
    assert curved_barrier_lie_derivative(
        state, perturbation, slope
    ) == pytest.approx(expected)
    assert backward_static_barrier_margin(0.3, "upper") == 0.3
    assert backward_static_barrier_margin(-0.3, "lower") == 0.3
    assert backward_static_barrier_margin(-0.3, "upper") < 0
    assert backward_static_barrier_margin(0.3, "lower") < 0
    with pytest.raises(ValueError, match="side"):
        backward_static_barrier_margin(0.0, "center")

    speed = 0.017
    j_dot = perturbed_first_integral_drift(state, perturbation)
    expected_faces = {
        "sigma_lower": -sigma_dot - speed,
        "sigma_upper": speed + sigma_dot,
        "j_lower": -j_dot - speed,
        "j_upper": speed + j_dot,
    }
    for face, expected_margin in expected_faces.items():
        assert backward_moving_tube_face_margin(
            state, perturbation, face, speed
        ) == pytest.approx(expected_margin)
    with pytest.raises(ValueError, match="face"):
        backward_moving_tube_face_margin(state, perturbation, "wrong", speed)


def test_causal_slab_bounds_require_a_positive_clock_and_contraction() -> None:
    assert causal_backward_crossing_time_bound(3.0, 0.25) == 12.0
    assert causal_slab_inverse_gain(0.2, 0.6) == pytest.approx(0.75)
    with pytest.raises(ValueError, match="positive"):
        causal_backward_crossing_time_bound(1.0, 0.0)
    with pytest.raises(ValueError, match="nonnegative"):
        causal_backward_crossing_time_bound(-1.0, 0.5)
    for invalid in (-0.1, 1.0, 1.2):
        with pytest.raises(ValueError, match=r"\[0,1\)"):
            causal_slab_inverse_gain(invalid, 1.0)


def test_theta_and_asymmetric_depth_two_hull_are_mpfr_directed() -> None:
    payload = json_ready_singular_reachable_hull_audit()
    certificate = payload["certificate"]
    theta = _interval(certificate["theta_horizon"])
    recomputed = _interval(certificate["theta_recomputed_from_period"])
    independent_lower, independent_upper = _independent_theta_bounds()
    assert theta.lower <= independent_lower <= independent_upper <= theta.upper
    assert recomputed.lower <= independent_lower
    assert recomputed.upper >= independent_upper
    assert theta.lower > 5
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        two_pi_upper = 2 * gmpy2.const_pi()
    assert theta.lower > two_pi_upper

    frozen_parent_theta = json.loads(
        (
            REPOSITORY
            / "experiments/results/fixed_epsilon_frozen_graph_operator.json"
        ).read_text(encoding="utf-8")
    )["audit"]["certificate"]["theta_interval"]
    assert certificate["theta_parent_endpoint_strings"] == [
        frozen_parent_theta["lower"],
        frozen_parent_theta["upper"],
    ]
    parent_theta = DirectedInterval.from_bounds(
        frozen_parent_theta["lower"],
        frozen_parent_theta["upper"],
        PRECISION_BITS,
    )
    assert theta.lower <= parent_theta.lower
    assert theta.upper >= parent_theta.upper

    depth_one_left = _interval(certificate["depth_one_left_endpoint"])
    depth_two_left = _interval(certificate["depth_two_left_endpoint"])
    depth_two_length = _interval(certificate["depth_two_exact_length"])
    symmetric_radius = _interval(
        certificate["prior_symmetric_depth_two_radius"]
    )
    margin = _interval(certificate["reference_plateau_margin_over_exact_hull"])

    assert depth_one_left.lower <= -5 - theta.upper
    assert depth_one_left.upper >= -5 - theta.lower
    assert depth_two_left.lower <= -5 - 2 * theta.upper
    assert depth_two_left.upper >= -5 - 2 * theta.lower
    assert depth_two_length.lower <= 10 + 2 * theta.lower
    assert depth_two_length.upper >= 10 + 2 * theta.upper
    assert symmetric_radius.lower > 5
    assert symmetric_radius.upper < 20
    assert margin.lower > gmpy2.mpfr("0.205")
    assert certificate["prior_symmetric_interval_is_only_an_overbound"] is True

    positive_cap = _interval(
        certificate["lower_positive_level_cap_at_sigma_20"]
    )
    level_condition = _interval(
        certificate["level_coordinate_condition_at_sigma_20_d0"]
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        cap_lower = gmpy2.exp(gmpy2.mpfr(-201)) / 2
        condition_lower = gmpy2.exp(gmpy2.mpfr(200))
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        cap_upper = gmpy2.exp(gmpy2.mpfr(-201)) / 2
        condition_upper = gmpy2.exp(gmpy2.mpfr(200))
    assert positive_cap.lower <= cap_lower <= cap_upper <= positive_cap.upper
    assert (
        level_condition.lower
        <= condition_lower
        <= condition_upper
        <= level_condition.upper
    )
    assert float(level_condition.lower) > 7.225e86
    normal_factor = _interval(
        certificate["backward_normal_factor_at_sigma_minus5_theta"]
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        normal_factor_lower = gmpy2.exp(
            5 * independent_lower + independent_lower**2 / 2
        )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        normal_factor_upper = gmpy2.exp(
            5 * independent_upper + independent_upper**2 / 2
        )
    assert normal_factor.lower <= normal_factor_lower
    assert normal_factor.upper >= normal_factor_upper
    assert float(normal_factor.lower) > 8.794e27


def test_claim_ledger_is_strict_and_cannot_promote_target_results() -> None:
    audit = json_ready_singular_reachable_hull_audit()
    certificate = audit["certificate"]
    expected_formulas = {
        "singular_coordinate_rhs": ["1-2d", "sigma*d"],
        "smooth_first_integral": "d*exp(-2d-sigma^2/2)",
        "canonical_trace_integral_relation": "mathscrH=(e/2)J",
        "lambert_inverse_formula": (
            "d_k=-(1/2)W_k(-2h*exp(sigma^2/2))"
        ),
        "positive_turning_phase_formula": "sqrt(-2*(1+log(2h)))",
        "flow_time_integrand_formula": (
            "1/(1+W_k(-2h*exp(sigma^2/2)))"
        ),
        "perturbed_coordinate_rhs": [
            "1-2d-2Delta_X",
            "sigma*d+sigma*Delta_X+Delta_Y",
        ],
        "perturbed_first_integral_drift": (
            "exp(-2d-sigma^2/2)*(sigma*Delta_X+(1-2d)*Delta_Y)"
        ),
        "curved_barrier_lie_derivative": "Jdot-j'(sigma)*sigma_dot",
        "backward_static_lower_condition": "Jdot<=0",
        "backward_static_upper_condition": "Jdot>=0",
        "backward_moving_face_conditions": [
            "-sigma_dot>=a'(r)",
            "-sigma_dot<=b'(r)",
            "-Jdot>=ell'(r)",
            "-Jdot<=u'(r)",
        ],
        "causal_clock_condition": "sigma_dot>=kappa>0",
        "causal_backward_crossing_bound": "slab_width/kappa",
        "causal_slab_forward_substitution": (
            "e_j<=(sum_{ell<j}P_jell*e_ell)/(1-lambda_j)"
        ),
    }
    assert {
        name: certificate[name] for name in expected_formulas
    } == expected_formulas
    assert all(certificate[name] is True for name in PROVED_FLAGS)
    assert all(certificate[name] is False for name in OPEN_FLAGS)
    validate_singular_reachable_hull_audit(audit)

    independently_open = (
        "positive_amplitude_graph_candidate_computed",
        "positive_amplitude_delta_bounds_validated",
        "positive_amplitude_barriers_instantiated",
        "positive_amplitude_depth_two_hull_validated",
        "fixed_target_localized_graph_theorem_proved",
        "remote_cutoff_independence_or_decay_proved",
        "left_preparation_independence_proved",
        "target_uniform_clock_bound_validated",
        "target_causal_slab_contractions_validated",
        "weighted_left_tail_decay_validated",
        "graph_fixed_point_inverse_validated",
        "fixed_epsilon_complete_history_root_validated",
    )
    assert all(certificate[name] is False for name in independently_open)
    assert (
        certificate[
            "right_completion_independence_proved_under_lemma_hypotheses"
        ]
        is True
    )
    assert "matched locally-Lipschitz" in certificate["causal_left_germ_condition"]
    assert "d*<1/2" in certificate["causal_lower_component_condition"]
    assert certificate["causal_lower_component_ambiguity_excluded"] is True

    for name in PROVED_FLAGS:
        tampered = deepcopy(audit)
        tampered["certificate"][name] = 1
        with pytest.raises(ValueError):
            validate_singular_reachable_hull_audit(tampered)
    for name in OPEN_FLAGS:
        tampered = deepcopy(audit)
        tampered["certificate"][name] = 0
        with pytest.raises(ValueError):
            validate_singular_reachable_hull_audit(tampered)

    for key, value in (
        ("precision_bits", True),
        ("precision_bits", 512.0),
        ("retained_phase_interval", [-5.0, 5.0]),
        ("delay_set", [4.0, 5.0, "Theta_*"]),
        ("lambert_inverse_formula", "wrong sign"),
        ("depth_two_exact_length", {"lower": "0", "upper": "1"}),
    ):
        tampered = deepcopy(audit)
        tampered["certificate"][key] = value
        with pytest.raises(ValueError):
            validate_singular_reachable_hull_audit(tampered)


def test_result_manifest_is_complete_source_bound_and_strict() -> None:
    payload = _result()
    validate_singular_reachable_hull_result(payload, REPOSITORY)
    manifest = payload["manifest"]
    assert manifest["arithmetic"] == MANIFEST_ARITHMETIC
    assert "Lambert-W point evaluation is diagnostic only" in manifest["arithmetic"]
    assert "no positive-amplitude flow" in manifest["arithmetic"]
    assert "root validation" in manifest["arithmetic"]
    assert manifest["proof_source_sha256"] == _digest(SOURCE)
    assert manifest["generator_sha256"] == _digest(GENERATOR)
    assert manifest["note_sha256"] == _digest(NOTE)
    assert all(value is True for value in manifest["parent_claim_checks"].values())
    assert set(manifest["parent_claim_checks"]) == {
        "frozen_graph_parent_requires_positive_amplitude_hull",
        "seed_parent_uses_retained_segment_minus5_plus5",
        "trace_parent_defines_canonical_first_integral",
        "parent_theta_and_period_endpoints_replayed_exactly",
    }
    certificate_keys = set(payload["audit"]["certificate"])
    assert {key for key in certificate_keys if "lambert" in key.lower()} == {
        "lambert_inverse_formula",
        "real_lambert_branch_classification_proved",
    }

    mutations = (
        ("proof_source_sha256", "0" * 64),
        ("generator", "experiments/wrong.py"),
        ("arithmetic", "binary64 guess"),
        ("python", "0.0"),
    )
    for key, value in mutations:
        tampered = deepcopy(payload)
        tampered["manifest"][key] = value
        with pytest.raises(ValueError):
            validate_singular_reachable_hull_result(tampered, REPOSITORY)

    tampered = deepcopy(payload)
    first_check = next(iter(tampered["manifest"]["parent_claim_checks"]))
    tampered["manifest"]["parent_claim_checks"][first_check] = 1
    with pytest.raises(ValueError):
        validate_singular_reachable_hull_result(tampered, REPOSITORY)
    tampered = deepcopy(payload)
    tampered["manifest"]["extra"] = "not allowed"
    with pytest.raises(ValueError):
        validate_singular_reachable_hull_result(tampered, REPOSITORY)


def test_parent_byte_change_is_detected(tmp_path: Path) -> None:
    payload = _result()
    relative_paths = (
        "src/canard_control/fixed_epsilon_singular_reachable_hull.py",
        "experiments/fixed_epsilon_singular_reachable_hull.py",
        "docs/fixed-epsilon-singular-reachable-hull.md",
        "experiments/results/fixed_epsilon_frozen_graph_operator.json",
        "experiments/results/fixed_window_prepared_gap_seed.json",
        "docs/long-delay-selected-trace-proof.md",
    )
    for relative in relative_paths:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPOSITORY / relative, target)
    parent = tmp_path / "docs/long-delay-selected-trace-proof.md"
    parent.write_bytes(parent.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="pinned parent"):
        validate_singular_reachable_hull_result(payload, tmp_path)


def test_direct_validator_replays_parent_endpoint_semantics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = _result()
    monkeypatch.setattr(geometry, "THETA_LOWER", "7.39708")
    tampered = deepcopy(payload)
    tampered["audit"] = geometry.json_ready_singular_reachable_hull_audit()
    with pytest.raises(ValueError, match="parent claim checks"):
        validate_singular_reachable_hull_result(tampered, REPOSITORY)


def test_generator_replays_byte_identically(tmp_path: Path) -> None:
    replay = tmp_path / "replay.json"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
        cwd=REPOSITORY,
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_artifact_hashes_and_claim_boundaries_are_pinned() -> None:
    assert _digest(SOURCE) == EXPECTED_SOURCE_SHA256
    assert _digest(GENERATOR) == EXPECTED_GENERATOR_SHA256
    assert _digest(RESULT) == EXPECTED_RESULT_SHA256
    assert _digest(NOTE) == EXPECTED_NOTE_SHA256

    note = NOTE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    assert "[-5-m\\Theta_*,5]" in note
    assert "It is not the exact reachable" in note
    assert "right remote cutoff: irrelevant" in note
    assert "left remote cutoff" in note
    assert "fixed-epsilon-singular-reachable-hull.md" in readme
    assert (
        "| Positive-amplitude graph candidate or \\(\\Delta\\) enclosure "
        "| **Open** |"
    ) in note
    assert (
        "| Instantiated positive-amplitude barriers and depth-two hull "
        "| **Open** |"
    ) in note
    assert (
        "| Preparation-independent or left-cutoff-independent graph "
        "| **Open** |"
    ) in note
    assert "under explicit clock/barrier/existence hypotheses" in note
