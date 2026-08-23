from __future__ import annotations

import numpy as np
import pytest
import sympy as sp
from scipy.linalg import expm

from canard_control.lifted_two_module_network import (
    audit_atomic_delay_residual,
    equitability_breaking_redistribution,
    lifted_fast_field,
    lifted_final_two_module_network,
    lifted_recovery_slow_field,
    matrix_infinity_operator_norm,
    max_norm_lifted_delay_audit,
    max_norm_local_jet_audit,
    max_norm_projection_audit,
    max_norm_transverse_semigroup_certificate,
    transverse_semigroup_certificate,
    weighted_frobenius_squared,
)


@pytest.mark.parametrize("n1,n2", [(1, 1), (2, 3), (4, 7)])
def test_replication_averaging_and_weighted_orthogonal_split(
    n1: int,
    n2: int,
) -> None:
    network = lifted_final_two_module_network(n1, n2)
    identity = sp.eye(network.node_count)

    assert network.module_average * network.embedding == sp.eye(2)
    assert (
        network.embedding.T * network.node_metric
        == network.module_metric * network.module_average
    )
    assert network.module_projector**2 == network.module_projector
    assert network.critical_projector**2 == network.critical_projector
    assert (
        network.module_transverse_projector**2
        == network.module_transverse_projector
    )
    assert network.within_projector**2 == network.within_projector
    assert (
        network.critical_projector
        + network.module_transverse_projector
        + network.within_projector
        == identity
    )
    assert (
        network.node_metric * network.critical_projector
        == network.critical_projector.T * network.node_metric
    )
    assert (
        network.node_metric * network.module_transverse_projector
        == network.module_transverse_projector.T * network.node_metric
    )
    assert (
        network.node_metric * network.within_projector
        == network.within_projector.T * network.node_metric
    )
    assert (
        network.critical_right.T
        * network.node_metric
        * network.critical_right
        == sp.ones(1, 1)
    )
    assert (
        network.module_transverse_right_lift.T
        * network.node_metric
        * network.module_transverse_right_lift
        == sp.ones(1, 1)
    )
    assert (
        network.critical_right.T
        * network.node_metric
        * network.module_transverse_right_lift
        == sp.zeros(1, 1)
    )


@pytest.mark.parametrize("n1,n2", [(1, 1), (2, 3), (4, 7), (17, 5)])
def test_max_norm_projection_constants_are_dimension_uniform(
    n1: int,
    n2: int,
) -> None:
    network = lifted_final_two_module_network(n1, n2)
    audit = max_norm_projection_audit(network)

    assert audit.embedding_norm == 1
    assert audit.module_average_norm == 1
    assert audit.module_projector_norm == 1
    assert audit.critical_projector_norm == sp.Rational(3, 2)
    assert audit.module_transverse_projector_norm == sp.Rational(3, 2)
    assert audit.within_projector_norm == max(
        2 * (1 - sp.Rational(1, n1)),
        2 * (1 - sp.Rational(1, n2)),
    )
    assert audit.transverse_projector_norm == max(
        sp.Rational(7, 4) - sp.Rational(1, n1),
        sp.Rational(5, 2) - sp.Rational(1, n2),
    )
    assert audit.within_projector_norm <= audit.uniform_within_projector_bound
    assert (
        audit.transverse_projector_norm
        <= audit.uniform_transverse_projector_bound
    )
    assert audit.critical_injection_norm == 2
    assert audit.critical_extraction_norm == sp.Rational(3, 4)
    assert audit.module_transverse_injection_norm == 2
    assert audit.module_transverse_extraction_norm == sp.Rational(3, 4)
    assert audit.uniform_coordinate_extraction_bound == sp.Rational(5, 2)
    assert audit.uniform_coordinate_reconstruction_bound == 3


