import sympy as sp

from canard_control.green_phase import green_phase_audit


def test_tangent_normal_frame_solves_the_variational_equation() -> None:
    result = green_phase_audit()

    assert result.tangent_residual == sp.zeros(2, 1)
    assert result.normal_residual == sp.zeros(2, 1)
    assert result.frame_determinant == -result.exponential


def test_variation_coefficients_and_reconstruction_are_exact() -> None:
    result = green_phase_audit()
    s = result.phase
    f_1, f_2 = result.forcing
    expected_a = sp.exp(-s**2 / 2) * (
        -(result.exponential - s * result.integral) * f_1
        + result.integral * f_2
    )
    expected_b = sp.exp(-s**2 / 2) * (s * f_1 + f_2)

    assert sp.simplify(
        result.tangent_coefficient_derivative - expected_a
    ) == 0
    assert sp.simplify(
        result.normal_coefficient_derivative - expected_b
    ) == 0
    assert result.reconstruction_residual == sp.zeros(2, 1)


def test_phase_and_nonlinear_h_boundary_have_the_claimed_form() -> None:
    result = green_phase_audit()
    a = sp.Symbol("a", real=True)

    assert result.phase_value == -a
    assert result.h_boundary_residual == 0
