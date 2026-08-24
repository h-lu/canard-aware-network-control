"""Exact model-fit certificate for a Dobrushin full-network root lift.

The quadratic period-lock theorem first produces a synchronous canonical
selected root.  This module records the exact algebra that promotes that
root to the canonical retained history graph of a genuine arbitrary-finite
balanced topology class.  The promotion uses a common Dobrushin gap for the
instantaneous scaffold and the already-proved dimension-uniform special-flow
history-graph theorem.

The certificate does not validate the root at epsilon=1/5, identify a
physical pulse event, or assert uniqueness among arbitrary RFDE histories
outside the canonical graph tube.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Any, Mapping

import sympy as sp


MODEL_ID = (
    "balanced-dobrushin-dual-scaffold-fhn-"
    "quadratic-period-lock-full-network-canonical-root"
)


@dataclass(frozen=True)
class DobrushinLiftAlgebra:
    """Exact non-rank-one witness and uniform block constants."""

    stationary_row: sp.Matrix
    collective_projector: sp.Matrix
    topology: sp.Matrix
    delay_layer_zero: sp.Matrix
    delay_layer_one: sp.Matrix
    topology_right_balance_residual: sp.Matrix
    topology_left_balance_residual: sp.Matrix
    layer_zero_right_balance_residual: sp.Matrix
    layer_one_right_balance_residual: sp.Matrix
    layer_zero_left_balance_residual: sp.Matrix
    layer_one_left_balance_residual: sp.Matrix
    projector_idempotence_residual: sp.Matrix
    topology_dobrushin_coefficient: sp.Rational
    topology_is_rank_one_projector: bool
    layer_sum_equals_topology: bool
    layer_sum_equals_projector: bool
    transverse_voltage_generator: str
    transverse_recovery_generator: str
    transverse_block_generator: str
    common_semigroup_prefactor: str
    common_semigroup_rate: str
    normalized_delay_layer_operator_bound: str
    quadratic_carrier_transverse_output: sp.Matrix
    quadratic_carrier_cross_term: sp.Expr


@dataclass(frozen=True)
class DobrushinLiftCertificate:
    """Proved/conditional/open ledger for the full-network promotion."""

    model_id: str
    admitted_topology_class: str
    transverse_norm: str
    fold_blowup: str
    transverse_block: str
    semigroup_bound: str
    canonical_root_response: str
    exact_non_rank_one_balanced_witness_validated: bool
    critical_transverse_projectors_uniform_in_dimension: bool
    transverse_block_semigroup_uniformly_exponentially_stable: bool
    balanced_delay_layers_preserve_transverse_space: bool
    balanced_delay_layer_operator_bounds_uniform: bool
    componentwise_polynomial_bounds_uniform: bool
    fixed_support_history_graph_model_fit_proved: bool
    synchronous_zero_transverse_graph_exactly_invariant: bool
    canonical_retained_transverse_graph_unique_and_zero: bool
    full_network_canonical_selected_root_unique_for_admitted_class: bool
    full_network_root_response_topology_independent: bool
    constants_uniform_in_network_size: bool
    arbitrary_balanced_topology_without_mixing_gap_covered: bool
    arbitrary_rfde_history_connection_unique_outside_graph_tube: bool
    fixed_epsilon_one_fifth_root_response_validated: bool
    input_independent_physical_onset_identified: bool
    pulse_quiet_basin_or_no_return_proved: bool


def _dobrushin_coefficient(matrix: sp.Matrix) -> sp.Rational:
    """Return the exact row Dobrushin coefficient of a rational matrix."""

    values: list[sp.Rational] = []
    for row_i in range(matrix.rows):
        for row_j in range(matrix.rows):
            values.append(
                sp.Rational(1, 2)
                * sum(
                    abs(matrix[row_i, column] - matrix[row_j, column])
                    for column in range(matrix.cols)
                )
            )
    return max(values)


def dobrushin_lift_algebra() -> DobrushinLiftAlgebra:
    """Construct an exact non-rank-one member of the admitted class."""

    pi = sp.Matrix([[sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]])
    ones = sp.ones(3, 1)
    projector = ones * pi
    identity = sp.eye(3)

    # Q = theta I + (1-theta) Pi is a transparent exact witness.  The
    # theorem quantifies over every balanced Q with the stated Dobrushin gap;
    # it does not restrict the class to this interpolation family.
    theta = sp.Rational(1, 4)
    topology = theta * identity + (1 - theta) * projector
    layer_zero = topology / 2
    layer_one = projector / 2

    z_now = sp.Matrix([2, -1, 0])
    z_delay = sp.Matrix([-2, 1, 0])
    if (pi * z_now)[0] != 0 or (pi * z_delay)[0] != 0:
        raise RuntimeError("the exact transverse witnesses are not pi-centred")

    x_now, x_delay = sp.symbols("x_now x_delay", real=True)
    transverse_action = sp.simplify(
        projector
        * (
            2 * x_now * z_now
            - 2 * x_delay * z_delay
        )
    )
    # In v=1+delta X 1+delta^2 z, the collective square has no X*z
    # contribution because pi^T z=0.  The first transverse return is z^2.
    cross_term = sp.simplify(2 * x_now * (pi * z_now)[0])

    return DobrushinLiftAlgebra(
        stationary_row=pi,
        collective_projector=projector,
        topology=topology,
        delay_layer_zero=layer_zero,
        delay_layer_one=layer_one,
        topology_right_balance_residual=sp.simplify(topology * ones - ones),
        topology_left_balance_residual=sp.simplify(pi * topology - pi),
        layer_zero_right_balance_residual=sp.simplify(
            layer_zero * ones - ones / 2
        ),
        layer_one_right_balance_residual=sp.simplify(
            layer_one * ones - ones / 2
        ),
        layer_zero_left_balance_residual=sp.simplify(
            pi * layer_zero - pi / 2
        ),
        layer_one_left_balance_residual=sp.simplify(
            pi * layer_one - pi / 2
        ),
        projector_idempotence_residual=sp.simplify(projector**2 - projector),
        topology_dobrushin_coefficient=_dobrushin_coefficient(topology),
        topology_is_rank_one_projector=bool(topology == projector),
        layer_sum_equals_topology=bool(layer_zero + layer_one == topology),
        layer_sum_equals_projector=bool(layer_zero + layer_one == projector),
        transverse_voltage_generator="3*(Q-I)|_E",
        transverse_recovery_generator="2*(Q-I)|_E",
        transverse_block_generator="[[3*(Q-I),0],[I,2*(Q-I)]]|_(E x E)",
        common_semigroup_prefactor="1+1/gamma",
        common_semigroup_rate="2*gamma",
        normalized_delay_layer_operator_bound="||B_j||_(E,osc)<=1/2",
        quadratic_carrier_transverse_output=transverse_action,
        quadratic_carrier_cross_term=cross_term,
    )


def semigroup_constants(gamma: Fraction) -> tuple[Fraction, Fraction]:
    """Return ``M, kappa`` in ``||exp(A t)|| <= M exp(-kappa t)``."""

    if gamma <= 0 or gamma > 1:
        raise ValueError("the Dobrushin gap must lie in (0,1]")
    return Fraction(1, 1) + Fraction(1, 1) / gamma, 2 * gamma


def dobrushin_lift_algebra_is_exact(
    algebra: DobrushinLiftAlgebra | None = None,
) -> bool:
    """Check the exact model-fit identities used by the theorem."""

    if algebra is None:
        algebra = dobrushin_lift_algebra()
    zero_vector = sp.zeros(3, 1)
    zero_row = sp.zeros(1, 3)
    return bool(
        algebra.topology_right_balance_residual == zero_vector
        and algebra.topology_left_balance_residual == zero_row
        and algebra.layer_zero_right_balance_residual == zero_vector
        and algebra.layer_one_right_balance_residual == zero_vector
        and algebra.layer_zero_left_balance_residual == zero_row
        and algebra.layer_one_left_balance_residual == zero_row
        and algebra.projector_idempotence_residual == sp.zeros(3)
        and algebra.topology_dobrushin_coefficient == sp.Rational(1, 4)
        and not algebra.topology_is_rank_one_projector
        and not algebra.layer_sum_equals_topology
        and not algebra.layer_sum_equals_projector
        and algebra.quadratic_carrier_transverse_output == zero_vector
        and algebra.quadratic_carrier_cross_term == 0
    )


def reference_dobrushin_lift_certificate() -> DobrushinLiftCertificate:
    """Return the strict theorem ledger."""

    algebra = dobrushin_lift_algebra()
    if not dobrushin_lift_algebra_is_exact(algebra):
        raise RuntimeError("the Dobrushin full-network model fit did not close")
    return DobrushinLiftCertificate(
        model_id=MODEL_ID,
        admitted_topology_class=(
            "every finite nonnegative balanced Q with tau(Q)<=1-gamma, "
            "gamma>0 common, and balanced half-mass B0,B1"
        ),
        transverse_norm=(
            "max{osc(z),osc(W)} on ker(pi^T) x ker(pi^T)"
        ),
        fold_blowup=(
            "v=1+delta*X*1+delta^2*z; "
            "w=2/3-delta^2*Y*1+delta^4*W"
        ),
        transverse_block=algebra.transverse_block_generator,
        semigroup_bound=(
            "||exp(A_N t)|| <= (1+1/gamma)*exp(-2*gamma*t)"
        ),
        canonical_root_response=(
            "a_c,N(delta,eta)-a_c,N(delta,0)="
            "-(Theta_*/2)*delta^3*eta+"
            "O(delta^4*|eta|+delta^3*eta^2)"
        ),
        exact_non_rank_one_balanced_witness_validated=True,
        critical_transverse_projectors_uniform_in_dimension=True,
        transverse_block_semigroup_uniformly_exponentially_stable=True,
        balanced_delay_layers_preserve_transverse_space=True,
        balanced_delay_layer_operator_bounds_uniform=True,
        componentwise_polynomial_bounds_uniform=True,
        fixed_support_history_graph_model_fit_proved=True,
        synchronous_zero_transverse_graph_exactly_invariant=True,
        canonical_retained_transverse_graph_unique_and_zero=True,
        full_network_canonical_selected_root_unique_for_admitted_class=True,
        full_network_root_response_topology_independent=True,
        constants_uniform_in_network_size=True,
        arbitrary_balanced_topology_without_mixing_gap_covered=False,
        arbitrary_rfde_history_connection_unique_outside_graph_tube=False,
        fixed_epsilon_one_fifth_root_response_validated=False,
        input_independent_physical_onset_identified=False,
        pulse_quiet_basin_or_no_return_proved=False,
    )


def reference_dobrushin_lift_payload() -> dict[str, Any]:
    """Serialize exact witness data and the strict theorem scope."""

    algebra = dobrushin_lift_algebra()
    certificate = reference_dobrushin_lift_certificate()
    return {
        "certificate": asdict(certificate),
        "exact_witness": {
            "stationary_row": [str(value) for value in algebra.stationary_row],
            "topology": [
                [str(algebra.topology[i, j]) for j in range(3)]
                for i in range(3)
            ],
            "delay_layer_zero": [
                [str(algebra.delay_layer_zero[i, j]) for j in range(3)]
                for i in range(3)
            ],
            "delay_layer_one": [
                [str(algebra.delay_layer_one[i, j]) for j in range(3)]
                for i in range(3)
            ],
            "dobrushin_coefficient": str(
                algebra.topology_dobrushin_coefficient
            ),
            "non_rank_one": not algebra.topology_is_rank_one_projector,
            "layer_sum_differs_from_topology": (
                not algebra.layer_sum_equals_topology
            ),
            "layer_sum_differs_from_projector": (
                not algebra.layer_sum_equals_projector
            ),
        },
        "scope": {
            "uniform_dobrushin_full_network_canonical_root": True,
            "arbitrary_balanced_without_gap": False,
            "arbitrary_history_global_uniqueness": False,
            "fixed_epsilon_one_fifth": False,
            "physical_onset": False,
            "biological_basin_no_return": False,
        },
    }


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def validate_dobrushin_lift_payload(payload: Mapping[str, Any]) -> None:
    """Reject any serialized promotion beyond the proved theorem."""

    expected = reference_dobrushin_lift_payload()
    if dict(_mapping(payload.get("certificate"), "certificate")) != expected[
        "certificate"
    ]:
        raise ValueError("the certificate does not match the proved theorem")
    if dict(_mapping(payload.get("exact_witness"), "exact witness")) != expected[
        "exact_witness"
    ]:
        raise ValueError("the exact witness changed")
    if dict(_mapping(payload.get("scope"), "scope")) != expected["scope"]:
        raise ValueError("the scope does not match the proved theorem")
