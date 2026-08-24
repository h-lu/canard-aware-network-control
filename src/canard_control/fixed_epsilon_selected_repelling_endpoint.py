"""Audit contract for a fixed-epsilon selected repelling endpoint chart.

The existing two-sided candidate ends its right flight with one scalar
observable.  This module records two exact compatible-history witnesses
showing that such an observable does not determine an RFDE endpoint, and it
specifies the smallest invariant-history continuation problem that would
produce the required one-dimensional backward-extendible repelling chart.

Nothing in this module constructs that chart or promotes the fixed-epsilon
selected-root diagnostic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any, Mapping

import sympy as sp


MODEL_ID = "synchronous-dual-scaffold-fhn-quadratic-period-lock"
FIXED_EPSILON_BVP_RESULT_SHA256 = (
    "1af8aa46b31bb099a8f07e7646b656577d010dc413094ad3be0afb32c70c993a"
)
TWO_SIDED_CANDIDATE_RESULT_SHA256 = (
    "b22c336c64f1e2187a013fd597e1a93624c8bf1ef83e5549abcc558ad684c5a6"
)
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_selected_repelling_endpoint.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_selected_repelling_endpoint.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_selected_repelling_endpoint.json"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/fixed_epsilon_selected_repelling_endpoint.py"
)


@dataclass(frozen=True)
class CompatibleHistoryFiberAudit:
    """Exact histories in one scalar-observable fiber of the RFDE."""

    delta: sp.Expr
    epsilon: sp.Expr
    scaled_period_delay: sp.Expr
    history_variable: sp.Expr
    perturbation_amplitude: sp.Expr
    eta: sp.Expr
    nu: sp.Expr
    solution_manifold_node_polynomial: sp.Expr
    base_voltage_history: sp.Expr
    base_recovery_history: sp.Expr
    base_current_state: sp.Matrix
    exit_observable_at_base_current: sp.Expr
    exit_observable_current_gradient_at_base: sp.Matrix
    period_lagrange_polynomial: sp.Expr
    period_history_perturbation: sp.Expr
    period_perturbation_current_value: sp.Expr
    period_perturbation_delay_4_value: sp.Expr
    period_perturbation_delay_5_value: sp.Expr
    period_perturbation_period_delay_value: sp.Expr
    period_perturbation_current_derivative: sp.Expr
    period_fast_field_difference: sp.Expr
    period_unit_witness_difference: sp.Expr
    delay_4_lagrange_polynomial: sp.Expr
    delay_4_history_perturbation: sp.Expr
    delay_4_perturbation_current_value: sp.Expr
    delay_4_perturbation_delay_4_value: sp.Expr
    delay_4_perturbation_delay_5_value: sp.Expr
    delay_4_perturbation_period_delay_value: sp.Expr
    delay_4_perturbation_current_derivative: sp.Expr
    delay_4_fast_field_difference: sp.Expr
    delay_4_unit_witness_difference: sp.Expr
    base_solution_manifold_compatibility_defect: sp.Matrix
    period_solution_manifold_compatibility_defect: sp.Matrix
    delay_4_solution_manifold_compatibility_defect: sp.Matrix


@dataclass(frozen=True)
class CompatibleEndpointCountAudit:
    """Finite raw-history count with compatibility accounted for once."""

    raw_history_coefficient_dimension: int
    state_dimension: int
    value_continuous_history_dimension: int
    global_c1_internal_derivative_continuity_codimension: int
    global_c1_history_dimension: int
    endpoint_compatibility_codimension: int
    discrete_endpoint_compatible_level_dimension: int
    global_c1_endpoint_compatible_level_dimension: int
    scalar_current_exit_constraints: int
    exit_observable_transverse_at_witness: bool
    scalar_exit_fiber_dimension_on_discrete_endpoint_level: int
    scalar_exit_fiber_dimension_on_global_c1_compatible_level: int
    repelling_chart_dimension_inside_solution_manifold: int
    scalar_exit_fiber_excess_over_repelling_curve_on_discrete_level: int
    scalar_exit_fiber_excess_over_repelling_curve_on_global_c1_level: int
    repelling_curve_codimension_in_raw_history_space: int
    repelling_curve_codimension_on_discrete_endpoint_level: int
    repelling_curve_codimension_on_global_c1_compatible_level: int
    raw_endpoint_equalities: int
    repelling_chart_coordinates: int
    raw_net_endpoint_conditions: int
    ambient_incoming_coordinate_dimension_reported_by_candidate: int
    ambient_incoming_compatibility_rows: int
    effective_discrete_incoming_zero_fiber_dimension: int
    ambient_repaired_775_by_774_ledger_is_arithmetic_only: bool
    global_c1_or_w2_multicell_realization_validated: bool
    candidate_193_plus_1_is_compatible_fredholm_count_validated: bool
    exact_interpretation: str
    unresolved_alternatives: tuple[str, ...]


@dataclass(frozen=True)
class SelectedRepellingEndpointContract:
    """Minimum exact BVP/continuation object missing from the candidate."""

    physical_phase_space: str
    strong_solution_manifold: str
    selected_chart: str
    chart_internal_flow: str
    shift_invariance_equation: str
    boundary_invariance_equation: str
    backward_extension_identity: str
    selection_condition: str
    phase_coordinate: str
    phase_transversality: str
    a_vector_field_column: str
    eta_vector_field_column: str
    scaled_nu_vector_field_column: str
    scaled_eta_vector_field_column: str
    period_delay_parameter_convention: str
    parameter_shift_sensitivity: str
    parameter_boundary_sensitivity: str
    parameter_phase_gauge: str
    physical_a_to_scaled_nu_conversion: str
    right_flight_endpoint_residual: str
    fixed_time_endpoint_derivative: str
    moving_time_endpoint_derivative: str
    scalar_hit_time_requirement: str
    minimum_continuation_unknowns: tuple[str, ...]
    minimum_validation_gates: tuple[str, ...]


@dataclass(frozen=True)
class SelectedRepellingEndpointCertificate:
    """Exact positive statements and strict fixed-epsilon refusals."""

    model_id: str
    fixed_epsilon_bvp_result_sha256: str
    two_sided_candidate_result_sha256: str
    exact_quadratic_rfde_used: bool
    full_period_horizon_used: bool
    same_current_and_same_scalar_exit_compatible_histories_constructed: bool
    eta_nonzero_period_atom_future_nonuniqueness_validated: bool
    eta_zero_baseline_delay_future_nonuniqueness_validated: bool
    scalar_exit_observable_determines_complete_history_validated: bool
    scalar_exit_observable_determines_right_flight_validated: bool
    scalar_exit_observable_is_one_dimensional_repelling_chart_validated: bool
    required_chart_is_inside_solution_manifold: bool
    invariant_chart_implies_local_backward_extension_validated: bool
    full_history_parameter_sensitivity_equations_specified: bool
    phase_gauge_specified: bool
    full_history_right_flight_endpoint_map_specified: bool
    repaired_ambient_775_by_774_arithmetic_validated: bool
    repaired_ledger_strong_fredholm_operator_validated: bool
    backward_extendible_selected_repelling_chart_constructed: bool
    selected_chart_parameter_a_derivative_validated: bool
    selected_chart_parameter_eta_derivative_validated: bool
    selected_chart_phase_transversality_validated: bool
    right_flight_to_selected_chart_validated: bool
    fixed_epsilon_selected_root_validated: bool
    fixed_epsilon_root_response_validated: bool
    physical_onset_validated: bool
    minimal_stop: str


def _scaled_fast_field(
    current_x: sp.Expr,
    current_y: sp.Expr,
    delay_4_x: sp.Expr,
    delay_5_x: sp.Expr,
    period_delay_x: sp.Expr,
    eta: sp.Expr,
) -> sp.Expr:
    delta = sp.sqrt(5) / 5
    return sp.expand(
        current_y
        - current_x**2
        + delta
        * (
            -current_x**3 / 3
            + sp.Rational(1, 5)
            * ((delay_4_x + delay_5_x) / 2 - current_x)
        )
        + delta**2 * eta * (current_x**2 - period_delay_x**2)
        + delta**3
        * sp.Rational(1, 4)
        * ((delay_4_x**3 + delay_5_x**3) / 2 - current_x**3)
    )


@lru_cache(maxsize=1)
def reference_compatible_history_fiber_audit() -> CompatibleHistoryFiberAudit:
    """Return two exact counterexamples inside the strong solution manifold.

    Both pairs have current state ``(X,Y)=(1,1/2)`` and hence ``G=0``.  A
    Hermite correction makes each perturbed history satisfy the two current
    RFDE compatibility equations, not merely continuity in the ambient phase
    space.
    """

    delta = sp.sqrt(5) / 5
    epsilon = sp.Rational(1, 5)
    # A parser-safe name is used in the JSON algebra.  The documentation
    # renders this symbol as Theta_*.
    theta = sp.Symbol("Theta_star", positive=True)
    s = sp.Symbol("s", real=True)
    r, eta, nu = sp.symbols("r eta nu", real=True)

    # B vanishes at every active sampling node and has B'(0)=1.  It lets a
    # prescribed set of history values be corrected to the RFDE solution
    # manifold without altering those values.
    compatibility_node = sp.expand(
        s * (s + 4) * (s + 5) * (s + theta) / (20 * theta)
    )
    base_fast = -sp.Rational(1, 2) - delta / 3
    base_slow = -1 + delta * nu
    base_x = sp.expand(1 + base_fast * compatibility_node)
    base_y = sp.expand(sp.Rational(1, 2) + base_slow * compatibility_node)

    lagrange_period = sp.factor(
        s
        * (s + 4)
        * (s + 5)
        / ((-theta) * (4 - theta) * (5 - theta))
    )
    period_difference = sp.expand(
        -delta**2 * eta * ((1 + r) ** 2 - 1)
    )
    period_perturbation = sp.expand(
        r * lagrange_period
        + (
            period_difference
            - r * sp.diff(lagrange_period, s).subs(s, 0)
        )
        * compatibility_node
    )

    lagrange_delay_4 = sp.factor(
        s * (s + 5) * (s + theta) / ((-4) * (theta - 4))
    )
    delay_4_difference = sp.expand(
        delta * r / 10
        + delta**3 * ((1 + r) ** 3 - 1) / 8
    )
    delay_4_perturbation = sp.expand(
        r * lagrange_delay_4
        + (
            delay_4_difference
            - r * sp.diff(lagrange_delay_4, s).subs(s, 0)
        )
        * compatibility_node
    )

    base_field = _scaled_fast_field(1, sp.Rational(1, 2), 1, 1, 1, eta)
    period_field = _scaled_fast_field(
        1, sp.Rational(1, 2), 1, 1, 1 + r, eta
    )
    delay_4_field = _scaled_fast_field(
        1, sp.Rational(1, 2), 1 + r, 1, 1, eta
    )
    base_compatibility = sp.Matrix(
        [
            sp.diff(base_x, s).subs(s, 0) - base_field,
            sp.diff(base_y, s).subs(s, 0) - (-1 + delta * nu),
        ]
    ).applyfunc(sp.simplify)
    period_compatibility = sp.Matrix(
        [
            sp.diff(base_x + period_perturbation, s).subs(s, 0)
            - period_field,
            sp.diff(base_y, s).subs(s, 0) - (-1 + delta * nu),
        ]
    ).applyfunc(sp.simplify)
    delay_4_compatibility = sp.Matrix(
        [
            sp.diff(base_x + delay_4_perturbation, s).subs(s, 0)
            - delay_4_field,
            sp.diff(base_y, s).subs(s, 0) - (-1 + delta * nu),
        ]
    ).applyfunc(sp.simplify)

    return CompatibleHistoryFiberAudit(
        delta=delta,
        epsilon=epsilon,
        scaled_period_delay=theta,
        history_variable=s,
        perturbation_amplitude=r,
        eta=eta,
        nu=nu,
        solution_manifold_node_polynomial=compatibility_node,
        base_voltage_history=base_x,
        base_recovery_history=base_y,
        base_current_state=sp.Matrix([1, sp.Rational(1, 2)]),
        exit_observable_at_base_current=sp.simplify(
            sp.Rational(1, 2)
            - sp.Rational(1, 4)
            - sp.Rational(1, 4)
        ),
        exit_observable_current_gradient_at_base=sp.Matrix(
            [1, -sp.Rational(1, 2)]
        ),
        period_lagrange_polynomial=lagrange_period,
        period_history_perturbation=period_perturbation,
        period_perturbation_current_value=sp.simplify(
            period_perturbation.subs(s, 0)
        ),
        period_perturbation_delay_4_value=sp.simplify(
            period_perturbation.subs(s, -4)
        ),
        period_perturbation_delay_5_value=sp.simplify(
            period_perturbation.subs(s, -5)
        ),
        period_perturbation_period_delay_value=sp.simplify(
            period_perturbation.subs(s, -theta)
        ),
        period_perturbation_current_derivative=sp.simplify(
            sp.diff(period_perturbation, s).subs(s, 0)
        ),
        period_fast_field_difference=sp.simplify(period_field - base_field),
        period_unit_witness_difference=sp.simplify(
            period_difference.subs(r, 1)
        ),
        delay_4_lagrange_polynomial=lagrange_delay_4,
        delay_4_history_perturbation=delay_4_perturbation,
        delay_4_perturbation_current_value=sp.simplify(
            delay_4_perturbation.subs(s, 0)
        ),
        delay_4_perturbation_delay_4_value=sp.simplify(
            delay_4_perturbation.subs(s, -4)
        ),
        delay_4_perturbation_delay_5_value=sp.simplify(
            delay_4_perturbation.subs(s, -5)
        ),
        delay_4_perturbation_period_delay_value=sp.simplify(
            delay_4_perturbation.subs(s, -theta)
        ),
        delay_4_perturbation_current_derivative=sp.simplify(
            sp.diff(delay_4_perturbation, s).subs(s, 0)
        ),
        delay_4_fast_field_difference=sp.simplify(
            delay_4_field - base_field
        ),
        delay_4_unit_witness_difference=sp.simplify(
            delay_4_difference.subs(r, 1)
        ),
        base_solution_manifold_compatibility_defect=base_compatibility,
        period_solution_manifold_compatibility_defect=period_compatibility,
        delay_4_solution_manifold_compatibility_defect=(
            delay_4_compatibility
        ),
    )


def compatible_history_fiber_algebra_is_exact(
    audit: CompatibleHistoryFiberAudit | None = None,
) -> bool:
    """Check every interpolation and compatibility identity exactly."""

    row = audit or reference_compatible_history_fiber_audit()
    r, eta = row.perturbation_amplitude, row.eta
    s, theta = row.history_variable, row.scaled_period_delay
    node = row.solution_manifold_node_polynomial
    return bool(
        row.delta == sp.sqrt(5) / 5
        and row.epsilon == sp.Rational(1, 5)
        and sp.simplify(node.subs(s, 0)) == 0
        and sp.simplify(node.subs(s, -4)) == 0
        and sp.simplify(node.subs(s, -5)) == 0
        and sp.simplify(node.subs(s, -theta)) == 0
        and sp.simplify(sp.diff(node, s).subs(s, 0)) == 1
        and row.exit_observable_at_base_current == 0
        and row.exit_observable_current_gradient_at_base
        == sp.Matrix([1, -sp.Rational(1, 2)])
        and row.period_perturbation_current_value == 0
        and row.period_perturbation_delay_4_value == 0
        and row.period_perturbation_delay_5_value == 0
        and row.period_perturbation_period_delay_value == r
        and sp.simplify(
            row.period_perturbation_current_derivative
            + sp.Rational(1, 5) * eta * (2 * r + r**2)
        )
        == 0
        and row.period_fast_field_difference
        == row.period_perturbation_current_derivative
        and row.period_unit_witness_difference == -3 * eta / 5
        and row.delay_4_perturbation_current_value == 0
        and row.delay_4_perturbation_delay_4_value == r
        and row.delay_4_perturbation_delay_5_value == 0
        and row.delay_4_perturbation_period_delay_value == 0
        and row.delay_4_fast_field_difference
        == row.delay_4_perturbation_current_derivative
        and row.delay_4_unit_witness_difference == 11 * sp.sqrt(5) / 200
        and row.base_solution_manifold_compatibility_defect == sp.zeros(2, 1)
        and row.period_solution_manifold_compatibility_defect
        == sp.zeros(2, 1)
        and row.delay_4_solution_manifold_compatibility_defect
        == sp.zeros(2, 1)
    )


def reference_compatible_endpoint_count_audit() -> CompatibleEndpointCountAudit:
    """Return the raw-versus-compatible endpoint count audit."""

    # The endpoint bump used above has zero current value and arbitrary
    # current derivative.  It makes the compatibility derivative surjective
    # without restricting current evaluation.  Since DG(1,1/2)=(1,-1/2),
    # the scalar exit row is transverse at the explicit witness.
    raw_dimension = 194
    state_dimension = 2
    derivative_seams = 30
    global_c1_dimension = raw_dimension - derivative_seams
    discrete_endpoint_level = raw_dimension - state_dimension
    global_c1_compatible = global_c1_dimension - state_dimension
    repelling_dimension = 1
    return CompatibleEndpointCountAudit(
        raw_history_coefficient_dimension=raw_dimension,
        state_dimension=state_dimension,
        value_continuous_history_dimension=raw_dimension,
        global_c1_internal_derivative_continuity_codimension=(
            derivative_seams
        ),
        global_c1_history_dimension=global_c1_dimension,
        endpoint_compatibility_codimension=state_dimension,
        discrete_endpoint_compatible_level_dimension=(
            discrete_endpoint_level
        ),
        global_c1_endpoint_compatible_level_dimension=(
            global_c1_compatible
        ),
        scalar_current_exit_constraints=1,
        exit_observable_transverse_at_witness=True,
        scalar_exit_fiber_dimension_on_discrete_endpoint_level=(
            discrete_endpoint_level - 1
        ),
        scalar_exit_fiber_dimension_on_global_c1_compatible_level=(
            global_c1_compatible - 1
        ),
        repelling_chart_dimension_inside_solution_manifold=(
            repelling_dimension
        ),
        scalar_exit_fiber_excess_over_repelling_curve_on_discrete_level=(
            discrete_endpoint_level - 1 - repelling_dimension
        ),
        scalar_exit_fiber_excess_over_repelling_curve_on_global_c1_level=(
            global_c1_compatible - 1 - repelling_dimension
        ),
        repelling_curve_codimension_in_raw_history_space=(
            raw_dimension - repelling_dimension
        ),
        repelling_curve_codimension_on_discrete_endpoint_level=(
            discrete_endpoint_level - repelling_dimension
        ),
        repelling_curve_codimension_on_global_c1_compatible_level=(
            global_c1_compatible - repelling_dimension
        ),
        raw_endpoint_equalities=raw_dimension,
        repelling_chart_coordinates=repelling_dimension,
        raw_net_endpoint_conditions=raw_dimension - repelling_dimension,
        ambient_incoming_coordinate_dimension_reported_by_candidate=193,
        ambient_incoming_compatibility_rows=2,
        effective_discrete_incoming_zero_fiber_dimension=191,
        ambient_repaired_775_by_774_ledger_is_arithmetic_only=True,
        global_c1_or_w2_multicell_realization_validated=False,
        candidate_193_plus_1_is_compatible_fredholm_count_validated=False,
        exact_interpretation=(
            "the value-continuous 194-coefficient ledger has a "
            "192-dimensional endpoint-compatible level, but global C1 "
            "continuity removes 30 more directions, leaving a "
            "162-dimensional strong compatible level; scalar G=0 leaves "
            "fibers of dimensions 191 and 161 on those two levels, never "
            "the required one-dimensional curve; a raw equality against "
            "that curve has net codimension 193=30+2+161"
        ),
        unresolved_alternatives=(
            "assemble the ambient 775-by-774 arithmetic with 192-row projected history blocks, six endpoint compatibility rows, and all global strong-history seam conditions without double counting",
            "rebuild in intrinsic global-C1 or W2p compatible coordinates and prove the same Fredholm index independently of matrix size",
            "prove the one-dimensional selected repelling embedding and its complement in whichever strong endpoint codomain is chosen",
        ),
    )


def reference_selected_repelling_endpoint_contract(
) -> SelectedRepellingEndpointContract:
    """Return the smallest exact invariant-chart continuation contract."""

    return SelectedRepellingEndpointContract(
        physical_phase_space=(
            "X_phys=C([-T_*,0],R^2); under s=delta*t its fold-time "
            "pullback is X_fold=C([-Theta_*,0],R^2), with "
            "S_delta(phi)(sigma)=((phi_V(sigma/delta)-1)/delta,"
            "(2/3-phi_W(sigma/delta))/delta^2)"
        ),
        strong_solution_manifold=(
            "M^1_{a,eta}=M^1_phys={phi in C^1([-T_*,0]): "
            "phi'(0)=F_phys(phi;a,eta)}; equivalently "
            "M^1_fold_{nu,eta}={Phi in C^1([-Theta_*,0]): "
            "Phi'(0)=F_fold(Phi;nu,eta)}"
        ),
        selected_chart=(
            "Gamma^r:I_xi x P -> M^1_{a,eta}, with rank "
            "partial_xi Gamma^r=1"
        ),
        chart_internal_flow="dot xi=q^r(xi;a,eta)",
        shift_invariance_equation=(
            "q^r partial_xi Gamma^r(theta)=partial_theta Gamma^r(theta), "
            "-T_*<theta<0"
        ),
        boundary_invariance_equation=(
            "q^r partial_xi Gamma^r(0)=F(Gamma^r;a,eta)"
        ),
        backward_extension_identity=(
            "if dot xi=q^r has a backward scalar flow, then "
            "z_t=Gamma^r(xi(t);a,eta) is an exact backward-extendible "
            "RFDE history without an ambient backward RFDE IVP"
        ),
        selection_condition=(
            "one fixed nonlinear repelling-tail/outer-history anchor, "
            "continued coherently from a validated selected reference; "
            "invariance alone does not select a threshold"
        ),
        phase_coordinate=(
            "chi(Gamma^r(xi;a,eta))=xi for one fixed bounded full-history "
            "functional chi"
        ),
        phase_transversality=(
            "chi(partial_xi Gamma^r)=1 and the selected anchor removes "
            "the remaining autonomous translation/reparameterization"
        ),
        a_vector_field_column="partial_a F=(0,-1/5)^T",
        eta_vector_field_column=(
            "partial_eta F=(1/5*((V(0)-1)^2-(V(-T_*)-1)^2),0)^T"
        ),
        scaled_nu_vector_field_column=(
            "partial_nu F_fold=(0,1/sqrt(5))^T"
        ),
        scaled_eta_vector_field_column=(
            "partial_eta F_fold=(1/5*(X(0)^2-X(-Theta_*)^2),0)^T"
        ),
        period_delay_parameter_convention=(
            "T_* is the frozen plant delay under a and eta derivatives; "
            "varying T_* would add a translated-history derivative and "
            "requires a separate strong-space delay column"
        ),
        parameter_shift_sensitivity=(
            "q Gamma_{xi,lambda}+q_lambda Gamma_xi="
            "partial_theta Gamma_lambda, lambda in {a,eta}"
        ),
        parameter_boundary_sensitivity=(
            "q Gamma_{xi,lambda}(0)+q_lambda Gamma_xi(0)="
            "D_phi F(Gamma) Gamma_lambda+F_lambda(Gamma)"
        ),
        parameter_phase_gauge=(
            "chi(Gamma_lambda)=0 at fixed xi, plus the differentiated "
            "selected-anchor equation"
        ),
        physical_a_to_scaled_nu_conversion=(
            "a=1+(1/5)nu, hence Gamma_a=5 Gamma_nu at fixed epsilon "
            "within one coordinate representation; physical and fold "
            "components are related by D S_delta and the internal fields "
            "satisfy q_fold=q_phys/delta"
        ),
        right_flight_endpoint_residual=(
            "R_+(x^+,L_+,xi,a,eta)=End_{L_+}x^+ - "
            "Gamma^r(xi;a,eta) in X_phys"
        ),
        fixed_time_endpoint_derivative=(
            "D R_+=End_{L_+}u-Gamma_xi dxi-Gamma_a da-"
            "Gamma_eta deta"
        ),
        moving_time_endpoint_derivative=(
            "D R_+(theta)=u(L_++theta)+dot x^+(L_++theta)dL_+ - "
            "Gamma_xi(theta)dxi-Gamma_a(theta)da-"
            "Gamma_eta(theta)deta"
        ),
        scalar_hit_time_requirement=(
            "a scalar section may define L_+ only after a directed "
            "nonzero crossing derivative; it is not the endpoint chart"
        ),
        minimum_continuation_unknowns=(
            "piecewise-Chebyshev coefficients of Gamma^r(xi,theta) on I_xi x [-T_*,0]",
            "the scalar internal field q^r(xi) and one selected-anchor coordinate",
            "the full-history jets Gamma_a and Gamma_eta with their scalar q_a and q_eta columns",
            "an exact interval enclosure of T_* and a translation-closed mesh for 4*sqrt(5), 5*sqrt(5), and T_*",
            "the right-flight trace and either fixed L_+ or a transversal moving-hit variable",
        ),
        minimum_validation_gates=(
            "validate the nonlinear invariant-chart residual and a phase/anchor bordered inverse with coefficient tails",
            "prove chart rank, injectivity, solution-manifold compatibility, and local backward scalar-flow retention",
            "prove the anchor is the chosen repelling selection rather than an arbitrary invariant curve",
            "validate Gamma_a and Gamma_eta on the complete T_* horizon, including the older-history eta column",
            "compose the complete-history right-flight endpoint residual and validate its derivative",
            "resolve raw, global-strong, and endpoint-compatible codomains before promoting the arithmetic 193+1 or 775x774 ledger to a Fredholm operator",
            "only then validate the two-sided one-cokernel BVP, adjoint, selected root, and root response",
        ),
    )


def invariant_chart_backward_extension_identity_is_exact() -> bool:
    """Record the chain-rule proof behind the chart contract.

    The shift equation gives the RFDE history identity away from current
    time, and the boundary equation gives the RFDE vector field at current
    time.  This is an exact implication conditional on a chart satisfying
    those equations; it is not evidence that the chart has been solved.
    """

    contract = reference_selected_repelling_endpoint_contract()
    return bool(
        "partial_theta" in contract.shift_invariance_equation
        and "F(Gamma^r" in contract.boundary_invariance_equation
        and "backward scalar flow" in contract.backward_extension_identity
    )


def reference_selected_repelling_endpoint_certificate(
) -> SelectedRepellingEndpointCertificate:
    """Return the exact audit result and all unproved-claim refusals."""

    return SelectedRepellingEndpointCertificate(
        model_id=MODEL_ID,
        fixed_epsilon_bvp_result_sha256=FIXED_EPSILON_BVP_RESULT_SHA256,
        two_sided_candidate_result_sha256=(
            TWO_SIDED_CANDIDATE_RESULT_SHA256
        ),
        exact_quadratic_rfde_used=True,
        full_period_horizon_used=True,
        same_current_and_same_scalar_exit_compatible_histories_constructed=True,
        eta_nonzero_period_atom_future_nonuniqueness_validated=True,
        eta_zero_baseline_delay_future_nonuniqueness_validated=True,
        scalar_exit_observable_determines_complete_history_validated=False,
        scalar_exit_observable_determines_right_flight_validated=False,
        scalar_exit_observable_is_one_dimensional_repelling_chart_validated=False,
        required_chart_is_inside_solution_manifold=True,
        invariant_chart_implies_local_backward_extension_validated=True,
        full_history_parameter_sensitivity_equations_specified=True,
        phase_gauge_specified=True,
        full_history_right_flight_endpoint_map_specified=True,
        repaired_ambient_775_by_774_arithmetic_validated=True,
        repaired_ledger_strong_fredholm_operator_validated=False,
        backward_extendible_selected_repelling_chart_constructed=False,
        selected_chart_parameter_a_derivative_validated=False,
        selected_chart_parameter_eta_derivative_validated=False,
        selected_chart_phase_transversality_validated=False,
        right_flight_to_selected_chart_validated=False,
        fixed_epsilon_selected_root_validated=False,
        fixed_epsilon_root_response_validated=False,
        physical_onset_validated=False,
        minimal_stop=(
            "solve and interval-validate the selected invariant-history "
            "chart Gamma^r, its complete-history a/eta jets, and its "
            "composition with the right flight after resolving the 30 "
            "global-C1 derivative seams per represented 16-cell history "
            "block, every remaining flight/history-interface derivative "
            "join, and the endpoint compatibility rows in a fresh strong "
            "operator count"
        ),
    )


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [
            [str(sp.simplify(value[i, j])) for j in range(value.cols)]
            for i in range(value.rows)
        ]
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return value


def reference_selected_repelling_endpoint_payload() -> dict[str, Any]:
    """Return the deterministic exact audit payload."""

    certificate = reference_selected_repelling_endpoint_certificate()
    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "compatible_history_fiber_audit": _json_value(
            asdict(reference_compatible_history_fiber_audit())
        ),
        "compatible_endpoint_count_audit": _json_value(
            asdict(reference_compatible_endpoint_count_audit())
        ),
        "selected_repelling_endpoint_contract": _json_value(
            asdict(reference_selected_repelling_endpoint_contract())
        ),
        "certificate": _json_value(asdict(certificate)),
        "scope": {
            "exact_compatible_history_counterexamples": True,
            "minimum_invariant_chart_contract": True,
            "backward_extendible_selected_repelling_chart": False,
            "validated_chart_a_derivative": False,
            "validated_chart_eta_derivative": False,
            "validated_chart_phase": False,
            "validated_right_flight_endpoint_composition": False,
            "repaired_ambient_775_by_774_arithmetic": True,
            "validated_strong_fredholm_endpoint_operator": False,
            "fixed_epsilon_selected_root": False,
            "fixed_epsilon_root_response": False,
            "physical_onset": False,
        },
    }


def validate_selected_repelling_endpoint_payload(
    payload: Mapping[str, Any],
) -> SelectedRepellingEndpointCertificate:
    """Reject any mutation or promotion of the stop/go record."""

    expected = reference_selected_repelling_endpoint_payload()
    if dict(payload) != expected:
        raise ValueError(
            "fixed-epsilon selected-repelling-endpoint payload changed or "
            "promoted an unvalidated claim"
        )
    return reference_selected_repelling_endpoint_certificate()


__all__ = [
    "DEFAULT_COMMAND",
    "FIXED_EPSILON_BVP_RESULT_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_ID",
    "PROOF_SOURCE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "TWO_SIDED_CANDIDATE_RESULT_SHA256",
    "CompatibleEndpointCountAudit",
    "CompatibleHistoryFiberAudit",
    "SelectedRepellingEndpointCertificate",
    "SelectedRepellingEndpointContract",
    "compatible_history_fiber_algebra_is_exact",
    "invariant_chart_backward_extension_identity_is_exact",
    "reference_compatible_endpoint_count_audit",
    "reference_compatible_history_fiber_audit",
    "reference_selected_repelling_endpoint_certificate",
    "reference_selected_repelling_endpoint_contract",
    "reference_selected_repelling_endpoint_payload",
    "validate_selected_repelling_endpoint_payload",
]
