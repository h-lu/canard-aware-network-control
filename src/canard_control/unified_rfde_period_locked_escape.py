"""Exact algebra for a period-locked unified-RFDE escape candidate.

The existing lifted selected-root theorem and the dual-scaffold periodic
theorem concern different RFDEs.  This module does not promote them into one
theorem.  It records two narrower facts:

* adding more distinct fixed delay atoms does not evade exact invisibility
  on every scalar synchronous history; and
* a third delay locked to one distinguished periodic orbit gives an exact
  orbit-annihilating operator with nonzero synchronous collective first
  moment, but its leading singular-canard pairing vanishes by parity.

The period lock also has a qualitative local three-parameter periodic branch
with a zero central eta response column.  It does *not* produce a nonzero
linear selected-root column: that fixed-epsilon question remains open.  The
separate quadratic carrier supplies the proved positive small-delta
mechanism.  No physical onset, basin, or root-to-event equivalence is encoded
here.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

import sympy as sp


COMPATIBILITY_RESULT_SHA256 = (
    "600c8f45fd420b284299921142b3b0ab337f7427df8f9b92d53e3d0555365adf"
)
PERIODIC_BOX_RESULT_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
BALANCED_CONTROL_CHAIN_RESULT_SHA256 = (
    "090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9"
)
AUTONOMOUS_HANDOFF_RESULT_SHA256 = (
    "38f612771fd5f7e50ffd4f77103ea680b447fd11a7af25cc5ccea95b9bf606f2"
)
ROOT_ADJOINT_GATE_RESULT_SHA256 = (
    "2c2471944d476f6fd6ba51c0a025ce1de6f6bdda8033e6a70a36aab57206e62f"
)
QUADRATIC_CARRIER_RESULT_SHA256 = (
    "4f80cd8ef53161e16886c06fdc52d99be774a9b1cf15d3e7ba534fe37925f7f8"
)
HETEROGENEOUS_ROOT_DOC_SHA256 = (
    "6432f8896459846130f70b559ebd7894ea4bf644688915476deac086bbc34e14"
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/unified_rfde_period_locked_escape.py"
)
GENERATOR_RELATIVE_PATH = "experiments/unified_rfde_period_locked_escape.py"
DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/unified_rfde_period_locked_escape.py"
)
ARITHMETIC_DESCRIPTION = (
    "exact SymPy finite-atom, curvature, non-rank-one balanced topology, "
    "collective projection, period-lock, normalized and epsilon-scaled "
    "first-moment, singular-canard parity cancellation, transverse, "
    "event-functional, off-synchrony witness, and block-determinant identities"
)
DISTINGUISHED_PERIOD_DEFINITION = (
    "T_p is the exact period of the phase-fixed validated synchronous orbit "
    "at a_per=3/5 and (kappa_1,kappa_3)=(1/5,1/4); the binary64 period in "
    "its parent artifact is diagnostic only"
)

MODEL_ID = (
    "balanced-general-topology-dual-scaffold-fhn-"
    "period-locked-collective-delay-escape-candidate"
)
ASSUMPTIONS_ID = (
    "finite-balanced-Q;pi>0,pi^T1=1,pi^TQ=pi^T;"
    "B_l1=(1/2)1,pi^TB_l=(1/2)pi^T;Pi=1pi^T;"
    "periodic-output-fiber-a_per=3/5;a_c-is-threshold-output;"
    "distinct-fixed-atoms-for-universal-obstruction;"
    "collective-third-delay-equals-distinguished-orbit-period;"
    "no-policy-dependent-event"
)


Matrix = sp.ImmutableMatrix


def _matrix(value: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(value)


@dataclass(frozen=True)
class FiniteAtomInvisibilityAudit:
    """Coefficient audit for three distinct synchronous delay evaluations."""

    evaluation_symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
    atom_sync_columns: Matrix
    synchronous_action: Matrix
    action_coefficient_matrix: Matrix
    universal_invisibility_substitution_action: Matrix
    third_atom_coefficient_after_first_two_annihilate: Matrix


@dataclass(frozen=True)
class HeterogeneousCurvatureSynchronyAudit:
    """Two-node form of the curvature/synchrony return obstruction."""

    curvature_vector: Matrix
    synchrony_residual: Matrix
    stable_vector: Matrix
    heterogeneous_return: sp.Expr
    homogeneous_synchrony_substitution_residual: Matrix
    homogeneous_synchrony_substitution_return: sp.Expr


@dataclass(frozen=True)
class PeriodLockedEscapeAudit:
    """Exact identities for one finite balanced topology candidate."""

    node_count: int
    epsilon: sp.Expr
    periodic_output_unfolding: sp.Expr
    kappa_center: tuple[sp.Expr, sp.Expr]
    base_delays: tuple[sp.Expr, sp.Expr]
    collective_projection: Matrix
    synchronous_right: Matrix
    synchronous_left: Matrix
    transverse_projection: Matrix
    stationary_sum_residual: sp.Expr
    collective_projection_idempotence_residual: Matrix
    collective_projection_on_sync_residual: Matrix
    collective_projection_left_residual: Matrix
    base_scaffold: Matrix
    base_scaffold_rank: int
    base_scaffold_entrywise_nonnegative: bool
    base_delay_layers_entrywise_nonnegative: bool
    stationary_weight_strictly_positive: bool
    base_scaffold_row_balance_residual: Matrix
    base_scaffold_left_balance_residual: Matrix
    base_scaffold_minus_collective_projection: Matrix
    base_delay_0: Matrix
    base_delay_1: Matrix
    base_delay_sum_minus_scaffold: Matrix
    base_delay_sum_minus_collective_projection: Matrix
    base_delay_0_row_balance_residual: Matrix
    base_delay_1_row_balance_residual: Matrix
    base_delay_0_left_balance_residual: Matrix
    base_delay_1_left_balance_residual: Matrix
    combined_delay_row_balance_residual: Matrix
    combined_delay_left_balance_residual: Matrix
    synchronous_scaffold_action: Matrix
    synchronous_linear_delay_action: Matrix
    expected_synchronous_linear_delay_action: Matrix
    normalized_structural_current_atom: Matrix
    normalized_structural_period_atom: Matrix
    normalized_structural_total_mass: Matrix
    normalized_structural_first_moment: Matrix
    normalized_projected_synchronous_first_moment: sp.Expr
    actual_eta_derivative_current_atom: Matrix
    actual_eta_derivative_period_atom: Matrix
    actual_eta_derivative_total_mass: Matrix
    actual_eta_derivative_first_moment: Matrix
    actual_projected_synchronous_first_moment: sp.Expr
    synchronous_action: Matrix
    constant_history_action: Matrix
    period_locked_action: Matrix
    affine_synchronous_action: Matrix
    structural_action_on_transverse_history: Matrix
    transverse_projection_of_structural_action: Matrix
    positive_event_functional: sp.Expr
    negative_event_functional: sp.Expr
    response_matrix: Matrix
    response_determinant: sp.Expr
    expected_response_determinant: sp.Expr
    offsync_direction: Matrix
    offsync_left: Matrix
    sync_annihilating_offsync_operator: Matrix
    offsync_operator_on_sync: Matrix
    offsync_operator_on_direction: Matrix
    offsync_projected_pairing: sp.Expr


@dataclass(frozen=True)
class LinearCanardParityAudit:
    """Exact leading singular-canard cancellation for the linear lock."""

    scaled_delay_shift: sp.Expr
    singular_canard: sp.Expr
    singular_history_difference: sp.Expr
    singular_fast_forcing_coefficient: sp.Expr
    fast_adjoint_component: sp.Expr
    leading_integrand: sp.Expr
    leading_pairing: sp.Expr


@dataclass(frozen=True)
class UnifiedEscapeCertificate:
    """Strict exact/conditional/open ledger for the escape candidate."""

    model_id: str
    assumptions_id: str
    compatibility_result_sha256: str
    periodic_box_result_sha256: str
    balanced_control_chain_result_sha256: str
    autonomous_handoff_result_sha256: str
    root_adjoint_gate_result_sha256: str
    quadratic_carrier_result_sha256: str
    heterogeneous_root_doc_sha256: str
    finite_atom_universal_invisibility_is_atomwise_validated: bool
    arbitrary_third_atom_escapes_universal_invisibility_validated: bool
    homogeneous_curvature_sync_forces_existing_return_zero_validated: bool
    balanced_general_topology_carrier_validated: bool
    delay_layers_need_not_sum_to_scaffold_or_projector_validated: bool
    topology_independent_synchronous_periodic_outputs_validated: bool
    period_locked_operator_preserves_synchrony_validated: bool
    period_locked_operator_preserves_constant_histories_validated: bool
    distinguished_periodic_orbit_annihilated_validated: bool
    pure_transverse_variational_action_zero_validated: bool
    normalized_projected_synchronous_first_moment_nonzero_validated: bool
    actual_eta_derivative_epsilon_factor_validated: bool
    actual_projected_synchronous_first_moment_nonzero_validated: bool
    linear_leading_singular_interior_pairing_zero_validated: bool
    nonzero_moment_sufficient_for_nonzero_root_response_validated: bool
    collective_mode_is_simple_canard_critical_direction_validated: bool
    general_topology_stable_history_invertibility_validated: bool
    fixed_event_functionals_policy_independent_validated: bool
    block_triangular_response_identity_validated: bool
    block_response_is_parameter_linked_validated: bool
    trajectory_linked_root_periodic_event_chain_validated: bool
    offsync_direct_forcing_witness_validated: bool
    same_extended_rfde_selected_root_validated: bool
    nonzero_selected_root_eta_response_validated: bool
    common_epsilon_root_and_periodic_regime_validated: bool
    qualitative_three_parameter_periodic_branch_validated: bool
    center_periodic_frequency_amplitude_eta_column_zero_validated: bool
    quantitative_eta_neighborhood_periodic_box_validated: bool
    eta_zero_inert_history_trajectory_embedding_validated: bool
    linear_enlarged_horizon_parameter_coherent_root_preparation_validated: bool
    quadratic_leading_singular_pairing_nonzero_parent_validated: bool
    quadratic_fixed_scaled_support_canonical_root_response_parent_validated: bool
    quadratic_fixed_epsilon_one_fifth_rho_nonzero_validated: bool
    eta_zero_balanced_controlled_voltage_excursions_validated: bool
    eta_neighborhood_balanced_controlled_voltage_excursions_validated: bool
    eta_neighborhood_autonomous_event_crossing_validated: bool
    root_event_zero_set_equivalence_validated: bool
    unforced_onset_validated: bool
    biological_pulse_basin_validated: bool
    no_return_validated: bool
    period_calibration_robustness_validated: bool
    full_network_periodic_attraction_validated: bool
    sparse_local_collective_channel_implementation_validated: bool


@lru_cache(maxsize=1)
def reference_finite_atom_invisibility_audit() -> FiniteAtomInvisibilityAudit:
    """Return the exact polynomial-coefficient test for three delay atoms."""

    x_0, x_1, x_2 = sp.symbols("x_0 x_1 x_2", real=True)
    entries = sp.symbols("u_00 u_01 u_02 u_10 u_11 u_12", real=True)
    columns = sp.Matrix(
        [
            [entries[0], entries[1], entries[2]],
            [entries[3], entries[4], entries[5]],
        ]
    )
    evaluations = sp.Matrix([x_0, x_1, x_2])
    action = sp.expand(columns * evaluations)
    coefficient_matrix = action.jacobian(evaluations)
    zero_substitution = {entry: 0 for entry in entries}
    first_two_zero = {
        entries[0]: 0,
        entries[1]: 0,
        entries[3]: 0,
        entries[4]: 0,
    }
    return FiniteAtomInvisibilityAudit(
        evaluation_symbols=(x_0, x_1, x_2),
        atom_sync_columns=_matrix(columns),
        synchronous_action=_matrix(action),
        action_coefficient_matrix=_matrix(coefficient_matrix),
        universal_invisibility_substitution_action=_matrix(
            action.subs(zero_substitution)
        ),
        third_atom_coefficient_after_first_two_annihilate=_matrix(
            action.subs(first_two_zero).jacobian(sp.Matrix([x_2]))
        ),
    )


@lru_cache(maxsize=1)
def reference_heterogeneous_curvature_synchrony_audit(
) -> HeterogeneousCurvatureSynchronyAudit:
    """Return the exact two-node curvature obstruction."""

    c_1, c_2, h = sp.symbols("c_1 c_2 h", real=True)
    one = sp.ones(2, 1)
    projection = one * one.T / 2
    curvature = sp.Matrix([c_1, c_2])
    stable = sp.Matrix([h, -h])
    residual = sp.simplify((sp.eye(2) - projection) * curvature)
    return_value = sp.simplify(
        (one.T / 2 * sp.diag(c_1, c_2) * stable)[0]
    )
    homogeneous = {c_2: c_1}
    return HeterogeneousCurvatureSynchronyAudit(
        curvature_vector=_matrix(curvature),
        synchrony_residual=_matrix(residual),
        stable_vector=_matrix(stable),
        heterogeneous_return=return_value,
        homogeneous_synchrony_substitution_residual=_matrix(
            residual.subs(homogeneous)
        ),
        homogeneous_synchrony_substitution_return=sp.simplify(
            return_value.subs(homogeneous)
        ),
    )


def balanced_period_locked_escape_audit(
    scaffold_value: object,
    stationary_weight: object,
    delay_0_value: object,
    delay_1_value: object,
) -> PeriodLockedEscapeAudit:
    """Return exact carrier residuals for one finite topology."""

    scaffold = sp.Matrix(scaffold_value)
    if scaffold.rows < 1 or scaffold.rows != scaffold.cols:
        raise ValueError("scaffold must be a nonempty square matrix")
    node_count = scaffold.rows
    left = sp.Matrix(stationary_weight)
    if left.shape == (1, node_count):
        left = left.T
    if left.shape != (node_count, 1):
        raise ValueError("stationary weight must have one entry per node")
    base_0 = sp.Matrix(delay_0_value)
    base_1 = sp.Matrix(delay_1_value)
    if base_0.shape != scaffold.shape or base_1.shape != scaffold.shape:
        raise ValueError("delay layers must match the scaffold shape")

    one = sp.ones(node_count, 1)
    projection = one * left.T
    transverse = sp.eye(node_count) - projection
    half = sp.Rational(1, 2)
    epsilon = sp.Rational(1, 5)
    periodic_unfolding = sp.Rational(3, 5)
    kappa_center = (sp.Rational(1, 5), sp.Rational(1, 4))
    base_delays = (4 * sp.sqrt(5), 5 * sp.sqrt(5))

    period = sp.symbols("T_p", positive=True)
    x_0, x_delay_0, x_delay_1, x_period, slope = sp.symbols(
        "x_0 x_delay_0 x_delay_1 x_period slope", real=True
    )
    synchronous_scaffold_action = sp.simplify(
        (scaffold - sp.eye(node_count)) * (x_0 * one)
    )
    synchronous_delay_action = sp.simplify(
        base_0 * (x_delay_0 * one)
        + base_1 * (x_delay_1 * one)
        - x_0 * one
    )
    expected_delay_action = sp.simplify(
        (half * x_delay_0 + half * x_delay_1 - x_0) * one
    )
    normalized_current_atom = projection
    normalized_period_atom = -projection
    normalized_first_moment = sp.simplify(period * normalized_period_atom)
    actual_current_atom = sp.simplify(epsilon * normalized_current_atom)
    actual_period_atom = sp.simplify(epsilon * normalized_period_atom)
    actual_first_moment = sp.simplify(period * actual_period_atom)
    sync_action = sp.simplify(
        normalized_current_atom * (x_0 * one)
        + normalized_period_atom * (x_period * one)
    )
    locked_action = sp.simplify(sync_action.subs({x_period: x_0}))
    affine_action = sp.simplify(
        sync_action.subs({x_period: x_0 - slope * period})
    )

    z_current = sp.Matrix(
        sp.symbols(f"z_current_0:{node_count}", real=True)
    )
    constant_action = sp.simplify(projection * (z_current - z_current))
    h_current = sp.Matrix(
        sp.symbols(f"h_current_0:{node_count}", real=True)
    )
    h_period = sp.Matrix(
        sp.symbols(f"h_period_0:{node_count}", real=True)
    )
    transverse_history_difference = transverse * (h_current - h_period)
    transverse_action = sp.simplify(
        projection * transverse_history_difference
    )

    event_state = sp.symbols("x_event", real=True)
    positive_event = event_state - sp.Rational(3, 2)
    negative_event = -event_state - sp.Rational(6, 5)

    f_1, f_3, amplitude_1, amplitude_3, p, q, rho = sp.symbols(
        "F_1 F_3 A_1 A_3 p q rho", real=True
    )
    response = sp.Matrix(
        [[f_1, f_3, 0], [amplitude_1, amplitude_3, 0], [p, q, rho]]
    )
    expected_determinant = sp.expand(
        (f_1 * amplitude_3 - f_3 * amplitude_1) * rho
    )

    offsync = sp.Matrix([1, 2])
    offsync_left = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 4)])
    offsync_operator = sp.Matrix([[-1, 1], [2, -2]])
    offsync_one = sp.ones(2, 1)

    return PeriodLockedEscapeAudit(
        node_count=node_count,
        epsilon=epsilon,
        periodic_output_unfolding=periodic_unfolding,
        kappa_center=kappa_center,
        base_delays=base_delays,
        collective_projection=_matrix(projection),
        synchronous_right=_matrix(one),
        synchronous_left=_matrix(left),
        transverse_projection=_matrix(transverse),
        stationary_sum_residual=sp.simplify((left.T * one)[0] - 1),
        collective_projection_idempotence_residual=_matrix(
            projection * projection - projection
        ),
        collective_projection_on_sync_residual=_matrix(
            projection * one - one
        ),
        collective_projection_left_residual=_matrix(
            left.T * projection - left.T
        ),
        base_scaffold=_matrix(scaffold),
        base_scaffold_rank=int(scaffold.rank()),
        base_scaffold_entrywise_nonnegative=all(
            entry.is_nonnegative is True for entry in scaffold
        ),
        base_delay_layers_entrywise_nonnegative=all(
            entry.is_nonnegative is True for entry in (*base_0, *base_1)
        ),
        stationary_weight_strictly_positive=all(
            entry.is_positive is True for entry in left
        ),
        base_scaffold_row_balance_residual=_matrix(scaffold * one - one),
        base_scaffold_left_balance_residual=_matrix(
            left.T * scaffold - left.T
        ),
        base_scaffold_minus_collective_projection=_matrix(
            scaffold - projection
        ),
        base_delay_0=_matrix(base_0),
        base_delay_1=_matrix(base_1),
        base_delay_sum_minus_scaffold=_matrix(base_0 + base_1 - scaffold),
        base_delay_sum_minus_collective_projection=_matrix(
            base_0 + base_1 - projection
        ),
        base_delay_0_row_balance_residual=_matrix(base_0 * one - one / 2),
        base_delay_1_row_balance_residual=_matrix(base_1 * one - one / 2),
        base_delay_0_left_balance_residual=_matrix(
            left.T * base_0 - left.T / 2
        ),
        base_delay_1_left_balance_residual=_matrix(
            left.T * base_1 - left.T / 2
        ),
        combined_delay_row_balance_residual=_matrix(
            (base_0 + base_1) * one - one
        ),
        combined_delay_left_balance_residual=_matrix(
            left.T * (base_0 + base_1) - left.T
        ),
        synchronous_scaffold_action=_matrix(synchronous_scaffold_action),
        synchronous_linear_delay_action=_matrix(synchronous_delay_action),
        expected_synchronous_linear_delay_action=_matrix(
            expected_delay_action
        ),
        normalized_structural_current_atom=_matrix(normalized_current_atom),
        normalized_structural_period_atom=_matrix(normalized_period_atom),
        normalized_structural_total_mass=_matrix(
            normalized_current_atom + normalized_period_atom
        ),
        normalized_structural_first_moment=_matrix(
            normalized_first_moment
        ),
        normalized_projected_synchronous_first_moment=sp.simplify(
            -(left.T * normalized_first_moment * one)[0]
        ),
        actual_eta_derivative_current_atom=_matrix(actual_current_atom),
        actual_eta_derivative_period_atom=_matrix(actual_period_atom),
        actual_eta_derivative_total_mass=_matrix(
            actual_current_atom + actual_period_atom
        ),
        actual_eta_derivative_first_moment=_matrix(actual_first_moment),
        actual_projected_synchronous_first_moment=sp.simplify(
            -(left.T * actual_first_moment * one)[0]
        ),
        synchronous_action=_matrix(sync_action),
        constant_history_action=_matrix(constant_action),
        period_locked_action=_matrix(locked_action),
        affine_synchronous_action=_matrix(affine_action),
        structural_action_on_transverse_history=_matrix(transverse_action),
        transverse_projection_of_structural_action=_matrix(
            transverse * projection
        ),
        positive_event_functional=positive_event,
        negative_event_functional=negative_event,
        response_matrix=_matrix(response),
        response_determinant=sp.factor(response.det()),
        expected_response_determinant=expected_determinant,
        offsync_direction=_matrix(offsync),
        offsync_left=_matrix(offsync_left),
        sync_annihilating_offsync_operator=_matrix(offsync_operator),
        offsync_operator_on_sync=_matrix(offsync_operator * offsync_one),
        offsync_operator_on_direction=_matrix(offsync_operator * offsync),
        offsync_projected_pairing=sp.simplify(
            (offsync_left.T * offsync_operator * offsync)[0]
        ),
    )


@lru_cache(maxsize=1)
def reference_period_locked_escape_audit() -> PeriodLockedEscapeAudit:
    """Return a non-rank-one, nonuniform-weight exact witness."""

    half = sp.Rational(1, 2)
    scaffold = sp.Matrix(
        [
            [half, sp.Rational(1, 4), sp.Rational(1, 4)],
            [sp.Rational(1, 8), sp.Rational(5, 8), sp.Rational(1, 4)],
            [sp.Rational(1, 12), sp.Rational(1, 6), sp.Rational(3, 4)],
        ]
    )
    stationary = [sp.Rational(1, 6), sp.Rational(1, 3), half]
    return balanced_period_locked_escape_audit(
        scaffold,
        stationary,
        scaffold / 2,
        sp.eye(3) / 2,
    )


@lru_cache(maxsize=1)
def reference_linear_canard_parity_audit() -> LinearCanardParityAudit:
    r"""Return the exact leading parity cancellation for the linear carrier.

    In fold time ``s=delta*t``, a fixed physical delay ``T`` becomes
    ``h=delta*T``.  The affine singular canard has a constant delayed
    difference, which pairs to zero with the odd Gaussian fast adjoint.
    This is an interior leading-order calculation only; it is not a
    fixed-epsilon selected-root theorem.
    """

    delta, period, alpha = sp.symbols(
        "delta T_star alpha", positive=True, finite=True
    )
    s = sp.Symbol("s", real=True)
    shift = delta * period
    singular_canard = -s / (2 * alpha)
    history_difference = sp.simplify(
        singular_canard - singular_canard.subs(s, s - shift)
    )
    # After division of the physical fast equation by delta**2, the
    # eta-column contains delta times the delayed history difference.
    forcing = sp.simplify(delta * history_difference)
    adjoint = s * sp.exp(-s**2 / 2)
    integrand = sp.simplify(adjoint * forcing)
    pairing = sp.simplify(sp.integrate(integrand, (s, -sp.oo, sp.oo)))
    return LinearCanardParityAudit(
        scaled_delay_shift=shift,
        singular_canard=singular_canard,
        singular_history_difference=history_difference,
        singular_fast_forcing_coefficient=forcing,
        fast_adjoint_component=adjoint,
        leading_integrand=integrand,
        leading_pairing=pairing,
    )


def linear_canard_parity_audit_is_exact(
    audit: LinearCanardParityAudit | None = None,
) -> bool:
    """Return whether the exact linear-carrier parity identities close."""

    if audit is None:
        audit = reference_linear_canard_parity_audit()
    delta, period, alpha = sp.symbols(
        "delta T_star alpha", positive=True, finite=True
    )
    return bool(
        audit.scaled_delay_shift == delta * period
        and sp.simplify(
            audit.singular_history_difference
            + delta * period / (2 * alpha)
        )
        == 0
        and sp.simplify(
            audit.singular_fast_forcing_coefficient
            + delta**2 * period / (2 * alpha)
        )
        == 0
        and audit.leading_pairing == 0
    )


def balanced_period_locked_escape_audit_is_exact(
    locked: PeriodLockedEscapeAudit,
) -> bool:
    """Return whether one audit satisfies the balanced carrier identities."""

    node_count = locked.node_count
    zero_column = sp.zeros(node_count, 1)
    zero_row = sp.zeros(1, node_count)
    zero_square = sp.zeros(node_count, node_count)
    period = sp.symbols("T_p", positive=True)
    slope = sp.symbols("slope", real=True)
    return bool(
        locked.epsilon == sp.Rational(1, 5)
        and locked.periodic_output_unfolding == sp.Rational(3, 5)
        and locked.kappa_center
        == (sp.Rational(1, 5), sp.Rational(1, 4))
        and locked.base_delays == (4 * sp.sqrt(5), 5 * sp.sqrt(5))
        and locked.stationary_sum_residual == 0
        and locked.collective_projection_idempotence_residual == zero_square
        and locked.collective_projection_on_sync_residual == zero_column
        and locked.collective_projection_left_residual == zero_row
        and locked.base_scaffold_entrywise_nonnegative
        and locked.base_delay_layers_entrywise_nonnegative
        and locked.stationary_weight_strictly_positive
        and locked.base_scaffold_row_balance_residual == zero_column
        and locked.base_scaffold_left_balance_residual == zero_row
        and locked.base_delay_0_row_balance_residual == zero_column
        and locked.base_delay_1_row_balance_residual == zero_column
        and locked.base_delay_0_left_balance_residual == zero_row
        and locked.base_delay_1_left_balance_residual == zero_row
        and locked.combined_delay_row_balance_residual == zero_column
        and locked.combined_delay_left_balance_residual == zero_row
        and locked.synchronous_scaffold_action == zero_column
        and locked.synchronous_linear_delay_action
        == locked.expected_synchronous_linear_delay_action
        and locked.normalized_structural_total_mass == zero_square
        and locked.normalized_structural_first_moment
        == -period * locked.collective_projection
        and locked.normalized_projected_synchronous_first_moment == period
        and locked.actual_eta_derivative_current_atom
        == locked.collective_projection / 5
        and locked.actual_eta_derivative_period_atom
        == -locked.collective_projection / 5
        and locked.actual_eta_derivative_total_mass == zero_square
        and locked.actual_eta_derivative_first_moment
        == -period * locked.collective_projection / 5
        and locked.actual_projected_synchronous_first_moment == period / 5
        and locked.constant_history_action == zero_column
        and locked.period_locked_action == zero_column
        and locked.affine_synchronous_action
        == slope * period * sp.ones(node_count, 1)
        and locked.structural_action_on_transverse_history == zero_column
        and locked.transverse_projection_of_structural_action == zero_square
        and sp.expand(
            locked.response_determinant - locked.expected_response_determinant
        )
        == 0
        and locked.offsync_operator_on_sync == sp.zeros(2, 1)
        and locked.offsync_operator_on_direction == sp.Matrix([1, -2])
        and locked.offsync_projected_pairing == 0
    )


@lru_cache(maxsize=1)
def escape_audits_are_exact() -> bool:
    """Return whether every advertised finite algebraic identity holds."""

    finite = reference_finite_atom_invisibility_audit()
    curvature = reference_heterogeneous_curvature_synchrony_audit()
    locked = reference_period_locked_escape_audit()
    parity = reference_linear_canard_parity_audit()
    zero_2 = sp.zeros(2, 1)
    zero_33 = sp.zeros(3, 3)
    return bool(
        finite.action_coefficient_matrix == finite.atom_sync_columns
        and finite.universal_invisibility_substitution_action == zero_2
        and finite.third_atom_coefficient_after_first_two_annihilate
        == finite.atom_sync_columns[:, 2]
        and curvature.synchrony_residual != zero_2
        and curvature.homogeneous_synchrony_substitution_residual == zero_2
        and curvature.homogeneous_synchrony_substitution_return == 0
        and balanced_period_locked_escape_audit_is_exact(locked)
        and linear_canard_parity_audit_is_exact(parity)
        and locked.base_scaffold_rank == 3
        and locked.base_scaffold_minus_collective_projection != zero_33
        and locked.base_delay_sum_minus_scaffold != zero_33
        and locked.base_delay_sum_minus_collective_projection != zero_33
    )


@lru_cache(maxsize=1)
def reference_unified_escape_certificate() -> UnifiedEscapeCertificate:
    """Return the strict theorem-status ledger."""

    if not escape_audits_are_exact():
        raise ValueError("the unified escape algebra failed")
    return UnifiedEscapeCertificate(
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        compatibility_result_sha256=COMPATIBILITY_RESULT_SHA256,
        periodic_box_result_sha256=PERIODIC_BOX_RESULT_SHA256,
        balanced_control_chain_result_sha256=BALANCED_CONTROL_CHAIN_RESULT_SHA256,
        autonomous_handoff_result_sha256=AUTONOMOUS_HANDOFF_RESULT_SHA256,
        root_adjoint_gate_result_sha256=ROOT_ADJOINT_GATE_RESULT_SHA256,
        quadratic_carrier_result_sha256=QUADRATIC_CARRIER_RESULT_SHA256,
        heterogeneous_root_doc_sha256=HETEROGENEOUS_ROOT_DOC_SHA256,
        finite_atom_universal_invisibility_is_atomwise_validated=True,
        arbitrary_third_atom_escapes_universal_invisibility_validated=False,
        homogeneous_curvature_sync_forces_existing_return_zero_validated=True,
        balanced_general_topology_carrier_validated=True,
        delay_layers_need_not_sum_to_scaffold_or_projector_validated=True,
        topology_independent_synchronous_periodic_outputs_validated=True,
        period_locked_operator_preserves_synchrony_validated=True,
        period_locked_operator_preserves_constant_histories_validated=True,
        distinguished_periodic_orbit_annihilated_validated=True,
        pure_transverse_variational_action_zero_validated=True,
        normalized_projected_synchronous_first_moment_nonzero_validated=True,
        actual_eta_derivative_epsilon_factor_validated=True,
        actual_projected_synchronous_first_moment_nonzero_validated=True,
        linear_leading_singular_interior_pairing_zero_validated=True,
        nonzero_moment_sufficient_for_nonzero_root_response_validated=False,
        collective_mode_is_simple_canard_critical_direction_validated=False,
        general_topology_stable_history_invertibility_validated=False,
        fixed_event_functionals_policy_independent_validated=True,
        block_triangular_response_identity_validated=True,
        block_response_is_parameter_linked_validated=True,
        trajectory_linked_root_periodic_event_chain_validated=False,
        offsync_direct_forcing_witness_validated=True,
        same_extended_rfde_selected_root_validated=False,
        nonzero_selected_root_eta_response_validated=False,
        common_epsilon_root_and_periodic_regime_validated=False,
        qualitative_three_parameter_periodic_branch_validated=True,
        center_periodic_frequency_amplitude_eta_column_zero_validated=True,
        quantitative_eta_neighborhood_periodic_box_validated=False,
        eta_zero_inert_history_trajectory_embedding_validated=True,
        linear_enlarged_horizon_parameter_coherent_root_preparation_validated=False,
        quadratic_leading_singular_pairing_nonzero_parent_validated=True,
        quadratic_fixed_scaled_support_canonical_root_response_parent_validated=True,
        quadratic_fixed_epsilon_one_fifth_rho_nonzero_validated=False,
        eta_zero_balanced_controlled_voltage_excursions_validated=True,
        eta_neighborhood_balanced_controlled_voltage_excursions_validated=False,
        eta_neighborhood_autonomous_event_crossing_validated=False,
        root_event_zero_set_equivalence_validated=False,
        unforced_onset_validated=False,
        biological_pulse_basin_validated=False,
        no_return_validated=False,
        period_calibration_robustness_validated=False,
        full_network_periodic_attraction_validated=False,
        sparse_local_collective_channel_implementation_validated=False,
    )


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _audit_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [[sp.sstr(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    if isinstance(value, tuple):
        return [_audit_value(item) for item in value]
    return value


def validate_unified_escape_payload(payload: object) -> UnifiedEscapeCertificate:
    """Validate the generated exact audit and reject analytic promotions."""

    root = _mapping(payload, "result payload")
    if set(root) != {"certificate", "exact_audits", "provenance", "scope"}:
        raise ValueError("result payload contains an unpinned section")
    provenance = _mapping(root.get("provenance"), "provenance")
    parents = _mapping(provenance.get("parent_sha256"), "parent_sha256")
    parent_checks = _mapping(
        provenance.get("parent_claim_checks"), "parent_claim_checks"
    )
    certificate_payload = _mapping(root.get("certificate"), "certificate")
    exact_audits = _mapping(root.get("exact_audits"), "exact_audits")
    scope = _mapping(root.get("scope"), "scope")

    expected_provenance_keys = {
        "generator",
        "generator_sha256",
        "proof_source",
        "proof_source_sha256",
        "parent_sha256",
        "parent_claim_checks",
        "argv",
        "default_command",
        "python",
        "platform",
        "arithmetic",
        "distinguished_period_definition",
    }
    if set(provenance) != expected_provenance_keys:
        raise ValueError("provenance contains an unpinned or missing field")
    source_path = Path(__file__).resolve()
    repository = source_path.parents[2]
    generator_path = repository / GENERATOR_RELATIVE_PATH
    expected_bound_provenance = {
        "generator": GENERATOR_RELATIVE_PATH,
        "generator_sha256": sha256(generator_path.read_bytes()).hexdigest(),
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "proof_source_sha256": sha256(source_path.read_bytes()).hexdigest(),
        "default_command": DEFAULT_COMMAND,
        "arithmetic": ARITHMETIC_DESCRIPTION,
        "distinguished_period_definition": DISTINGUISHED_PERIOD_DEFINITION,
    }
    for key, value in expected_bound_provenance.items():
        if provenance.get(key) != value:
            raise ValueError(f"provenance {key} is not source-bound")
    argv = provenance.get("argv")
    if (
        not isinstance(argv, list)
        or len(argv) != 2
        or not isinstance(argv[0], str)
        or not argv[0]
        or argv[1] != GENERATOR_RELATIVE_PATH
    ):
        raise ValueError("provenance argv is not the declared generator call")
    for key in ("python", "platform"):
        if not isinstance(provenance.get(key), str) or not provenance[key]:
            raise ValueError(f"provenance {key} must be a nonempty string")

    expected = reference_unified_escape_certificate()
    expected_certificate = {
        field: getattr(expected, field) for field in expected.__dataclass_fields__
    }
    if dict(certificate_payload) != expected_certificate:
        raise ValueError("certificate does not match the strict escape ledger")
    expected_parents = {
        "compatibility_result": COMPATIBILITY_RESULT_SHA256,
        "periodic_box_result": PERIODIC_BOX_RESULT_SHA256,
        "balanced_control_chain_result": BALANCED_CONTROL_CHAIN_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
        "root_adjoint_gate_result": ROOT_ADJOINT_GATE_RESULT_SHA256,
        "quadratic_carrier_result": QUADRATIC_CARRIER_RESULT_SHA256,
        "heterogeneous_root_doc": HETEROGENEOUS_ROOT_DOC_SHA256,
    }
    if dict(parents) != expected_parents:
        raise ValueError("parent provenance does not match the pinned inputs")
    expected_parent_checks = {
        "parent_refuses_literal_model_identity": True,
        "parent_refuses_existing_three_input_theorem": True,
        "center_periodic_orbit_and_response_validated": True,
        "center_periodic_unique_extrema_validated": True,
        "center_periodic_bordered_inverse_validated": True,
        "balanced_parent_allows_arbitrary_finite_node_count": True,
        "balanced_parent_has_topology_independent_synchronous_restriction": True,
        "balanced_parent_refuses_full_network_periodic_attraction": True,
        "balanced_parent_has_two_controlled_voltage_excursions": True,
        "balanced_parent_refuses_unforced_biological_action_potential": True,
        "handoff_uses_same_baseline_at_eta_zero": True,
        "handoff_has_finite_autonomous_crossings_after_controlled_handoff": True,
        "handoff_refuses_autonomous_onset": True,
        "linear_parent_has_exact_singular_parity_cancellation": True,
        "linear_parent_refuses_moment_only_root_inference": True,
        "linear_parent_refuses_fixed_epsilon_nonzero_rho": True,
        "quadratic_parent_has_nonzero_leading_pairing": True,
        "quadratic_parent_has_canonical_small_delta_root_response": True,
        "quadratic_parent_has_qualitative_periodic_branch": True,
        "quadratic_parent_has_zero_center_periodic_eta_column": True,
        "quadratic_parent_refuses_quantitative_eta_periodic_box": True,
        "quadratic_parent_refuses_fixed_epsilon_nonzero_rho": True,
    }
    if dict(parent_checks) != expected_parent_checks:
        raise ValueError("parent claim checks do not match the pinned inputs")

    expected_audits = {
        "finite_atom": {
            field: _audit_value(
                getattr(reference_finite_atom_invisibility_audit(), field)
            )
            for field in FiniteAtomInvisibilityAudit.__dataclass_fields__
        },
        "heterogeneous_curvature": {
            field: _audit_value(
                getattr(
                    reference_heterogeneous_curvature_synchrony_audit(),
                    field,
                )
            )
            for field in HeterogeneousCurvatureSynchronyAudit.__dataclass_fields__
        },
        "period_locked": {
            field: _audit_value(
                getattr(reference_period_locked_escape_audit(), field)
            )
            for field in PeriodLockedEscapeAudit.__dataclass_fields__
        },
        "linear_canard_parity": {
            field: _audit_value(
                getattr(reference_linear_canard_parity_audit(), field)
            )
            for field in LinearCanardParityAudit.__dataclass_fields__
        },
    }
    if dict(exact_audits) != expected_audits:
        raise ValueError("exact_audits do not match the exact algebra")

    expected_scope = {
        field.removesuffix("_validated"): getattr(expected, field)
        for field in expected.__dataclass_fields__
        if field.endswith("_validated")
    }
    if dict(scope) != expected_scope:
        false_promotions = [
            key
            for key, value in expected_scope.items()
            if value is False and scope.get(key) is True
        ]
        if false_promotions:
            raise ValueError("an analytic or physical claim was promoted")
        raise ValueError("scope contains an unpinned or missing claim")
    return expected


__all__ = [
    "ARITHMETIC_DESCRIPTION",
    "ASSUMPTIONS_ID",
    "AUTONOMOUS_HANDOFF_RESULT_SHA256",
    "BALANCED_CONTROL_CHAIN_RESULT_SHA256",
    "COMPATIBILITY_RESULT_SHA256",
    "DEFAULT_COMMAND",
    "DISTINGUISHED_PERIOD_DEFINITION",
    "FiniteAtomInvisibilityAudit",
    "HETEROGENEOUS_ROOT_DOC_SHA256",
    "HeterogeneousCurvatureSynchronyAudit",
    "LinearCanardParityAudit",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_ID",
    "PERIODIC_BOX_RESULT_SHA256",
    "QUADRATIC_CARRIER_RESULT_SHA256",
    "PeriodLockedEscapeAudit",
    "PROOF_SOURCE_RELATIVE_PATH",
    "ROOT_ADJOINT_GATE_RESULT_SHA256",
    "UnifiedEscapeCertificate",
    "balanced_period_locked_escape_audit",
    "balanced_period_locked_escape_audit_is_exact",
    "escape_audits_are_exact",
    "linear_canard_parity_audit_is_exact",
    "reference_finite_atom_invisibility_audit",
    "reference_heterogeneous_curvature_synchrony_audit",
    "reference_linear_canard_parity_audit",
    "reference_period_locked_escape_audit",
    "reference_unified_escape_certificate",
    "validate_unified_escape_payload",
]
