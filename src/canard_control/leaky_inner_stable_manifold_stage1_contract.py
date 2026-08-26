"""Stage-1 contract for a quantitative inner stable manifold.

The already validated inner Floquet count makes the inner periodic orbit
hyperbolic, with one unstable multiplier after the autonomous phase has been
removed.  A standard RFDE stable-manifold theorem therefore gives a
qualitative codimension-one local stable manifold.  This module records that
qualitative consequence separately from the constants needed to enclose a
stable graph on the physical-pulse scale.

The quantitative part is an executable Lyapunov--Perron majorant for the
phase-fixed Poincare map.  Missing spectral-gap, projection, dichotomy,
section, return-map C2, nonlinear-remainder, and neighborhood bounds are
represented by ``None`` and force every quantitative/onset claim to remain
false.  A complete *design budget* is also evaluated, but is explicitly not
evidence for this RFDE.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import (
    Decimal,
    InvalidOperation,
    ROUND_CEILING,
    ROUND_FLOOR,
    localcontext,
)
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA_ID = "leaky-inner-stable-manifold-stage1-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_stable_manifold_stage1_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_stable_manifold_stage1_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage1_contract.json"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-inner-stable-manifold-stage1-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_stable_manifold_stage1_contract.py"
)

INNER_COVER_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_right_half_cover.json"
)
INNER_ROOT_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_unstable_root.json"
)
FLOQUET_TRANSFER_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_transfer.json"
)
REDUCED_HISTORY_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_reduced_history.json"
)
PULSE_TARGET_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_validation_target.json"
)

TRACKED_PARENT_SHA256 = {
    INNER_COVER_RESULT_RELATIVE_PATH: (
        "f0458acf59b8fad96e43f204df37fd8d37f356ebbf67701180c8ff31c668739a"
    ),
    INNER_ROOT_RESULT_RELATIVE_PATH: (
        "ab2876efc8a26df544f56257ab00b9fde0fea4ba043f4500f1450e0d0885fa2c"
    ),
    FLOQUET_TRANSFER_RESULT_RELATIVE_PATH: (
        "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
    ),
    REDUCED_HISTORY_RESULT_RELATIVE_PATH: (
        "4555fb765a5060a3767a7ea669deb2f4921b8d7410d7d4e15ad077e552da8870"
    ),
    PULSE_TARGET_RESULT_RELATIVE_PATH: (
        "175a03bad09c81c9289ee5747d870113c6afcc22b1ec23942379c4c81bcda917"
    ),
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_inner_stable_manifold_stage1_contract.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source-manifest binding; 96-digit Decimal "
    "evaluation of a disclosed scalar Lyapunov--Perron majorant; the "
    "registered RFDE evidence has missing quantitative inputs, while the "
    "complete numerical row is a design target rather than directed evidence"
)

HVL_REFERENCE = (
    "J. K. Hale and S. M. Verduyn Lunel, Introduction to Functional "
    "Differential Equations, Springer, 1993, Chapter 10, Section 10.3, "
    "Theorem 3.3, p. 319"
)
HVL_DOI = "10.1007/978-1-4612-4342-7_11"

TARGET_STABLE_SEED_RADIUS = "0.0002"
PULSE_REQUESTED_RADIUS_DECIMAL = "0.00020000000000000001"

REQUIRED_QUANTITATIVE_FIELDS = (
    "stable_spectral_radius_upper",
    "unstable_backward_rate_upper",
    "stable_projection_norm_upper",
    "unstable_projection_norm_upper",
    "stable_dichotomy_constant_upper",
    "unstable_dichotomy_constant_upper",
    "sequence_weight_beta",
    "section_event_speed_lower",
    "section_defining_function_c2_upper",
    "poincare_return_c2_upper",
    "nonlinear_derivative_remainder_coefficient_upper",
    "validated_return_map_ball_radius_lower",
)

QUANTITATIVE_FALSE_FLAGS = (
    "left_shifted_stable_spectral_gap_validated",
    "riesz_projection_norms_validated",
    "stable_and_unstable_dichotomy_constants_validated",
    "phase_fixed_poincare_section_quantitatively_validated",
    "poincare_return_c2_bound_validated",
    "nonlinear_remainder_bound_validated",
    "continuous_graph_ball_radius_validated",
    "lyapunov_perron_contraction_for_rfde_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "specific_pulse_voltage_section_transversality_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
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


def _json_normalize(value: Any) -> Any:
    """Round-trip a dataclass payload to its deterministic JSON value."""

    return json.loads(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )


def _decimal(value: str | None, name: str) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string or null")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")
    return number


def _floor(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_FLOOR
        return format(+value, "f")


def _ceiling(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        return format(+value, "f")


def _sqrt_floor(value: Decimal) -> Decimal:
    """Return a 96-significant-digit lower bound for ``sqrt(value)``."""

    if value < 0:
        raise ValueError("cannot take a directed square root of a negative value")
    with localcontext() as high:
        high.prec = 220
        approximation = value.sqrt(context=high)
    with localcontext() as down:
        down.prec = 96
        down.rounding = ROUND_FLOOR
        candidate = +approximation
        with localcontext() as exact_check:
            exact_check.prec = 220
            if candidate * candidate > value:
                candidate = down.next_minus(candidate)
    return candidate


def _positive_decimal(value: Any, name: str) -> Decimal:
    number = _decimal(value if isinstance(value, str) else None, name)
    if number is None or number <= 0:
        raise ValueError(f"{name} must be a positive decimal string")
    return number


def _validate_source_hash_map(
    manifest: Mapping[str, Any], repository: Path, label: str
) -> None:
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or not source_hashes:
        raise ValueError(f"{label} source manifest is missing")
    for relative, digest in source_hashes.items():
        if not isinstance(relative, str) or not isinstance(digest, str):
            raise ValueError(f"{label} source manifest is malformed")
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"{label} source changed: {relative}")


def _validate_named_parent_hashes(
    manifest: Mapping[str, Any], repository: Path, label: str
) -> None:
    for name, digest in manifest.items():
        if not name.endswith("_sha256") or name == "certificate_sha256":
            continue
        path_name = name[: -len("_sha256")]
        relative = manifest.get(path_name)
        if isinstance(relative, str) and isinstance(digest, str):
            if _sha256_path(repository / relative) != digest:
                raise ValueError(f"{label} bound parent changed: {relative}")
    parent_hashes = manifest.get("parent_result_sha256")
    if parent_hashes is not None:
        if not isinstance(parent_hashes, Mapping):
            raise ValueError(f"{label} parent digest map is malformed")
        for relative, digest in parent_hashes.items():
            if not isinstance(relative, str) or not isinstance(digest, str):
                raise ValueError(f"{label} parent digest map is malformed")
            if _sha256_path(repository / relative) != digest:
                raise ValueError(f"{label} bound parent changed: {relative}")


def _load_tracked_parent(repository: Path, relative: str) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    expected = TRACKED_PARENT_SHA256[relative]
    if sha256(raw).hexdigest() != expected:
        raise ValueError(f"tracked Stage-1 parent changed: {relative}")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"Stage-1 parent is not a mapping: {relative}")
    manifest = payload.get("manifest")
    if not isinstance(manifest, Mapping):
        raise ValueError(f"Stage-1 parent manifest is missing: {relative}")
    if isinstance(manifest.get("source_sha256"), Mapping):
        _validate_source_hash_map(manifest, repository, relative)
    _validate_named_parent_hashes(manifest, repository, relative)
    return payload


@dataclass(frozen=True)
class StableGraphInputBudget:
    """Quantitative inputs for one phase-fixed Poincare return map.

    ``rho_s`` and ``rho_u`` are rates strictly below one.  ``K_s`` and
    ``K_u`` are power-bound constants, and the two projection norms are in
    the declared reduced-history section norm.  If ``P=L+N``, the last C2
    and nonlinear fields must establish

    ``||DN(x)|| <= C_N ||x||`` and ``||N(x)|| <= C_N ||x||^2/2``.
    """

    stable_spectral_radius_upper: str | None
    unstable_backward_rate_upper: str | None
    stable_projection_norm_upper: str | None
    unstable_projection_norm_upper: str | None
    stable_dichotomy_constant_upper: str | None
    unstable_dichotomy_constant_upper: str | None
    sequence_weight_beta: str | None
    section_event_speed_lower: str | None
    section_defining_function_c2_upper: str | None
    poincare_return_c2_upper: str | None
    nonlinear_derivative_remainder_coefficient_upper: str | None
    validated_return_map_ball_radius_lower: str | None
    stable_seed_radius_target: str
    evidence_status: str


@dataclass(frozen=True)
class LyapunovPerronMajorant:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    input_order_conditions_hold: bool
    nonlinear_remainder_dominates_return_c2: bool
    stable_kernel_upper: str | None
    unstable_kernel_upper: str | None
    lyapunov_perron_kernel_upper: str | None
    nonlinear_kernel_product_upper: str | None
    strict_feasibility_discriminant_lower: str | None
    critical_nonlinear_remainder_upper_strict: str | None
    candidate_sequence_radius_upper: str | None
    candidate_contraction_upper: str | None
    candidate_invariance_margin_lower: str | None
    candidate_graph_quadratic_coefficient_upper: str | None
    candidate_graph_lipschitz_upper: str | None
    candidate_within_validated_return_ball: bool
    graph_majorant_closes: bool
    lyapunov_perron_kernel_formula: str
    contraction_formula: str
    invariant_ball_formula: str
    candidate_radius_formula: str
    necessary_and_sufficient_scalar_feasibility_formula: str


@dataclass(frozen=True)
class QualitativeStableManifoldAudit:
    reference: str
    reference_doi: str
    theorem_hypothesis_rfde_c1_or_better_matched: bool
    polynomial_retarded_vector_field_c_infinity: bool
    validated_periodic_orbit_nonconstant: bool
    one_period_monodromy_compact: bool
    neutral_multiplier_algebraically_simple: bool
    no_other_unit_modulus_multiplier: bool
    unstable_multiplier_count: int
    hyperbolic_periodic_orbit_in_rfde_sense: bool
    abstract_transverse_section_exists: bool
    full_history_local_stable_manifold_c1_proved: bool
    full_history_local_stable_manifold_codimension: int
    reduced_history_nonzero_spectrum_factorization_proved: bool
    reduced_history_local_stable_manifold_c1_proved: bool
    reduced_phase_section_local_stable_manifold_c1_codimension_one_proved: bool
    particular_pulse_voltage_section_speed_lower_validated: bool
    qualitative_result_supplies_explicit_radius_or_graph_constant: bool
    qualitative_result_proves_separator_or_onset: bool


@dataclass(frozen=True)
class Stage1StableManifoldContract:
    schema_id: str
    model_id: str
    branch: str
    phase_space: str
    phase_fixed_return_map_normal_form: str
    parent_result_sha256: dict[str, str]
    qualitative_audit: dict[str, Any]
    proved_parent_evidence: dict[str, Any]
    actual_evidence_budget: dict[str, Any]
    actual_evidence_evaluation: dict[str, Any]
    design_budget_not_evidence: dict[str, Any]
    design_budget_evaluation: dict[str, Any]
    next_certificate_interface: dict[str, Any]
    claim_status: dict[str, bool]


def evaluate_lyapunov_perron_majorant(
    budget: StableGraphInputBudget,
) -> LyapunovPerronMajorant:
    """Evaluate the disclosed scalar majorant.

    For the weighted sequence norm ``sup beta^{-n} ||x_n||``, set

    ``C_beta=K_s p_s/(beta-rho_s)+K_u p_u rho_u/(1-beta rho_u)``.

    Taylor's theorem then gives contraction constant
    ``q(R)=C_N C_beta R`` and the invariant-ball condition
    ``K_s r + (C_N C_beta/2) R^2 <= R``.  Within this scalar
    majorant there is an ``R`` with ``q(R)<1`` precisely when
    ``2 K_s C_N C_beta r < 1``; the smaller quadratic root is the
    least candidate radius and must also lie inside the validated map ball.
    """

    values = asdict(budget)
    parsed = {
        field.name: _decimal(values[field.name], field.name)
        for field in fields(StableGraphInputBudget)
        if field.name != "evidence_status"
    }
    missing = tuple(
        name for name in REQUIRED_QUANTITATIVE_FIELDS if values[name] is None
    )
    formulas = {
        "lyapunov_perron_kernel_formula": (
            "C_beta=K_s*p_s/(beta-rho_s)+"
            "K_u*p_u*rho_u/(1-beta*rho_u)"
        ),
        "contraction_formula": "q(R)=C_N*C_beta*R<1",
        "invariant_ball_formula": (
            "K_s*r+(C_N*C_beta/2)*R^2<=R"
        ),
        "candidate_radius_formula": (
            "R_min=2*K_s*r/(1+sqrt(1-2*K_s*C_N*C_beta*r))"
        ),
        "necessary_and_sufficient_scalar_feasibility_formula": (
            "exists R<=R_0 satisfying the displayed invariant-ball and "
            "strict-contraction inequalities iff "
            "2*K_s*C_N*C_beta*r<1 and R_min<=R_0"
        ),
    }
    if missing:
        return LyapunovPerronMajorant(
            input_complete=False,
            missing_inputs=missing,
            input_order_conditions_hold=False,
            nonlinear_remainder_dominates_return_c2=False,
            stable_kernel_upper=None,
            unstable_kernel_upper=None,
            lyapunov_perron_kernel_upper=None,
            nonlinear_kernel_product_upper=None,
            strict_feasibility_discriminant_lower=None,
            critical_nonlinear_remainder_upper_strict=None,
            candidate_sequence_radius_upper=None,
            candidate_contraction_upper=None,
            candidate_invariance_margin_lower=None,
            candidate_graph_quadratic_coefficient_upper=None,
            candidate_graph_lipschitz_upper=None,
            candidate_within_validated_return_ball=False,
            graph_majorant_closes=False,
            **formulas,
        )

    if any(value is None for value in parsed.values()):
        raise AssertionError("a supposedly complete Stage-1 budget has nulls")
    numbers = {name: value for name, value in parsed.items() if value is not None}
    rho_s = numbers["stable_spectral_radius_upper"]
    rho_u = numbers["unstable_backward_rate_upper"]
    p_s = numbers["stable_projection_norm_upper"]
    p_u = numbers["unstable_projection_norm_upper"]
    k_s = numbers["stable_dichotomy_constant_upper"]
    k_u = numbers["unstable_dichotomy_constant_upper"]
    beta = numbers["sequence_weight_beta"]
    event_speed = numbers["section_event_speed_lower"]
    section_c2 = numbers["section_defining_function_c2_upper"]
    return_c2 = numbers["poincare_return_c2_upper"]
    c_n = numbers["nonlinear_derivative_remainder_coefficient_upper"]
    r_zero = numbers["validated_return_map_ball_radius_lower"]
    seed = numbers["stable_seed_radius_target"]

    positive = (
        rho_s > 0
        and rho_u > 0
        and p_s >= 1
        and p_u >= 1
        and k_s >= 1
        and k_u >= 1
        and event_speed > 0
        and section_c2 >= 0
        and return_c2 > 0
        and c_n > 0
        and r_zero > 0
        and seed > 0
    )
    order = positive and rho_s < beta < 1 and rho_u < 1
    c2_dominance = return_c2 <= c_n
    if not order or not c2_dominance:
        raise ValueError(
            "the complete Stage-1 budget violates rate, norm, C2, or "
            "nonlinear-remainder conditions"
        )

    with localcontext() as up:
        up.prec = 96
        up.rounding = ROUND_CEILING
        stable_kernel = k_s * p_s / (beta - rho_s)
        unstable_kernel = k_u * p_u * rho_u / (1 - beta * rho_u)
        kernel = stable_kernel + unstable_kernel
        product = c_n * kernel
        feasibility_loss = 2 * k_s * product * seed
    with localcontext() as down:
        down.prec = 96
        down.rounding = ROUND_FLOOR
        discriminant = Decimal(1) - feasibility_loss
        critical_c_n = Decimal(1) / (2 * k_s * kernel * seed)

    if discriminant <= 0:
        return LyapunovPerronMajorant(
            input_complete=True,
            missing_inputs=(),
            input_order_conditions_hold=True,
            nonlinear_remainder_dominates_return_c2=True,
            stable_kernel_upper=_ceiling(stable_kernel),
            unstable_kernel_upper=_ceiling(unstable_kernel),
            lyapunov_perron_kernel_upper=_ceiling(kernel),
            nonlinear_kernel_product_upper=_ceiling(product),
            strict_feasibility_discriminant_lower=_floor(discriminant),
            critical_nonlinear_remainder_upper_strict=_floor(critical_c_n),
            candidate_sequence_radius_upper=None,
            candidate_contraction_upper=None,
            candidate_invariance_margin_lower=None,
            candidate_graph_quadratic_coefficient_upper=None,
            candidate_graph_lipschitz_upper=None,
            candidate_within_validated_return_ball=False,
            graph_majorant_closes=False,
            **formulas,
        )

    sqrt_lower = _sqrt_floor(discriminant)
    with localcontext() as up:
        up.prec = 96
        up.rounding = ROUND_CEILING
        radius = 2 * k_s * seed / (1 + sqrt_lower)
        q_value = product * radius
        half = Decimal("0.5")
        graph_quadratic = (
            half
            * c_n
            * unstable_kernel
            * (k_s / (1 - q_value)) ** 2
        )
        graph_lipschitz = (
            c_n
            * radius
            * unstable_kernel
            * k_s
            / (1 - q_value)
        )
    with localcontext() as down:
        down.prec = 96
        down.rounding = ROUND_FLOOR
        invariance_margin = (
            radius - product * radius * radius / 2 - k_s * seed
        )
    if invariance_margin == 0:
        invariance_margin = Decimal(0)
    inside = radius <= r_zero
    closes = q_value < 1 and invariance_margin >= 0 and inside
    return LyapunovPerronMajorant(
        input_complete=True,
        missing_inputs=(),
        input_order_conditions_hold=True,
        nonlinear_remainder_dominates_return_c2=True,
        stable_kernel_upper=_ceiling(stable_kernel),
        unstable_kernel_upper=_ceiling(unstable_kernel),
        lyapunov_perron_kernel_upper=_ceiling(kernel),
        nonlinear_kernel_product_upper=_ceiling(product),
        strict_feasibility_discriminant_lower=_floor(discriminant),
        critical_nonlinear_remainder_upper_strict=_floor(critical_c_n),
        candidate_sequence_radius_upper=_ceiling(radius),
        candidate_contraction_upper=_ceiling(q_value),
        candidate_invariance_margin_lower=_floor(invariance_margin),
        candidate_graph_quadratic_coefficient_upper=_ceiling(
            graph_quadratic
        ),
        candidate_graph_lipschitz_upper=_ceiling(graph_lipschitz),
        candidate_within_validated_return_ball=inside,
        graph_majorant_closes=closes,
        **formulas,
    )


def _binary64_decimal(record: Any, name: str) -> str:
    if not isinstance(record, Mapping) or set(record) != {
        "binary64_hex",
        "decimal",
    }:
        raise ValueError(f"{name} is not a binary64 record")
    value = record.get("decimal")
    if not isinstance(value, str):
        raise ValueError(f"{name} decimal is missing")
    return value


def _proved_parent_evidence(
    cover: Mapping[str, Any],
    root: Mapping[str, Any],
    transfer: Mapping[str, Any],
    reduced: Mapping[str, Any],
    pulse: Mapping[str, Any],
) -> tuple[dict[str, Any], QualitativeStableManifoldAudit, str]:
    cover_certificate = cover.get("certificate")
    root_certificate = root.get("certificate")
    transfer_artifact = transfer.get("artifact")
    reduced_certificate = reduced.get("certificate")
    pulse_target = pulse.get("target")
    if not all(
        isinstance(value, Mapping)
        for value in (
            cover_certificate,
            root_certificate,
            transfer_artifact,
            reduced_certificate,
            pulse_target,
        )
    ):
        raise ValueError("a Stage-1 parent theorem body is missing")
    branches = transfer_artifact.get("branches")
    if not isinstance(branches, Mapping):
        raise ValueError("the Floquet-transfer branches are missing")
    inner_transfer = branches.get(BRANCH)
    if not isinstance(inner_transfer, Mapping):
        raise ValueError("the inner Floquet-transfer branch is missing")

    required_true = (
        cover_certificate.get("inner_total_unstable_multiplier_count_validated")
        is True
        and cover_certificate.get("inner_no_other_right_half_roots_validated")
        is True
        and cover_certificate.get("inner_saddle_floquet_index_validated") is True
        and cover_certificate.get("directed_unstable_multiplier_count") == 1
        and root_certificate.get("associated_multiplier_strictly_greater_than_one")
        is True
        and root_certificate.get("root_analytic_algebraic_multiplicity_one")
        is True
        and inner_transfer.get("neutral_multiplier_algebraically_simple_validated")
        is True
        and inner_transfer.get("monodromy_compact") is True
        and inner_transfer.get("regularity_bridge_to_history_monodromy") is True
        and reduced_certificate.get("full_semiflow_factors_through_reduced_semiflow_proved")
        is True
        and reduced_certificate.get("global_orbital_stable_set_pullback_equality_proved")
        is True
        and reduced_certificate.get("inner_monodromy_nonzero_spectrum_reduction_proved")
        is True
        and reduced_certificate.get("local_stable_manifold_codimension_preserved_by_pullback_proved")
        is True
        and reduced_certificate.get("projection_has_continuous_split_right_inverse_proved")
        is True
    )
    if not required_true:
        raise ValueError("the qualitative inner stable-manifold hypotheses regressed")

    mu_lower = _positive_decimal(
        root_certificate.get("multiplier_modulus_lower"),
        "inner unstable multiplier lower bound",
    )
    mu_upper = _positive_decimal(
        root_certificate.get("multiplier_modulus_upper"),
        "inner unstable multiplier upper bound",
    )
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        rho_u = Decimal(1) / mu_lower
    if not rho_u < 1:
        raise ArithmeticError("the proved unstable inverse rate is not below one")

    observed = pulse_target.get("observed_margins")
    requested = pulse_target.get("requested_directed_certificate_bounds")
    claims = pulse_target.get("claim_status")
    if not all(isinstance(value, Mapping) for value in (observed, requested, claims)):
        raise ValueError("the pulse target budget is missing")
    if claims.get("inner_local_stable_graph_validated") is not False:
        raise ValueError("the pulse target improperly promotes a stable graph")
    target_radius = _binary64_decimal(
        requested.get("local_reduced_history_radius_lower"),
        "requested local reduced-history radius",
    )
    if Decimal(target_radius) != Decimal(PULSE_REQUESTED_RADIUS_DECIMAL):
        raise ValueError("the registered pulse graph-radius target changed")

    nonconstant_lower = _positive_decimal(
        inner_transfer.get("nonconstant_fourier_mode_lower"),
        "inner nonconstant-mode lower bound",
    )
    qualitative = QualitativeStableManifoldAudit(
        reference=HVL_REFERENCE,
        reference_doi=HVL_DOI,
        theorem_hypothesis_rfde_c1_or_better_matched=True,
        polynomial_retarded_vector_field_c_infinity=True,
        validated_periodic_orbit_nonconstant=nonconstant_lower > 0,
        one_period_monodromy_compact=True,
        neutral_multiplier_algebraically_simple=True,
        no_other_unit_modulus_multiplier=True,
        unstable_multiplier_count=1,
        hyperbolic_periodic_orbit_in_rfde_sense=True,
        abstract_transverse_section_exists=True,
        full_history_local_stable_manifold_c1_proved=True,
        full_history_local_stable_manifold_codimension=1,
        reduced_history_nonzero_spectrum_factorization_proved=True,
        reduced_history_local_stable_manifold_c1_proved=True,
        reduced_phase_section_local_stable_manifold_c1_codimension_one_proved=True,
        particular_pulse_voltage_section_speed_lower_validated=False,
        qualitative_result_supplies_explicit_radius_or_graph_constant=False,
        qualitative_result_proves_separator_or_onset=False,
    )
    evidence = {
        "inner_closed_right_half_characteristic_value_count": (
            cover_certificate["directed_closed_right_half_characteristic_value_count"]
        ),
        "inner_nontranslation_unstable_multiplier_count": 1,
        "inner_no_other_nontranslation_multiplier_on_or_outside_unit_circle": True,
        "unstable_multiplier_modulus_lower": format(mu_lower, "f"),
        "unstable_multiplier_modulus_upper": format(mu_upper, "f"),
        "unstable_backward_rate_upper_derived": _ceiling(rho_u),
        "stable_spectral_radius_strictly_below_one_qualitative": True,
        "stable_spectral_radius_numerical_upper_below_one": None,
        "nonconstant_fourier_mode_lower": format(nonconstant_lower, "f"),
        "one_period_monodromy_compact": True,
        "history_monodromy_regularity_bridge_registered": True,
        "reduced_history_factorization_exact": True,
        "stable_set_pullback_equality_exact": True,
        "stable_manifold_codimension_preserved_by_pullback": True,
        "old_recovery_history_contributes_only_zero_spectrum": True,
        "requested_graph_seed_radius_not_proved": target_radius,
        "pulse_endpoint_coordinate_margin_observed_binary64": _binary64_decimal(
            observed.get("minimum_absolute_endpoint_coordinate"),
            "pulse endpoint coordinate margin",
        ),
        "pulse_derivative_margin_observed_binary64": _binary64_decimal(
            observed.get("minimum_sampled_derivative_magnitude"),
            "pulse derivative margin",
        ),
        "pulse_endpoint_reduced_sup_distance_observed_binary64": _binary64_decimal(
            observed.get("maximum_endpoint_sampled_reduced_sup_distance"),
            "pulse endpoint reduced sup distance",
        ),
    }
    return evidence, qualitative, _ceiling(rho_u)


def build_stage1_stable_manifold_contract(
    repository: Path,
) -> Stage1StableManifoldContract:
    repository = repository.resolve()
    parents = {
        relative: _load_tracked_parent(repository, relative)
        for relative in TRACKED_PARENT_SHA256
    }
    evidence, qualitative, rho_u = _proved_parent_evidence(
        parents[INNER_COVER_RESULT_RELATIVE_PATH],
        parents[INNER_ROOT_RESULT_RELATIVE_PATH],
        parents[FLOQUET_TRANSFER_RESULT_RELATIVE_PATH],
        parents[REDUCED_HISTORY_RESULT_RELATIVE_PATH],
        parents[PULSE_TARGET_RESULT_RELATIVE_PATH],
    )

    actual_budget = StableGraphInputBudget(
        stable_spectral_radius_upper=None,
        unstable_backward_rate_upper=rho_u,
        stable_projection_norm_upper=None,
        unstable_projection_norm_upper=None,
        stable_dichotomy_constant_upper=None,
        unstable_dichotomy_constant_upper=None,
        sequence_weight_beta=None,
        section_event_speed_lower=None,
        section_defining_function_c2_upper="0",
        poincare_return_c2_upper=None,
        nonlinear_derivative_remainder_coefficient_upper=None,
        validated_return_map_ball_radius_lower=None,
        stable_seed_radius_target=TARGET_STABLE_SEED_RADIUS,
        evidence_status="source_bound_partial_evidence",
    )
    actual_evaluation = evaluate_lyapunov_perron_majorant(actual_budget)
    if actual_evaluation.graph_majorant_closes:
        raise AssertionError("partial Stage-1 evidence closed a quantitative graph")

    # This row is a concrete target for the next directed calculation.  It is
    # deliberately conservative enough to exhibit strict scalar slack while
    # remaining entirely separate from the RFDE evidence row.
    design_budget = StableGraphInputBudget(
        stable_spectral_radius_upper="0.9",
        unstable_backward_rate_upper=rho_u,
        stable_projection_norm_upper="2",
        unstable_projection_norm_upper="2",
        stable_dichotomy_constant_upper="2",
        unstable_dichotomy_constant_upper="2",
        sequence_weight_beta="0.95",
        section_event_speed_lower="0.01",
        section_defining_function_c2_upper="0",
        poincare_return_c2_upper="10",
        nonlinear_derivative_remainder_coefficient_upper="10",
        validated_return_map_ball_radius_lower="0.00052",
        stable_seed_radius_target=TARGET_STABLE_SEED_RADIUS,
        evidence_status="design_target_not_proved",
    )
    design_evaluation = evaluate_lyapunov_perron_majorant(design_budget)
    if not design_evaluation.graph_majorant_closes:
        raise ArithmeticError("the declared Stage-1 design budget has no slack")

    claim_status = {
        "qualitative_full_history_inner_stable_manifold_c1_proved": True,
        "qualitative_reduced_history_inner_stable_manifold_c1_proved": True,
        "qualitative_reduced_phase_section_codimension_one_proved": True,
        **{name: False for name in QUANTITATIVE_FALSE_FLAGS},
        "design_budget_promoted_to_rfde_evidence": False,
    }
    return Stage1StableManifoldContract(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        phase_space="Y=C([-5*sqrt(5),0],R)xR",
        phase_fixed_return_map_normal_form=(
            "P(x)=L*x+N(x), x=P_u*x+P_s*x, N(0)=DN(0)=0"
        ),
        parent_result_sha256=dict(TRACKED_PARENT_SHA256),
        qualitative_audit=asdict(qualitative),
        proved_parent_evidence=evidence,
        actual_evidence_budget=asdict(actual_budget),
        actual_evidence_evaluation=asdict(actual_evaluation),
        design_budget_not_evidence=asdict(design_budget),
        design_budget_evaluation=asdict(design_evaluation),
        next_certificate_interface={
            "required_quantitative_fields": list(REQUIRED_QUANTITATIVE_FIELDS),
            "directed_norm": (
                "one declared continuous reduced-history section norm; all "
                "projection, dichotomy, C2, and ball constants use this norm"
            ),
            "stable_power_bound": "||L_s^n||<=K_s*rho_s^n, n>=0",
            "unstable_backward_power_bound": (
                "||L_u^(-n)||<=K_u*rho_u^n, n>=0"
            ),
            "section_gate": (
                "a directed lower bound on the exact RFDE section event "
                "speed, plus a C2 section chart bound"
            ),
            "return_map_gate": (
                "a directed C2 bound for the exact first-return map on a "
                "continuous-history ball"
            ),
            "nonlinear_gate": (
                "directed ||DN(x)||<=C_N||x|| and "
                "||N(x)||<=C_N||x||^2/2"
            ),
            "strict_scalar_gate": (
                "2*K_s*C_N*C_beta*r<1 and R_min<=R_0"
            ),
            "pulse_voltage_section_is_a_separate_gate": True,
            "design_row_is_not_admissible_as_evidence": True,
        },
        claim_status=claim_status,
    )


def build_stage1_stable_manifold_result(repository: Path) -> dict[str, Any]:
    contract = _json_normalize(
        asdict(build_stage1_stable_manifold_contract(repository))
    )
    return {
        "contract": contract,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "contract_sha256": canonical_sha256(contract),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(TRACKED_PARENT_SHA256),
        },
    }


def validate_stage1_stable_manifold_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "contract",
        "manifest",
    }:
        raise ValueError("the Stage-1 result schema changed")
    contract = payload.get("contract")
    manifest = payload.get("manifest")
    if not isinstance(contract, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the Stage-1 contract or manifest is missing")
    expected_fields = {field.name for field in fields(Stage1StableManifoldContract)}
    if set(contract) != expected_fields:
        raise ValueError("the Stage-1 contract dataclass schema changed")
    expected = _json_normalize(
        asdict(build_stage1_stable_manifold_contract(repository))
    )
    if dict(contract) != expected:
        raise ValueError("the Stage-1 contract differs from source replay")
    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "contract_sha256",
        "source_sha256",
        "parent_result_sha256",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-1 manifest schema changed")
    scalars = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "contract_sha256": canonical_sha256(contract),
    }
    for name, expected_value in scalars.items():
        if manifest.get(name) != expected_value:
            raise ValueError(f"the Stage-1 manifest {name} changed")
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(
        SOURCE_MANIFEST
    ):
        raise ValueError("the Stage-1 source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-1 source changed: {relative}")
    if manifest.get("parent_result_sha256") != TRACKED_PARENT_SHA256:
        raise ValueError("the Stage-1 parent digest map changed")
    for relative, digest in TRACKED_PARENT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-1 parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "HVL_DOI",
    "HVL_REFERENCE",
    "LyapunovPerronMajorant",
    "NOTE_RELATIVE_PATH",
    "PULSE_REQUESTED_RADIUS_DECIMAL",
    "QUANTITATIVE_FALSE_FLAGS",
    "REQUIRED_QUANTITATIVE_FIELDS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "StableGraphInputBudget",
    "Stage1StableManifoldContract",
    "TARGET_STABLE_SEED_RADIUS",
    "TRACKED_PARENT_SHA256",
    "build_stage1_stable_manifold_contract",
    "build_stage1_stable_manifold_result",
    "canonical_sha256",
    "evaluate_lyapunov_perron_majorant",
    "validate_stage1_stable_manifold_result",
]
