import sympy as sp

from canard_control.shared_recovery_moment import (
    finite_section_adjoint,
    shared_recovery_inner,
)


def test_shared_recovery_removes_the_extra_slow_center() -> None:
    result = shared_recovery_inner()
    spectral_parameter = sp.Symbol("lambda")
    recovery_gap = sp.Symbol("D_w", positive=True)

    assert result.unrepaired_characteristic == (
        spectral_parameter**3 * (spectral_parameter + 2)
    )
    assert result.shared_recovery_characteristic == (
        spectral_parameter**2 * (spectral_parameter + 2)
    )
    assert result.recovery_scaffold_characteristic == (
        spectral_parameter**2
        * (spectral_parameter + 2)
        * (spectral_parameter + recovery_gap)
    )
    assert result.unrepaired_kernel_dimension == 2
    assert result.shared_recovery_kernel_dimension == 1
    assert result.recovery_scaffold_kernel_dimension == 1
    assert result.scaffold_transverse_response == sp.Matrix(
        [-sp.Rational(1, 2), 0]
    )


def test_shared_recovery_modal_normal_form_is_canonical() -> None:
    result = shared_recovery_inner()
    x, z, y = sp.symbols("x z y")

    assert (result.critical_left.T * result.critical_right)[0] == 1
    assert (result.transverse_left.T * result.transverse_right)[0] == 1
    assert (result.critical_left.T * result.transverse_right)[0] == 0
    assert (result.transverse_left.T * result.critical_right)[0] == 0
    assert result.fast_jacobian * result.critical_right == sp.zeros(2, 1)
    assert (
        result.fast_jacobian * result.transverse_right
        == -2 * result.transverse_right
    )
    assert sp.simplify(
        result.canonical_critical_quadratic - y + (x + z) ** 2
    ) == 0
    assert sp.simplify(
        result.canonical_transverse_quadratic + 2 * z + (x + z) ** 2
    ) == 0
    assert result.kernel_residual == sp.zeros(2, 1)
    assert result.adjoint_residual == sp.zeros(2, 1)


def test_formal_transverse_range_returns_to_critical_solvability() -> None:
    result = shared_recovery_inner()
    delta = sp.Symbol("delta", positive=True)
    eta, K = sp.symbols("eta K", real=True)
    theta_0, theta_1, s = sp.symbols("theta_0 theta_1 s", real=True)
    delay_gap = theta_0 - theta_1

    assert result.leading_canard == -s / 2
    assert result.delay_translation_difference == delay_gap / 2
    assert sp.simplify(
        result.fiber_transverse_response
        + delta * K * eta * delay_gap / 4
    ) == 0
    assert result.fiber_range_residual == 0
    assert result.zero_incoming_range_residual == 0
    assert result.zero_incoming_boundary_residual == 0
    assert sp.simplify(
        result.second_order_transverse_coefficient
        + K * eta * delay_gap / 4
    ) == 0
    assert sp.simplify(
        result.critical_return_force + K * eta * delay_gap * s / 4
    ) == 0
    assert sp.simplify(
        result.whole_line_numerator
        + sp.sqrt(2 * sp.pi) * K * eta * delay_gap / 4
    ) == 0
    assert result.parameter_denominator == sp.sqrt(2 * sp.pi)
    assert sp.simplify(
        result.whole_line_root_coefficient - K * eta * delay_gap / 4
    ) == 0
    assert sp.simplify(
        result.whole_line_transverse_functional - eta * delay_gap / 4
    ) == 0


def test_finite_section_adjoint_exposes_endpoint_contribution() -> None:
    result = finite_section_adjoint()
    L = sp.Symbol("L", positive=True)
    eta, delta_theta = sp.symbols("eta DeltaTheta", real=True)
    beta_minus, beta_plus = sp.symbols(
        "beta_minus beta_plus", real=True
    )
    gaussian_endpoint = sp.exp(-L**2 / 2)

    assert result.left_endpoint_annihilation == sp.zeros(2, 1)
    assert result.right_endpoint_annihilation == sp.zeros(2, 1)
    assert result.phase_multiplier == 0
    assert sp.simplify(
        result.quadratic_pairing
        - result.parameter_pairing
        + 2 * L * gaussian_endpoint
    ) == 0
    assert result.boundary_pairing == (
        gaussian_endpoint * (beta_minus - beta_plus)
    )
    assert sp.simplify(
        result.interior_transverse_functional
        - eta
        * delta_theta
        * result.quadratic_pairing
        / (4 * result.parameter_pairing)
    ) == 0
    assert result.whole_line_limit == eta * delta_theta / 4
