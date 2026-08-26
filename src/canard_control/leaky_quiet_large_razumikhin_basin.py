"""Large directed Razumikhin basin for the leaky quiet equilibrium.

The small rational Halanay ball in :mod:`leaky_quiet_history_basin` uses a
global norm bound on the nonlinear remainder.  Here the same quadratic form
is evaluated on its ellipsoidal level sets.  Completing the square gives an
exact angular parameterization, while monotonicity of the delayed coupling
reduces each delayed voltage to one of two endpoints.  A directed angular
cover and a degree-two Bernstein bound in the radial variable then prove a
much larger complete-history basin.

Only the autonomous quiet basin is proved.  Entry of the physical ``J=.30``
pulse is a separate validated-integration gate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2
import sympy as sp

from canard_control.autonomous_leaky_recovery_bistable import (
    EPSILON,
    KAPPA_1,
    KAPPA_3,
    UNFOLDING,
)
from canard_control.directed_interval import (
    DirectedInterval,
    cos_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    sin_interval,
)
from canard_control.leaky_quiet_history_basin import (
    P11,
    P12,
    P22,
    RESULT_RELATIVE_PATH as SMALL_BASIN_RESULT_RELATIVE_PATH,
    validate_quiet_history_basin_result,
)


SCHEMA_ID = "leaky-quiet-large-razumikhin-basin-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_quiet_large_razumikhin_basin.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_quiet_large_razumikhin_basin.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-quiet-large-razumikhin-basin.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_quiet_large_razumikhin_basin.json"
)
INTERVAL_SOURCE_RELATIVE_PATH = "src/canard_control/directed_interval.py"
SMALL_BASIN_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_quiet_history_basin.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_quiet_large_razumikhin_basin.py"
)
MANIFEST_ARITHMETIC = (
    "exact rational/SymPy algebra and 160-bit outward-rounded MPFR; "
    "16384-cell directed angular cover; exact degree-two Bernstein "
    "radial bound"
)

PRECISION_BITS = 160
ANGULAR_CELL_COUNT = 16384
HISTORY_SUBLEVEL = Fraction(1, 125)
RAZUMIKHIN_RATIO = Fraction(101, 100)
DECAY_RATE = Fraction(1, 10000)
PHYSICAL_DELAY_MULTIPLIERS = (4, 5)
MAXIMUM_DELAY_UPPER = Fraction(45, 4)
EXPONENTIAL_DELAY_FACTOR_UPPER = Fraction(8000, 7991)

TRUE_FLAGS = (
    "exact_elliptic_boundary_parameterization_proved",
    "exact_radial_reduction_proved",
    "exact_two_delayed_slot_reduction_proved",
    "equilibrium_cuberoot_enclosure_proved",
    "delayed_voltage_endpoint_reduction_proved",
    "directed_angular_cover_validated",
    "strict_razumikhin_derivative_margin_proved",
    "first_maximum_razumikhin_argument_proved",
    "large_history_ellipsoid_forward_invariant_proved",
    "large_history_ellipsoid_exponential_decay_proved",
    "large_quiet_history_basin_validated",
)

FALSE_FLAGS = (
    "pulse_J_030_enters_large_quiet_ball_validated",
    "global_quiet_basin_validated",
    "history_space_separator_validated",
    "physical_pulse_onset_validated",
)


def _interval_fraction(value: Fraction, precision: int) -> DirectedInterval:
    return (
        DirectedInterval.from_decimal(value.numerator, precision)
        / DirectedInterval.from_decimal(value.denominator, precision)
    )


def _alpha_interval(precision: int) -> DirectedInterval:
    """Return an outward MPFR enclosure of ``(3/4)^(1/3)``."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower = gmpy2.cbrt(gmpy2.mpfr(3) / gmpy2.mpfr(4))
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        upper = gmpy2.cbrt(gmpy2.mpfr(3) / gmpy2.mpfr(4))
    return DirectedInterval(lower, upper, precision)


