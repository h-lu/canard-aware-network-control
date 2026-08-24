"""Sliding-window and weak-space repair for the fixed-epsilon RFDE BVP.

Two independent obstructions in the previous fixed-epsilon blueprint admit
exact structural repairs.

First, a nonstationary one-dimensional invariant history chart is locally the
sliding-window trace of one history-extended classical trajectory segment.
A strictly monotone history phase turns an independently selected complete
orbit into such a chart, but the converse gives completeness only when the
scalar phase flow is complete.  The fixed-phase parameter jets then follow
from the inverse-function chain rule.  This removes a two-dimensional
``(phase, history)`` chart PDE from the minimum computation, but it does not
select the orbit.

Second, continuous piecewise polynomials are conforming in ``W^{1,p}`` even
when their first derivatives jump at cell joins.  The natural fixed-delay,
fixed-flight first-order BVP therefore uses orbit space ``W^{1,p}``, flow
residual space ``L^p``, and full-history trace space ``W^{1,p}``.  Endpoint
derivative compatibility is not a continuous row in this topology; selected
traces must inherit compatibility from independently constructed exact orbit
or stable-fibre endpoint embeddings.  The old
``W^{2,p} -> L^p`` principal scale cannot be Fredholm because all branch
columns are compact on bounded intervals.

The module proves exact algebraic identities and audits one binary64 phase
diagnostic from the existing two-sided candidate.  It does not construct the
independently selected orbit, prove the actual trace-pair hypotheses, or
validate a fixed-epsilon root or response.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any, Mapping

import sympy as sp


MODEL_ID = "synchronous-dual-scaffold-fhn-quadratic-period-lock"
AUDIT_ID = "fixed-epsilon-sliding-window-w1p-fredholm-bridge"
ASSUMPTIONS_ID = (
    "epsilon=1/5;delta=1/sqrt(5);fixed-delays-and-flight-times;"
    "1<p<infinity;continuous-piecewise-degree-six-trials;"
    "selected-endpoint-traces-derived-from-independent-exact-compatible-"
    "orbit-or-stable-fibre-embeddings"
)
TWO_SIDED_CANDIDATE_RESULT_SHA256 = (
    "a35c23f58cb80a83b5d14d303edccc160a66e402e9f042b18d0e992a2388dabd"
)
SELECTED_REPELLING_ENDPOINT_RESULT_SHA256 = (
    "1ab9678e2fdd28439c6552c05e80c1c751a88a493fb02319fbc76d9a73a337e4"
)
GROWING_TUBE_GRAPH_DOC_SHA256 = (
    "d9f16108a9e3680a38db9a9cdf7ea0092e879673195c69c95d4677b4cffb021a"
)
GREEN_PHASE_TRACES_DOC_SHA256 = (
    "543ae331d0ffc656bba3a667dab1301fed29f9796afe8a84c4390fcff4088dc8"
)
CANONICAL_LONG_DELAY_DOC_SHA256 = (
    "a3770c52520c52815593eb926251123c5aca9cfeda4b13c44dc6443f8408e262"
)
QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256 = (
    "f08632721279f6bfc00d0aa4d118a9a7c5bda2b489f5457003e9914c540b87e3"
)
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_sliding_window_w1p_bridge.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_sliding_window_w1p_bridge.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_sliding_window_w1p_bridge.json"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/fixed_epsilon_sliding_window_w1p_bridge.py"
)


@dataclass(frozen=True)
class SlidingWindowIdentityAudit:
    """Exact orbit/chart equivalence and fixed-phase jet identities."""

    rfde: str
    selected_orbit_requirement: str
    orbit_and_jet_regularity_hypothesis: str
    phase_function: str
    phase_linear_part: str
    monotonicity_hypothesis: str
    inverse_phase_map: str
    sliding_window_chart: str
    internal_field: str
    phase_gauge: str
    phase_tangent_gauge: str
    shift_invariance: str
    transport_equation_interpretation: str
    boundary_invariance: str
    chart_is_inside_solution_manifold: bool
    chart_rank_is_one: bool
    converse_characteristic_identity: str
    local_backward_time: str
    ambient_backward_rfde_ivp_used: bool
    fixed_time_orbit_jet_equation: str
    inverse_phase_parameter_jet: str
    fixed_phase_history_jet: str
    fixed_phase_internal_field_jet: str
    second_inverse_phase_jet: str
    fixed_phase_second_history_jet: str
    fixed_phase_second_internal_field_jet: str
    fixed_phase_gauge_defect: sp.Expr
    internal_field_chain_rule_defect: sp.Expr
    independent_selection_block: str
    circular_endpoint_definition: str
    independent_phase_endpoint_derivative: str
    independent_phase_endpoint_derivative_range: str
    circular_endpoint_residual: sp.Expr
    circular_endpoint_total_derivative: sp.Expr


@dataclass(frozen=True)
class PhysicalFoldPhaseAudit:
    """Exact phase-field and time-scaling identities for this plant."""

    delta: sp.Expr
    physical_state_chart: str
    fold_phase: str
    physical_phase: str
    fold_internal_field: sp.Expr
    physical_internal_field: sp.Expr
    physical_minus_scaled_fold_defect: sp.Expr
    clock_conversion: str
    history_rescaling: str
    history_rescaling_derivative: str
    fold_nu_jet: str
    fold_eta_jet: str
    physical_a_jet: str
    physical_eta_jet: str
    fold_history_nu_conversion: str
    fold_history_eta_conversion: str
    fold_internal_nu_conversion: str
    fold_internal_eta_conversion: str


@dataclass(frozen=True)
class WeakSpaceAudit:
    """Exact finite-element counts and the W1p compatibility obstruction."""

    sobolev_exponent: str
    natural_history_space: str
    natural_orbit_space: str
    natural_flow_codomain: str
    fixed_history_restriction: str
    method_of_steps_isomorphism: str
    polynomial_degree: int
    history_cells: int
    flight_cells_per_branch: int
    state_dimension: int
    scalar_history_coefficients: int
    history_coefficients: int
    scalar_branch_coefficients: int
    branch_coefficients: int
    history_internal_value_joins: int
    history_derivative_seams_needed_for_w1p: int
    history_derivative_seams_needed_for_global_c1_w2p: int
    global_c1_history_coefficients: int
    global_c1_endpoint_compatible_coefficients: int
    branch_derivative_seams_needed_for_global_c1_w2p: int
    global_c1_branch_coefficients: int
    distributional_derivative_statement: str
    endpoint_bump: sp.Expr
    endpoint_bump_value_at_left: sp.Expr
    endpoint_bump_derivative_at_left: sp.Expr
    endpoint_bump_value_at_current: sp.Expr
    endpoint_bump_derivative_at_current: sp.Expr
    endpoint_bump_l2_norm_squared: sp.Expr
    endpoint_bump_derivative_l2_norm_squared: sp.Expr
    endpoint_bump_w12_norm_squared: sp.Expr
    endpoint_bump_w12_norm_limit: sp.Expr
    compatible_strong_histories_dense_in_w1p_for_this_finite_delay_field: bool
    endpoint_derivative_trace_continuous_on_w1p: bool
    compatibility_is_closed_codimension_two_in_w1p: bool
    discrete_194_to_192_is_continuous_w1p_solution_manifold_count: bool
    exact_zero_regularizes_on_flight: str
    w2p_to_lp_branch_column: str
    w2p_to_w1p_history_trace: str
    old_w2p_to_lp_principal_operator_can_be_fredholm: bool
    strong_space_alternative: str
    moving_delay_or_flight_time_warning: str


@dataclass(frozen=True)
class NaturalDiscreteLedger:
    """Two equivalent W1p formal index-minus-one finite ledgers."""

    branch_coefficients_each: int
    two_branch_coefficients: int
    flow_rows_each: int
    full_history_rows_each: int
    full_history_blocks: int
    entry_chart_coordinates: int
    exit_chart_coordinates: int
    phase_rows: int
    explicit_chart_unknowns: int
    explicit_chart_residuals: int
    explicit_chart_residual_minus_unknown: int
    compatibility_rows: int
    projected_history_rows: int
    implicit_attracting_function: str
    implicit_entry_unknowns: int
    implicit_entry_residuals: int
    implicit_entry_residual_minus_unknown: int
    arithmetic_775_by_774_recovered: bool
    arithmetic_is_fredholm_proof: bool
    point_collocation_uniform_inf_sup_validated: bool


@dataclass(frozen=True)
class FredholmPairReduction:
    """Abstract trace-pair theorem after the IVP blocks are eliminated."""

    history_space: str
    attracting_trace_range: str
    repelling_trace_range: str
    difference_operator: str
    kernel_identity: str
    cokernel_identity: str
    trace_ranges_assumed_closed: bool
    trace_maps_split_topological_embeddings_assumed: bool
    assumed_intersection_dimension: int
    assumed_sum_codimension: int
    assumed_intersection_generator: str
    difference_operator_index: int
    phase_transversality: str
    phase_augmented_kernel_dimension: int
    phase_augmented_cokernel_dimension: int
    phase_augmented_index: int
    jump_complement_condition: str
    bordered_operator_index: int
    bordered_operator_isomorphism_under_hypotheses: bool
    actual_trace_pair_closedness_validated: bool
    actual_trace_maps_split_embeddings_validated: bool
    actual_selected_trace_pair_hypotheses_validated: bool
    coefficient_count_can_replace_trace_pair_proof: bool
    adjoint_space: str
    full_cokernel_covector: str
    interior_dynamic_adjoint: str
    classical_advanced_equation_requires_extra_multiplier_regularity: bool


@dataclass(frozen=True)
class CandidatePhaseDiagnostic:
    """Recomputed binary64 node diagnostic; never a selected-chart proof."""

    source_result_sha256: str
    section_half_width: float
    mesh_per_scaled_time: int
    active_scaled_history: float
    two_flight_length: float
    artificial_entry_tail_remaining_at_exit: float
    represented_history_steps: int
    right_flight_nodes: int
    nu_candidate: float
    a_candidate: float
    entry_template_q_candidate: float
    fold_phase: str
    fold_internal_field_node_minimum: float
    fold_internal_field_node_maximum: float
    physical_internal_field_node_minimum: float
    physical_internal_field_node_maximum: float
    exit_gap_crossing_derivative: float
    nodewise_phase_monotonicity_observed: bool
    interval_phase_monotonicity_validated: bool
    candidate_right_trace_independent_of_connection: bool
    entry_template_q_is_repelling_internal_field: bool
    candidate_exit_gap_crossing_nonzero_observed: bool
    selected_orbit_exit_gap_anchor_validated: bool
    exit_gap_selects_repelling_orbit: bool
    candidate_can_seed_independent_orbit_continuation: bool
    candidate_endpoint_and_adjoint_can_be_reused: bool


@dataclass(frozen=True)
class BridgeCertificate:
    """Strict proved/diagnostic/open claim ledger."""

    model_id: str
    audit_id: str
    assumptions_id: str
    sliding_window_chart_from_independent_orbit_proved: bool
    invariant_nonstationary_chart_is_locally_sliding_window_proved: bool
    fixed_phase_parameter_jet_formulas_proved: bool
    physical_fold_phase_scaling_proved: bool
    c0_piecewise_polynomials_are_w1p_conforming_proved: bool
    derivative_seams_required_for_w1p: bool
    compatibility_continuous_on_w1p: bool
    w2p_to_lp_old_principal_scale_rejected: bool
    natural_w1p_formal_775_by_774_ledger_derived: bool
    abstract_index_minus_one_trace_pair_reduction_proved: bool
    candidate_y_phase_node_diagnostic_computed: bool
    independent_selected_attracting_trace_constructed: bool
    attracting_stable_fibre_trace_range_constructed: bool
    independent_selected_repelling_orbit_constructed: bool
    frozen_target_graph_family_validated: bool
    prepared_planar_trace_family_validated: bool
    fixed_window_gap_row_validated: bool
    canonical_graph_continuation_completed: bool
    regularized_gap_validated: bool
    retained_physical_history_hull_validated: bool
    terminal_local_phase_validated: bool
    actual_trace_pair_fredholm_hypotheses_validated: bool
    continuous_advanced_adjoint_validated: bool
    fixed_epsilon_selected_root_validated: bool
    fixed_epsilon_response_validated: bool
    physical_onset_validated: bool
    shortest_next_problem: str


def reference_sliding_window_identity_audit() -> SlidingWindowIdentityAudit:
    """Return exact inverse-phase and circularity identities."""

    q, p_lambda, p_tt, p_tlambda = sp.symbols(
        "q p_lambda p_tt p_tlambda", nonzero=True
    )
    tau_lambda = -p_lambda / q
    fixed_phase_defect = sp.simplify(p_lambda + q * tau_lambda)
    q_lambda = p_tlambda + p_tt * tau_lambda
    expected_q_lambda = p_tlambda - p_lambda * p_tt / q

    endpoint, chart_endpoint = sp.symbols("endpoint chart_endpoint")
    circular_chart = endpoint
    circular_residual = sp.simplify(endpoint - circular_chart)
    d_endpoint, d_chart_endpoint = sp.symbols(
        "d_endpoint d_chart_endpoint"
    )
    circular_total_derivative = sp.simplify(
        d_endpoint - d_chart_endpoint
    ).subs(d_chart_endpoint, d_endpoint)

    return SlidingWindowIdentityAudit(
        rfde="dot z(t)=F(z_t;lambda), z_t(theta)=z(t+theta)",
        selected_orbit_requirement=(
            "z^r(t;lambda) is selected by a tail/outer residual and a "
            "transverse anchor containing no Lin connection variables"
        ),
        orbit_and_jet_regularity_hypothesis=(
            "z is W2p in time on every retained history window for a C1 "
            "W1p-valued chart (C2 is a stronger sufficient hypothesis, not "
            "an equivalent one); Gamma_{lambda mu} in W1p is ensured by z "
            "in W3p, u_lambda and u_mu in W2p, and u_{lambda mu} in W1p; "
            "for a general ell in (W1p)^*, the displayed q_{lambda mu} is "
            "ensured by z in W4p and matching mixed-jet regularity, whereas "
            "current-state evaluation admits weaker pointwise C3 conditions"
        ),
        phase_function=(
            "chi(phi)=ell(phi)+c is one fixed bounded affine history phase; "
            "p(t,lambda)=chi(z^r_t(lambda))"
        ),
        phase_linear_part="ell=D chi is fixed and bounded",
        monotonicity_hypothesis="abs(partial_t p)>=kappa>0",
        inverse_phase_map="t=tau(xi,lambda), p(tau(xi,lambda),lambda)=xi",
        sliding_window_chart=(
            "Gamma^r(xi;lambda)(theta)="
            "z^r(tau(xi,lambda)+theta;lambda)"
        ),
        internal_field="q^r(xi,lambda)=partial_t p(tau(xi,lambda),lambda)",
        phase_gauge="chi(Gamma^r)=xi",
        phase_tangent_gauge="ell(partial_xi Gamma^r)=1",
        shift_invariance="q^r Gamma^r_xi=partial_theta Gamma^r",
        transport_equation_interpretation=(
            "the transport identity holds in Lp, hence almost everywhere "
            "in theta; because q Gamma_xi is W1p it bootstraps each history "
            "to W2p, supplies the endpoint derivative trace, and the "
            "characteristic identity is interpreted through Sobolev ACL "
            "representatives"
        ),
        boundary_invariance="q^r Gamma^r_xi(0)=F(Gamma^r;lambda)",
        chart_is_inside_solution_manifold=True,
        chart_rank_is_one=True,
        converse_characteristic_identity=(
            "for an immersed W1p-valued chart satisfying the affine phase "
            "gauge and both invariance equations, "
            "Gamma(xi(t))(theta)=Gamma(xi(t+theta))(0) whenever the "
            "scalar characteristic remains in the chart domain for every "
            "theta in [-h,0]; the converse produces a local trajectory "
            "segment unless scalar-flow completeness is separately assumed"
        ),
        local_backward_time=(
            "for q>0, b_-(xi_0)=integral_{xi_-}^{xi_0} dxi/q(xi) is the "
            "certified time before leaving the validated phase-chart patch"
        ),
        ambient_backward_rfde_ivp_used=False,
        fixed_time_orbit_jet_equation=(
            "dot u_lambda=D_phi F(z_t;lambda)(u_lambda)_t+F_lambda"
        ),
        inverse_phase_parameter_jet="tau_lambda=-p_lambda/q",
        fixed_phase_history_jet=(
            "Gamma_lambda=(u_lambda)_tau-p_lambda Gamma_xi, with "
            "p_lambda=ell((u_lambda)_tau)"
        ),
        fixed_phase_internal_field_jet=(
            "q_lambda=p_{t lambda}-(p_lambda/q)p_{tt}"
        ),
        second_inverse_phase_jet=(
            "tau_{lambda mu}=-(p_{lambda mu}+p_{t lambda}tau_mu+"
            "p_{t mu}tau_lambda+p_{tt}tau_lambda tau_mu)/q"
        ),
        fixed_phase_second_history_jet=(
            "Gamma_{lambda mu}=u_{lambda mu,tau}+dot u_{lambda,tau}tau_mu+"
            "dot u_{mu,tau}tau_lambda+ddot z_tau tau_lambda tau_mu+"
            "dot z_tau tau_{lambda mu}"
        ),
        fixed_phase_second_internal_field_jet=(
            "q_{lambda mu}=p_{t lambda mu}+p_{tt lambda}tau_mu+"
            "p_{tt mu}tau_lambda+p_{ttt}tau_lambda tau_mu+"
            "p_{tt}tau_{lambda mu}; all p derivatives are first taken at "
            "fixed orbit time and then evaluated at t=tau(xi,lambda)"
        ),
        fixed_phase_gauge_defect=fixed_phase_defect,
        internal_field_chain_rule_defect=sp.simplify(
            q_lambda - expected_q_lambda
        ),
        independent_selection_block=(
            "the orbit-selection equations may be solved separately or in "
            "one block-triangular coupled system at fixed shared parameters, "
            "but cannot contain x^- or x^+; their anchored derivative must "
            "be an isomorphism so the Lin block does not select a residual "
            "orbit kernel, and shared-parameter columns must be retained"
        ),
        circular_endpoint_definition=(
            "if Gamma_x is the valid sliding chart of the same unknown right "
            "branch and xi_L=p_x(L), then Gamma_x(xi_L)=End_L(x) by definition"
        ),
        independent_phase_endpoint_derivative=(
            "for E=End_L(x), R(x,xi)=E-Gamma_x(xi), and evaluation at "
            "xi=chi(E), d tau=(d xi-ell(dE))/q and "
            "dR=Gamma_xi*(ell(dE)-d xi)"
        ),
        independent_phase_endpoint_derivative_range=(
            "with xi independent, range(DR) is contained in "
            "span{Gamma_xi}; after composing xi=chi(E), DR=0"
        ),
        circular_endpoint_residual=circular_residual,
        circular_endpoint_total_derivative=circular_total_derivative,
    )


def reference_physical_fold_phase_audit() -> PhysicalFoldPhaseAudit:
    """Return exact Y-phase and physical/fold clock conversions."""

    delta = sp.sqrt(5) / 5
    x, nu = sp.symbols("X nu", real=True)
    voltage = 1 + delta * x
    parameter_a = 1 + delta**2 * nu
    q_fold = -x + delta * nu
    q_phys = parameter_a - voltage
    return PhysicalFoldPhaseAudit(
        delta=delta,
        physical_state_chart=(
            "V=1+delta X, W=2/3-delta^2 Y, a=1+delta^2 nu, s=delta t"
        ),
        fold_phase="xi=Y(0)",
        physical_phase="xi=(2/3-W(0))/delta^2",
        fold_internal_field=q_fold,
        physical_internal_field=q_phys,
        physical_minus_scaled_fold_defect=sp.simplify(
            q_phys - delta * q_fold
        ),
        clock_conversion="q_fold=q_phys/delta",
        history_rescaling=(
            "(S_delta phi)(sigma)=((phi_V(sigma/delta)-1)/delta,"
            "(2/3-phi_W(sigma/delta))/delta^2)"
        ),
        history_rescaling_derivative=(
            "(D S_delta u)(sigma)=(u_V(sigma/delta)/delta,"
            "-u_W(sigma/delta)/delta^2)"
        ),
        fold_nu_jet="q^f_nu=delta-(Gamma^f_nu)_X(0)",
        fold_eta_jet="q^f_eta=-(Gamma^f_eta)_X(0)",
        physical_a_jet="q^p_a=1-(Gamma^p_a)_V(0)",
        physical_eta_jet="q^p_eta=-(Gamma^p_eta)_V(0)",
        fold_history_nu_conversion=(
            "Gamma^f_nu=delta^2 D S_delta Gamma^p_a"
        ),
        fold_history_eta_conversion=(
            "Gamma^f_eta=D S_delta Gamma^p_eta"
        ),
        fold_internal_nu_conversion="q^f_nu=delta q^p_a",
        fold_internal_eta_conversion="q^f_eta=q^p_eta/delta",
    )


def reference_weak_space_audit() -> WeakSpaceAudit:
    """Return exact W1p-conformity counts and a vanishing-norm bump."""

    pdeg = 6
    history_cells = 16
    flight_cells = 8
    states = 2
    scalar_history = history_cells * pdeg + 1
    history_dimension = states * scalar_history
    scalar_branch = (history_cells + flight_cells) * pdeg + 1
    branch_dimension = states * scalar_branch

    ell, theta = sp.symbols("ell theta", positive=True, real=True)
    u = (theta + ell) / ell
    bump = sp.expand(theta * (theta + ell) ** 2 / ell**2)
    bump_derivative = sp.diff(bump, theta)
    value_norm_squared = sp.simplify(ell**3 / 105)
    derivative_norm_squared = sp.simplify(2 * ell / 15)
    w12_norm_squared = sp.simplify(
        value_norm_squared + derivative_norm_squared
    )

    return WeakSpaceAudit(
        sobolev_exponent="1<p<infinity",
        natural_history_space="H=W^{1,p}([-h,0],R^2)",
        natural_orbit_space=(
            "W^{1,p}([-L_--h,0],R^2) x "
            "W^{1,p}([-h,L_+],R^2)"
        ),
        natural_flow_codomain=(
            "L^p([-L_-,0],R^2) x L^p([0,L_+],R^2)"
        ),
        fixed_history_restriction=(
            "End_t:W^{1,p}(I^h)->W^{1,p}([-h,0]) is bounded for fixed t"
        ),
        method_of_steps_isomorphism=(
            "for finitely many fixed retarded delays and L-infinity "
            "coefficient matrices A_j, u -> "
            "(u'-sum_j A_j u(.-tau_j),u|initial history) is a bounded "
            "W1p-to-(Lp x W1p) isomorphism on each fixed interval"
        ),
        polynomial_degree=pdeg,
        history_cells=history_cells,
        flight_cells_per_branch=flight_cells,
        state_dimension=states,
        scalar_history_coefficients=scalar_history,
        history_coefficients=history_dimension,
        scalar_branch_coefficients=scalar_branch,
        branch_coefficients=branch_dimension,
        history_internal_value_joins=history_cells - 1,
        history_derivative_seams_needed_for_w1p=0,
        history_derivative_seams_needed_for_global_c1_w2p=(
            states * (history_cells - 1)
        ),
        global_c1_history_coefficients=(
            history_dimension - states * (history_cells - 1)
        ),
        global_c1_endpoint_compatible_coefficients=(
            history_dimension - states * (history_cells - 1) - states
        ),
        branch_derivative_seams_needed_for_global_c1_w2p=(
            states * (history_cells + flight_cells - 1)
        ),
        global_c1_branch_coefficients=(
            branch_dimension - states * (history_cells + flight_cells - 1)
        ),
        distributional_derivative_statement=(
            "the distributional derivative equals the piecewise derivative "
            "plus value-jump Dirac masses; C0 continuity removes every Dirac "
            "mass, while derivative jumps remain admissible in W1p"
        ),
        endpoint_bump=bump,
        endpoint_bump_value_at_left=sp.simplify(bump.subs(theta, -ell)),
        endpoint_bump_derivative_at_left=sp.simplify(
            bump_derivative.subs(theta, -ell)
        ),
        endpoint_bump_value_at_current=sp.simplify(bump.subs(theta, 0)),
        endpoint_bump_derivative_at_current=sp.simplify(
            bump_derivative.subs(theta, 0)
        ),
        endpoint_bump_l2_norm_squared=value_norm_squared,
        endpoint_bump_derivative_l2_norm_squared=derivative_norm_squared,
        endpoint_bump_w12_norm_squared=w12_norm_squared,
        endpoint_bump_w12_norm_limit=sp.limit(
            sp.sqrt(w12_norm_squared), ell, 0, dir="+"
        ),
        compatible_strong_histories_dense_in_w1p_for_this_finite_delay_field=True,
        endpoint_derivative_trace_continuous_on_w1p=False,
        compatibility_is_closed_codimension_two_in_w1p=False,
        discrete_194_to_192_is_continuous_w1p_solution_manifold_count=False,
        exact_zero_regularizes_on_flight=(
            "an exact W1p zero has u'=F(u_t) with continuous right-hand side; "
            "hence it is C1 (and, for this smooth fixed-delay field, gains "
            "the corresponding interior regularity) a posteriori"
        ),
        w2p_to_lp_branch_column=(
            "W^{2,p} --d/dt--> W^{1,p} compactly embeds into L^p"
        ),
        w2p_to_w1p_history_trace=(
            "fixed restriction W^{2,p}(I^h)->W^{1,p}([-h,0]) is compact"
        ),
        old_w2p_to_lp_principal_operator_can_be_fredholm=False,
        strong_space_alternative=(
            "if W2p is retained, use a W1p flow codomain and rebuild all "
            "strong traces, compatibility conditions, and counts"
        ),
        moving_delay_or_flight_time_warning=(
            "derivatives with respect to moving delays or endpoint times "
            "require a stronger space or a Banach-scale formulation"
        ),
    )


def reference_natural_discrete_ledger() -> NaturalDiscreteLedger:
    """Return both exact formal index-minus-one W1p ledgers."""

    branch = 290
    flow = 96
    history = 194
    entry_coordinates = 193
    exit_coordinates = 1
    explicit_unknowns = 2 * branch + entry_coordinates + exit_coordinates
    explicit_residuals = 2 * flow + 3 * history + 1

    implicit_unknowns = 2 * branch + exit_coordinates
    implicit_residuals = 2 * flow + 2 * history + 1 + 1
    return NaturalDiscreteLedger(
        branch_coefficients_each=branch,
        two_branch_coefficients=2 * branch,
        flow_rows_each=flow,
        full_history_rows_each=history,
        full_history_blocks=3,
        entry_chart_coordinates=entry_coordinates,
        exit_chart_coordinates=exit_coordinates,
        phase_rows=1,
        explicit_chart_unknowns=explicit_unknowns,
        explicit_chart_residuals=explicit_residuals,
        explicit_chart_residual_minus_unknown=(
            explicit_residuals - explicit_unknowns
        ),
        compatibility_rows=0,
        projected_history_rows=0,
        implicit_attracting_function=(
            "replace the 193-coordinate entry chart and 194-row entry match "
            "by one regular scalar B_-(history)=0"
        ),
        implicit_entry_unknowns=implicit_unknowns,
        implicit_entry_residuals=implicit_residuals,
        implicit_entry_residual_minus_unknown=(
            implicit_residuals - implicit_unknowns
        ),
        arithmetic_775_by_774_recovered=(
            explicit_unknowns == 774 and explicit_residuals == 775
        ),
        arithmetic_is_fredholm_proof=False,
        point_collocation_uniform_inf_sup_validated=False,
    )


def reference_fredholm_pair_reduction() -> FredholmPairReduction:
    """Return the exact closed-subspace index reduction."""

    return FredholmPairReduction(
        history_space="H=W^{1,p}([-h,0],R^2)",
        attracting_trace_range="E_a subset H, closed",
        repelling_trace_range="E_r subset H, closed",
        difference_operator="D:E_a x E_r -> H, D(v,w)=v-w",
        kernel_identity="ker D is isomorphic to E_a intersect E_r",
        cokernel_identity="coker D is isomorphic to H/(E_a+E_r)",
        trace_ranges_assumed_closed=True,
        trace_maps_split_topological_embeddings_assumed=True,
        assumed_intersection_dimension=1,
        assumed_sum_codimension=1,
        assumed_intersection_generator="the common translation tangent",
        difference_operator_index=0,
        phase_transversality=(
            "one phase row is nonzero on the common translation tangent"
        ),
        phase_augmented_kernel_dimension=0,
        phase_augmented_cokernel_dimension=1,
        phase_augmented_index=-1,
        jump_complement_condition=(
            "the jump-slot column e has nonzero pairing with the cokernel"
        ),
        bordered_operator_index=0,
        bordered_operator_isomorphism_under_hypotheses=True,
        actual_trace_pair_closedness_validated=False,
        actual_trace_maps_split_embeddings_validated=False,
        actual_selected_trace_pair_hypotheses_validated=False,
        coefficient_count_can_replace_trace_pair_proof=False,
        adjoint_space=(
            "p_+/- in L^q and history multipliers in the full dual "
            "H^*=(W^{1,p})^*, which includes endpoint evaluations and must "
            "not be identified with the zero-boundary W^{-1,q} convention"
        ),
        full_cokernel_covector=(
            "Psi=(p_-,p_+,lambda_entry,lambda_exit,mu_seam,gamma_phase)"
        ),
        interior_dynamic_adjoint=(
            "-p'=A_0^T p+sum_j 1_{t+tau_j in I} A_j(t+tau_j)^T "
            "p(t+tau_j), only after all history loads are included"
        ),
        classical_advanced_equation_requires_extra_multiplier_regularity=True,
    )


def _candidate_audit(candidate_payload: Mapping[str, Any]) -> Mapping[str, Any]:
    value = candidate_payload.get("audit", candidate_payload)
    if not isinstance(value, Mapping):
        raise ValueError("candidate payload must contain an audit mapping")
    return value


def reference_candidate_phase_diagnostic(
    candidate_payload: Mapping[str, Any],
) -> CandidatePhaseDiagnostic:
    """Recompute the Y-phase node range from the pinned candidate vector."""

    audit = _candidate_audit(candidate_payload)
    finest = audit.get("finest_primal_and_adjoint_candidate")
    rows = audit.get("rows")
    if not isinstance(finest, Mapping) or not isinstance(rows, list):
        raise ValueError("candidate payload is missing the finest vector")

    section = float(finest["section_half_width"])
    mesh = int(finest["mesh_per_scaled_time"])
    vector = [float(value) for value in finest["primal_components"]]
    row = next(
        item
        for item in rows
        if int(item["mesh_per_scaled_time"]) == mesh
        and abs(float(item["section_half_width"]) - section) < 1.0e-14
    )
    horizon = float(row["active_scaled_history"])
    history_steps = int(math.ceil(horizon * mesh))
    flight_steps = int(round(section * mesh))
    nodes = history_steps + flight_steps + 1
    expected_dimension = 4 * nodes + 2
    if len(vector) != expected_dimension:
        raise ValueError("candidate vector dimension disagrees with its mesh")

    right_offset = 2 * nodes
    right_x = [
        vector[right_offset + 2 * node] for node in range(nodes)
    ]
    right_y = [
        vector[right_offset + 2 * node + 1] for node in range(nodes)
    ]
    nu = float(vector[-1])
    entry_q = float(vector[-2])
    delta = 1.0 / math.sqrt(5.0)
    q_fold = [
        -right_x[node] + delta * nu
        for node in range(history_steps, nodes)
    ]
    q_phys = [delta * value for value in q_fold]

    endpoint = nodes - 1
    x = right_x[endpoint]
    y = right_y[endpoint]
    x4 = right_x[endpoint - 4 * mesh]
    x5 = right_x[endpoint - 5 * mesh]
    offset = horizon * mesh
    integer = int(math.floor(offset))
    fraction = offset - integer
    upper = endpoint - integer
    if fraction <= 2.0e-13:
        x_period = right_x[upper]
    else:
        lower = upper - 1
        x_period = (
            fraction * right_x[lower]
            + (1.0 - fraction) * right_x[upper]
        )
    xdot = (
        y
        - x * x
        + delta * (-x**3 / 3.0 + 0.2 * ((x4 + x5) / 2.0 - x))
        + delta**3 * 0.25 * ((x4**3 + x5**3) / 2.0 - x**3)
    )
    # eta=0 in the pinned candidate; x_period is nevertheless reconstructed
    # above to audit the full represented history geometry.
    _ = x_period
    ydot = -x + delta * nu
    gap_crossing = x * xdot - 0.5 * ydot

    return CandidatePhaseDiagnostic(
        source_result_sha256=TWO_SIDED_CANDIDATE_RESULT_SHA256,
        section_half_width=section,
        mesh_per_scaled_time=mesh,
        active_scaled_history=horizon,
        two_flight_length=2.0 * section,
        artificial_entry_tail_remaining_at_exit=horizon - 2.0 * section,
        represented_history_steps=history_steps,
        right_flight_nodes=flight_steps + 1,
        nu_candidate=nu,
        a_candidate=1.0 + nu / 5.0,
        entry_template_q_candidate=entry_q,
        fold_phase="xi=Y(0)",
        fold_internal_field_node_minimum=min(q_fold),
        fold_internal_field_node_maximum=max(q_fold),
        physical_internal_field_node_minimum=min(q_phys),
        physical_internal_field_node_maximum=max(q_phys),
        exit_gap_crossing_derivative=gap_crossing,
        nodewise_phase_monotonicity_observed=min(q_fold) > 0.0,
        interval_phase_monotonicity_validated=False,
        candidate_right_trace_independent_of_connection=False,
        entry_template_q_is_repelling_internal_field=False,
        candidate_exit_gap_crossing_nonzero_observed=(
            abs(gap_crossing) > 1.0
        ),
        selected_orbit_exit_gap_anchor_validated=False,
        exit_gap_selects_repelling_orbit=False,
        candidate_can_seed_independent_orbit_continuation=True,
        candidate_endpoint_and_adjoint_can_be_reused=False,
    )


def reference_bridge_certificate() -> BridgeCertificate:
    """Return the strict promotion boundary after both structural repairs."""

    return BridgeCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        assumptions_id=ASSUMPTIONS_ID,
        sliding_window_chart_from_independent_orbit_proved=True,
        invariant_nonstationary_chart_is_locally_sliding_window_proved=True,
        fixed_phase_parameter_jet_formulas_proved=True,
        physical_fold_phase_scaling_proved=True,
        c0_piecewise_polynomials_are_w1p_conforming_proved=True,
        derivative_seams_required_for_w1p=False,
        compatibility_continuous_on_w1p=False,
        w2p_to_lp_old_principal_scale_rejected=True,
        natural_w1p_formal_775_by_774_ledger_derived=True,
        abstract_index_minus_one_trace_pair_reduction_proved=True,
        candidate_y_phase_node_diagnostic_computed=True,
        independent_selected_attracting_trace_constructed=False,
        attracting_stable_fibre_trace_range_constructed=False,
        independent_selected_repelling_orbit_constructed=False,
        frozen_target_graph_family_validated=False,
        prepared_planar_trace_family_validated=False,
        fixed_window_gap_row_validated=False,
        canonical_graph_continuation_completed=False,
        regularized_gap_validated=False,
        retained_physical_history_hull_validated=False,
        terminal_local_phase_validated=False,
        actual_trace_pair_fredholm_hypotheses_validated=False,
        continuous_advanced_adjoint_validated=False,
        fixed_epsilon_selected_root_validated=False,
        fixed_epsilon_response_validated=False,
        physical_onset_validated=False,
        shortest_next_problem=(
            "freeze the retained window S and wider graph cutoff S_hat=S+B; "
            "separately construct the graph fixed point and the canonically "
            "prepared planar trace field; derive "
            "the finite-window row A_{S,P} nu+B_{S,P} from the linearized "
            "prepared one-sided BVP (or validate a same-preparation positive-"
            "rho root), enclose A_{S,P} away from zero, and only then "
            "continue to delta=1/sqrt(5), validate terminal-local phase "
            "patches and complete-history jets, construct the attracting "
            "stable-fibre endpoint trace range, and assemble the W1p/Lp "
            "index-minus-one Lin operator"
        ),
    )


def reference_sliding_window_w1p_bridge_payload(
    candidate_payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Return the complete machine-readable proof and refusal ledger."""

    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "audit_id": AUDIT_ID,
        "assumptions_id": ASSUMPTIONS_ID,
        "sliding_window_identity": asdict(
            reference_sliding_window_identity_audit()
        ),
        "physical_fold_phase": asdict(reference_physical_fold_phase_audit()),
        "weak_space": asdict(reference_weak_space_audit()),
        "natural_discrete_ledger": asdict(reference_natural_discrete_ledger()),
        "fredholm_pair_reduction": asdict(reference_fredholm_pair_reduction()),
        "candidate_phase_diagnostic": asdict(
            reference_candidate_phase_diagnostic(candidate_payload)
        ),
        "certificate": asdict(reference_bridge_certificate()),
    }


