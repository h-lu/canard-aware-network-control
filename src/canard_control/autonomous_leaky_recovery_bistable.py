"""Exact certificate for the autonomous leaky-recovery RFDE proposal.

Only the unique equilibrium and its delay-independent local exponential
stability are proved here.  Periodic orbits, Floquet indices, basin routing,
physical-pulse onset, response invertibility, and network lifting remain
numerical candidates or open gates, as recorded by the strict claim ledger.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any, Mapping

import sympy as sp


MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
AUDIT_ID = "autonomous-leaky-recovery-equilibrium-stability-v1"
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/autonomous_leaky_recovery_bistable_probe.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/autonomous_leaky_recovery_bistable_probe.json"
)
NOTE_RELATIVE_PATH = (
    "docs/autonomous-leaky-recovery-bistable-rfde-proposal.md"
)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "python3 experiments/autonomous_leaky_recovery_bistable_probe.py"
)
MANIFEST_ARITHMETIC = (
    "exact Fraction and SymPy equilibrium/characteristic algebra with a "
    "rational H-infinity small-gain margin; binary64 Fourier collocation, "
    "method-of-steps, monodromy, onset-bracket, and response diagnostics "
    "are explicitly non-directed"
)
OUTPUT_CONTROL_COORDINATES = (
    "unfolding_a",
    "kappa_3",
    "pulse_amplitude_J",
)

EPSILON = Fraction(1, 5)
UNFOLDING = Fraction(1, 4)
RECOVERY_LEAK = Fraction(1)
KAPPA_1 = Fraction(1, 250)
KAPPA_3 = Fraction(1, 200)
ALPHA_LOWER = Fraction(1817, 2000)
ALPHA_UPPER = Fraction(4543, 5000)


Interval = tuple[Fraction, Fraction]


PROVED_FLAGS = {
    "unique_equilibrium_proved",
    "delay_independent_no_closed_right_half_plane_roots_proved",
    "local_exponential_equilibrium_stability_proved",
    "post_pulse_vector_field_autonomous_by_definition",
}
CANDIDATE_FLAGS = {
    "outer_periodic_candidate_computed",
    "inner_periodic_candidate_computed",
    "finite_monodromy_index_candidate_computed",
    "finite_duration_pulse_endpoint_candidates_computed",
    "a_kappa3_response_candidate_computed",
}
OPEN_FLAGS = {
    "outer_periodic_orbit_validated",
    "inner_periodic_orbit_validated",
    "rfde_floquet_indices_validated",
    "history_space_separator_validated",
    "finite_duration_physical_pulse_unique_onset_validated",
    "frequency_amplitude_jacobian_invertibility_validated",
    "three_output_local_diffeomorphism_proved",
    "finite_network_lift_proved",
    "dimension_uniform_network_basin_radius_proved",
    "fixed_epsilon_leaky_canard_root_validated",
    "canard_root_equals_physical_onset_proved",
}
REFUSED_FLAGS = {
    "binary64_diagnostics_promoted_to_proof",
    "constant_history_kick_substituted_for_physical_pulse",
    "planar_annulus_claimed_as_rfde_history_space_separator",
    "epsilon_used_as_final_frequency_amplitude_control_coordinate",
}


@dataclass(frozen=True)
class ExactEquilibriumAlgebra:
    """Exact symbolic objects entering the characteristic determinant."""

    spectral_parameter: sp.Symbol
    delay_0: sp.Symbol
    delay_1: sp.Symbol
    epsilon: sp.Expr
    unfolding: sp.Expr
    recovery_leak: sp.Expr
    kappa_1: sp.Expr
    kappa_3: sp.Expr
    equilibrium_voltage: sp.Expr
    equilibrium_recovery: sp.Expr
    delayed_gain: sp.Expr
    current_coefficient: sp.Expr
    delay_average: sp.Expr
    characteristic_determinant: sp.Expr
    reference_polynomial: sp.Expr
    beta: sp.Expr
    gamma: sp.Expr


@dataclass(frozen=True)
class EquilibriumStabilityCertificate:
    """Canonical JSON schema for Proposition 2.1."""

    model_id: str
    audit_id: str
    epsilon: str
    unfolding_a: str
    recovery_leak_b: str
    kappa_1: str
    kappa_3: str
    equilibrium_equation_formula: str
    equilibrium_voltage_formula: str
    equilibrium_recovery_formula: str
    characteristic_determinant_formula: str
    reference_polynomial_formula: str
    beta_formula: str
    gamma_formula: str
    d_polynomial_formula: str
    alpha_interval: dict[str, str]
    effective_delay_gain_interval: dict[str, str]
    current_coefficient_interval: dict[str, str]
    epsilon_minus_current_interval: dict[str, str]
    one_minus_current_interval: dict[str, str]
    beta_interval: dict[str, str]
    gamma_interval: dict[str, str]
    four_gamma_minus_beta_squared_interval: dict[str, str]
    cube_root_bracket_strict: bool
    unique_real_equilibrium_proved: bool
    base_polynomial_hurwitz_proved: bool
    beta_strictly_negative_proved: bool
    gamma_strictly_positive_proved: bool
    four_gamma_minus_beta_squared_strictly_positive_proved: bool
    d_positive_on_nonnegative_axis_proved: bool
    delay_average_bounded_by_one_on_closed_right_half_plane_proved: bool
    right_half_plane_small_gain_strictly_below_one_proved: bool
    characteristic_zero_free_on_closed_right_half_plane_proved: bool
    local_exponential_equilibrium_stability_proved: bool


@dataclass(frozen=True)
class AutonomousBistableClaimLedger:
    """Truth-valued scope ledger for analytic and diagnostic claims."""

    unique_equilibrium_proved: bool
    delay_independent_no_closed_right_half_plane_roots_proved: bool
    local_exponential_equilibrium_stability_proved: bool
    post_pulse_vector_field_autonomous_by_definition: bool
    outer_periodic_candidate_computed: bool
    inner_periodic_candidate_computed: bool
    finite_monodromy_index_candidate_computed: bool
    finite_duration_pulse_endpoint_candidates_computed: bool
    a_kappa3_response_candidate_computed: bool
    outer_periodic_orbit_validated: bool
    inner_periodic_orbit_validated: bool
    rfde_floquet_indices_validated: bool
    history_space_separator_validated: bool
    finite_duration_physical_pulse_unique_onset_validated: bool
    frequency_amplitude_jacobian_invertibility_validated: bool
    three_output_local_diffeomorphism_proved: bool
    finite_network_lift_proved: bool
    dimension_uniform_network_basin_radius_proved: bool
    fixed_epsilon_leaky_canard_root_validated: bool
    canard_root_equals_physical_onset_proved: bool
    binary64_diagnostics_promoted_to_proof: bool
    constant_history_kick_substituted_for_physical_pulse: bool
    planar_annulus_claimed_as_rfde_history_space_separator: bool
    epsilon_used_as_final_frequency_amplitude_control_coordinate: bool


def _iadd(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def _ineg(value: Interval) -> Interval:
    return -value[1], -value[0]


def _imul(left: Interval, right: Interval) -> Interval:
    products = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return min(products), max(products)


def _iscale(factor: Fraction, value: Interval) -> Interval:
    return _imul((factor, factor), value)


def _isquare(value: Interval) -> Interval:
    lower, upper = value
    if lower >= 0:
        return lower * lower, upper * upper
    if upper <= 0:
        return upper * upper, lower * lower
    return Fraction(0), max(lower * lower, upper * upper)


def _interval_payload(value: Interval) -> dict[str, str]:
    return {
        "lower_fraction": str(value[0]),
        "upper_fraction": str(value[1]),
        "lower_decimal": format(float(value[0]), ".17g"),
        "upper_decimal": format(float(value[1]), ".17g"),
    }


@lru_cache(maxsize=1)
def exact_equilibrium_algebra() -> ExactEquilibriumAlgebra:
    """Return exact SymPy expressions for every characteristic symbol."""

    lam = sp.symbols("lambda")
    tau_0, tau_1 = sp.symbols("tau_0 tau_1", positive=True)
    epsilon = sp.Rational(EPSILON.numerator, EPSILON.denominator)
    unfolding = sp.Rational(UNFOLDING.numerator, UNFOLDING.denominator)
    recovery_leak = sp.Integer(1)
    kappa_1 = sp.Rational(KAPPA_1.numerator, KAPPA_1.denominator)
    kappa_3 = sp.Rational(KAPPA_3.numerator, KAPPA_3.denominator)
    alpha = sp.real_root(3 * unfolding, 3)
    recovery = sp.simplify(alpha - unfolding)
    delayed_gain = sp.simplify(
        epsilon * (kappa_1 + 3 * kappa_3 * (alpha - 1) ** 2)
    )
    current = sp.simplify(1 - alpha**2 - delayed_gain)
    delay_average = (
        sp.exp(-tau_0 * lam) + sp.exp(-tau_1 * lam)
    ) / 2
    characteristic = sp.expand(
        (lam - current - delayed_gain * delay_average) * (lam + epsilon)
        + epsilon
    )
    polynomial = sp.expand((lam - current) * (lam + epsilon) + epsilon)
    beta = sp.simplify(
        (epsilon - current) ** 2
        - 2 * epsilon * (1 - current)
        - delayed_gain**2
    )
    gamma = sp.simplify(
        epsilon**2 * ((1 - current) ** 2 - delayed_gain**2)
    )
    return ExactEquilibriumAlgebra(
        spectral_parameter=lam,
        delay_0=tau_0,
        delay_1=tau_1,
        epsilon=epsilon,
        unfolding=unfolding,
        recovery_leak=recovery_leak,
        kappa_1=kappa_1,
        kappa_3=kappa_3,
        equilibrium_voltage=alpha,
        equilibrium_recovery=recovery,
        delayed_gain=delayed_gain,
        current_coefficient=current,
        delay_average=delay_average,
        characteristic_determinant=characteristic,
        reference_polynomial=polynomial,
        beta=beta,
        gamma=gamma,
    )


@lru_cache(maxsize=1)
def build_equilibrium_stability_certificate() -> EquilibriumStabilityCertificate:
    """Build the exact rational interval certificate for Proposition 2.1."""

    target_cube = Fraction(3, 4)
    alpha: Interval = (ALPHA_LOWER, ALPHA_UPPER)
    one: Interval = (Fraction(1), Fraction(1))
    alpha_minus_one = _iadd(alpha, (Fraction(-1), Fraction(-1)))
    delay_gain = _iscale(
        EPSILON,
        _iadd(
            (KAPPA_1, KAPPA_1),
            _iscale(3 * KAPPA_3, _isquare(alpha_minus_one)),
        ),
    )
    current = _iadd(
        _iadd(one, _ineg(_isquare(alpha))),
        _ineg(delay_gain),
    )
    epsilon_minus_current = _iadd(
        (EPSILON, EPSILON), _ineg(current)
    )
    one_minus_current = _iadd(one, _ineg(current))
    beta = _iadd(
        _iadd(
            _isquare(epsilon_minus_current),
            _ineg(_iscale(2 * EPSILON, one_minus_current)),
        ),
        _ineg(_isquare(delay_gain)),
    )
    gamma = _iscale(
        EPSILON**2,
        _iadd(_isquare(one_minus_current), _ineg(_isquare(delay_gain))),
    )
    four_gamma_minus_beta_squared = _iadd(
        _iscale(Fraction(4), gamma), _ineg(_isquare(beta))
    )
    cube_strict = ALPHA_LOWER**3 < target_cube < ALPHA_UPPER**3
    hurwitz = (
        epsilon_minus_current[0] > 0 and one_minus_current[0] > 0
    )
    beta_negative = beta[1] < 0
    gamma_positive = gamma[0] > 0
    discriminant_margin = four_gamma_minus_beta_squared[0] > 0
    if not all(
        (
            cube_strict,
            hurwitz,
            beta_negative,
            gamma_positive,
            discriminant_margin,
        )
    ):
        raise ArithmeticError("an exact equilibrium-stability gate failed")
    return EquilibriumStabilityCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        epsilon=str(EPSILON),
        unfolding_a=str(UNFOLDING),
        recovery_leak_b=str(RECOVERY_LEAK),
        kappa_1=str(KAPPA_1),
        kappa_3=str(KAPPA_3),
        equilibrium_equation_formula="alpha^3=3*a=3/4",
        equilibrium_voltage_formula="alpha=(3/4)^(1/3)",
        equilibrium_recovery_formula="w_e=alpha-1/4",
        characteristic_determinant_formula=(
            "Delta(lambda)=(lambda-A-C*E(lambda))*(lambda+epsilon)+epsilon"
        ),
        reference_polynomial_formula=(
            "p(lambda)=(lambda-A)*(lambda+epsilon)+epsilon"
        ),
        beta_formula=(
            "beta=(epsilon-A)^2-2*epsilon*(1-A)-C^2"
        ),
        gamma_formula="gamma=epsilon^2*((1-A)^2-C^2)",
        d_polynomial_formula="D(r)=r^2+beta*r+gamma",
        alpha_interval=_interval_payload(alpha),
        effective_delay_gain_interval=_interval_payload(delay_gain),
        current_coefficient_interval=_interval_payload(current),
        epsilon_minus_current_interval=_interval_payload(
            epsilon_minus_current
        ),
        one_minus_current_interval=_interval_payload(one_minus_current),
        beta_interval=_interval_payload(beta),
        gamma_interval=_interval_payload(gamma),
        four_gamma_minus_beta_squared_interval=_interval_payload(
            four_gamma_minus_beta_squared
        ),
        cube_root_bracket_strict=True,
        unique_real_equilibrium_proved=True,
        base_polynomial_hurwitz_proved=True,
        beta_strictly_negative_proved=True,
        gamma_strictly_positive_proved=True,
        four_gamma_minus_beta_squared_strictly_positive_proved=True,
        d_positive_on_nonnegative_axis_proved=True,
        delay_average_bounded_by_one_on_closed_right_half_plane_proved=True,
        right_half_plane_small_gain_strictly_below_one_proved=True,
        characteristic_zero_free_on_closed_right_half_plane_proved=True,
        local_exponential_equilibrium_stability_proved=True,
    )


@lru_cache(maxsize=1)
def build_claim_ledger() -> AutonomousBistableClaimLedger:
    """Return the immutable analytic/candidate/open claim partition."""

    return AutonomousBistableClaimLedger(
        **{name: True for name in PROVED_FLAGS},
        **{name: True for name in CANDIDATE_FLAGS},
        **{name: False for name in OPEN_FLAGS},
        **{name: False for name in REFUSED_FLAGS},
    )


def json_ready_autonomous_bistable_audit() -> dict[str, Any]:
    """Return the canonical JSON-ready proof and scope audit."""

    return json.loads(
        json.dumps(
            {
                "equilibrium_certificate": asdict(
                    build_equilibrium_stability_certificate()
                ),
                "claim_ledger": asdict(build_claim_ledger()),
            }
        )
    )


def validate_autonomous_bistable_audit(payload: Mapping[str, Any]) -> None:
    """Reject algebra, scalar-type, or truth-status tampering."""

    if not isinstance(payload, Mapping):
        raise ValueError("audit payload must be a mapping")
    equilibrium = payload.get("equilibrium_certificate")
    ledger = payload.get("claim_ledger")
    if not isinstance(equilibrium, Mapping) or not isinstance(ledger, Mapping):
        raise ValueError("audit certificate or claim ledger is missing")
    expected_equilibrium = asdict(build_equilibrium_stability_certificate())
    expected_ledger = asdict(build_claim_ledger())
    if set(equilibrium) != set(expected_equilibrium):
        raise ValueError("equilibrium-certificate schema differs from reference")
    if set(ledger) != set(expected_ledger):
        raise ValueError("claim-ledger schema differs from reference")
    for key, expected_value in expected_equilibrium.items():
        value = equilibrium[key]
        if type(value) is not type(expected_value):
            raise ValueError(
                f"equilibrium-certificate field {key} has the wrong type"
            )
    for key, expected_value in expected_ledger.items():
        value = ledger[key]
        if type(value) is not type(expected_value):
            raise ValueError(f"claim-ledger field {key} has the wrong type")
    boolean_fields = {
        field.name
        for field in fields(AutonomousBistableClaimLedger)
        if field.type in (bool, "bool")
    }
    declared = PROVED_FLAGS | CANDIDATE_FLAGS | OPEN_FLAGS | REFUSED_FLAGS
    if boolean_fields != declared:
        raise AssertionError("the Boolean claim ledger does not cover its schema")
    if any(ledger.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("a proved equilibrium/autonomy flag was weakened")
    if any(ledger.get(name) is not True for name in CANDIDATE_FLAGS):
        raise ValueError("a computed candidate flag was deleted")
    if any(ledger.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open theorem gate was promoted")
    if any(ledger.get(name) is not False for name in REFUSED_FLAGS):
        raise ValueError("a refused interpretation was promoted")
    expected = json_ready_autonomous_bistable_audit()
    if dict(payload) != expected:
        raise ValueError("autonomous bistable audit differs from reference")


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _required_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"candidate evidence {key} is missing")
    return value


def _finite_candidate_number(
    payload: Mapping[str, Any], key: str, *, positive: bool = False
) -> float:
    raw = payload.get(key)
    if isinstance(raw, bool) or not isinstance(raw, (str, int, float)):
        raise ValueError(f"candidate field {key} is not a scalar number")
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"candidate field {key} is not numeric") from exc
    if not math.isfinite(value):
        raise ValueError(f"candidate field {key} is nonfinite")
    if positive and value <= 0.0:
        raise ValueError(f"candidate field {key} is not positive")
    return value


def _validate_endpoint_candidate(
    payload: Mapping[str, Any], expected_classification: str
) -> None:
    if payload.get("classification") != expected_classification:
        raise ValueError("a pulse endpoint classification changed")
    values = {
        key: _finite_candidate_number(payload, key)
        for key in (
            "final_time",
            "initial_voltage_kick",
            "pulse_amplitude",
            "pulse_duration",
            "tail_voltage_amplitude",
            "tail_voltage_maximum",
            "tail_voltage_minimum",
        )
    }
    if values["final_time"] <= 0.0 or values["tail_voltage_amplitude"] < 0.0:
        raise ValueError("a pulse endpoint time or amplitude is invalid")
    if values["tail_voltage_maximum"] < values["tail_voltage_minimum"]:
        raise ValueError("a pulse endpoint range is reversed")


def _validate_bracket_candidate(
    payload: Mapping[str, Any], key: str
) -> tuple[float, float]:
    bracket = payload.get(key)
    if not isinstance(bracket, list) or len(bracket) != 2:
        raise ValueError(f"candidate bracket {key} is malformed")
    holder = {"lower": bracket[0], "upper": bracket[1]}
    lower = _finite_candidate_number(holder, "lower")
    upper = _finite_candidate_number(holder, "upper")
    if not lower < upper:
        raise ValueError(f"candidate bracket {key} is not ordered")
    return lower, upper


def _validate_cycle_candidate(
    payload: Mapping[str, Any], expected_outside_count: int
) -> None:
    positive_keys = (
        "period",
        "frequency",
        "voltage_amplitude",
        "bordered_smallest_singular_value",
    )
    for key in positive_keys:
        _finite_candidate_number(payload, key, positive=True)
    nonnegative_keys = ("collocation_residual_inf", "oversampled_residual_inf")
    for key in nonnegative_keys:
        if _finite_candidate_number(payload, key) < 0.0:
            raise ValueError(f"candidate field {key} is negative")
    maximum = _finite_candidate_number(payload, "voltage_maximum")
    minimum = _finite_candidate_number(payload, "voltage_minimum")
    if not maximum > minimum:
        raise ValueError("a periodic-candidate voltage range is invalid")

    rows = payload.get("monodromy_diagnostic")
    if not isinstance(rows, list) or len(rows) < 3:
        raise ValueError("periodic-candidate monodromy evidence is missing")
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("a monodromy row is malformed")
        if row.get("observed_nontrivial_outside_unit_disk_count") != (
            expected_outside_count
        ):
            raise ValueError("a candidate monodromy index changed")
        for key in ("history_steps", "matrix_dimension", "step_count"):
            if _finite_candidate_number(row, key, positive=True) % 1.0 != 0.0:
                raise ValueError("a monodromy dimension is not integral")
        if _finite_candidate_number(row, "neutral_error_from_one") < 0.0:
            raise ValueError("a neutral-multiplier error is negative")
        neutral = row.get("neutral_multiplier")
        if not isinstance(neutral, list) or len(neutral) != 2:
            raise ValueError("a neutral multiplier is malformed")
        _finite_candidate_number(
            {"real": neutral[0]}, "real"
        )
        _finite_candidate_number(
            {"imag": neutral[1]}, "imag"
        )
        multipliers = row.get("leading_nontrivial_multipliers")
        if not isinstance(multipliers, list) or not multipliers:
            raise ValueError("leading multiplier evidence is missing")
        for multiplier in multipliers:
            if not isinstance(multiplier, Mapping):
                raise ValueError("a leading multiplier is malformed")
            for key in ("real", "imag", "modulus"):
                value = _finite_candidate_number(multiplier, key)
                if key == "modulus" and value < 0.0:
                    raise ValueError("a multiplier modulus is negative")


def validate_autonomous_bistable_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate the committed result, hashes, controls, and claim boundary."""

    if not isinstance(payload, Mapping):
        raise ValueError("result payload must be a mapping")
    audit = payload.get("audit")
    if not isinstance(audit, Mapping):
        raise ValueError("result audit is missing")
    validate_autonomous_bistable_audit(audit)
    if payload.get("proved_analytic_equilibrium_certificate") != audit.get(
        "equilibrium_certificate"
    ):
        raise ValueError("the analytic certificate was duplicated inconsistently")
    if payload.get("claim_status") != audit.get("claim_ledger"):
        raise ValueError("the result claim status differs from the strict ledger")

    response = _required_mapping(payload, "frequency_amplitude_response_candidate")
    pulse = _required_mapping(payload, "finite_duration_physical_pulse_diagnostic")
    kick = _required_mapping(payload, "constant_history_kick_diagnostic")
    ode = _required_mapping(payload, "ode_diagnostic")
    cycles = _required_mapping(payload, "rfde_periodic_candidates")

    for key in ("stable_cycle_period", "unstable_cycle_period"):
        _finite_candidate_number(ode, key, positive=True)
    if _finite_candidate_number(ode, "unstable_cycle_poincare_derivative") <= 1.0:
        raise ValueError("the ODE unstable-cycle candidate lost its expansion")
    _finite_candidate_number(ode, "unstable_cycle_section_recovery")

    outer = _required_mapping(cycles, "outer_pulse")
    inner = _required_mapping(cycles, "inner_saddle_candidate")
    _validate_cycle_candidate(outer, 0)
    _validate_cycle_candidate(inner, 1)

    _validate_bracket_candidate(kick, "candidate_onset_bracket")
    _validate_endpoint_candidate(
        _required_mapping(kick, "quiet_endpoint"), "quiet_candidate"
    )
    _validate_endpoint_candidate(
        _required_mapping(kick, "pulse_endpoint"), "pulse_candidate"
    )
    if kick.get("unique_threshold_validated") is not False:
        raise ValueError("a constant-kick bracket was promoted to onset proof")

    _validate_bracket_candidate(pulse, "candidate_onset_amplitude_bracket")
    _validate_endpoint_candidate(
        _required_mapping(pulse, "subthreshold_endpoint"), "quiet_candidate"
    )
    _validate_endpoint_candidate(
        _required_mapping(pulse, "suprathreshold_endpoint"), "pulse_candidate"
    )
    if response.get("controls") != ["unfolding_a", "kappa_3"]:
        raise ValueError("the final output controls are not (a,kappa_3)")
    if response.get("outputs") != ["frequency", "voltage_amplitude"]:
        raise ValueError("the response outputs changed")
    jacobian = response.get("jacobian")
    if (
        not isinstance(jacobian, list)
        or len(jacobian) != 2
        or any(not isinstance(row, list) or len(row) != 2 for row in jacobian)
    ):
        raise ValueError("the response Jacobian is malformed")
    for row in jacobian:
        for entry in row:
            _finite_candidate_number({"entry": entry}, "entry")
    singular_values = response.get("singular_values")
    if not isinstance(singular_values, list) or len(singular_values) != 2:
        raise ValueError("the response singular values are malformed")
    for entry in singular_values:
        _finite_candidate_number({"entry": entry}, "entry", positive=True)
    if _finite_candidate_number(response, "determinant") == 0.0:
        raise ValueError("the response candidate determinant vanished")
    for key in ("centered_difference_step", "kappa_3_centered_difference_step"):
        _finite_candidate_number(response, key, positive=True)
    if pulse.get("post_pulse_vector_field_autonomous") is not True:
        raise ValueError("post-pulse autonomy was weakened")
    if pulse.get("unique_threshold_validated") is not False:
        raise ValueError("a binary64 pulse bracket was promoted to onset proof")

    manifest = payload.get("manifest")
    if not isinstance(manifest, Mapping):
        raise ValueError("result manifest is missing")
    paths = {
        "generator": repository / GENERATOR_RELATIVE_PATH,
        "proof_source": repository / PROOF_SOURCE_RELATIVE_PATH,
        "note": repository / NOTE_RELATIVE_PATH,
    }
    expected_paths = {
        "generator": GENERATOR_RELATIVE_PATH,
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
    }
    for key, path in paths.items():
        if manifest.get(key) != expected_paths[key]:
            raise ValueError(f"the {key} relative path changed")
        if manifest.get(f"{key}_sha256") != _digest(path):
            raise ValueError(f"the {key} SHA-256 changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("the default replay command changed")
    if manifest.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("the arithmetic claim changed")
    if manifest.get("output_control_coordinates") != list(
        OUTPUT_CONTROL_COORDINATES
    ):
        raise ValueError("the three output-control coordinates changed")
    if not isinstance(manifest.get("python"), str) or not isinstance(
        manifest.get("platform"), str
    ):
        raise ValueError("runtime provenance is malformed")
