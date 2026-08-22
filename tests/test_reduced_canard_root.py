import sympy as sp

from canard_control.reduced_canard_root import (
    reduced_canard_root_audit,
)


def test_krupa_szmolyan_chart_and_first_integral_are_exact() -> None:
    result = reduced_canard_root_audit()
    s = result.inner_time

    assert result.canonical_vector_field_residual == sp.zeros(2, 1)
    assert result.canonical_canard == sp.Matrix(
        [s / 2, s**2 / 4 - sp.Rational(1, 2)]
    )
    assert result.first_integral_residual == 0
    assert sp.simplify(
        result.canonical_first_integral.subs(
            {
                sp.Symbol("x", real=True): result.canonical_canard[0],
                sp.Symbol("y", real=True): result.canonical_canard[1],
            }
        )
    ) == 0
    assert result.adjoint_residual == sp.zeros(2, 1)


def test_leading_gap_is_simple_and_selects_the_baseline_root() -> None:
    result = reduced_canard_root_audit()
    s = result.inner_time
    expected_fast_jet = (
        11 * s**3
        - 12
        * result.weak_gain
        * (result.theta_0 + 2 * result.theta_1)
    ) / (72 * result.alpha)

    assert sp.simplify(
        result.first_reduced_fast_jet_on_canard - expected_fast_jet
    ) == 0
    assert sp.simplify(
        result.leading_normalized_gap
        - result.gaussian_mass
        * (
            result.unfolding
            + sp.Rational(11, 24) / result.alpha
        )
    ) == 0
    assert result.leading_gap_unfolding_derivative == result.gaussian_mass
    assert result.baseline_unfolding == (
        -sp.Rational(11, 24) / result.alpha
    )


def test_mixed_eta_splitting_gives_the_claimed_root_shift() -> None:
    result = reduced_canard_root_audit()
    expected = (
        result.weak_gain
        * (result.theta_0 - result.theta_1)
        / (4 * result.alpha)
    )

    assert sp.simplify(
        result.eta_second_fast_jet_on_canard
        + expected * result.inner_time
    ) == 0
    assert sp.simplify(
        result.mixed_eta_gap_coefficient
        + expected * result.gaussian_mass
    ) == 0
    assert sp.simplify(result.eta_root_coefficient - expected) == 0
    assert sp.simplify(
        result.leading_root_difference
        - result.delta * result.eta * expected
    ) == 0
    assert sp.simplify(
        result.leading_physical_difference
        - result.delta**3 * result.eta * expected
    ) == 0


def test_parameter_normalization_and_tail_budget() -> None:
    result = reduced_canard_root_audit()

    assert result.ks_inner_parameter == (
        -result.alpha * result.delta * result.unfolding
    )
    assert result.ks_physical_parameter == (
        -result.alpha * result.delta**2 * result.unfolding
    )
    assert sp.simplify(
        result.ks_physical_difference
        + result.alpha * result.leading_physical_difference
    ) == 0
    assert result.tail_accounting_residual == 0
    assert sp.simplify(
        result.finite_second_moment
        - (
            result.finite_gaussian_mass
            - 2
            * result.section_radius
            * sp.exp(-result.section_radius**2 / 2)
        )
    ) == 0
    assert sp.limit(
        result.omitted_second_moment,
        result.section_radius,
        sp.oo,
    ) == 0