def _lower_text(value: gmpy2.mpfr, digits: int = 55) -> str:
    return decimal_lower(value, digits)


def _upper_text(value: gmpy2.mpfr, digits: int = 55) -> str:
    return decimal_upper(value, digits)


@lru_cache(maxsize=1)
def exact_large_basin_defects() -> tuple[sp.Expr, ...]:
    """Audit the ellipse, radial scaling, and both delayed slots exactly."""

    q, x_template, y_template, d_0, d_1, d = sp.symbols(
        "q X Y D_0 D_1 D", real=True
    )
    cosine, sine = sp.symbols("c_theta s_theta", real=True)
    alpha = sp.symbols("alpha", positive=True, real=True)
    epsilon = sp.Rational(EPSILON.numerator, EPSILON.denominator)
    kappa_1 = sp.Rational(KAPPA_1.numerator, KAPPA_1.denominator)
    kappa_3 = sp.Rational(KAPPA_3.numerator, KAPPA_3.denominator)
    sublevel = sp.Rational(
        HISTORY_SUBLEVEL.numerator, HISTORY_SUBLEVEL.denominator
    )
    p11 = sp.Rational(P11.numerator, P11.denominator)
    p12 = sp.Rational(P12.numerator, P12.denominator)
    p22 = sp.Rational(P22.numerator, P22.denominator)
    determinant = p11 * p22 - p12**2
    matrix = sp.Matrix([[p11, p12], [p12, p22]])

    voltage_radius = sp.sqrt(sublevel * p22 / determinant)
    recovery_radius = sp.sqrt(sublevel / p22)
    boundary_x = voltage_radius * cosine
    boundary_y = -(p12 / p22) * boundary_x + recovery_radius * sine
    elliptic_defect = sp.simplify(
        sp.Matrix([boundary_x, boundary_y]).dot(
            matrix * sp.Matrix([boundary_x, boundary_y])
        )
        - sublevel * (cosine**2 + sine**2)
    )

    x = q * x_template
    y = q * y_template
    beta = alpha - 1

    fast_two_slots = (
        (1 - alpha**2) * x
        - alpha * x**2
        - x**3 / 3
        - y
        + epsilon * kappa_1 * (q * (d_0 + d_1) / 2 - x)
        + epsilon
        * kappa_3
        * (
            ((beta + q * d_0) ** 3 + (beta + q * d_1) ** 3) / 2
            - (beta + x) ** 3
        )
    )
    normalized_two_slots = (
        (1 - alpha**2) * x_template
        - y_template
        + epsilon
        * (kappa_1 + 3 * kappa_3 * beta**2)
        * ((d_0 + d_1) / 2 - x_template)
        + q
        * (
            -alpha * x_template**2
            + 3
            * epsilon
            * kappa_3
            * beta
            * ((d_0**2 + d_1**2) / 2 - x_template**2)
        )
        + q**2
        * (
            -x_template**3 / 3
            + epsilon
            * kappa_3
            * ((d_0**3 + d_1**3) / 2 - x_template**3)
        )
    )
    normalized_common_endpoint = (
        (1 - alpha**2) * x_template
        - y_template
        + epsilon
        * (kappa_1 + 3 * kappa_3 * beta**2)
        * (d - x_template)
        + q
        * (
            -alpha * x_template**2
            + 3
            * epsilon
            * kappa_3
            * beta
            * (d**2 - x_template**2)
        )
        + q**2
        * (
            -x_template**3 / 3
            + epsilon * kappa_3 * (d**3 - x_template**3)
        )
    )
    delayed_profile = (
        kappa_1 * d
        + kappa_3
        * (3 * beta**2 * d + 3 * beta * q * d**2 + q**2 * d**3)
    )
    delayed_derivative = sp.diff(delayed_profile, d)
    expected_derivative = (
        kappa_1 + 3 * kappa_3 * (beta + q * d) ** 2
    )
    z = sp.Matrix([x, y])
    template = sp.Matrix([x_template, y_template])
    radial_defect = sp.expand(
        z.dot(matrix * z) - q**2 * template.dot(matrix * template)
    )
    pz_1 = p11 * x_template + p12 * y_template
    pz_2 = p12 * x_template + p22 * y_template
    normalized_v_derivative = (
        pz_1 * normalized_two_slots
        + pz_2 * epsilon * (x_template - y_template)
    )
    full_v_derivative = 2 * (q * pz_1) * fast_two_slots + 2 * (
        q * pz_2
    ) * (epsilon * q * (x_template - y_template))
    return (
        elliptic_defect,
        radial_defect,
        sp.expand(fast_two_slots - q * normalized_two_slots),
        sp.expand(
            normalized_two_slots.subs({d_0: d, d_1: d})
            - normalized_common_endpoint
        ),
        sp.expand(delayed_derivative - expected_derivative),
        sp.expand(
            full_v_derivative - 2 * q**2 * normalized_v_derivative
        ),
    )