def validate_sliding_window_w1p_bridge_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject any payload that promotes a diagnostic or loses an identity."""

    if payload.get("schema_version") != 1:
        raise ValueError("schema version drifted")
    if payload.get("model_id") != MODEL_ID:
        raise ValueError("model identifier drifted")
    if payload.get("audit_id") != AUDIT_ID:
        raise ValueError("audit identifier drifted")
    if payload.get("assumptions_id") != ASSUMPTIONS_ID:
        raise ValueError("assumptions identifier drifted")

    sliding = payload.get("sliding_window_identity", {})
    weak = payload.get("weak_space", {})
    ledger = payload.get("natural_discrete_ledger", {})
    fredholm = payload.get("fredholm_pair_reduction", {})
    diagnostic = payload.get("candidate_phase_diagnostic", {})
    certificate = payload.get("certificate", {})

    if certificate.get("model_id") != MODEL_ID:
        raise ValueError("certificate model identifier drifted")
    if certificate.get("audit_id") != AUDIT_ID:
        raise ValueError("certificate audit identifier drifted")
    if certificate.get("assumptions_id") != ASSUMPTIONS_ID:
        raise ValueError("certificate assumptions identifier drifted")

    exact_zeroes = (
        sliding.get("fixed_phase_gauge_defect") == 0,
        sliding.get("internal_field_chain_rule_defect") == 0,
        sliding.get("circular_endpoint_residual") == 0,
        sliding.get("circular_endpoint_total_derivative") == 0,
        weak.get("endpoint_bump_w12_norm_limit") == 0,
    )
    if not all(exact_zeroes):
        raise ValueError("an exact sliding-window or Sobolev identity failed")

    required_true = (
        sliding.get("chart_is_inside_solution_manifold"),
        sliding.get("chart_rank_is_one"),
        weak.get("compatible_strong_histories_dense_in_w1p_for_this_finite_delay_field"),
        ledger.get("arithmetic_775_by_774_recovered"),
        fredholm.get("trace_ranges_assumed_closed"),
        fredholm.get("trace_maps_split_topological_embeddings_assumed"),
        fredholm.get("bordered_operator_isomorphism_under_hypotheses"),
        diagnostic.get("nodewise_phase_monotonicity_observed"),
        diagnostic.get("candidate_exit_gap_crossing_nonzero_observed"),
        diagnostic.get("candidate_can_seed_independent_orbit_continuation"),
        certificate.get("abstract_index_minus_one_trace_pair_reduction_proved"),
    )
    if not all(value is True for value in required_true):
        raise ValueError("a proved identity or intended diagnostic is absent")

    required_false = (
        sliding.get("ambient_backward_rfde_ivp_used"),
        weak.get("endpoint_derivative_trace_continuous_on_w1p"),
        weak.get("compatibility_is_closed_codimension_two_in_w1p"),
        weak.get("old_w2p_to_lp_principal_operator_can_be_fredholm"),
        ledger.get("arithmetic_is_fredholm_proof"),
        diagnostic.get("interval_phase_monotonicity_validated"),
        diagnostic.get("candidate_right_trace_independent_of_connection"),
        diagnostic.get("entry_template_q_is_repelling_internal_field"),
        diagnostic.get("selected_orbit_exit_gap_anchor_validated"),
        diagnostic.get("exit_gap_selects_repelling_orbit"),
        diagnostic.get("candidate_endpoint_and_adjoint_can_be_reused"),
        fredholm.get("actual_trace_pair_closedness_validated"),
        fredholm.get("actual_trace_maps_split_embeddings_validated"),
        fredholm.get("actual_selected_trace_pair_hypotheses_validated"),
        certificate.get("independent_selected_attracting_trace_constructed"),
        certificate.get("attracting_stable_fibre_trace_range_constructed"),
        certificate.get("independent_selected_repelling_orbit_constructed"),
        certificate.get("frozen_target_graph_family_validated"),
        certificate.get("prepared_planar_trace_family_validated"),
        certificate.get("fixed_window_gap_row_validated"),
        certificate.get("canonical_graph_continuation_completed"),
        certificate.get("regularized_gap_validated"),
        certificate.get("retained_physical_history_hull_validated"),
        certificate.get("terminal_local_phase_validated"),
        certificate.get("actual_trace_pair_fredholm_hypotheses_validated"),
        certificate.get("continuous_advanced_adjoint_validated"),
        certificate.get("fixed_epsilon_selected_root_validated"),
        certificate.get("fixed_epsilon_response_validated"),
        certificate.get("physical_onset_validated"),
    )
    if not all(value is False for value in required_false):
        raise ValueError("an open claim was accidentally promoted")

    if ledger.get("explicit_chart_unknowns") != 774:
        raise ValueError("the W1p explicit-chart unknown count drifted")
    if ledger.get("explicit_chart_residuals") != 775:
        raise ValueError("the W1p explicit-chart residual count drifted")
    if ledger.get("implicit_entry_residual_minus_unknown") != 1:
        raise ValueError("the implicit-entry index count drifted")
    if fredholm.get("phase_augmented_index") != -1:
        raise ValueError("the phase-augmented Fredholm index drifted")
    if fredholm.get("actual_selected_trace_pair_hypotheses_validated") != (
        certificate.get("actual_trace_pair_fredholm_hypotheses_validated")
    ):
        raise ValueError("the trace-pair claim ledger is inconsistent")

    q_min = float(diagnostic.get("fold_internal_field_node_minimum", -1.0))
    q_max = float(diagnostic.get("fold_internal_field_node_maximum", -1.0))
    crossing = float(diagnostic.get("exit_gap_crossing_derivative", 0.0))
    if abs(q_min - 0.09505982129277968) > 5.0e-14:
        raise ValueError("the pinned nodewise phase minimum drifted")
    if abs(q_max - 1.7244298573163501) > 5.0e-14:
        raise ValueError("the pinned nodewise phase maximum drifted")
    if abs(crossing + 1.5031215576539718) > 5.0e-13:
        raise ValueError("the pinned exit crossing diagnostic drifted")


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [
            [_json_value(value[i, j]) for j in range(value.cols)]
            for i in range(value.rows)
        ]
    if isinstance(value, sp.Basic) and value == 0:
        return 0
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


def json_ready_sliding_window_w1p_bridge_payload(
    candidate_payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic JSON representation of the audit."""

    payload = reference_sliding_window_w1p_bridge_payload(candidate_payload)
    validate_sliding_window_w1p_bridge_payload(payload)
    return _json_value(payload)


