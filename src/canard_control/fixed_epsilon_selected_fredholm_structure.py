"""Exact finite-section ledger for the selected fixed-epsilon Fredholm BVP.

This module repairs an endpoint-compatibility omission in the previously
proposed ``775 x 774`` ambient coefficient ledger.  The 194-dimensional
piecewise-polynomial history space used here is C0 across cell joins.  The
module proves an exact rank-two statement for its discrete endpoint-
compatibility map and gives a concrete 192-row projection.  It does *not*
provide a globally C1/W2 spectral realization, construct the selected
endpoint charts or rectangular derivative, or validate an interval inverse.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

import sympy as sp


MODEL_ID = "synchronous-dual-scaffold-fhn-quadratic-period-lock"

# These pins are deliberately collected in one place.  The upstream
# two-sided candidate may be regenerated when its obsolete endpoint ledger is
# replaced by the repaired ledger proved here.
BLUEPRINT_SOURCE_SHA256 = (
    "03423f924baa23afc8a1c5093392f67836af7864cc37e1b47aa7f7c30c1f36c4"
)
BLUEPRINT_RESULT_SHA256 = (
    "1af8aa46b31bb099a8f07e7646b656577d010dc413094ad3be0afb32c70c993a"
)
BLUEPRINT_NOTE_SHA256 = (
    "b0e10e37deb71ce9fb7bcde0b173694eb76d8b96ab631eb9d477ef6d11fb79ba"
)
CANDIDATE_SOURCE_SHA256 = (
    "282bfdcb26e082470894724eeffe4c094dff0a138cbb3bf956b4caef45eb482a"
)
CANDIDATE_RESULT_SHA256 = (
    "b22c336c64f1e2187a013fd597e1a93624c8bf1ef83e5549abcc558ad684c5a6"
)
CANDIDATE_NOTE_SHA256 = (
    "87b048dfffc7ce98477077a342ceb4c083cb3018afd5055d0f58425f9e154edf"
)


@dataclass(frozen=True)
class FredholmDimensionLedger:
    """Exact coefficient, residual, border, and root-system dimensions."""

    polynomial_degree: int
    history_cells: int
    flight_cells_per_branch: int
    state_dimension: int
    scalar_history_dimension: int
    raw_history_dimension: int
    compatibility_rank: int
    compatible_history_dimension: int
    attracting_normal_codimension: int
    effective_attracting_trace_dimension: int
    ambient_entry_chart_coordinates: int
    compatible_exit_chart_coordinates: int
    branch_state_coefficients: int
    phase_fixed_unknown_dimension: int
    flow_rows_per_branch: int
    projected_entry_rows: int
    projected_seam_rows: int
    projected_exit_rows: int
    left_initial_compatibility_rows: int
    entry_chart_compatibility_rows: int
    right_initial_compatibility_rows: int
    phase_rows: int
    phase_fixed_residual_dimension: int
    jump_complement_square_dimension: int
    gap_root_square_dimension: int


@dataclass(frozen=True)
class CompatibilityStructure:
    """Concrete coordinates and exact rank-two compatibility proof."""

    history_coordinate_representation: str
    last_cell_width_condition: str
    endpoint_bubble: str
    bubble_endpoint_values: tuple[str, str]
    bubble_right_derivative: str
    delayed_samples_unchanged: bool
    compatibility_map: str
    retained_projection: str
    projection_shape: tuple[int, int]
    bubble_right_inverse_shape: tuple[int, int]
    projection_times_right_inverse_is_zero: bool
    compatibility_jacobian_times_right_inverse_is_identity: bool
    stacked_coordinate_jacobian: str
    stacked_coordinate_jacobian_determinant: str
    stacked_coordinate_jacobian_inverse: str
    compatibility_rank_two_proved_for_every_frozen_history: bool


@dataclass(frozen=True)
class FredholmClaimLedger:
    """Structural conclusions and explicit theorem refusals."""

    raw_775_count_without_compatibility_is_valid: bool
    three_raw_194_history_equalities_are_retained: bool
    three_raw_equalities_are_simply_deleted: bool
    three_projected_equalities_plus_compatibility_rows_defined: bool
    compatibility_rank_two_structurally_proved: bool
    compatible_history_dimension_proved: bool
    effective_attracting_trace_dimension_if_transverse: int
    ambient_repaired_775_by_774_ledger_defined: bool
    repaired_ledger_is_fredholm_invertibility_evidence: bool
    entry_chart_compatibility_transversality_validated: bool
    exit_chart_compatibility_is_a_construction_hypothesis: bool
    terminal_compatibility_requires_right_inclusive_flow_collocation: bool
    raw_history_space_is_only_c0_across_cell_joins: bool
    global_c1_or_w2_realization_validated: bool
    internal_derivative_jump_rows_counted: bool
    selected_entry_chart_constructed: bool
    selected_exit_chart_constructed: bool
    actual_775_by_774_derivative_constructed: bool
    full_column_rank_validated: bool
    one_dimensional_cokernel_validated: bool
    jump_complement_frozen: bool
    bordered_inverse_validated: bool
    continuous_advanced_adjoint_with_boundary_multipliers_validated: bool
    coefficient_tail_bound_validated: bool
    period_interval_propagated: bool
    selected_root_validated: bool
    rho_star_enclosed_away_from_zero: bool


def reference_dimension_ledger() -> FredholmDimensionLedger:
    """Return the repaired exact finite-section count."""

    p = 6
    history_cells = 16
    flight_cells = 8
    state_dimension = 2
    scalar_history = p * history_cells + 1
    raw_history = state_dimension * scalar_history
    compatibility_rank = state_dimension
    compatible_history = raw_history - compatibility_rank
    attracting_normal_codimension = 1
    effective_attracting = compatible_history - attracting_normal_codimension
    ambient_entry = raw_history - attracting_normal_codimension
    compatible_exit = 1
    branch = state_dimension * (p * (history_cells + flight_cells) + 1)
    unknowns = 2 * branch + ambient_entry + compatible_exit
    flow = state_dimension * p * flight_cells
    projected = compatible_history
    residuals = 2 * flow + 3 * projected + 3 * compatibility_rank + 1
    return FredholmDimensionLedger(
        polynomial_degree=p,
        history_cells=history_cells,
        flight_cells_per_branch=flight_cells,
        state_dimension=state_dimension,
        scalar_history_dimension=scalar_history,
        raw_history_dimension=raw_history,
        compatibility_rank=compatibility_rank,
        compatible_history_dimension=compatible_history,
        attracting_normal_codimension=attracting_normal_codimension,
        effective_attracting_trace_dimension=effective_attracting,
        ambient_entry_chart_coordinates=ambient_entry,
        compatible_exit_chart_coordinates=compatible_exit,
        branch_state_coefficients=branch,
        phase_fixed_unknown_dimension=unknowns,
        flow_rows_per_branch=flow,
        projected_entry_rows=projected,
        projected_seam_rows=projected,
        projected_exit_rows=projected,
        left_initial_compatibility_rows=compatibility_rank,
        entry_chart_compatibility_rows=compatibility_rank,
        right_initial_compatibility_rows=compatibility_rank,
        phase_rows=1,
        phase_fixed_residual_dimension=residuals,
        jump_complement_square_dimension=residuals,
        gap_root_square_dimension=residuals + 1,
    )


def retained_projection_matrix() -> sp.SparseMatrix:
    """Return the concrete P_N=[I_192 0] in the declared bubble basis."""

    ledger = reference_dimension_ledger()
    kept = ledger.compatible_history_dimension
    raw = ledger.raw_history_dimension
    return sp.SparseMatrix(kept, raw, {(j, j): 1 for j in range(kept)})


def endpoint_bubble_right_inverse() -> sp.SparseMatrix:
    """Return E_N whose columns are the X and Y endpoint bubbles."""

    ledger = reference_dimension_ledger()
    kept = ledger.compatible_history_dimension
    raw = ledger.raw_history_dimension
    return sp.SparseMatrix(
        raw,
        ledger.compatibility_rank,
        {(kept + j, j): 1 for j in range(ledger.compatibility_rank)},
    )


def compatibility_jacobian_from_remainder(
    remainder: sp.MatrixBase,
) -> sp.MatrixBase:
    """Return DC_N=[A I_2] for any frozen-history remainder block A."""

    ledger = reference_dimension_ledger()
    expected = (
        ledger.compatibility_rank,
        ledger.compatible_history_dimension,
    )
    if remainder.shape != expected:
        raise ValueError(f"compatibility remainder must have shape {expected}")
    return remainder.row_join(sp.eye(ledger.compatibility_rank))


def stacked_compatibility_coordinates(
    remainder: sp.MatrixBase,
) -> sp.MatrixBase:
    """Return [P_N;DC_N]=[[I,0],[A,I]] at a frozen history."""

    return retained_projection_matrix().col_join(
        compatibility_jacobian_from_remainder(remainder)
    )


def verify_exact_compatibility_structure() -> bool:
    """Verify the endpoint bubble and block-coordinate proof exactly."""

    u, ell = sp.symbols("u ell", positive=True)
    bubble = ell * u * (u - 1)
    endpoint_identity = bool(
        sp.simplify(bubble.subs(u, 0)) == 0
        and sp.simplify(bubble.subs(u, 1)) == 0
        and sp.simplify(sp.diff(bubble, u).subs(u, 1) / ell) == 1
    )
    ledger = reference_dimension_ledger()
    # A deterministic exact A checks the full block algebra.  The symbolic
    # proof is uniform in A because only block multiplication is used.
    remainder = sp.Matrix(
        ledger.compatibility_rank,
        ledger.compatible_history_dimension,
        lambda i, j: sp.Rational((i + 1) * ((j % 7) - 3), j + 11),
    )
    projection = retained_projection_matrix()
    right_inverse = endpoint_bubble_right_inverse()
    derivative = compatibility_jacobian_from_remainder(remainder)
    stacked = stacked_compatibility_coordinates(remainder)
    block_inverse = sp.eye(ledger.compatible_history_dimension).row_join(
        sp.zeros(
            ledger.compatible_history_dimension,
            ledger.compatibility_rank,
        )
    ).col_join(
        (-remainder).row_join(sp.eye(ledger.compatibility_rank))
    )
    return bool(
        endpoint_identity
        and projection * right_inverse
        == sp.zeros(
            ledger.compatible_history_dimension,
            ledger.compatibility_rank,
        )
        and derivative * right_inverse == sp.eye(ledger.compatibility_rank)
        and stacked * block_inverse
        == sp.eye(ledger.raw_history_dimension)
        and block_inverse * stacked
        == sp.eye(ledger.raw_history_dimension)
    )


def reference_compatibility_structure() -> CompatibilityStructure:
    """Return the exact compatibility-coordinate certificate."""

    ledger = reference_dimension_ledger()
    projection = retained_projection_matrix()
    right_inverse = endpoint_bubble_right_inverse()
    zero_product = projection * right_inverse == sp.zeros(
        ledger.compatible_history_dimension,
        ledger.compatibility_rank,
    )
    return CompatibilityStructure(
        history_coordinate_representation=(
            "C0 only across cell joins; per component: 17 shared endpoint "
            "values plus 5 endpoint-zero bubble coefficients on each of 16 "
            "degree-6 cells; reorder the two last-cell ell*u*(u-1) "
            "coefficients as alpha_X,alpha_Y"
        ),
        last_cell_width_condition="0<ell<min{4,5,Theta_*}",
        endpoint_bubble="b(u)=ell*u*(u-1), 0<=u<=1",
        bubble_endpoint_values=("b(0)=0", "b(1)=0"),
        bubble_right_derivative="d b/d theta at u=1 equals 1",
        delayed_samples_unchanged=True,
        compatibility_map=(
            "C_N(phi)=partial_theta^- phi(0)-f(phi(0),phi(-4),"
            "phi(-5),phi(-Theta_*);nu,eta)"
        ),
        retained_projection="P_N=[I_192 0] in (r,alpha_X,alpha_Y) coordinates",
        projection_shape=projection.shape,
        bubble_right_inverse_shape=right_inverse.shape,
        projection_times_right_inverse_is_zero=bool(zero_product),
        compatibility_jacobian_times_right_inverse_is_identity=True,
        stacked_coordinate_jacobian="[P_N;DC_N]=[[I_192,0],[A(bar_phi),I_2]]",
        stacked_coordinate_jacobian_determinant="1",
        stacked_coordinate_jacobian_inverse="[[I_192,0],[-A(bar_phi),I_2]]",
        compatibility_rank_two_proved_for_every_frozen_history=(
            verify_exact_compatibility_structure()
        ),
    )


def exact_parameter_columns() -> dict[str, str]:
    """Return exact fold-time residual columns and moving-delay factors."""

    return {
        "residual_convention": "R=x'-f",
        "nu_interior_column": "R_nu=(0,-delta)^T",
        "eta_interior_column": (
            "R_eta=(-delta^2*(X^2-X_Theta^2),0)^T"
        ),
        "scaled_delay_column": (
            "R_Theta=(-2*delta^2*eta*X_Theta*X_Theta_prime,0)^T"
        ),
        "physical_period_column": (
            "R_T=delta*R_Theta=(-2*delta^3*eta*X_Theta*"
            "X_Theta_prime,0)^T"
        ),
        "physical_period_column_at_eta_zero": "R_T|_{eta=0}=0",
        "eta_period_mixed_column_at_eta_zero": (
            "partial_eta R_T|_{eta=0}=(-2*delta^3*X_Theta*"
            "X_Theta_prime,0)^T"
        ),
        "endpoint_requirement": (
            "append parameter derivatives of both endpoint charts; on a "
            "moving domain also append the chosen trivialization columns"
        ),
    }


def exact_parameter_columns_are_valid() -> bool:
    """Check the signs and all delta factors symbolically."""

    delta = sp.sqrt(5) / 5
    eta, x_theta, x_theta_prime = sp.symbols(
        "eta X_Theta X_Theta_prime", real=True
    )
    shifted_term = -delta**2 * eta * x_theta**2
    # d/dTheta X(s-Theta)=-X'(s-Theta).
    field_theta = sp.diff(shifted_term, x_theta) * (-x_theta_prime)
    residual_theta = -field_theta
    residual_period = sp.simplify(delta * residual_theta)
    expected_theta = -2 * delta**2 * eta * x_theta * x_theta_prime
    expected_period = -2 * delta**3 * eta * x_theta * x_theta_prime
    expected_mixed = -2 * delta**3 * x_theta * x_theta_prime
    return bool(
        sp.simplify(residual_theta - expected_theta) == 0
        and sp.simplify(residual_period - expected_period) == 0
        and residual_period.subs(eta, 0) == 0
        and sp.simplify(
            sp.diff(residual_period, eta).subs(eta, 0) - expected_mixed
        )
        == 0
    )


def reference_claim_ledger() -> FredholmClaimLedger:
    """Return exact achievements and non-achievements of this package."""

    return FredholmClaimLedger(
        raw_775_count_without_compatibility_is_valid=False,
        three_raw_194_history_equalities_are_retained=False,
        three_raw_equalities_are_simply_deleted=False,
        three_projected_equalities_plus_compatibility_rows_defined=True,
        compatibility_rank_two_structurally_proved=True,
        compatible_history_dimension_proved=True,
        effective_attracting_trace_dimension_if_transverse=191,
        ambient_repaired_775_by_774_ledger_defined=True,
        repaired_ledger_is_fredholm_invertibility_evidence=False,
        entry_chart_compatibility_transversality_validated=False,
        exit_chart_compatibility_is_a_construction_hypothesis=True,
        terminal_compatibility_requires_right_inclusive_flow_collocation=True,
        raw_history_space_is_only_c0_across_cell_joins=True,
        global_c1_or_w2_realization_validated=False,
        internal_derivative_jump_rows_counted=False,
        selected_entry_chart_constructed=False,
        selected_exit_chart_constructed=False,
        actual_775_by_774_derivative_constructed=False,
        full_column_rank_validated=False,
        one_dimensional_cokernel_validated=False,
        jump_complement_frozen=False,
        bordered_inverse_validated=False,
        continuous_advanced_adjoint_with_boundary_multipliers_validated=False,
        coefficient_tail_bound_validated=False,
        period_interval_propagated=False,
        selected_root_validated=False,
        rho_star_enclosed_away_from_zero=False,
    )


def reference_selected_fredholm_structure_payload() -> dict[str, Any]:
    """Return the deterministic structural certificate and refusal ledger."""

    ledger = reference_dimension_ledger()
    compatibility = asdict(reference_compatibility_structure())
    compatibility["bubble_endpoint_values"] = list(
        compatibility["bubble_endpoint_values"]
    )
    compatibility["projection_shape"] = list(compatibility["projection_shape"])
    compatibility["bubble_right_inverse_shape"] = list(
        compatibility["bubble_right_inverse_shape"]
    )
    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "dimension_ledger": asdict(ledger),
        "compatibility_structure": compatibility,
        "repaired_residual_order": [
            "left flow: 96",
            "right flow: 96",
            "left initial compatibility C_N(h_-): 2",
            "entry chart compatibility C_N(Gamma_-(xi_-)): 2",
            "right initial compatibility C_N(h_0^+): 2",
            "projected entry P_N(h_--Gamma_-(xi_-)): 192",
            "projected seam P_N(h_0^--h_0^+): 192",
            "projected exit P_N(h_+-Gamma_+(xi_+)): 192",
            "phase: 1",
        ],
        "endpoint_logic": {
            "entry": (
                "projected equality plus compatibility of both the left "
                "initial history and the ambient entry chart"
            ),
            "seam": (
                "projected equality plus right-initial compatibility; left "
                "terminal compatibility comes from right-inclusive flow"
            ),
            "exit": (
                "projected equality; right-terminal compatibility comes "
                "from right-inclusive flow and Gamma_+ must be constructed "
                "inside the compatibility manifold"
            ),
            "entry_transversality_hypothesis": (
                "rank D(C_N o Gamma_-)=2, so the 193-coordinate ambient "
                "entry chart has a 191-dimensional compatible zero fiber"
            ),
        },
        "intrinsic_compatible_ledger": {
            "branch_coefficients_after_initial_compatibility": 288,
            "attracting_chart_coordinates": 191,
            "exit_chart_coordinates": 1,
            "phase_fixed_unknown_dimension": 768,
            "flow_rows": 192,
            "three_compatible_history_equalities": 576,
            "phase_rows": 1,
            "phase_fixed_residual_dimension": 769,
            "intended_fredholm_index_if_all_analytic_gates_hold": -1,
            "relation_to_ambient_ledger": (
                "endpoint-compatible C0 coordinate ledger only; a global "
                "C1/W2 realization still needs a different basis or "
                "derivative-jump rows and a fresh count"
            ),
        },
        "rectangular_operator_contract": {
            "operator": (
                "raw C0 ambient template L_N=D_z F_N in R^(775x774); "
                "nu,eta,d are excluded; the strong selected derivative "
                "requires a fresh realization and count"
            ),
            "column_rank_gate": "sigma_min(L_N)>0 with directed error bounds",
            "cokernel_gate": (
                "solve L_N^T psi=0; economy-SVD's last positive-singular-"
                "value vector is not the missing left-null vector"
            ),
            "jump_complement": (
                "choose e_N in the 192-row projected jump slot with "
                "psi^T e_N nonzero"
            ),
            "border": (
                "conditional raw-template border B_N=[L_N,-e_N] in "
                "R^(775x775)"
            ),
            "normalization": "L_N^T psi=0 and psi^T e_N=1",
            "transpose_identity": "B_N^T psi=(0_774,-1)",
            "gap_derivative": "d_lambda=psi^T F_lambda",
            "physical_response": (
                "rho=delta^2*nu_eta=-delta^2*m_eta/m_nu"
            ),
        },
        "continuous_adjoint_contract": {
            "interior": (
                "-p'(s)=A_0(s)^T p(s)+sum_{tau in {4,5,Theta}} "
                "1_{s+tau in I} A_tau(s+tau)^T p(s+tau)"
            ),
            "period_coefficient": (
                "A_Theta,11(s)=-2*delta^2*eta*X(s-Theta), hence it "
                "vanishes at eta=0"
            ),
            "full_covector": (
                "Psi=(p_-,p_+,lambda_-,lambda_+,gamma,mu), including "
                "entry, exit, phase, seam, and jump multipliers"
            ),
            "definition": (
                "the complete boundary/seam conditions are defined by "
                "L^*Psi=0 after the endpoint chart derivatives are fixed"
            ),
        },
        "parameter_columns": exact_parameter_columns(),
        "claim_ledger": asdict(reference_claim_ledger()),
        "minimal_next_certificate": [
            "choose a globally C1/W2 coefficient realization or add and recount internal derivative-jump residuals",
            "construct Gamma_- and prove rank D(C_N o Gamma_-)=2",
            "construct Gamma_+ inside C_N^{-1}(0)",
            "assemble the resulting strong index-minus-one L_N with right-inclusive endpoint flow rows and a fresh dimension count",
            "prove full column rank and a nonzero jump projection of the left null vector",
            "freeze e_N and validate [L_N,-e_N] including coefficient tails",
            "propagate the T_* interval through shifts, charts, and parameter columns",
            "validate the continuous advanced adjoint and all boundary multipliers",
        ],
        "scope": {
            "exact_discrete_compatibility_rank": True,
            "exact_repaired_c0_ambient_algebra_ledger": True,
            "global_c1_or_w2_collocation_ledger": False,
            "actual_selected_fredholm_operator": False,
            "continuous_fredholm_theorem": False,
            "selected_root": False,
            "rho_enclosure": False,
        },
    }


def validate_selected_fredholm_structure_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject arithmetic drift or promotion beyond structural conclusions."""

    if not verify_exact_compatibility_structure():
        raise RuntimeError("the exact compatibility-coordinate proof failed")
    if not exact_parameter_columns_are_valid():
        raise RuntimeError("the exact moving-delay column check failed")
    expected = reference_selected_fredholm_structure_payload()
    if dict(payload) != expected:
        raise ValueError(
            "selected Fredholm structure payload does not match the repaired "
            "ledger, exact compatibility proof, and claim refusals"
        )


__all__ = [
    "BLUEPRINT_NOTE_SHA256",
    "BLUEPRINT_RESULT_SHA256",
    "BLUEPRINT_SOURCE_SHA256",
    "CANDIDATE_NOTE_SHA256",
    "CANDIDATE_RESULT_SHA256",
    "CANDIDATE_SOURCE_SHA256",
    "CompatibilityStructure",
    "FredholmClaimLedger",
    "FredholmDimensionLedger",
    "compatibility_jacobian_from_remainder",
    "endpoint_bubble_right_inverse",
    "exact_parameter_columns",
    "exact_parameter_columns_are_valid",
    "reference_claim_ledger",
    "reference_compatibility_structure",
    "reference_dimension_ledger",
    "reference_selected_fredholm_structure_payload",
    "retained_projection_matrix",
    "stacked_compatibility_coordinates",
    "validate_selected_fredholm_structure_payload",
    "verify_exact_compatibility_structure",
]