@dataclass(frozen=True)
class LargeQuietBasinCertificate:
    schema_id: str
    model_id: str
    precision_bits: int
    angular_cell_count: int
    lyapunov_matrix: tuple[tuple[str, str], tuple[str, str]]
    equilibrium_voltage_lower: str
    equilibrium_voltage_upper: str
    physical_delays: tuple[str, str]
    history_sublevel: str
    previous_history_sublevel: str
    sublevel_enlargement_factor: str
    razumikhin_ratio: str
    decay_rate: str
    maximum_delay_upper: str
    exponential_delay_factor_upper: str
    exponential_ratio_margin_lower: str
    voltage_template_radius_lower: str
    voltage_template_radius_upper: str
    recovery_template_radius_lower: str
    recovery_template_radius_upper: str
    maximum_normalized_derivative_upper: str
    strict_normalized_derivative_margin_lower: str
    derivative_rate_lower: str
    decay_rate_margin_lower: str
    maximizing_angular_cell: int
    ambiguous_endpoint_cell_count: int
    exact_symbolic_zero_defect_count: int
    theorem_statement: str
    exact_elliptic_boundary_parameterization_proved: bool
    exact_radial_reduction_proved: bool
    exact_two_delayed_slot_reduction_proved: bool
    equilibrium_cuberoot_enclosure_proved: bool
    delayed_voltage_endpoint_reduction_proved: bool
    directed_angular_cover_validated: bool
    strict_razumikhin_derivative_margin_proved: bool
    first_maximum_razumikhin_argument_proved: bool
    large_history_ellipsoid_forward_invariant_proved: bool
    large_history_ellipsoid_exponential_decay_proved: bool
    large_quiet_history_basin_validated: bool
    pulse_J_030_enters_large_quiet_ball_validated: bool
    global_quiet_basin_validated: bool
    history_space_separator_validated: bool
    physical_pulse_onset_validated: bool


