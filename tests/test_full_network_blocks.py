from __future__ import annotations

import sympy as sp

from canard_control.full_network_blocks import (
    audit_source_history_layers,
    fast_voltage_jacobian,
    full_fold_jacobian,
    two_module_block_algebra,
    uniform_history_layer,
)
from canard_control.reference_fhn import block_averaging_matrix


def test_weighted_projectors_resolve_collective_difference_and_within_modes() -> None:
    algebra = two_module_block_algebra(2, 3)
    node_count = algebra.node_count
    identity = sp.eye(node_count)
    modal_inverse = algebra.modal_basis.inv()

    assert algebra.module_average * algebra.embedding == sp.eye(2)
    assert algebra.module_projector**2 == algebra.module_projector
    assert algebra.collective_projector**2 == algebra.collective_projector
    assert algebra.collective_projector == block_averaging_matrix(2, 3)
    assert (
        algebra.module_metric * algebra.module_collective_projector
        == algebra.module_collective_projector.T * algebra.module_metric
    )
    assert (
        algebra.node_metric * algebra.collective_projector
        == algebra.collective_projector.T * algebra.node_metric
    )
    assert algebra.module_average * algebra.module_difference_vector == sp.Matrix(
        [1, -1]
    )
    assert algebra.modal_basis.det() != 0

    collective_coordinates = (
        modal_inverse * algebra.collective_projector * algebra.modal_basis
    )
    module_coordinates = (
        modal_inverse * algebra.module_projector * algebra.modal_basis
    )
    assert collective_coordinates == sp.diag(1, 0, 0, 0, 0)
    assert module_coordinates == sp.diag(1, 1, 0, 0, 0)
    assert (
        algebra.collective_projector
        + (algebra.module_projector - algebra.collective_projector)
        + (identity - algebra.module_projector)
        == identity
    )


def test_fixed_collective_averaging_scaffold_has_one_zero_mode() -> None:
    algebra = two_module_block_algebra(2, 3)
    node_count = algebra.node_count
    coupling = sp.symbols("D", nonzero=True)
    voltage = fast_voltage_jacobian(algebra, coupling)
    modal_voltage = sp.simplify(
        algebra.modal_basis.inv() * voltage * algebra.modal_basis
    )

    assert modal_voltage == sp.diag(0, *([-coupling] * (node_count - 1)))
    spectral_parameter = sp.symbols("z")
    assert sp.factor(voltage.charpoly(spectral_parameter).as_expr()) == (
        spectral_parameter * (spectral_parameter + coupling) ** (node_count - 1)
    )


def test_epsilon_zero_full_fold_has_generalized_center_dimension_n_plus_one() -> None:
    algebra = two_module_block_algebra(2, 3)
    node_count = algebra.node_count
    coupling = sp.Integer(2)
    jacobian = full_fold_jacobian(algebra, coupling)
    spectral_parameter = sp.symbols("z")

    assert sp.factor(jacobian.charpoly(spectral_parameter).as_expr()) == (
        spectral_parameter ** (node_count + 1)
        * (spectral_parameter + coupling) ** (node_count - 1)
    )
    assert 2 * node_count - jacobian.rank() == node_count
    assert 2 * node_count - (jacobian**2).rank() == node_count + 1


def test_candidate_recovery_scaffold_leaves_only_collective_jordan_center() -> None:
    algebra = two_module_block_algebra(2, 3)
    node_count = algebra.node_count
    coupling = sp.symbols("D", positive=True)
    recovery = sp.symbols("E", positive=True)
    spectral_parameter = sp.symbols("z")
    jacobian = full_fold_jacobian(
        algebra,
        coupling,
        recovery_coupling=recovery,
    )

    assert sp.factor(jacobian.charpoly(spectral_parameter).as_expr()) == (
        spectral_parameter**2
        * (spectral_parameter + coupling) ** (node_count - 1)
        * (spectral_parameter + recovery) ** (node_count - 1)
    )

    state_modal_basis = sp.diag(algebra.modal_basis, algebra.modal_basis)
    modal_jacobian = sp.simplify(
        state_modal_basis.inv() * jacobian * state_modal_basis
    )
    assert modal_jacobian.extract([0, node_count], [0, node_count]) == sp.Matrix(
        [[0, -1], [0, 0]]
    )
    for mode in range(1, node_count):
        indices = [mode, node_count + mode]
        assert modal_jacobian.extract(indices, indices) == sp.Matrix(
            [[-coupling, -1], [0, -recovery]]
        )

    # Exact finite-dimensional center audit for one fixed positive pair.
    numeric_jacobian = full_fold_jacobian(
        algebra,
        sp.Integer(2),
        recovery_coupling=sp.Integer(3),
    )
    assert 2 * node_count - numeric_jacobian.rank() == 1
    assert 2 * node_count - (numeric_jacobian**2).rank() == 2


