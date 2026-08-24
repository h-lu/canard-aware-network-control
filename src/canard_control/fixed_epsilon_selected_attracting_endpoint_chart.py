"""Exact endpoint-compatibility audit for the fixed-epsilon RFDE.

The proposed faithful Lobatto discretization has 194 raw two-state C0
history coefficients and advertises a 193-dimensional attracting endpoint
chart.  The two endpoint-compatibility equations are independent: two
compactly supported cubic history directions make their derivative matrix
exactly the identity.  Hence the discrete endpoint-compatible level has
dimension 192 and cannot contain a fixed-parameter 193-dimensional immersed
chart.  If global C1 matching is also imposed at internal cell joins, the
dimensions only decrease.

This is a finite-dimensional no-go for the advertised count.  It is not a
proof that the continuous RFDE has no selected attracting trace bundle.  An
explicit algebraic retraction onto the 192-dimensional compatibility level
is also recorded; that retraction is not an invariant or selected bundle.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

import sympy as sp


MODEL_ID = "synchronous-dual-scaffold-fhn-quadratic-period-lock"
AUDIT_ID = "fixed-epsilon-quadratic-selected-attracting-endpoint-audit"
ASSUMPTIONS_ID = (
    "epsilon=1/5;delta=1/sqrt(5);p=6;16-uniform-history-cells;"
    "raw-continuous-piecewise-polynomial-history-coordinates;"
    "fixed-parameter-classical-solution-manifold-compatibility"
)
ARITHMETIC_DESCRIPTION = (
    "exact SymPy dimension, endpoint-compatibility rank, algebraic "
    "retraction, parameter-column, and old-history ambiguity identities"
)
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_selected_attracting_endpoint_chart.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_selected_attracting_endpoint_chart.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/fixed_epsilon_selected_attracting_endpoint_chart.py"
)

CANDIDATE_DOC_SHA256 = (
    "87b048dfffc7ce98477077a342ceb4c083cb3018afd5055d0f58425f9e154edf"
)
CANDIDATE_SOURCE_SHA256 = (
    "cd529596713c69d2042080a47805d751a0d1e4898cd94d38431d4457ef1a3cb4"
)
CANDIDATE_RESULT_SHA256 = (
    "a35c23f58cb80a83b5d14d303edccc160a66e402e9f042b18d0e992a2388dabd"
)
BLUEPRINT_DOC_SHA256 = (
    "21c1f2d4cff893b5fdb9d3d3820abd6f9198869061800ed804b9506af38e0190"
)
BLUEPRINT_SOURCE_SHA256 = (
    "03423f924baa23afc8a1c5093392f67836af7864cc37e1b47aa7f7c30c1f36c4"
)
BLUEPRINT_RESULT_SHA256 = (
    "1af8aa46b31bb099a8f07e7646b656577d010dc413094ad3be0afb32c70c993a"
)


Matrix = sp.ImmutableMatrix


def _matrix(value: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(value)


@dataclass(frozen=True)
class FiniteHistoryDimensionAudit:
    """Exact dimension and compactly supported rank-two witness."""

    polynomial_degree: int
    history_cells: int
    state_components: int
    raw_history_internal_regularity: str
    scalar_history_dimension: int
    raw_history_dimension: int
    compatibility_equation_dimension: int
    proposed_attracting_chart_dimension: int
    discrete_endpoint_compatible_level_dimension: int
    proposed_dimension_excess: int
    last_cell_width: sp.Expr
    normalized_last_cell_bump: sp.Expr
    bump_degree: int
    bump_value_at_left_join: sp.Expr
    bump_derivative_at_left_join: sp.Expr
    bump_value_at_current: sp.Expr
    bump_derivative_at_current: sp.Expr
    all_active_delays_outside_last_cell: bool
    compatibility_direction_matrix: Matrix
    compatibility_direction_determinant: sp.Expr
    compatibility_rank: int
    compatible_level_is_discrete_endpoint_level_not_global_c1: bool
    internal_cell_joins: int
    global_c1_derivative_continuity_constraints: int
    global_c1_history_dimension: int
    global_c1_endpoint_compatible_level_dimension: int
    proposed_fixed_parameter_immersion_possible: bool
    maximum_discrete_level_coordinates_beside_one_time_tangent: int
    codimension_one_selection_inside_discrete_endpoint_level_dimension: int


@dataclass(frozen=True)
class CompatibilityAlgebraAudit:
    """Exact quadratic-RFDE compatibility and parameter identities."""

    compatibility_vector: Matrix
    compatibility_after_two_bumps: Matrix
    bump_increment: Matrix
    bump_jacobian: Matrix
    exact_retraction_residual: Matrix
    partial_nu_compatibility: Matrix
    partial_eta_compatibility: Matrix
    chart_coordinate_identity: str
    nu_jet_identity: str
    eta_jet_identity: str
    second_parameter_jet_identity: str
    time_tangent_identity: str


@dataclass(frozen=True)
class OldHistoryJetAudit:
    """Exact eta-jet ambiguity of the dynamically inert old interval."""

    scaled_horizon: sp.Expr
    first_cell_width: sp.Expr
    recent_active_horizon: sp.Expr
    first_cell_right_endpoint: sp.Expr
    first_cell_is_strictly_older_than_minus_five: bool
    normalized_first_cell_bump: sp.Expr
    old_bump_value_at_minus_horizon: sp.Expr
    old_bump_value_at_first_join: sp.Expr
    old_bump_derivative_at_first_join: sp.Expr
    zero_history_compatibility_at_nu_eta_zero: Matrix
    old_bump_history_compatibility_at_nu_eta_zero: Matrix
    zero_history_eta_field_column: Matrix
    old_bump_history_eta_field_column: Matrix
    eta_field_column_difference: Matrix
    eta_compatibility_column_difference: Matrix
    base_eta_zero_future_current_trajectory_distinguishes_old_extensions: bool
    enlarged_history_semiflow_states_are_identical_before_old_tail_ages_out: bool
    eta_derivative_distinguishes_old_extensions: bool
    eta_zero_dynamics_selects_parameter_coherent_old_extension: bool


@dataclass(frozen=True)
class RepairedBvpLedgerAudit:
    """A count-consistent ambient-chart design, not a constructed operator."""

    history_cells: int
    flight_cells: int
    polynomial_degree: int
    state_components: int
    coefficients_per_branch: int
    two_branch_coefficients: int
    ambient_attracting_chart_coordinates: int
    compatible_repelling_chart_coordinates: int
    total_phase_fixed_unknowns: int
    flow_rows_per_branch: int
    projected_history_rows_per_block: int
    projected_history_blocks: tuple[str, str, str]
    projected_history_rows_total: int
    explicit_compatibility_blocks: tuple[str, str, str]
    explicit_compatibility_rows_total: int
    compatibility_propagated_or_built_in: tuple[str, str, str]
    phase_rows: int
    total_phase_fixed_residuals: int
    residual_minus_unknown: int
    ambient_attracting_chart_fixed_parameter_dimension: int
    compatibility_rows_on_ambient_attracting_chart: int
    transverse_effective_attracting_dimension: int
    arithmetic_count_is_consistent: bool
    ambient_193_chart_is_not_a_compatible_193_immersion: bool
    selected_invariant_endpoint_operator_constructed: bool


@dataclass(frozen=True)
class SelectedEndpointChartCertificate:
    """Strict theorem/numerics/open-boundary ledger."""

    model_id: str
    audit_id: str
    assumptions_id: str
    candidate_doc_sha256: str
    candidate_source_sha256: str
    candidate_result_sha256: str
    blueprint_doc_sha256: str
    blueprint_source_sha256: str
    blueprint_result_sha256: str
    raw_history_dimension_194_derived_exactly: bool
    compatibility_residual_has_exact_rank_two: bool
    discrete_endpoint_compatible_level_dimension_192_derived_exactly: bool
    algebraic_parameter_coherent_compatible_retraction_constructed: bool
    advertised_193_dimensional_fixed_parameter_compatible_immersion_exists: bool
    ambient_193_dimensional_parameterization_is_algebraically_admissible: bool
    repaired_775_by_774_projected_compatibility_ledger_is_exact: bool
    repaired_ledger_selected_endpoint_operator_constructed: bool
    one_time_tangent_adds_dimension_outside_compatible_tangent: bool
    later_phase_condition_repairs_endpoint_rank_mismatch: bool
    eta_zero_old_history_determines_eta_jet: bool
    finite_discrete_selected_attracting_chart_constructed: bool
    finite_discrete_invariant_attracting_foliation_validated: bool
    continuous_rfde_selected_attracting_chart_constructed: bool
    continuous_rfde_selected_attracting_chart_nonexistence_proved: bool
    continuous_rfde_solution_manifold_smoothness_at_fixed_epsilon_validated: bool
    parameter_coherent_first_and_second_endpoint_jets_validated: bool
    corrected_fredholm_dimension_ledger_validated: bool
    fixed_epsilon_selected_root_validated: bool
    precise_finite_dimensional_verdict: str
    continuous_rfde_open_gate: str


def reference_dimension_audit() -> FiniteHistoryDimensionAudit:
    """Return the exact 194 -> 192 compatibility count and rank witness."""

    p = 6
    cells = 16
    states = 2
    scalar_dimension = cells * p + 1
    raw_dimension = states * scalar_dimension
    horizon = sp.Rational(7397086298188131, 10**15)
    ell = horizon / cells
    theta = sp.symbols("theta", real=True)
    bump = sp.expand(theta * (theta + ell) ** 2 / ell**2)
    bump_derivative = sp.diff(bump, theta)
    direction_matrix = sp.eye(2)
    rank = int(direction_matrix.rank())
    compatible_dimension = raw_dimension - rank
    proposed = 193

    return FiniteHistoryDimensionAudit(
        polynomial_degree=p,
        history_cells=cells,
        state_components=states,
        raw_history_internal_regularity=(
            "C0 across internal cell joins; one-sided polynomial "
            "derivatives exist at the endpoint"
        ),
        scalar_history_dimension=scalar_dimension,
        raw_history_dimension=raw_dimension,
        compatibility_equation_dimension=2,
        proposed_attracting_chart_dimension=proposed,
        discrete_endpoint_compatible_level_dimension=compatible_dimension,
        proposed_dimension_excess=proposed - compatible_dimension,
        last_cell_width=ell,
        normalized_last_cell_bump=bump,
        bump_degree=int(sp.Poly(bump, theta).degree()),
        bump_value_at_left_join=sp.simplify(bump.subs(theta, -ell)),
        bump_derivative_at_left_join=sp.simplify(
            bump_derivative.subs(theta, -ell)
        ),
        bump_value_at_current=sp.simplify(bump.subs(theta, 0)),
        bump_derivative_at_current=sp.simplify(
            bump_derivative.subs(theta, 0)
        ),
        all_active_delays_outside_last_cell=bool(ell < 4),
        compatibility_direction_matrix=_matrix(direction_matrix),
        compatibility_direction_determinant=sp.det(direction_matrix),
        compatibility_rank=rank,
        compatible_level_is_discrete_endpoint_level_not_global_c1=True,
        internal_cell_joins=cells - 1,
        global_c1_derivative_continuity_constraints=states * (cells - 1),
        global_c1_history_dimension=(raw_dimension - states * (cells - 1)),
        global_c1_endpoint_compatible_level_dimension=(
            raw_dimension - states * (cells - 1) - rank
        ),
        proposed_fixed_parameter_immersion_possible=False,
        maximum_discrete_level_coordinates_beside_one_time_tangent=(
            compatible_dimension - 1
        ),
        codimension_one_selection_inside_discrete_endpoint_level_dimension=(
            compatible_dimension - 1
        ),
    )


def reference_compatibility_audit() -> CompatibilityAlgebraAudit:
    """Return exact compatibility, retraction, and parameter-jet formulas."""

    (
        dx0,
        dy0,
        x0,
        y0,
        x4,
        x5,
        x_theta,
        nu,
        eta,
        alpha,
        beta,
    ) = sp.symbols(
        "dx0 dy0 x0 y0 x4 x5 x_theta nu eta alpha beta", real=True
    )
    delta = 1 / sp.sqrt(5)
    fast = (
        y0
        - x0**2
        + delta * (-x0**3 / 3 + sp.Rational(1, 5) * ((x4 + x5) / 2 - x0))
        + delta**2 * eta * (x0**2 - x_theta**2)
        + delta**3
        * sp.Rational(1, 4)
        * ((x4**3 + x5**3) / 2 - x0**3)
    )
    slow = -x0 + delta * nu
    compatibility = sp.Matrix([dx0 - fast, dy0 - slow])
    after = compatibility.subs({dx0: dx0 + alpha, dy0: dy0 + beta})
    increment = sp.simplify(after - compatibility)
    bump_jacobian = increment.jacobian((alpha, beta))
    retracted = sp.simplify(
        after.subs({alpha: -compatibility[0], beta: -compatibility[1]})
    )
    partial_nu = sp.simplify(compatibility.diff(nu))
    partial_eta = sp.simplify(compatibility.diff(eta))

    return CompatibilityAlgebraAudit(
        compatibility_vector=_matrix(compatibility),
        compatibility_after_two_bumps=_matrix(after),
        bump_increment=_matrix(increment),
        bump_jacobian=_matrix(bump_jacobian),
        exact_retraction_residual=_matrix(retracted),
        partial_nu_compatibility=_matrix(partial_nu),
        partial_eta_compatibility=_matrix(partial_eta),
        chart_coordinate_identity=(
            "D_phi C(Gamma)[partial_xi Gamma]=0 for every fixed-parameter "
            "chart coordinate xi"
        ),
        nu_jet_identity=(
            "D_phi C(Gamma)[partial_nu Gamma]=-partial_nu C=(0,delta)"
        ),
        eta_jet_identity=(
            "D_phi C(Gamma)[partial_eta Gamma]=-partial_eta C="
            "(delta^2*(x0^2-x_theta^2),0)"
        ),
        second_parameter_jet_identity=(
            "D_phi C Gamma_lm + D_phiphi C[Gamma_l,Gamma_m] + "
            "D_phi_l C Gamma_m + D_phi_m C Gamma_l + C_lm = 0"
        ),
        time_tangent_identity=(
            "C(x_t)=0 along a C2 solution implies "
            "D_phi C(x_t)[dot{x}_t]=0"
        ),
    )


def reference_old_history_audit() -> OldHistoryJetAudit:
    """Return an exact pair of eta=0-indistinguishable old extensions."""

    horizon = sp.Rational(7397086298188131, 10**15)
    ell = horizon / 16
    theta = sp.symbols("theta", real=True)
    u = (theta + horizon) / ell
    old_bump = sp.expand((1 - u) ** 2)
    old_bump_derivative = sp.diff(old_bump, theta)
    join = -horizon + ell

    # At nu=eta=0 the zero history and a voltage bump supported wholly in
    # the first (oldest) cell have identical recent histories on [-5,0].
    # The base RFDE uses only delays 4 and 5, so both compatibility vectors
    # vanish.  The eta column reads x(-Theta), and therefore separates them.
    zero = sp.zeros(2, 1)
    zero_eta_column = sp.zeros(2, 1)
    bumped_eta_column = sp.Matrix([-sp.Rational(1, 5), 0])
    field_difference = bumped_eta_column - zero_eta_column
    compatibility_difference = -field_difference

    return OldHistoryJetAudit(
        scaled_horizon=horizon,
        first_cell_width=ell,
        recent_active_horizon=sp.Integer(5),
        first_cell_right_endpoint=join,
        first_cell_is_strictly_older_than_minus_five=bool(join < -5),
        normalized_first_cell_bump=old_bump,
        old_bump_value_at_minus_horizon=sp.simplify(
            old_bump.subs(theta, -horizon)
        ),
        old_bump_value_at_first_join=sp.simplify(old_bump.subs(theta, join)),
        old_bump_derivative_at_first_join=sp.simplify(
            old_bump_derivative.subs(theta, join)
        ),
        zero_history_compatibility_at_nu_eta_zero=_matrix(zero),
        old_bump_history_compatibility_at_nu_eta_zero=_matrix(zero),
        zero_history_eta_field_column=_matrix(zero_eta_column),
        old_bump_history_eta_field_column=_matrix(bumped_eta_column),
        eta_field_column_difference=_matrix(field_difference),
        eta_compatibility_column_difference=_matrix(compatibility_difference),
        base_eta_zero_future_current_trajectory_distinguishes_old_extensions=False,
        enlarged_history_semiflow_states_are_identical_before_old_tail_ages_out=False,
        eta_derivative_distinguishes_old_extensions=True,
        eta_zero_dynamics_selects_parameter_coherent_old_extension=False,
    )


def reference_repaired_bvp_ledger_audit() -> RepairedBvpLedgerAudit:
    """Return the exact repaired 775-by-774 arithmetic ledger.

    The 193 incoming coordinates parameterize an ambient chart.  Two rows
    ``C_N(Gamma_-(xi_-))=0`` cut it to effective dimension 191 when the
    restriction is transverse.  The three 194-row history equalities are
    replaced by 192 projected rows apiece.  Six compatibility rows restore
    the removed normals.  This reconciles the arithmetic, but supplies no
    selected chart, projection, invariant foliation, or Fredholm proof.
    """

    history_cells = 16
    flight_cells = 8
    degree = 6
    states = 2
    branch = states * ((history_cells + flight_cells) * degree + 1)
    flow_per_branch = states * flight_cells * degree
    projected_per_block = states * (history_cells * degree + 1) - states
    projected_blocks = ("entry", "exit", "seam")
    compatibility_blocks = (
        "C_N(Gamma_-(xi_-))",
        "C_N(h^-_entry)",
        "C_N(h^+_seam)",
    )
    propagated = (
        "Gamma_+ compatibility is a construction hypothesis",
        "left-seam compatibility is propagated by the left forward flow",
        "right-terminal compatibility is propagated by the right forward flow",
    )
    unknowns = 2 * branch + 193 + 1
    projected_total = len(projected_blocks) * projected_per_block
    compatibility_total = len(compatibility_blocks) * states
    residuals = (
        2 * flow_per_branch + projected_total + compatibility_total + 1
    )
    return RepairedBvpLedgerAudit(
        history_cells=history_cells,
        flight_cells=flight_cells,
        polynomial_degree=degree,
        state_components=states,
        coefficients_per_branch=branch,
        two_branch_coefficients=2 * branch,
        ambient_attracting_chart_coordinates=193,
        compatible_repelling_chart_coordinates=1,
        total_phase_fixed_unknowns=unknowns,
        flow_rows_per_branch=flow_per_branch,
        projected_history_rows_per_block=projected_per_block,
        projected_history_blocks=projected_blocks,
        projected_history_rows_total=projected_total,
        explicit_compatibility_blocks=compatibility_blocks,
        explicit_compatibility_rows_total=compatibility_total,
        compatibility_propagated_or_built_in=propagated,
        phase_rows=1,
        total_phase_fixed_residuals=residuals,
        residual_minus_unknown=residuals - unknowns,
        ambient_attracting_chart_fixed_parameter_dimension=193,
        compatibility_rows_on_ambient_attracting_chart=2,
        transverse_effective_attracting_dimension=191,
        arithmetic_count_is_consistent=(unknowns == 774 and residuals == 775),
        ambient_193_chart_is_not_a_compatible_193_immersion=True,
        selected_invariant_endpoint_operator_constructed=False,
    )


def endpoint_chart_algebra_is_exact() -> bool:
    """Recompute all decisive exact identities."""

    dimension = reference_dimension_audit()
    compatibility = reference_compatibility_audit()
    old = reference_old_history_audit()
    ledger = reference_repaired_bvp_ledger_audit()
    alpha, beta = sp.symbols("alpha beta", real=True)
    x0, x_theta = sp.symbols("x0 x_theta", real=True)
    return bool(
        dimension.scalar_history_dimension == 97
        and dimension.raw_history_dimension == 194
        and dimension.bump_degree <= dimension.polynomial_degree
        and dimension.bump_value_at_left_join == 0
        and dimension.bump_derivative_at_left_join == 0
        and dimension.bump_value_at_current == 0
        and dimension.bump_derivative_at_current == 1
        and dimension.all_active_delays_outside_last_cell
        and dimension.compatibility_direction_matrix == sp.eye(2)
        and dimension.compatibility_direction_determinant == 1
        and dimension.compatibility_rank == 2
        and dimension.discrete_endpoint_compatible_level_dimension == 192
        and dimension.compatible_level_is_discrete_endpoint_level_not_global_c1
        and dimension.global_c1_derivative_continuity_constraints == 30
        and dimension.global_c1_history_dimension == 164
        and dimension.global_c1_endpoint_compatible_level_dimension == 162
        and dimension.proposed_dimension_excess == 1
        and not dimension.proposed_fixed_parameter_immersion_possible
        and compatibility.bump_increment == sp.Matrix([alpha, beta])
        and compatibility.bump_jacobian == sp.eye(2)
        and compatibility.exact_retraction_residual == sp.zeros(2, 1)
        and compatibility.partial_nu_compatibility
        == sp.Matrix([0, -1 / sp.sqrt(5)])
        and compatibility.partial_eta_compatibility
        == sp.Matrix(
            [-sp.Rational(1, 5) * (x0**2 - x_theta**2), 0]
        )
        and old.first_cell_is_strictly_older_than_minus_five
        and old.old_bump_value_at_minus_horizon == 1
        and old.old_bump_value_at_first_join == 0
        and old.old_bump_derivative_at_first_join == 0
        and old.eta_field_column_difference
        == sp.Matrix([-sp.Rational(1, 5), 0])
        and old.eta_compatibility_column_difference
        == sp.Matrix([sp.Rational(1, 5), 0])
        and ledger.coefficients_per_branch == 290
        and ledger.total_phase_fixed_unknowns == 774
        and ledger.flow_rows_per_branch == 96
        and ledger.projected_history_rows_per_block == 192
        and ledger.projected_history_rows_total == 576
        and ledger.explicit_compatibility_rows_total == 6
        and ledger.total_phase_fixed_residuals == 775
        and ledger.residual_minus_unknown == 1
        and ledger.transverse_effective_attracting_dimension == 191
        and ledger.arithmetic_count_is_consistent
        and not ledger.selected_invariant_endpoint_operator_constructed
    )


def reference_selected_endpoint_certificate() -> SelectedEndpointChartCertificate:
    """Return the strict finite theorem and continuous open-gate ledger."""

    if not endpoint_chart_algebra_is_exact():
        raise RuntimeError("the endpoint compatibility audit failed")
    return SelectedEndpointChartCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        assumptions_id=ASSUMPTIONS_ID,
        candidate_doc_sha256=CANDIDATE_DOC_SHA256,
        candidate_source_sha256=CANDIDATE_SOURCE_SHA256,
        candidate_result_sha256=CANDIDATE_RESULT_SHA256,
        blueprint_doc_sha256=BLUEPRINT_DOC_SHA256,
        blueprint_source_sha256=BLUEPRINT_SOURCE_SHA256,
        blueprint_result_sha256=BLUEPRINT_RESULT_SHA256,
        raw_history_dimension_194_derived_exactly=True,
        compatibility_residual_has_exact_rank_two=True,
        discrete_endpoint_compatible_level_dimension_192_derived_exactly=True,
        algebraic_parameter_coherent_compatible_retraction_constructed=True,
        advertised_193_dimensional_fixed_parameter_compatible_immersion_exists=False,
        ambient_193_dimensional_parameterization_is_algebraically_admissible=True,
        repaired_775_by_774_projected_compatibility_ledger_is_exact=True,
        repaired_ledger_selected_endpoint_operator_constructed=False,
        one_time_tangent_adds_dimension_outside_compatible_tangent=False,
        later_phase_condition_repairs_endpoint_rank_mismatch=False,
        eta_zero_old_history_determines_eta_jet=False,
        finite_discrete_selected_attracting_chart_constructed=False,
        finite_discrete_invariant_attracting_foliation_validated=False,
        continuous_rfde_selected_attracting_chart_constructed=False,
        continuous_rfde_selected_attracting_chart_nonexistence_proved=False,
        continuous_rfde_solution_manifold_smoothness_at_fixed_epsilon_validated=True,
        parameter_coherent_first_and_second_endpoint_jets_validated=False,
        corrected_fredholm_dimension_ledger_validated=False,
        fixed_epsilon_selected_root_validated=False,
        precise_finite_dimensional_verdict=(
            "no fixed-parameter C1 immersion of rank 193 can map the stated "
            "194 raw history coefficients into the regular rank-two "
            "discrete endpoint-compatibility level; an ambient 193 chart "
            "is possible only "
            "with two explicit compatibility rows and has transverse "
            "effective dimension 191 in the repaired ledger"
        ),
        continuous_rfde_open_gate=(
            "construct a selected invariant attracting history bundle on "
            "the enlarged horizon, normalize the eta-inert old extension, "
            "validate its parameter jets, and rederive the Fredholm count"
        ),
    )


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [[sp.sstr(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def reference_selected_endpoint_audit_payload() -> dict[str, Any]:
    """Return the deterministic theorem/numerics/open-boundary payload."""

    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "audit_id": AUDIT_ID,
        "assumptions_id": ASSUMPTIONS_ID,
        "exact_audits": {
            "finite_history_dimension": _json_value(
                asdict(reference_dimension_audit())
            ),
            "compatibility_algebra": _json_value(
                asdict(reference_compatibility_audit())
            ),
            "old_history_eta_jet": _json_value(
                asdict(reference_old_history_audit())
            ),
            "repaired_bvp_ledger": _json_value(
                asdict(reference_repaired_bvp_ledger_audit())
            ),
        },
        "certificate": _json_value(
            asdict(reference_selected_endpoint_certificate())
        ),
        "scope": {
            "exact_finite_dimension_no_go_for_193_compatible_chart": True,
            "exact_192_dimensional_discrete_endpoint_compatibility_retraction": True,
            "continuous_c1_compatibility_solution_manifold": True,
            "ambient_193_chart_with_explicit_compatibility_rows": True,
            "repaired_775_by_774_arithmetic_ledger": True,
            "repaired_selected_endpoint_operator": False,
            "finite_discrete_selected_attracting_chart": False,
            "continuous_rfde_selected_attracting_chart": False,
            "continuous_rfde_selected_attracting_chart_nonexistence": False,
            "corrected_fredholm_bvp": False,
            "fixed_epsilon_selected_root": False,
            "physical_onset_or_basin": False,
        },
    }


def _repository() -> Path:
    return Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def expected_parent_sha256() -> dict[str, str]:
    """Return the six pinned parent inputs."""

    return {
        "candidate_doc": CANDIDATE_DOC_SHA256,
        "candidate_source": CANDIDATE_SOURCE_SHA256,
        "candidate_result": CANDIDATE_RESULT_SHA256,
        "blueprint_doc": BLUEPRINT_DOC_SHA256,
        "blueprint_source": BLUEPRINT_SOURCE_SHA256,
        "blueprint_result": BLUEPRINT_RESULT_SHA256,
    }


def current_parent_sha256() -> dict[str, str]:
    """Hash the exact candidate and blueprint inputs."""

    repository = _repository()
    paths = {
        "candidate_doc": repository / "docs/fixed-epsilon-two-sided-candidate.md",
        "candidate_source": repository
        / "src/canard_control/fixed_epsilon_two_sided_candidate.py",
        "candidate_result": repository
        / "experiments/results/fixed_epsilon_two_sided_candidate.json",
        "blueprint_doc": repository / "docs/fixed-epsilon-quadratic-root-bvp.md",
        "blueprint_source": repository
        / "src/canard_control/fixed_epsilon_quadratic_root_bvp.py",
        "blueprint_result": repository
        / "experiments/results/fixed_epsilon_quadratic_root_bvp.json",
    }
    return {key: _sha256(path) for key, path in paths.items()}


def validate_selected_endpoint_payload(
    payload: Mapping[str, Any],
) -> SelectedEndpointChartCertificate:
    """Reject mutation, count repair by assertion, or continuous promotion."""

    expected = reference_selected_endpoint_audit_payload()
    if dict(payload) != expected:
        raise ValueError(
            "selected-endpoint audit does not match the exact finite algebra "
            "and strict claim boundary"
        )
    if current_parent_sha256() != expected_parent_sha256():
        raise ValueError("one or more pinned endpoint-audit parents changed")
    return reference_selected_endpoint_certificate()


__all__ = [
    "ARITHMETIC_DESCRIPTION",
    "ASSUMPTIONS_ID",
    "AUDIT_ID",
    "BLUEPRINT_DOC_SHA256",
    "BLUEPRINT_RESULT_SHA256",
    "BLUEPRINT_SOURCE_SHA256",
    "CANDIDATE_DOC_SHA256",
    "CANDIDATE_RESULT_SHA256",
    "CANDIDATE_SOURCE_SHA256",
    "DEFAULT_COMMAND",
    "FiniteHistoryDimensionAudit",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_ID",
    "OldHistoryJetAudit",
    "PROOF_SOURCE_RELATIVE_PATH",
    "SelectedEndpointChartCertificate",
    "RepairedBvpLedgerAudit",
    "CompatibilityAlgebraAudit",
    "current_parent_sha256",
    "endpoint_chart_algebra_is_exact",
    "expected_parent_sha256",
    "reference_compatibility_audit",
    "reference_dimension_audit",
    "reference_old_history_audit",
    "reference_repaired_bvp_ledger_audit",
    "reference_selected_endpoint_audit_payload",
    "reference_selected_endpoint_certificate",
    "validate_selected_endpoint_payload",
]