def test_lift_preserves_simple_fold_module_layers_and_module_return_channel() -> None:
    eta = sp.Symbol("eta", real=True)
    voltage_rate = sp.Symbol("D_v", positive=True)
    recovery_rate = sp.Symbol("D_w", positive=True)
    network = lifted_final_two_module_network(
        2,
        3,
        within_voltage_rate=voltage_rate,
        recovery_rate=recovery_rate,
        module_redistribution=eta,
    )
    node_count = network.node_count

    assert (
        network.fast_voltage_jacobian
        == -2 * network.module_transverse_projector
        - voltage_rate * network.within_projector
    )
    assert (
        network.recovery_jacobian
        == -recovery_rate * network.transverse_projector
    )
    assert (
        network.module_average
        * network.fast_voltage_jacobian
        * network.embedding
        == network.base_fast_jacobian
    )
    assert (
        network.fast_voltage_jacobian * network.critical_right
        == sp.zeros(node_count, 1)
    )
    assert (
        network.critical_left.T * network.fast_voltage_jacobian
        == sp.zeros(1, node_count)
    )
    assert network.fold_curvature == -sp.sqrt(sp.Rational(3, 2))

    assert network.layer_0 + network.layer_1 == network.total_layer
    assert (
        network.module_average * network.layer_0 * network.embedding
        == network.module_layer_0
    )
    assert network.layer_0 * network.embedding == (
        network.embedding * network.module_layer_0
    )
    assert (
        network.critical_left.T
        * network.layer_0
        * network.critical_right
        == sp.Matrix([[sp.Rational(1, 3)]])
    )
    assert (
        network.critical_left.T
        * network.layer_1
        * network.critical_right
        == sp.Matrix([[sp.Rational(2, 3)]])
    )

    # This is the lifted module-difference mechanism from the proved base
    # model.  It is distinct from the within-module equitability breaker.
    module_direction_lift = network.layer_0.diff(eta)
    assert (
        module_direction_lift * network.critical_right
        == network.module_transverse_right_lift
    )
    assert (
        network.critical_left.T
        * module_direction_lift
        * network.critical_right
        == sp.zeros(1, 1)
    )

    zero_eigenvector = sp.Matrix.vstack(
        network.critical_right, sp.zeros(node_count, 1)
    )
    generalized_vector = sp.Matrix.vstack(
        sp.zeros(node_count, 1), -network.critical_right
    )
    assert network.singular_jacobian * zero_eigenvector == sp.zeros(
        2 * node_count, 1
    )
    assert (
        network.singular_jacobian * generalized_vector
        == zero_eigenvector
    )


def test_nodewise_nonlinear_field_restricts_exactly_and_has_declared_fold_jet() -> None:
    network = lifted_final_two_module_network(
        2,
        3,
        within_voltage_rate=sp.Rational(7, 4),
    )
    node_count = network.node_count
    voltage_symbols = sp.Matrix(sp.symbols(f"v0:{node_count}"))
    recovery_symbols = sp.Matrix(sp.symbols(f"w0:{node_count}"))
    fast_field = lifted_fast_field(
        network, voltage_symbols, recovery_symbols
    )
    equilibrium_substitution = {
        **dict(zip(voltage_symbols, network.equilibrium_voltage, strict=True)),
        **dict(zip(recovery_symbols, network.equilibrium_recovery, strict=True)),
    }
    assert fast_field.subs(equilibrium_substitution) == sp.zeros(node_count, 1)
    assert (
        fast_field.jacobian(voltage_symbols).subs(equilibrium_substitution)
        == network.fast_voltage_jacobian
    )
    assert fast_field.jacobian(recovery_symbols) == -sp.eye(node_count)

    z_1, z_2, y_1, y_2 = sp.symbols("z_1 z_2 y_1 y_2")
    module_voltage = sp.Matrix([z_1, z_2])
    module_recovery = sp.Matrix([y_1, y_2])
    restricted = lifted_fast_field(
        network,
        network.embedding * module_voltage,
        network.embedding * module_recovery,
    )
    base_field = sp.Matrix(
        [
            z_1 - z_1**3 / 3 - y_1 + (z_2 - z_1) / 2,
            z_2 - z_2**3 / 3 - y_2 + 2 * (z_1 - z_2),
        ]
    )
    assert restricted == network.embedding * base_field

    x, mu = sp.symbols("X mu")
    slow_on_critical_line = lifted_recovery_slow_field(
        network,
        network.equilibrium_voltage + network.critical_right * x,
        mu,
    )
    assert slow_on_critical_line == network.critical_right * (x - mu)


