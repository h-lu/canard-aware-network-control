"""Exact Bernstein certificate for the frozen C4 incoming target chart.

The C4 preparation seam is polynomial on its final half-unit.  After the
affine change

    u = 2 r + 1,             v = 10 lambda + 1/2,

the patch rectangle ``-1/2 <= r <= 0``, ``|lambda| <= 1/20`` becomes the
unit square.  This module converts the three principal-minor polynomials

    -X_t,        Y_lambda,        -det D_(t,lambda)(X,Y)

to their tensor-product Bernstein forms over ``Q(sqrt(5))``.  Exact sign
decisions on every coefficient give convex-hull lower bounds.  No floating
point interval, sampling argument, or subdivision is used in the proof.

Outside the patch the incoming chart is the uncorrected polynomial history,
where the three quantities are exactly ``1/2``, ``1`` and ``1/2``.  Thus the
Bernstein bounds prove the P-matrix property on the full retained incoming
history rectangle.  The physical method-of-steps strip and the glued target
chart remain separate open problems.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import platform
from typing import Mapping, Sequence

import sympy as sp

from canard_control.fixed_epsilon_target_c4_preparation_seam import (
    EXACT_ETA,
    EXACT_INCOMING_TIME,
    EXACT_NU,
    EXACT_PATCH_WIDTH,
    EXACT_PHASE_SHIFT,
    EXACT_RHO,
    EXACT_SECTION_HALF_WIDTH,
    EXACT_THETA,
    EXACT_TRANSVERSE_RADIUS,
    MAXIMUM_JET_ORDER,
    SMOOTHERSTEP9_COEFFICIENTS,
    exact_target_endpoint_jets,
    validate_target_c4_preparation_seam_result,
)


MODEL_ID = "fixed-epsilon-target-c4-history-exact-bernstein"
AUDIT_ID = "fixed-epsilon-target-c4-history-exact-bernstein-v1"

PARENT_RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_c4_preparation_seam.json"
)
PARENT_RESULT_SHA256 = (
    "5cc678e56a2d1c203d174a27617c28963082ba8e7cf9c6dc48f3f6de8bff840b"
)
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_c4_history_bernstein.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_target_c4_history_bernstein.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_c4_history_bernstein.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-c4-history-bernstein.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_c4_history_bernstein.py"
)
MANIFEST_ARITHMETIC = (
    "exact symbolic algebra over Q(sqrt(5)); exact tensor-product Bernstein "
    "conversion and coefficient sign decisions on the unit box; no binary64 "
    "sample, interval-flow enclosure, physical-strip certificate, glued "
    "target embedding, fixed graph, selected trace, or history root"
)

RELATIVE_TIME = sp.Symbol("r", real=True)
TRANSVERSE = sp.Symbol("lambda", real=True)
UNIT_TIME = sp.Symbol("u", real=True)
UNIT_TRANSVERSE = sp.Symbol("v", real=True)
QUADRATIC_GENERATOR = sp.Symbol("z", real=True)
SQRT_FIVE = sp.sqrt(5)

PATCH_MARGIN_BY_NAME = {
    "negative_x_time_derivative": sp.Rational(9, 100),
    "positive_y_transverse_derivative": sp.Rational(24, 25),
    "negative_raw_jacobian_determinant": sp.Rational(2, 5),
}


def _exact_entry_shift() -> sp.Expr:
    """Return the frozen entry shift without importing a private helper."""

    x0 = (EXACT_SECTION_HALF_WIDTH - EXACT_PHASE_SHIFT) / 2
    x4 = (EXACT_SECTION_HALF_WIDTH + 4 - EXACT_PHASE_SHIFT) / 2
    x5 = (EXACT_SECTION_HALF_WIDTH + 5 - EXACT_PHASE_SHIFT) / 2
    xtheta = (
        EXACT_SECTION_HALF_WIDTH + EXACT_THETA - EXACT_PHASE_SHIFT
    ) / 2
    correction = (
        EXACT_RHO
        * (-x0**3 / 3 + ((x4 + x5) / 2 - x0) / 5)
        + EXACT_RHO**2 * EXACT_ETA * (x0**2 - xtheta**2)
        + EXACT_RHO**3
        / 4
        * ((x4**3 + x5**3) / 2 - x0**3)
    )
    return sp.expand(-correction)


def exact_unpatched_history_state(
    relative_time: sp.Expr = RELATIVE_TIME,
    transverse: sp.Expr = TRANSVERSE,
) -> tuple[sp.Expr, sp.Expr]:
    """Return the exact uncorrected history at ``t=-3+r``."""

    time = EXACT_INCOMING_TIME + relative_time
    shifted = time + EXACT_PHASE_SHIFT
    return (
        sp.expand(-shifted / 2),
        sp.expand(
            (shifted**2 - 2) / 4
            + EXACT_RHO
            * EXACT_NU
            * (time + EXACT_SECTION_HALF_WIDTH)
            + _exact_entry_shift()
            + transverse
        ),
    )


def exact_c4_patch_state() -> tuple[sp.Expr, sp.Expr]:
    """Return the exact degree-nine-Hermite corrected history polynomial."""

    base = exact_unpatched_history_state()
    base_endpoint_jets = tuple(
        tuple(
            sp.diff(base[component], RELATIVE_TIME, order).subs(
                RELATIVE_TIME, 0
            )
            for component in range(2)
        )
        for order in range(MAXIMUM_JET_ORDER + 1)
    )
    endpoint_jets = exact_target_endpoint_jets(TRANSVERSE)
    if any(
        sp.expand(endpoint_jets[0][component] - base_endpoint_jets[0][component])
        != 0
        for component in range(2)
    ):
        raise AssertionError("the C4 correction changed the endpoint curve")
    unit_cutoff = 1 + RELATIVE_TIME / EXACT_PATCH_WIDTH
    cutoff = sum(
        coefficient * unit_cutoff**power
        for power, coefficient in zip(
            range(5, 10), SMOOTHERSTEP9_COEFFICIENTS, strict=True
        )
    )
    state: list[sp.Expr] = []
    for component in range(2):
        correction = sum(
            (
                endpoint_jets[order][component]
                - base_endpoint_jets[order][component]
            )
            * RELATIVE_TIME**order
            * cutoff
            / sp.factorial(order)
            for order in range(1, MAXIMUM_JET_ORDER + 1)
        )
        state.append(sp.expand(base[component] + correction))
    return state[0], state[1]


def exact_history_p_matrix_polynomials() -> dict[str, sp.Expr]:
    """Return the three exact P-matrix quantities on the C4 patch."""

    x_coordinate, y_coordinate = exact_c4_patch_state()
    x_time = sp.diff(x_coordinate, RELATIVE_TIME)
    y_time = sp.diff(y_coordinate, RELATIVE_TIME)
    x_transverse = sp.diff(x_coordinate, TRANSVERSE)
    y_transverse = sp.diff(y_coordinate, TRANSVERSE)
    determinant = x_time * y_transverse - y_time * x_transverse
    return {
        "negative_x_time_derivative": sp.expand(-x_time),
        "positive_y_transverse_derivative": sp.expand(y_transverse),
        "negative_raw_jacobian_determinant": sp.expand(-determinant),
    }


def quadratic_field_parts(value: sp.Expr) -> tuple[sp.Rational, sp.Rational]:
    """Write one element of ``Q(sqrt(5))`` uniquely as ``a+b sqrt(5)``."""

    replaced = sp.expand(value).xreplace({SQRT_FIVE: QUADRATIC_GENERATOR})
    try:
        polynomial = sp.Poly(replaced, QUADRATIC_GENERATOR, domain=sp.QQ)
    except sp.PolynomialError as error:
        raise ValueError("value does not belong to Q(sqrt(5))") from error
    if polynomial.degree() > 1:
        raise ValueError("value is not in the quadratic basis 1,sqrt(5)")
    return sp.Rational(polynomial.nth(0)), sp.Rational(polynomial.nth(1))


def quadratic_field_sign(value: sp.Expr) -> int:
    """Decide the sign of an element of ``Q(sqrt(5))`` exactly."""

    rational_part, radical_part = quadratic_field_parts(value)
    if rational_part == 0:
        return 1 if radical_part > 0 else -1 if radical_part < 0 else 0
    if radical_part == 0:
        return 1 if rational_part > 0 else -1
    if rational_part > 0 and radical_part > 0:
        return 1
    if rational_part < 0 and radical_part < 0:
        return -1
    squared_comparison = rational_part**2 - 5 * radical_part**2
    if squared_comparison == 0:
        return 0
    comparison_sign = 1 if squared_comparison > 0 else -1
    return comparison_sign if rational_part > 0 else -comparison_sign


@dataclass(frozen=True)
class ExactBernsteinForm:
    """A tensor-product Bernstein form on the unit square."""

    degree_u: int
    degree_v: int
    coefficients: tuple[tuple[sp.Expr, ...], ...]
    transformed_polynomial: sp.Expr


def exact_tensor_bernstein_form(polynomial: sp.Expr) -> ExactBernsteinForm:
    """Convert a bivariate power polynomial to the exact Bernstein basis."""

    transformed = sp.expand(
        polynomial.subs(
            {
                RELATIVE_TIME: (UNIT_TIME - 1) / 2,
                TRANSVERSE: (2 * UNIT_TRANSVERSE - 1) / 20,
            }
        )
    )
    power = sp.Poly(
        transformed, UNIT_TIME, UNIT_TRANSVERSE, extension=SQRT_FIVE
    )
    degree_u = int(power.degree(UNIT_TIME))
    degree_v = int(power.degree(UNIT_TRANSVERSE))
    monomial = tuple(
        tuple(
            power.coeff_monomial(UNIT_TIME**i * UNIT_TRANSVERSE**j)
            for j in range(degree_v + 1)
        )
        for i in range(degree_u + 1)
    )
    coefficients = tuple(
        tuple(
            sp.expand(
                sum(
                    monomial[i][j]
                    * sp.Rational(comb(k, i), comb(degree_u, i))
                    * sp.Rational(comb(ell, j), comb(degree_v, j))
                    for i in range(k + 1)
                    for j in range(ell + 1)
                )
            )
            for ell in range(degree_v + 1)
        )
        for k in range(degree_u + 1)
    )
    return ExactBernsteinForm(
        degree_u=degree_u,
        degree_v=degree_v,
        coefficients=coefficients,
        transformed_polynomial=transformed,
    )


def exact_bernstein_reconstruction(form: ExactBernsteinForm) -> sp.Expr:
    """Reconstruct a tensor Bernstein polynomial in the power basis."""

    return sp.expand(
        sum(
            form.coefficients[k][ell]
            * sp.binomial(form.degree_u, k)
            * UNIT_TIME**k
            * (1 - UNIT_TIME) ** (form.degree_u - k)
            * sp.binomial(form.degree_v, ell)
            * UNIT_TRANSVERSE**ell
            * (1 - UNIT_TRANSVERSE) ** (form.degree_v - ell)
            for k in range(form.degree_u + 1)
            for ell in range(form.degree_v + 1)
        )
    )


def _coefficient_digest(coefficients: Sequence[Sequence[sp.Expr]]) -> str:
    serialization = "|".join(
        f"{rational_part},{radical_part}"
        for row in coefficients
        for coefficient in row
        for rational_part, radical_part in (quadratic_field_parts(coefficient),)
    )
    return sha256(serialization.encode("utf-8")).hexdigest()


def _minimum_coefficient(
    coefficients: Sequence[Sequence[sp.Expr]],
) -> tuple[int, int, sp.Expr]:
    candidates = tuple(
        (row, column, coefficient)
        for row, values in enumerate(coefficients)
        for column, coefficient in enumerate(values)
    )
    minimum = candidates[0]
    for candidate in candidates[1:]:
        if quadratic_field_sign(candidate[2] - minimum[2]) < 0:
            minimum = candidate
    return minimum


@dataclass(frozen=True)
class ExactBernsteinMargin:
    quantity: str
    degree_u: int
    degree_v: int
    coefficient_count: int
    accepted_unit_box_count: int
    subdivision_depth: int
    strict_rational_lower_bound: str
    minimum_coefficient_index: tuple[int, int]
    minimum_coefficient_rational_part: str
    minimum_coefficient_sqrt5_part: str
    coefficient_sha256: str
    exact_reconstruction_identity_verified: bool
    every_coefficient_strictly_above_rational_bound: bool


def exact_bernstein_margin_records() -> tuple[ExactBernsteinMargin, ...]:
    """Build and verify the three exact one-box Bernstein certificates."""

    records: list[ExactBernsteinMargin] = []
    for name, polynomial in exact_history_p_matrix_polynomials().items():
        form = exact_tensor_bernstein_form(polynomial)
        reconstruction_defect = sp.Poly(
            exact_bernstein_reconstruction(form)
            - form.transformed_polynomial,
            UNIT_TIME,
            UNIT_TRANSVERSE,
            extension=SQRT_FIVE,
        )
        reconstruction_verified = reconstruction_defect.is_zero
        lower_bound = PATCH_MARGIN_BY_NAME[name]
        all_strict = all(
            quadratic_field_sign(coefficient - lower_bound) > 0
            for row in form.coefficients
            for coefficient in row
        )
        if not reconstruction_verified:
            raise AssertionError(f"Bernstein reconstruction failed for {name}")
        if not all_strict:
            raise AssertionError(f"Bernstein lower bound failed for {name}")
        row, column, minimum = _minimum_coefficient(form.coefficients)
        rational_part, radical_part = quadratic_field_parts(minimum)
        records.append(
            ExactBernsteinMargin(
                quantity=name,
                degree_u=form.degree_u,
                degree_v=form.degree_v,
                coefficient_count=(form.degree_u + 1) * (form.degree_v + 1),
                accepted_unit_box_count=1,
                subdivision_depth=0,
                strict_rational_lower_bound=sp.sstr(lower_bound),
                minimum_coefficient_index=(row, column),
                minimum_coefficient_rational_part=sp.sstr(rational_part),
                minimum_coefficient_sqrt5_part=sp.sstr(radical_part),
                coefficient_sha256=_coefficient_digest(form.coefficients),
                exact_reconstruction_identity_verified=True,
                every_coefficient_strictly_above_rational_bound=True,
            )
        )
    return tuple(records)


@dataclass(frozen=True)
class TargetC4HistoryBernsteinCertificate:
    model_id: str
    audit_id: str
    arithmetic: str
    parent_result_sha256: str
    frozen_rho: str
    frozen_nu: str
    frozen_eta: str
    frozen_theta: str
    incoming_time: str
    retained_relative_time_interval: tuple[str, str]
    far_history_relative_time_interval: tuple[str, str]
    patch_relative_time_interval: tuple[str, str]
    transverse_interval: tuple[str, str]
    unit_box_change: tuple[str, str]
    history_output_frame: tuple[tuple[int, int], tuple[int, int]]
    far_history_exact_p_matrix_margins: tuple[str, str, str]
    patch_exact_bernstein_margins: tuple[ExactBernsteinMargin, ...]
    retained_history_strict_rational_margins: tuple[str, str, str]
    total_exact_bernstein_coefficient_count: int
    exact_scope: str
    open_scope: str
    frozen_c4_patch_is_bivariate_polynomial_over_q_sqrt5_proved: bool
    exact_tensor_bernstein_reconstruction_proved: bool
    exact_one_box_coefficient_lower_bounds_proved: bool
    exact_far_history_p_matrix_proved: bool
    exact_retained_c4_history_p_matrix_proved: bool
    exact_retained_c4_history_negative_orientation_proved: bool
    exact_retained_c4_history_global_injectivity_proved: bool
    exact_retained_c4_history_gale_nikaido_hypotheses_verified: bool
    physical_state_variational_interval_flow_validated: bool
    physical_p_matrix_validated: bool
    physical_cross_separation_validated: bool
    full_target_chart_global_injectivity_proved: bool
    expanded_target_embedding_collar_proved: bool
    target_boundary_degree_validated: bool
    target_global_graph_fixed_point_validated: bool
    selected_trace_or_complete_history_root_validated: bool


EXACT_TRUE_FLAGS = (
    "frozen_c4_patch_is_bivariate_polynomial_over_q_sqrt5_proved",
    "exact_tensor_bernstein_reconstruction_proved",
    "exact_one_box_coefficient_lower_bounds_proved",
    "exact_far_history_p_matrix_proved",
    "exact_retained_c4_history_p_matrix_proved",
    "exact_retained_c4_history_negative_orientation_proved",
    "exact_retained_c4_history_global_injectivity_proved",
    "exact_retained_c4_history_gale_nikaido_hypotheses_verified",
)

OPEN_FALSE_FLAGS = (
    "physical_state_variational_interval_flow_validated",
    "physical_p_matrix_validated",
    "physical_cross_separation_validated",
    "full_target_chart_global_injectivity_proved",
    "expanded_target_embedding_collar_proved",
    "target_boundary_degree_validated",
    "target_global_graph_fixed_point_validated",
    "selected_trace_or_complete_history_root_validated",
)


def build_target_c4_history_bernstein_certificate(
) -> TargetC4HistoryBernsteinCertificate:
    """Return the exact retained-history P-matrix certificate."""

    records = exact_bernstein_margin_records()
    expected = {
        "negative_x_time_derivative": (12, 3, 52, "9/100"),
        "positive_y_transverse_derivative": (13, 1, 28, "24/25"),
        "negative_raw_jacobian_determinant": (25, 4, 130, "2/5"),
    }
    for record in records:
        observed = (
            record.degree_u,
            record.degree_v,
            record.coefficient_count,
            record.strict_rational_lower_bound,
        )
        if observed != expected[record.quantity]:
            raise AssertionError(f"Bernstein degree or margin changed for {record.quantity}")
    return TargetC4HistoryBernsteinCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        arithmetic=MANIFEST_ARITHMETIC,
        parent_result_sha256=PARENT_RESULT_SHA256,
        frozen_rho="sqrt(5)/5",
        frozen_nu=sp.sstr(EXACT_NU),
        frozen_eta=sp.sstr(EXACT_ETA),
        frozen_theta=sp.sstr(EXACT_THETA),
        incoming_time=sp.sstr(EXACT_INCOMING_TIME),
        retained_relative_time_interval=(sp.sstr(-EXACT_THETA), "0"),
        far_history_relative_time_interval=(
            sp.sstr(-EXACT_THETA),
            sp.sstr(-EXACT_PATCH_WIDTH),
        ),
        patch_relative_time_interval=(sp.sstr(-EXACT_PATCH_WIDTH), "0"),
        transverse_interval=(
            sp.sstr(-EXACT_TRANSVERSE_RADIUS),
            sp.sstr(EXACT_TRANSVERSE_RADIUS),
        ),
        unit_box_change=("u=2*r+1", "v=10*lambda+1/2"),
        history_output_frame=((-1, 0), (0, 1)),
        far_history_exact_p_matrix_margins=("1/2", "1", "1/2"),
        patch_exact_bernstein_margins=records,
        retained_history_strict_rational_margins=("9/100", "24/25", "2/5"),
        total_exact_bernstein_coefficient_count=sum(
            record.coefficient_count for record in records
        ),
        exact_scope=(
            "the frozen-anchor C4 incoming history on "
            "[-3-Theta_*,-3]x[-1/20,1/20], including global injectivity "
            "of that history chart"
        ),
        open_scope=(
            "validated physical state-plus-variation flow, physical P-matrix "
            "and cross separation, full glued embedding and collar, degree, "
            "target graph, selected traces, and complete-history root"
        ),
        frozen_c4_patch_is_bivariate_polynomial_over_q_sqrt5_proved=True,
        exact_tensor_bernstein_reconstruction_proved=True,
        exact_one_box_coefficient_lower_bounds_proved=True,
        exact_far_history_p_matrix_proved=True,
        exact_retained_c4_history_p_matrix_proved=True,
        exact_retained_c4_history_negative_orientation_proved=True,
        exact_retained_c4_history_global_injectivity_proved=True,
        exact_retained_c4_history_gale_nikaido_hypotheses_verified=True,
        physical_state_variational_interval_flow_validated=False,
        physical_p_matrix_validated=False,
        physical_cross_separation_validated=False,
        full_target_chart_global_injectivity_proved=False,
        expanded_target_embedding_collar_proved=False,
        target_boundary_degree_validated=False,
        target_global_graph_fixed_point_validated=False,
        selected_trace_or_complete_history_root_validated=False,
    )


def json_ready_target_c4_history_bernstein() -> dict[str, object]:
    """Return the deterministic exact certificate as JSON-compatible data."""

    return json.loads(
        json.dumps(
            {"certificate": asdict(build_target_c4_history_bernstein_certificate())}
        )
    )


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def verify_parent_result(repository: Path) -> dict[str, bool]:
    """Validate the pinned exact C4 seam and its relevant claim boundary."""

    path = repository / PARENT_RESULT_RELATIVE_PATH
    if _sha256(path) != PARENT_RESULT_SHA256:
        raise ValueError("the exact C4 seam parent digest changed")
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_target_c4_preparation_seam_result(payload, repository)
    certificate = payload.get("audit", {}).get("certificate", {})
    checks = {
        "parent_exact_c4_seam_constructed": certificate.get(
            "target_frozen_anchor_c4_preparation_seam_constructed_exactly"
        )
        is True,
        "parent_left_history_jacobian_at_sampling_only": certificate.get(
            "sampled_preparation_strip_jacobian_is_negative"
        )
        is True,
        "parent_left_full_chart_injectivity_open": certificate.get(
            "target_chart_global_injectivity_proved"
        )
        is False,
    }
    if not all(checks.values()):
        raise ValueError("the C4 seam parent claim boundary changed")
    return checks


def validate_target_c4_history_bernstein_audit(
    audit: Mapping[str, object],
) -> None:
    """Reject algebraic weakening, false promotion, or record tampering."""

    if not isinstance(audit, Mapping):
        raise ValueError("history Bernstein audit must be a mapping")
    certificate = audit.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("history Bernstein audit requires a certificate")
    expected_fields = {
        field.name for field in fields(TargetC4HistoryBernsteinCertificate)
    }
    if set(certificate) != expected_fields:
        raise ValueError("history Bernstein certificate fields changed")
    if any(certificate.get(key) is not True for key in EXACT_TRUE_FLAGS):
        raise ValueError("an exact history Bernstein claim was weakened")
    if any(certificate.get(key) is not False for key in OPEN_FALSE_FLAGS):
        raise ValueError("an open physical or target-chart gate was promoted")
    if certificate.get("model_id") != MODEL_ID:
        raise ValueError("history Bernstein model id changed")
    if certificate.get("audit_id") != AUDIT_ID:
        raise ValueError("history Bernstein audit id changed")
    if certificate.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("history Bernstein arithmetic changed")
    if certificate.get("parent_result_sha256") != PARENT_RESULT_SHA256:
        raise ValueError("history Bernstein parent digest changed")
    records = certificate.get("patch_exact_bernstein_margins")
    if not isinstance(records, list) or len(records) != 3:
        raise ValueError("exactly three Bernstein margin records are required")
    if certificate.get("total_exact_bernstein_coefficient_count") != 210:
        raise ValueError("the exact Bernstein coefficient count changed")
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("every Bernstein margin record must be a mapping")
        if record.get("accepted_unit_box_count") != 1:
            raise ValueError("the exact certificate must cover one whole box")
        if record.get("subdivision_depth") != 0:
            raise ValueError("unexpected Bernstein subdivision appeared")
        if record.get("exact_reconstruction_identity_verified") is not True:
            raise ValueError("a Bernstein reconstruction identity was weakened")
        if (
            record.get("every_coefficient_strictly_above_rational_bound")
            is not True
        ):
            raise ValueError("a strict exact coefficient margin was weakened")
    if dict(audit) != json_ready_target_c4_history_bernstein():
        raise ValueError("history Bernstein audit differs from reference")


def validate_target_c4_history_bernstein_result(
    payload: Mapping[str, object], repository: Path
) -> None:
    """Validate a generated certificate, manifest, and exact seam parent."""

    if not isinstance(payload, Mapping):
        raise ValueError("history Bernstein result must be a mapping")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("history Bernstein result requires audit and manifest")
    validate_target_c4_history_bernstein_audit(audit)
    parent_checks = verify_parent_result(repository)
    expected_paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
    }
    for name, relative in expected_paths.items():
        if manifest.get(name) != relative:
            raise ValueError(f"manifest {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256(repository / relative):
            raise ValueError(f"manifest {name} digest changed")
    if manifest.get("parent_result") != PARENT_RESULT_RELATIVE_PATH:
        raise ValueError("manifest parent path changed")
    if manifest.get("parent_result_sha256") != PARENT_RESULT_SHA256:
        raise ValueError("manifest parent digest changed")
    if manifest.get("parent_claim_checks") != parent_checks:
        raise ValueError("manifest parent claim checks changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("manifest command changed")
    if manifest.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("manifest arithmetic changed")
    if manifest.get("python") != platform.python_version():
        raise ValueError("manifest Python version changed")
    if manifest.get("sympy") != sp.__version__:
        raise ValueError("manifest SymPy version changed")
    if manifest.get("platform") != platform.platform():
        raise ValueError("manifest platform changed")


__all__ = [
    "AUDIT_ID",
    "DEFAULT_COMMAND",
    "EXACT_TRUE_FLAGS",
    "ExactBernsteinForm",
    "ExactBernsteinMargin",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_ARITHMETIC",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "OPEN_FALSE_FLAGS",
    "PARENT_RESULT_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "PATCH_MARGIN_BY_NAME",
    "PROOF_SOURCE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "TargetC4HistoryBernsteinCertificate",
    "build_target_c4_history_bernstein_certificate",
    "exact_bernstein_margin_records",
    "exact_bernstein_reconstruction",
    "exact_c4_patch_state",
    "exact_history_p_matrix_polynomials",
    "exact_tensor_bernstein_form",
    "exact_unpatched_history_state",
    "json_ready_target_c4_history_bernstein",
    "quadratic_field_parts",
    "quadratic_field_sign",
    "validate_target_c4_history_bernstein_audit",
    "validate_target_c4_history_bernstein_result",
    "verify_parent_result",
]
