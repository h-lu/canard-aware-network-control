from __future__ import annotations

import itertools

import pytest
import sympy as sp

from canard_control.lifted_selected_root_response import (
    balanced_sign_swap_permutation,
    canonical_root_response_coefficient,
    module_permutation_matrix,
    symmetry_breaking_response_audit,
)
from canard_control.lifted_two_module_network import (
    equitability_breaking_redistribution,
    lifted_final_two_module_network,
    matrix_infinity_operator_norm,
)


@pytest.mark.parametrize(
    "n1,n2,receiving,source",
    [(2, 1, 1, 1), (3, 2, 1, 2), (1, 4, 2, 1), (5, 3, 2, 2)],
)
def test_combined_direction_is_non_equitable_but_reynolds_reads_module_part(
    n1: int,
    n2: int,
    receiving: int,
    source: int,
) -> None:
    network = lifted_final_two_module_network(n1, n2)
    kappa = sp.Rational(3, 7)
    audit = symmetry_breaking_response_audit(
        network,
        kappa=kappa,
        receiving_module=receiving,
        source_module=source,
    )
    module_t = sp.ImmutableMatrix([[1, 0], [-2, 0]])

    assert audit.module_restriction_0 == module_t
    assert audit.module_restriction_1 == -module_t
    assert audit.critical_pairing_0 == 0
    assert audit.critical_pairing_1 == 0
    assert audit.total_direction.is_zero_matrix
    assert not audit.equitability_defect.is_zero_matrix
    assert audit.reynolds_within_generator.is_zero_matrix
    assert (
        audit.reynolds_combined_layer_0_direction
        == audit.module_direction
    )
    direction_norm = matrix_infinity_operator_norm(
        audit.combined_layer_0_direction
    )
    generator_norm = matrix_infinity_operator_norm(
        audit.within_generator
    )
    module_norm = matrix_infinity_operator_norm(audit.module_direction)
    assert direction_norm >= module_norm
    assert direction_norm <= module_norm + kappa * generator_norm


def test_reynolds_zero_is_literal_finite_group_average() -> None:
    network = lifted_final_two_module_network(3, 2)
    breaker = equitability_breaking_redistribution(
        network,
        1,
        receiving_module=1,
        source_module=2,
    )
    generator = sp.Matrix(breaker.generator)
    conjugates = []
    for permutation in itertools.permutations(range(network.n1)):
        p = sp.Matrix(module_permutation_matrix(network, 1, permutation))
        conjugates.append(p * generator * p.T)
    average = sp.simplify(
        sum(conjugates, sp.zeros(network.node_count)) / len(conjugates)
    )
    assert average == sp.zeros(network.node_count)


@pytest.mark.parametrize("receiving,n1,n2", [(1, 4, 3), (2, 3, 6)])
def test_even_distributed_breaker_has_exact_sign_swap(
    receiving: int,
    n1: int,
    n2: int,
) -> None:
    network = lifted_final_two_module_network(n1, n2)
    breaker = equitability_breaking_redistribution(
        network,
        1,
        receiving_module=receiving,
        source_module=1,
    )
    p = balanced_sign_swap_permutation(
        network,
        receiving_module=receiving,
    )
    assert p is not None
    p_matrix = sp.Matrix(p)
    assert sp.simplify(
        p_matrix * breaker.generator * p_matrix.T + breaker.generator
    ) == sp.zeros(network.node_count)


def test_odd_distributed_breaker_has_no_declared_sign_swap() -> None:
    network = lifted_final_two_module_network(3, 2)
    assert balanced_sign_swap_permutation(
        network,
        receiving_module=1,
    ) is None


def test_response_coefficient_is_the_two_module_value() -> None:
    coupling, theta_0, theta_1 = sp.symbols(
        "K theta_0 theta_1", real=True
    )
    coefficient = canonical_root_response_coefficient(
        coupling,
        theta_0,
        theta_1,
    )
    assert coefficient == coupling * (theta_0 - theta_1) / sp.sqrt(6)


def test_projection_neutrality_does_not_kill_a_node_labelled_matcher() -> None:
    network = lifted_final_two_module_network(2, 3)
    breaker = equitability_breaking_redistribution(
        network,
        1,
        receiving_module=1,
        source_module=2,
    )
    labelled_readout = sp.zeros(1, network.node_count)
    labelled_readout[0, 0] = 1

    # The invariant critical readout kills the generator, while an arbitrary
    # node-labelled scalar does not.  Thus the Reynolds cancellation theorem
    # genuinely needs a relabeling-covariant preparation and matcher.
    assert network.critical_left.T * breaker.generator == sp.zeros(
        1, network.node_count
    )
    assert (
        labelled_readout * breaker.generator * network.critical_right
    )[0] != 0


def test_module_permutation_rejects_invalid_data() -> None:
    network = lifted_final_two_module_network(2, 3)
    with pytest.raises(ValueError, match="module"):
        module_permutation_matrix(network, 3, (0, 1))
    with pytest.raises(ValueError, match="every local index"):
        module_permutation_matrix(network, 1, (0, 0))