__all__ = [
    "ASSUMPTIONS_ID",
    "AUDIT_ID",
    "BridgeCertificate",
    "CandidatePhaseDiagnostic",
    "CANONICAL_LONG_DELAY_DOC_SHA256",
    "DEFAULT_COMMAND",
    "FredholmPairReduction",
    "GENERATOR_RELATIVE_PATH",
    "GREEN_PHASE_TRACES_DOC_SHA256",
    "GROWING_TUBE_GRAPH_DOC_SHA256",
    "MODEL_ID",
    "NaturalDiscreteLedger",
    "PROOF_SOURCE_RELATIVE_PATH",
    "PhysicalFoldPhaseAudit",
    "RESULT_RELATIVE_PATH",
    "QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256",
    "SELECTED_REPELLING_ENDPOINT_RESULT_SHA256",
    "SlidingWindowIdentityAudit",
    "TWO_SIDED_CANDIDATE_RESULT_SHA256",
    "WeakSpaceAudit",
    "json_ready_sliding_window_w1p_bridge_payload",
    "reference_bridge_certificate",
    "reference_candidate_phase_diagnostic",
    "reference_fredholm_pair_reduction",
    "reference_natural_discrete_ledger",
    "reference_physical_fold_phase_audit",
    "reference_sliding_window_identity_audit",
    "reference_sliding_window_w1p_bridge_payload",
    "reference_weak_space_audit",
    "validate_sliding_window_w1p_bridge_payload",
]