@pytest.mark.parametrize("n1,n2", [(1, 1), (2, 3), (5, 8)])
def test_dimension_independent_transverse_semigroup_bound(
    n1: int,
    n2: int,
) -> None:
    network = lifted_final_two_module_network(
        n1,
        n2,
        within_voltage_rate=sp.Rational(3, 2),
        recovery_rate=sp.Rational(5, 2),
    )
    certificate = transverse_semigroup_certificate(network)
    assert certificate.minimum_rate == sp.Rational(3, 2)
    assert certificate.decay_rate == sp.Rational(3, 4)
    assert certificate.multiplicative_constant == 1 + 4 / (3 * sp.E)

    jacobian = np.asarray(network.singular_jacobian, dtype=float)
    transverse = np.asarray(network.state_transverse_projector, dtype=float)
    node_metric = np.asarray(network.node_metric, dtype=float)
    state_metric = np.block(
        [
            [node_metric, np.zeros_like(node_metric)],
            [np.zeros_like(node_metric), node_metric],
        ]
    )
    square_root = np.diag(np.sqrt(np.diag(state_metric)))
    inverse_square_root = np.diag(1.0 / np.sqrt(np.diag(state_metric)))
    decay = float(certificate.decay_rate)
    multiplier = float(certificate.multiplicative_constant)

    for time in (0.0, 0.1, 0.5, 1.0, 3.0, 8.0):
        restricted_semigroup = expm(jacobian * time) @ transverse
        weighted = square_root @ restricted_semigroup @ inverse_square_root
        induced_norm = np.linalg.svd(weighted, compute_uv=False)[0]
        assert induced_norm <= multiplier * np.exp(-decay * time) + 1.0e-12


@pytest.mark.parametrize("n1,n2", [(1, 1), (2, 3), (5, 8), (13, 4)])
def test_dimension_independent_max_norm_transverse_semigroup_bound(
    n1: int,
    n2: int,
) -> None:
    network = lifted_final_two_module_network(
        n1,
        n2,
        within_voltage_rate=sp.Rational(3, 2),
        recovery_rate=sp.Rational(5, 2),
    )
    certificate = max_norm_transverse_semigroup_certificate(network)
    assert certificate.minimum_rate == sp.Rational(3, 2)
    assert certificate.decay_rate == sp.Rational(3, 4)
    assert certificate.projector_sum_bound == sp.Rational(7, 2)
    assert certificate.multiplicative_constant == sp.Rational(7, 2) * (
        1 + 4 / (3 * sp.E)
    )

    jacobian = np.asarray(network.singular_jacobian, dtype=float)
    transverse = np.asarray(network.state_transverse_projector, dtype=float)
    decay = float(certificate.decay_rate)
    multiplier = float(certificate.multiplicative_constant)
    for time in (0.0, 0.1, 0.5, 1.0, 3.0, 8.0):
        restricted_semigroup = expm(jacobian * time) @ transverse
        induced_norm = np.linalg.norm(restricted_semigroup, ord=np.inf)
        assert induced_norm <= multiplier * np.exp(-decay * time) + 1.0e-12


