from __future__ import annotations

import numpy as np
import pytest
import sympy as sp
from scipy.linalg import expm

from canard_control.lifted_network_blowup import (
    fixed_two_atom_evaluation_audit,
    lifted_network_blowup_audit,
)
from canard_control.lifted_two_module_network import (
    matrix_infinity_operator_norm,
)
from canard_control.nonlocal_graph_jet import nonlocal_graph_jet_audit


@pytest.fixture(scope="module")
def unequal_audit():
    return lifted_network_blowup_audit(
        1,
        2,
        within_voltage_rate=sp.Rational(3, 2),
        recovery_rate=sp.Rational(5, 2),
    )


@pytest.fixture(scope="module")
def base_audit():
    return lifted_network_blowup_audit(
        1,
        1,
        within_voltage_rate=sp.Rational(3, 2),
        recovery_rate=sp.Rational(5, 2),
    )


def test_exact_full_fiber_blowup_and_delta_divisibility(unequal_audit) -> None:
    audit = unequal_audit
    assert audit.physical_fast_scaling_remainder.is_zero_matrix
    assert audit.physical_slow_scaling_remainder.is_zero_matrix
    assert audit.center_divisibility_remainder.is_zero_matrix
    assert audit.stable_divisibility_remainder.is_zero_matrix
    assert audit.fast_reconstruction_residual.is_zero_matrix
    assert audit.slow_reconstruction_residual.is_zero_matrix
    assert audit.center_rhs[1] == -audit.critical_x + (
        audit.delta * audit.unfolding
    )

    node_count = audit.network.node_count
    transverse = sp.Matrix(audit.network.transverse_projector)
    for stable_vector in (
        audit.shifted_voltage,
        audit.shifted_recovery,
        audit.delayed_shifted_voltage_0,
        audit.delayed_shifted_voltage_1,
    ):
        assert transverse * stable_vector == stable_vector
    assert audit.stable_state_projector * audit.stable_generator == (
        audit.stable_generator * audit.stable_state_projector
    )
    assert audit.stable_state_projector.shape == (
        2 * node_count,
        2 * node_count,
    )


def test_projection_invisible_module_channel_enters_only_stable_G_at_delta_zero(
    unequal_audit,
) -> None:
    audit = unequal_audit
    node_count = audit.network.node_count
    stable_symbols = set()
    for vector in (
        audit.shifted_voltage,
        audit.shifted_recovery,
        audit.delayed_shifted_voltage_0,
        audit.delayed_shifted_voltage_1,
    ):
        stable_symbols.update(vector.free_symbols)
    zero_stable = {symbol: 0 for symbol in stable_symbols}

    center_eta_source = sp.simplify(
        audit.center_remainder.diff(audit.module_redistribution)
        .subs(audit.delta, 0)
        .subs(zero_stable)
    )
    stable_eta_source = sp.simplify(
        audit.stable_remainder.diff(audit.module_redistribution)
        .subs(audit.delta, 0)
        .subs(zero_stable)
    )
    expected_voltage_source = (
        -audit.weak_gain
        * sp.Matrix(audit.network.module_transverse_right_lift)
        * (audit.delayed_x_0 - audit.delayed_x_1)
    )

    assert center_eta_source.is_zero_matrix
    assert sp.simplify(
        stable_eta_source[:node_count, :] - expected_voltage_source
    ).is_zero_matrix
    assert stable_eta_source[node_count:, :].is_zero_matrix


def test_block_constant_restriction_is_the_existing_two_module_shifted_chart(
    base_audit,
) -> None:
    audit = base_audit
    base = nonlocal_graph_jet_audit()
    scalar_u, scalar_v, scalar_u_0, scalar_u_1 = sp.symbols(
        "UU VV UU0 UU1", real=True
    )
    q = sp.Matrix(audit.network.module_transverse_right_lift)
    value_by_name = {
        "U0": q[0] * scalar_u,
        "U1": q[1] * scalar_u,
        "V0": q[0] * scalar_v,
        "V1": q[1] * scalar_v,
        "Utheta0_0": q[0] * scalar_u_0,
        "Utheta0_1": q[1] * scalar_u_0,
        "Utheta1_0": q[0] * scalar_u_1,
        "Utheta1_1": q[1] * scalar_u_1,
    }
    symbols = set(audit.center_rhs.free_symbols)
    symbols.update(audit.shifted_stable_rhs.free_symbols)
    lift_substitution = {
        symbol: value_by_name[str(symbol)]
        for symbol in symbols
        if str(symbol) in value_by_name
    }
    base_substitution = {
        scalar_u: base.shifted_voltage,
        scalar_v: base.shifted_recovery,
        scalar_u_0: sp.Symbol("U_theta_0", real=True),
        scalar_u_1: sp.Symbol("U_theta_1", real=True),
        base.recovery_gap: sp.Rational(5, 2),
    }

    restricted_center = sp.simplify(
        audit.center_rhs[0]
        .subs(lift_substitution)
        .subs(base_substitution)
    )
    restricted_voltage = sp.simplify(
        audit.shifted_stable_rhs[:2, :]
        .subs(lift_substitution)
        .subs(base_substitution)
    )
    restricted_recovery = sp.simplify(
        audit.shifted_stable_rhs[2:, :]
        .subs(lift_substitution)
        .subs(base_substitution)
    )

    assert sp.simplify(
        restricted_center
        - base.shifted_critical_rhs.subs(base_substitution)
    ) == 0
    assert sp.simplify(
        restricted_voltage
        - q * base.shifted_delta_voltage_rhs.subs(base_substitution)
    ).is_zero_matrix
    assert sp.simplify(
        restricted_recovery
        - q * base.shifted_delta_recovery_rhs.subs(base_substitution)
    ).is_zero_matrix


def test_shifted_stable_generator_has_dimension_uniform_max_norm_bound(
    unequal_audit,
) -> None:
    audit = unequal_audit
    generator = np.asarray(audit.stable_generator, dtype=float)
    projector = np.asarray(audit.stable_state_projector, dtype=float)
    minimum_rate = min(
        2.0,
        float(audit.network.within_voltage_rate),
        float(audit.network.recovery_rate),
    )
    projector_sum = 3.5

    for time in (0.0, 0.1, 0.5, 1.0, 3.0, 8.0):
        restricted_semigroup = expm(generator * time) @ projector
        induced_norm = np.linalg.norm(restricted_semigroup, ord=np.inf)
        bound = projector_sum * (1.0 + time) * np.exp(
            -minimum_rate * time
        )
        assert induced_norm <= bound + 1.0e-12


def test_fixed_two_atom_evaluation_has_dimension_free_operator_tv(
    unequal_audit,
) -> None:
    atom_audit = fixed_two_atom_evaluation_audit(unequal_audit.network)
    assert matrix_infinity_operator_norm(atom_audit.atom_0_injection) == 1
    assert matrix_infinity_operator_norm(atom_audit.atom_1_injection) == 1
    assert atom_audit.atom_norms == (1, 1)
    assert atom_audit.operator_total_variation == 2
    assert atom_audit.parameter_derivative_total_variation == 0