def test_two_delay_source_history_lift_restricts_exactly_to_declared_layers() -> None:
    algebra = two_module_block_algebra(2, 3)
    c_0 = sp.Matrix(
        [
            [sp.Rational(1, 2), sp.Rational(1, 3)],
            [sp.Rational(2, 5), sp.Rational(3, 7)],
        ]
    )
    c_1 = sp.Matrix(
        [
            [sp.Rational(1, 4), sp.Rational(2, 9)],
            [sp.Rational(3, 8), sp.Rational(1, 6)],
        ]
    )
    a_0 = uniform_history_layer(algebra, c_0)
    a_1 = uniform_history_layer(algebra, c_1)
    audit = audit_source_history_layers(algebra, (a_0, a_1), (c_0, c_1))

    assert audit.restrictions == (c_0, c_1)
    assert all(residual.is_zero_matrix for residual in audit.restriction_mismatches)
    assert all(residual.is_zero_matrix for residual in audit.declared_row_residuals)
    assert all(forcing.is_zero_matrix for forcing in audit.transverse_forcing)
    assert audit.eta_squared == 0

    z_0 = sp.Matrix(sp.symbols("z00 z01"))
    z_1 = sp.Matrix(sp.symbols("z10 z11"))
    full_history_lift = (
        a_0 * algebra.embedding * z_0
        + a_1 * algebra.embedding * z_1
    )
    reduced_history_lift = algebra.embedding * (c_0 * z_0 + c_1 * z_1)
    assert full_history_lift == reduced_history_lift


def test_eta_exposes_transverse_row_failure_in_a_two_delay_layer() -> None:
    algebra = two_module_block_algebra(2, 2)
    eta = sp.symbols("eta", real=True)
    c_0 = sp.Matrix([[1, 2], [3, 4]])
    c_1 = sp.Matrix([[5, 6], [7, 8]])
    a_0 = sp.Matrix(uniform_history_layer(algebra, c_0))
    a_1 = uniform_history_layer(algebra, c_1)

    # Opposite receiving-row perturbations retain the 2-by-2 averaged
    # restriction but violate rowwise closure and force a within-module mode.
    a_0[0, 0] += eta
    a_0[1, 0] -= eta
    audit = audit_source_history_layers(algebra, (a_0, a_1), (c_0, c_1))

    expected_forcing_0 = sp.Matrix(
        [
            [eta, 0],
            [-eta, 0],
            [0, 0],
            [0, 0],
        ]
    )
    assert audit.restrictions == (c_0, c_1)
    assert all(mismatch.is_zero_matrix for mismatch in audit.restriction_mismatches)
    assert audit.transverse_forcing[0] == expected_forcing_0
    assert audit.transverse_forcing[1].is_zero_matrix
    assert audit.declared_row_residuals[0] == expected_forcing_0
    assert audit.eta_squared == 2 * eta**2

    z_0 = sp.Matrix(sp.symbols("z00 z01"))
    z_1 = sp.Matrix(sp.symbols("z10 z11"))
    exact_full_lift = (
        a_0 * algebra.embedding * z_0
        + a_1 * algebra.embedding * z_1
    )
    declared_module_lift_plus_eta = (
        algebra.embedding * (c_0 * z_0 + c_1 * z_1)
        + audit.declared_row_residuals[0] * z_0
        + audit.declared_row_residuals[1] * z_1
    )
    assert sp.simplify(
        exact_full_lift - declared_module_lift_plus_eta
    ) == sp.zeros(algebra.node_count, 1)