@pytest.mark.parametrize("n1,n2", [(1, 1), (2, 3), (6, 11)])
def test_local_cubic_jets_have_fixed_max_norm_bounds(
    n1: int,
    n2: int,
) -> None:
    network = lifted_final_two_module_network(
        n1,
        n2,
        within_voltage_rate=sp.Rational(7, 4),
    )
    audit = max_norm_local_jet_audit(
        network,
        voltage_box_radius=sp.Rational(1, 2),
        recovery_box_radius=sp.Rational(1, 3),
        unfolding_box_radius=sp.Rational(1, 5),
    )
    absolute_voltage = sp.sqrt(sp.Rational(3, 2)) + sp.Rational(1, 2)
    assert audit.absolute_voltage_bound == absolute_voltage
    assert sp.simplify(
        audit.fast_jet_bounds[1]
        - (6 + absolute_voltage**2 + sp.Rational(3, 2))
    ) == 0
    assert audit.fast_jet_bounds[2] == 2 * absolute_voltage
    assert audit.fast_jet_bounds[3] == 2
    assert all(bound == 0 for bound in audit.fast_jet_bounds[4:])
    assert audit.slow_jet_bounds[:2] == (sp.Rational(9, 10), 3)
    assert all(bound == 0 for bound in audit.slow_jet_bounds[2:])

    # Check the zeroth- and first-order estimates at a box corner.  The
    # higher-order bounds are exact diagonal-cubic derivative formulas.
    voltage = network.equilibrium_voltage + sp.ones(network.node_count, 1) / 2
    recovery = network.equilibrium_recovery - sp.ones(network.node_count, 1) / 3
    field = lifted_fast_field(network, voltage, recovery)
    assert matrix_infinity_operator_norm(field) <= audit.fast_jet_bounds[0]

    voltage_symbols = sp.Matrix(sp.symbols(f"x0:{network.node_count}"))
    recovery_symbols = sp.Matrix(sp.symbols(f"y0:{network.node_count}"))
    symbolic_field = lifted_fast_field(
        network, voltage_symbols, recovery_symbols
    )
    state_symbols = voltage_symbols.col_join(recovery_symbols)
    jacobian = symbolic_field.jacobian(state_symbols).subs(
        dict(zip(voltage_symbols, voltage, strict=True))
    )
    assert (
        matrix_infinity_operator_norm(jacobian)
        <= audit.fast_jet_bounds[1]
    )


@pytest.mark.parametrize("n1,n2", [(1, 1), (2, 3), (7, 12)])
def test_equitable_lifted_layers_have_uniform_max_norm_tv(
    n1: int,
    n2: int,
) -> None:
    network = lifted_final_two_module_network(n1, n2)
    audit = max_norm_lifted_delay_audit(network)
    assert audit.module_layer_norms == (
        sp.Rational(5, 12),
        sp.Rational(11, 12),
    )
    assert audit.lifted_layer_norms == audit.module_layer_norms
    assert audit.module_total_layer_norm == sp.Rational(4, 3)
    assert audit.lifted_total_layer_norm == sp.Rational(4, 3)
    assert audit.delayed_operator_tv == sp.Rational(4, 3)
    assert audit.balanced_feedback_bound == sp.Rational(8, 3)


def test_projection_invisible_small_residual_breaks_equitability() -> None:
    amplitude = sp.Symbol("rho", positive=True)
    network = lifted_final_two_module_network(2, 3)
    breaker = equitability_breaking_redistribution(
        network,
        amplitude,
        receiving_module=2,
        source_module=1,
    )
    audit = audit_atomic_delay_residual(
        network,
        (breaker.residual_layer_0, breaker.residual_layer_1),
        (sp.Rational(1, 2), sp.Integer(1)),
    )

    assert breaker.generator.rank() == 1
    assert weighted_frobenius_squared(
        breaker.generator, network.node_metric
    ) == 1
    assert breaker.exact_layer_weighted_operator_norm == amplitude
    assert breaker.exact_operator_tv_weighted == 2 * amplitude
    assert all(value.is_zero_matrix for value in audit.module_restrictions)
    assert all(
        value.is_zero_matrix for value in audit.average_output_residuals
    )
    assert all(
        value.is_zero_matrix for value in audit.critical_output_residuals
    )
    assert audit.total_layer_residual.is_zero_matrix
    assert not audit.equitability_residuals[0].is_zero_matrix
    assert not audit.equitability_residuals[1].is_zero_matrix
    assert audit.operator_tv_frobenius_upper == 2 * amplitude
    assert audit.balanced_feedback_frobenius_upper == 2 * amplitude
    assert (
        audit.operator_tv_infinity_upper
        == breaker.exact_operator_tv_infinity
    )
    assert audit.balanced_feedback_infinity_upper == (
        breaker.exact_operator_tv_infinity
    )
    assert breaker.receiving_pattern == "distributed"
    assert breaker.affected_entry_symmetric_radius == 1 / (
        12 * sp.sqrt(2)
    )
    assert breaker.dimension_uniform_affected_radius_lower_bound == 1 / (
        12 * sp.sqrt(2)
    )
    assert breaker.unaffected_base_positivity_status is True
    assert breaker.all_base_positivity_status is True
    assert breaker.certified_full_positivity_radius == 1 / (12 * sp.sqrt(2))
    assert breaker.dimension_uniform_infinity_generator_bound == 2 * sp.sqrt(2)

    # The residual is arbitrarily small in operator TV, but every nonzero
    # amplitude breaks rowwise module closure.  No nonzero canard coefficient
    # is inferred for this within-module zero-average direction.
    assert (
        breaker.generator * network.embedding
        != sp.zeros(network.node_count, 2)
    )