@lru_cache(maxsize=1)
def build_large_quiet_basin_certificate(
    *,
    precision: int = PRECISION_BITS,
    angular_cell_count: int = ANGULAR_CELL_COUNT,
) -> LargeQuietBasinCertificate:
    """Run the directed angular/radial Razumikhin cover."""

    if precision != PRECISION_BITS:
        raise ValueError("the theorem precision is pinned at 160 bits")
    if angular_cell_count != ANGULAR_CELL_COUNT:
        raise ValueError("the theorem angular cover is pinned at 16384 cells")
    defects = exact_large_basin_defects()
    if defects != (0,) * len(defects):
        raise AssertionError("the exact radial reduction changed")

    point = lambda value: DirectedInterval.from_decimal(value, precision)
    alpha = _alpha_interval(precision)
    alpha_lower_numerator, alpha_lower_denominator = (
        alpha.lower.as_integer_ratio()
    )
    alpha_upper_numerator, alpha_upper_denominator = (
        alpha.upper.as_integer_ratio()
    )
    alpha_lower_exact = Fraction(
        int(alpha_lower_numerator), int(alpha_lower_denominator)
    )
    alpha_upper_exact = Fraction(
        int(alpha_upper_numerator), int(alpha_upper_denominator)
    )
    target_cube = Fraction(3, 4)
    if not (
        alpha_lower_exact**3 < target_cube < alpha_upper_exact**3
    ):
        raise ArithmeticError("the directed equilibrium cuberoot failed")

    maximum_delay_multiplier = max(PHYSICAL_DELAY_MULTIPLIERS)
    if not (
        maximum_delay_multiplier > 0
        and maximum_delay_multiplier**2 * 5 < MAXIMUM_DELAY_UPPER**2
    ):
        raise ArithmeticError("the exact physical-delay upper bound failed")
    delay_rate_product = DECAY_RATE * MAXIMUM_DELAY_UPPER
    if delay_rate_product != Fraction(9, 8000):
        raise ArithmeticError("the delay-rate product changed")
    if EXPONENTIAL_DELAY_FACTOR_UPPER != 1 / (1 - delay_rate_product):
        raise ArithmeticError("the rational exponential majorant changed")
    if EXPONENTIAL_DELAY_FACTOR_UPPER >= RAZUMIKHIN_RATIO:
        raise ArithmeticError("the Razumikhin ratio no longer dominates")

    beta = alpha - 1
    epsilon = _interval_fraction(EPSILON, precision)
    kappa_1 = _interval_fraction(KAPPA_1, precision)
    kappa_3 = _interval_fraction(KAPPA_3, precision)
    p11 = _interval_fraction(P11, precision)
    p12 = _interval_fraction(P12, precision)
    p22 = _interval_fraction(P22, precision)
    determinant = p11 * p22 - p12**2
    sublevel = _interval_fraction(HISTORY_SUBLEVEL, precision)
    ratio = _interval_fraction(RAZUMIKHIN_RATIO, precision)
    voltage_radius = (sublevel * p22 / determinant).sqrt()
    recovery_radius = (sublevel / p22).sqrt()
    delayed_voltage_radius = voltage_radius * ratio.sqrt()
    full_delayed_voltage = DirectedInterval(
        (-delayed_voltage_radius).lower,
        delayed_voltage_radius.upper,
        precision,
    )

    two_pi = point(2) * pi_interval(precision)
    largest_upper: gmpy2.mpfr | None = None
    maximizing_cell = -1
    ambiguous = 0
    for index in range(angular_cell_count):
        angular_fraction = DirectedInterval.from_bounds(
            _interval_fraction(Fraction(index, angular_cell_count), precision).lower,
            _interval_fraction(
                Fraction(index + 1, angular_cell_count), precision
            ).upper,
            precision,
        )
        angle = two_pi * angular_fraction
        x_template = voltage_radius * cos_interval(angle)
        y_template = (
            -(p12 / p22) * x_template
            + recovery_radius * sin_interval(angle)
        )
        pz_1 = p11 * x_template + p12 * y_template
        pz_2 = p12 * x_template + p22 * y_template
        if pz_1.lower >= 0:
            delayed_template = delayed_voltage_radius
        elif pz_1.upper <= 0:
            delayed_template = -delayed_voltage_radius
        else:
            delayed_template = full_delayed_voltage
            ambiguous += 1

        fast_0 = (
            (1 - alpha**2) * x_template
            - y_template
            + epsilon
            * (kappa_1 + 3 * kappa_3 * beta**2)
            * (delayed_template - x_template)
        )
        fast_1 = (
            -alpha * x_template**2
            + 3
            * epsilon
            * kappa_3
            * beta
            * (delayed_template**2 - x_template**2)
        )
        fast_2 = (
            -(x_template**3) / 3
            + epsilon
            * kappa_3
            * (delayed_template**3 - x_template**3)
        )
        coefficient_0 = (
            pz_1 * fast_0
            + pz_2 * epsilon * (x_template - y_template)
        )
        coefficient_1 = pz_1 * fast_1
        coefficient_2 = pz_1 * fast_2

        # Power coefficients c0+c1*q+c2*q^2 converted exactly to the
        # Bernstein coefficients on 0<=q<=1.
        bernstein_0 = coefficient_0
        bernstein_1 = coefficient_0 + coefficient_1 / 2
        bernstein_2 = coefficient_0 + coefficient_1 + coefficient_2
        upper = max(
            bernstein_0.upper,
            bernstein_1.upper,
            bernstein_2.upper,
        )
        if largest_upper is None or upper > largest_upper:
            largest_upper = upper
            maximizing_cell = index

    if largest_upper is None or largest_upper >= 0:
        raise ArithmeticError("the large Razumikhin angular cover did not close")
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        normalized_margin = -largest_upper
        derivative_rate = 2 * normalized_margin / sublevel.upper
        decay_rate = gmpy2.mpfr(DECAY_RATE.numerator) / DECAY_RATE.denominator
        decay_margin = derivative_rate - decay_rate
        exponential_ratio_margin = (
            gmpy2.mpfr(RAZUMIKHIN_RATIO.numerator)
            / RAZUMIKHIN_RATIO.denominator
            - gmpy2.mpfr(EXPONENTIAL_DELAY_FACTOR_UPPER.numerator)
            / EXPONENTIAL_DELAY_FACTOR_UPPER.denominator
        )
    if derivative_rate <= decay_rate or exponential_ratio_margin <= 0:
        raise ArithmeticError("the explicit Razumikhin decay rate did not close")

    previous = Fraction(21, 1_000_000)
    return LargeQuietBasinCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        precision_bits=precision,
        angular_cell_count=angular_cell_count,
        lyapunov_matrix=((str(P11), str(P12)), (str(P12), str(P22))),
        equilibrium_voltage_lower=_lower_text(alpha.lower),
        equilibrium_voltage_upper=_upper_text(alpha.upper),
        physical_delays=("4*sqrt(5)", "5*sqrt(5)"),
        history_sublevel=str(HISTORY_SUBLEVEL),
        previous_history_sublevel=str(previous),
        sublevel_enlargement_factor=str(HISTORY_SUBLEVEL / previous),
        razumikhin_ratio=str(RAZUMIKHIN_RATIO),
        decay_rate=str(DECAY_RATE),
        maximum_delay_upper=str(MAXIMUM_DELAY_UPPER),
        exponential_delay_factor_upper=str(
            EXPONENTIAL_DELAY_FACTOR_UPPER
        ),
        exponential_ratio_margin_lower=_lower_text(exponential_ratio_margin),
        voltage_template_radius_lower=_lower_text(voltage_radius.lower),
        voltage_template_radius_upper=_upper_text(voltage_radius.upper),
        recovery_template_radius_lower=_lower_text(recovery_radius.lower),
        recovery_template_radius_upper=_upper_text(recovery_radius.upper),
        maximum_normalized_derivative_upper=_upper_text(largest_upper),
        strict_normalized_derivative_margin_lower=_lower_text(
            normalized_margin
        ),
        derivative_rate_lower=_lower_text(derivative_rate),
        decay_rate_margin_lower=_lower_text(decay_margin),
        maximizing_angular_cell=maximizing_cell,
        ambiguous_endpoint_cell_count=ambiguous,
        exact_symbolic_zero_defect_count=len(defects),
        theorem_statement=(
            "for delays (4*sqrt(5),5*sqrt(5)), if "
            "sup_{theta in [-5*sqrt(5),0]} "
            "(phi(theta)-E_q)^T P (phi(theta)-E_q)<=1/125, "
            "then V(z(t))<=exp(-t/10000)*sup_history V"
        ),
        **{name: True for name in TRUE_FLAGS},
        **{name: False for name in FALSE_FLAGS},
    )


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    ).hexdigest()


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_large_quiet_basin_result(repository: Path) -> dict[str, Any]:
    parent_path = repository / SMALL_BASIN_RESULT_RELATIVE_PATH
    parent_payload = json.loads(parent_path.read_text(encoding="utf-8"))
    validate_quiet_history_basin_result(parent_payload, repository)
    certificate = asdict(build_large_quiet_basin_certificate())
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "interval_source": INTERVAL_SOURCE_RELATIVE_PATH,
        "small_basin_source": SMALL_BASIN_SOURCE_RELATIVE_PATH,
    }
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic": MANIFEST_ARITHMETIC,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.__version__,
            "mpfr": gmpy2.mpfr_version(),
            "sympy": sp.__version__,
            "certificate_sha256": canonical_sha256(certificate),
            "small_basin_result": SMALL_BASIN_RESULT_RELATIVE_PATH,
            "small_basin_result_sha256": _sha256_path(parent_path),
            "source_sha256": {
                name: _sha256_path(repository / relative)
                for name, relative in sources.items()
            },
            **sources,
        },
    }


