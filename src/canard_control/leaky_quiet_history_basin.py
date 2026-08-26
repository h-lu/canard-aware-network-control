"""Exact Razumikhin--Halanay basin for the leaky quiet equilibrium.

The spectral argument in :mod:`autonomous_leaky_recovery_bistable` proves
local exponential stability but gives no explicit history neighborhood.
This module supplies one.  Every numerical-looking constant below is a
``Fraction`` and every matrix inequality is reduced to exact rational signs.

The result is deliberately local.  It does not prove that a physical pulse
trajectory enters the ellipsoid, does not describe the outer periodic basin,
and does not identify an onset threshold.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from canard_control.autonomous_leaky_recovery_bistable import (
    ALPHA_LOWER,
    ALPHA_UPPER,
    EPSILON,
    KAPPA_3,
    MODEL_ID,
    PROOF_SOURCE_RELATIVE_PATH as EQUILIBRIUM_SOURCE_RELATIVE_PATH,
    build_equilibrium_stability_certificate,
)


SCHEMA_ID = "leaky-quiet-history-basin-razumikhin-v1"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_quiet_history_basin.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_quiet_history_basin.py"
NOTE_RELATIVE_PATH = "docs/leaky-quiet-history-basin.md"
RESULT_RELATIVE_PATH = "experiments/results/leaky_quiet_history_basin.json"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_quiet_history_basin.py"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    EQUILIBRIUM_SOURCE_RELATIVE_PATH,
)

# A simple rational Lyapunov matrix chosen near the exact solution of the
# nominal two-dimensional Lyapunov equation.
P11 = Fraction(2823, 100)
P12 = Fraction(-1351, 50)
P22 = Fraction(13759, 100)
P_LOWER = Fraction(21)
P_UPPER = Fraction(144)
P_FIRST_COLUMN_NORM_UPPER = Fraction(40)
Q_LOWER = Fraction(99, 100)
STATE_RADIUS = Fraction(1, 1000)
DECAY_RATE = Fraction(1, 10000)


def _fraction_record(value: Fraction) -> dict[str, str]:
    return {
        "fraction": str(value),
        "decimal": format(float(value), ".17g"),
    }


def _parse_fraction_record(
    value: Mapping[str, Any], name: str
) -> Fraction:
    if not isinstance(value, Mapping) or set(value) != {"fraction", "decimal"}:
        raise ValueError(f"{name} is not a rational record")
    exact = Fraction(str(value["fraction"]))
    if format(float(exact), ".17g") != value["decimal"]:
        raise ValueError(f"{name} decimal disagrees with its fraction")
    return exact


def _positive_definite_2x2(
    a11: Fraction, a12: Fraction, a22: Fraction
) -> bool:
    return a11 > 0 and a22 > 0 and a11 * a22 - a12 * a12 > 0


def _q_entries(current: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    """Return ``Q=-(A0^T P+P A0)`` for the current coefficient."""

    q11 = -2 * (current * P11 + EPSILON * P12)
    q12 = -(
        current * P12
        + EPSILON * P22
        - P11
        - EPSILON * P12
    )
    q22 = 2 * P12 + 2 * EPSILON * P22
    return q11, q12, q22


@dataclass(frozen=True)
class QuietHistoryBasinCertificate:
    """Exact data for the explicit local history-space basin theorem."""

    schema_id: str
    model_id: str
    perturbation_equation: str
    lyapunov_matrix: tuple[tuple[str, str], tuple[str, str]]
    equilibrium_voltage_lower: dict[str, str]
    equilibrium_voltage_upper: dict[str, str]
    current_coefficient_lower: dict[str, str]
    current_coefficient_upper: dict[str, str]
    delayed_linear_gain_upper: dict[str, str]
    state_radius: dict[str, str]
    p_lower: dict[str, str]
    p_upper: dict[str, str]
    p_first_column_norm_upper: dict[str, str]
    q_lower: dict[str, str]
    p_minus_lower_identity_determinant: dict[str, str]
    upper_identity_minus_p_determinant: dict[str, str]
    q_minus_lower_identity_determinant_lower: dict[str, str]
    nonlinear_current_gain_upper: dict[str, str]
    nonlinear_each_delay_gain_upper: dict[str, str]
    nonlinear_total_gain_upper: dict[str, str]
    halanay_current_coefficient_lower: dict[str, str]
    halanay_history_coefficient_upper: dict[str, str]
    halanay_eta_lower: dict[str, str]
    halanay_strict_margin_lower: dict[str, str]
    maximum_delay_upper: dict[str, str]
    decay_rate: dict[str, str]
    exponential_factor_upper: dict[str, str]
    decay_rate_margin_lower: dict[str, str]
    initial_history_lyapunov_sublevel: dict[str, str]
    exact_perturbation_identity_proved: bool
    rational_lyapunov_matrix_positive_definite_proved: bool
    uniform_current_dissipation_proved: bool
    nonlinear_history_gain_proved: bool
    strict_halanay_margin_proved: bool
    explicit_history_ellipsoid_forward_invariant_proved: bool
    explicit_exponential_decay_rate_proved: bool
    quiet_local_history_basin_validated: bool
    pulse_J_030_enters_quiet_ball_validated: bool
    global_quiet_basin_validated: bool
    history_space_separator_validated: bool
    physical_pulse_onset_validated: bool


def build_quiet_history_basin_certificate() -> QuietHistoryBasinCertificate:
    """Construct the exact rational certificate.

    For ``z=(v-alpha,w-alpha+a)``, write the perturbation equation as

    ``z'=A0 z + (C/2)e1(x_tau0+x_tau1) + e1*N``.

    The nonlinear remainder is bounded on the Euclidean radius ``R`` by
    ``L(R)`` times the largest current/delayed state norm.
    """

    parent = build_equilibrium_stability_certificate()
    current_lower = Fraction(
        parent.current_coefficient_interval["lower_fraction"]
    )
    current_upper = Fraction(
        parent.current_coefficient_interval["upper_fraction"]
    )
    delayed_gain_upper = Fraction(
        parent.effective_delay_gain_interval["upper_fraction"]
    )

    # P_LOWER I < P < P_UPPER I.
    lower_det = (
        (P11 - P_LOWER) * (P22 - P_LOWER) - P12 * P12
    )
    upper_det = (
        (P_UPPER - P11) * (P_UPPER - P22) - P12 * P12
    )
    if not _positive_definite_2x2(
        P11 - P_LOWER, P12, P22 - P_LOWER
    ):
        raise ArithmeticError("the lower Lyapunov matrix bound failed")
    if not _positive_definite_2x2(
        P_UPPER - P11, -P12, P_UPPER - P22
    ):
        raise ArithmeticError("the upper Lyapunov matrix bound failed")
    if P11 * P11 + P12 * P12 >= P_FIRST_COLUMN_NORM_UPPER**2:
        raise ArithmeticError("the first-column norm bound failed")

    # Q(A)-Q_LOWER I is enclosed for the entire exact A interval.
    q_lower_entries = _q_entries(current_lower)
    q_upper_entries = _q_entries(current_upper)
    q11_lower = min(q_lower_entries[0], q_upper_entries[0])
    q22 = q_lower_entries[2]
    if q22 != q_upper_entries[2]:
        raise ArithmeticError("the recovery dissipation unexpectedly varies")
    q12_abs_upper = max(
        abs(q_lower_entries[1]), abs(q_upper_entries[1])
    )
    q_shift_det_lower = (
        (q11_lower - Q_LOWER) * (q22 - Q_LOWER)
        - q12_abs_upper * q12_abs_upper
    )
    if not (
        q11_lower > Q_LOWER
        and q22 > Q_LOWER
        and q_shift_det_lower > 0
    ):
        raise ArithmeticError("uniform current dissipation failed")

    beta_abs_upper = max(
        abs(ALPHA_LOWER - 1), abs(ALPHA_UPPER - 1)
    )
    current_nonlinear_gain = (
        ALPHA_UPPER + 3 * EPSILON * KAPPA_3 * beta_abs_upper
    ) * STATE_RADIUS + (
        Fraction(1, 3) + EPSILON * KAPPA_3
    ) * STATE_RADIUS**2
    each_delay_nonlinear_gain = (
        3 * EPSILON * KAPPA_3 * beta_abs_upper / 2
    ) * STATE_RADIUS + (
        EPSILON * KAPPA_3 / 2
    ) * STATE_RADIUS**2
    nonlinear_total_gain = (
        current_nonlinear_gain + 2 * each_delay_nonlinear_gain
    )

    # V' <= -(a-b)V + b sup_[t-r,t] V.
    halanay_a = Q_LOWER / P_UPPER
    halanay_b = (
        P_FIRST_COLUMN_NORM_UPPER
        * (delayed_gain_upper + nonlinear_total_gain)
        / P_LOWER
    )
    halanay_eta = halanay_a - halanay_b
    halanay_margin = halanay_eta - halanay_b
    if halanay_margin <= 0:
        raise ArithmeticError("the strict Halanay margin failed")

    # sqrt(5)<9/4, hence tau_1=5sqrt(5)<45/4.  For x=9/8000,
    # exp(x)<=1/(1-x)=8000/7991.
    maximum_delay_upper = Fraction(45, 4)
    exponential_factor_upper = Fraction(8000, 7991)
    if DECAY_RATE * maximum_delay_upper != Fraction(9, 8000):
        raise ArithmeticError("the delay-rate product changed")
    decay_margin = (
        halanay_eta
        - DECAY_RATE
        - halanay_b * exponential_factor_upper
    )
    if decay_margin <= 0:
        raise ArithmeticError("the explicit exponential rate failed")

    history_sublevel = P_LOWER * STATE_RADIUS**2
    return QuietHistoryBasinCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        perturbation_equation=(
            "z'=A0*z+(C/2)*e1*(x_tau0+x_tau1)+e1*N; "
            "A0=[[A,-1],[1/5,-1/5]]"
        ),
        lyapunov_matrix=(
            (str(P11), str(P12)),
            (str(P12), str(P22)),
        ),
        equilibrium_voltage_lower=_fraction_record(ALPHA_LOWER),
        equilibrium_voltage_upper=_fraction_record(ALPHA_UPPER),
        current_coefficient_lower=_fraction_record(current_lower),
        current_coefficient_upper=_fraction_record(current_upper),
        delayed_linear_gain_upper=_fraction_record(delayed_gain_upper),
        state_radius=_fraction_record(STATE_RADIUS),
        p_lower=_fraction_record(P_LOWER),
        p_upper=_fraction_record(P_UPPER),
        p_first_column_norm_upper=_fraction_record(
            P_FIRST_COLUMN_NORM_UPPER
        ),
        q_lower=_fraction_record(Q_LOWER),
        p_minus_lower_identity_determinant=_fraction_record(lower_det),
        upper_identity_minus_p_determinant=_fraction_record(upper_det),
        q_minus_lower_identity_determinant_lower=_fraction_record(
            q_shift_det_lower
        ),
        nonlinear_current_gain_upper=_fraction_record(
            current_nonlinear_gain
        ),
        nonlinear_each_delay_gain_upper=_fraction_record(
            each_delay_nonlinear_gain
        ),
        nonlinear_total_gain_upper=_fraction_record(nonlinear_total_gain),
        halanay_current_coefficient_lower=_fraction_record(halanay_a),
        halanay_history_coefficient_upper=_fraction_record(halanay_b),
        halanay_eta_lower=_fraction_record(halanay_eta),
        halanay_strict_margin_lower=_fraction_record(halanay_margin),
        maximum_delay_upper=_fraction_record(maximum_delay_upper),
        decay_rate=_fraction_record(DECAY_RATE),
        exponential_factor_upper=_fraction_record(exponential_factor_upper),
        decay_rate_margin_lower=_fraction_record(decay_margin),
        initial_history_lyapunov_sublevel=_fraction_record(history_sublevel),
        exact_perturbation_identity_proved=True,
        rational_lyapunov_matrix_positive_definite_proved=True,
        uniform_current_dissipation_proved=True,
        nonlinear_history_gain_proved=True,
        strict_halanay_margin_proved=True,
        explicit_history_ellipsoid_forward_invariant_proved=True,
        explicit_exponential_decay_rate_proved=True,
        quiet_local_history_basin_validated=True,
        pulse_J_030_enters_quiet_ball_validated=False,
        global_quiet_basin_validated=False,
        history_space_separator_validated=False,
        physical_pulse_onset_validated=False,
    )


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_quiet_history_basin_result(repository: Path) -> dict[str, Any]:
    certificate = asdict(build_quiet_history_basin_certificate())
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic": (
                "exact Python Fraction signs; no floating-point value enters "
                "a theorem inequality"
            ),
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
        },
    }


def validate_quiet_history_basin_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Recompute the theorem and reject source or claim tampering."""

    if set(payload) != {"certificate", "manifest"}:
        raise ValueError("quiet-basin result has the wrong outer schema")
    expected = json.loads(
        json.dumps(asdict(build_quiet_history_basin_certificate()))
    )
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping):
        raise ValueError("quiet-basin certificate is missing")
    normalized_certificate = json.loads(json.dumps(certificate))
    if normalized_certificate != expected:
        raise ValueError("quiet-basin certificate differs from exact replay")
    if not isinstance(manifest, Mapping):
        raise ValueError("quiet-basin manifest is missing")
    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic",
        "certificate_sha256",
        "source_sha256",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("quiet-basin manifest has missing or unknown fields")
    expected_manifest_scalars = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic": (
            "exact Python Fraction signs; no floating-point value enters "
            "a theorem inequality"
        ),
        "certificate_sha256": canonical_sha256(certificate),
    }
    for name, expected_value in expected_manifest_scalars.items():
        if manifest.get(name) != expected_value:
            raise ValueError(f"quiet-basin manifest {name} changed")
    hashes = manifest.get("source_sha256")
    if not isinstance(hashes, Mapping) or set(hashes) != set(SOURCE_MANIFEST):
        raise ValueError("quiet-basin source manifest changed")
    for relative in SOURCE_MANIFEST:
        if hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"quiet-basin source hash changed for {relative}")
    # Exercise every rational record through its exact decimal consistency.
    for name, value in normalized_certificate.items():
        if isinstance(value, Mapping) and set(value) == {"fraction", "decimal"}:
            _parse_fraction_record(value, name)


__all__ = [
    "DECAY_RATE",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "P11",
    "P12",
    "P22",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATE_RADIUS",
    "QuietHistoryBasinCertificate",
    "build_quiet_history_basin_certificate",
    "build_quiet_history_basin_result",
    "canonical_sha256",
    "validate_quiet_history_basin_result",
]