def test_finite_size_positivity_margin_and_singleton_obstruction() -> None:
    network = lifted_final_two_module_network(2, 3)
    unit_breaker = equitability_breaking_redistribution(
        network,
        sp.Integer(1),
        receiving_module=2,
        source_module=1,
    )
    sample_amplitude = unit_breaker.certified_full_positivity_radius / 2
    breaker = equitability_breaking_redistribution(
        network,
        sample_amplitude,
        receiving_module=2,
        source_module=1,
    )
    for layer in (
        sp.Matrix(network.layer_0 + breaker.residual_layer_0),
        sp.Matrix(network.layer_1 + breaker.residual_layer_1),
    ):
        assert all(bool(entry > 0) for entry in layer)

    singleton_network = lifted_final_two_module_network(1, 1)
    with pytest.raises(ValueError, match="at least two nodes"):
        equitability_breaking_redistribution(singleton_network, sp.Symbol("a"))


@pytest.mark.parametrize("receiving_size", [2, 3, 4, 9, 32])
def test_distributed_breaker_has_uniform_positive_layer_margin(
    receiving_size: int,
) -> None:
    network = lifted_final_two_module_network(2, receiving_size)
    breaker = equitability_breaking_redistribution(
        network,
        sp.Integer(1),
        receiving_module=2,
        source_module=1,
    )
    expected_lower_bound = 1 / (12 * sp.sqrt(2))
    assert (
        sp.simplify(
            breaker.certified_full_positivity_radius
            - expected_lower_bound
        )
        >= 0
    )
    assert (
        breaker.certified_dimension_uniform_full_positivity_lower_bound
        == expected_lower_bound
    )
    generator_norm = matrix_infinity_operator_norm(breaker.generator)
    positive_count = receiving_size // 2
    expected_generator_norm = 2 * sp.sqrt(
        sp.Rational(receiving_size - positive_count, positive_count)
    )
    assert sp.simplify(generator_norm - expected_generator_norm) == 0
    assert breaker.exact_layer_infinity_operator_norm == generator_norm
    assert breaker.exact_operator_tv_infinity == 2 * generator_norm
    assert generator_norm <= 2 * sp.sqrt(2)


def test_positive_affected_entries_do_not_certify_negative_unaffected_entries() -> None:
    network = lifted_final_two_module_network(
        2,
        3,
        module_redistribution=-sp.Rational(1, 5),
    )
    breaker = equitability_breaking_redistribution(
        network,
        sp.Integer(1),
        receiving_module=2,
        source_module=1,
    )

    # The breaker changes only the (module 2 <- module 1) block, whose base
    # entries remain positive.  Nevertheless C_0^eta[1,1]=-1/30 is an
    # untouched negative entry, so no full positive-layer radius exists.
    assert breaker.affected_entry_symmetric_radius > 0
    assert breaker.unaffected_base_positivity_status is False
    assert breaker.all_base_positivity_status is False
    assert breaker.certified_full_positivity_radius == 0
    assert (
        breaker.certified_dimension_uniform_full_positivity_lower_bound == 0
    )


def test_sparse_breaker_is_only_a_finite_size_contrast() -> None:
    network = lifted_final_two_module_network(2, 5)
    breaker = equitability_breaking_redistribution(
        network,
        sp.Integer(1),
        receiving_module=2,
        source_module=1,
        receiving_pattern="sparse",
    )
    assert breaker.receiving_pattern == "sparse"
    assert breaker.dimension_uniform_affected_radius_lower_bound == 0
    assert breaker.dimension_uniform_infinity_generator_bound == sp.oo
    assert matrix_infinity_operator_norm(breaker.generator) == sp.sqrt(10)