def validate_large_quiet_basin_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("large quiet-basin result has the wrong outer schema")
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("large quiet-basin records must be mappings")
    if set(certificate) != {
        field.name for field in fields(LargeQuietBasinCertificate)
    }:
        raise ValueError("large quiet-basin certificate schema changed")
    expected_certificate = json.loads(
        json.dumps(asdict(build_large_quiet_basin_certificate()))
    )
    normalized_certificate = json.loads(json.dumps(certificate))
    for name, expected_value in expected_certificate.items():
        if type(normalized_certificate.get(name)) is not type(expected_value):
            raise ValueError(
                f"large quiet-basin certificate {name} has the wrong type"
            )
    if normalized_certificate != expected_certificate:
        raise ValueError("large quiet-basin certificate differs from replay")
    if any(certificate.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved large-basin flag was weakened")
    if any(certificate.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open pulse/onset flag was promoted")

    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "interval_source": INTERVAL_SOURCE_RELATIVE_PATH,
        "small_basin_source": SMALL_BASIN_SOURCE_RELATIVE_PATH,
    }
    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic",
        "python",
        "platform",
        "gmpy2",
        "mpfr",
        "sympy",
        "certificate_sha256",
        "small_basin_result",
        "small_basin_result_sha256",
        "source_sha256",
        *sources,
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("large quiet-basin manifest schema changed")
    scalar_expected = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic": MANIFEST_ARITHMETIC,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gmpy2": gmpy2.__version__,
        "mpfr": gmpy2.mpfr_version(),
        "sympy": sp.__version__,
        "small_basin_result": SMALL_BASIN_RESULT_RELATIVE_PATH,
    }
    for name, expected in scalar_expected.items():
        if manifest.get(name) != expected:
            raise ValueError(f"large quiet-basin manifest {name} changed")
    if manifest.get("certificate_sha256") != canonical_sha256(
        normalized_certificate
    ):
        raise ValueError("large quiet-basin certificate digest changed")
    parent_path = repository / SMALL_BASIN_RESULT_RELATIVE_PATH
    if manifest.get("small_basin_result_sha256") != _sha256_path(parent_path):
        raise ValueError("large quiet-basin parent result hash changed")
    parent_payload = json.loads(parent_path.read_text(encoding="utf-8"))
    validate_quiet_history_basin_result(parent_payload, repository)
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(sources):
        raise ValueError("large quiet-basin source hash schema changed")
    for name, relative in sources.items():
        if manifest.get(name) != relative:
            raise ValueError(f"large quiet-basin {name} path changed")
        if source_hashes.get(name) != _sha256_path(repository / relative):
            raise ValueError(f"large quiet-basin {name} hash changed")
