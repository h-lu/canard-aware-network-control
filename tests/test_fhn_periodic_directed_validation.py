from __future__ import annotations

import json
from pathlib import Path

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
    cos_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    sin_interval,
)
from canard_control.fhn_periodic_candidate import solve_fhn_periodic_orbit
from canard_control.fhn_periodic_directed_validation import (
    directed_dft,
    directed_fhn_validation,
    directed_odd_fourier_matrices,
)


def test_decimal_interval_arithmetic_encloses_exact_rationals() -> None:
    precision = 96
    one_tenth = DirectedInterval.from_decimal("0.1", precision)
    one_fifth = DirectedInterval.from_decimal("0.2", precision)
    three_tenths = one_tenth + one_fifth
    exact = gmpy2.mpq(3, 10)
    assert three_tenths.lower <= exact <= three_tenths.upper

    product = one_tenth * one_fifth
    assert product.lower <= gmpy2.mpq(1, 50) <= product.upper
    quotient = one_tenth / one_fifth
    assert quotient.lower <= gmpy2.mpq(1, 2) <= quotient.upper
    negative = -three_tenths
    assert negative.lower.precision == precision
    assert negative.upper.precision == precision
    assert negative.lower <= -exact <= negative.upper

    crossing = DirectedInterval.from_bounds("-0.1", "0.2", precision)
    square = crossing**2
    assert square.lower == 0
    assert square.upper >= gmpy2.mpq(1, 25)

    upper_text = decimal_upper(three_tenths.upper)
    lower_text = decimal_lower(three_tenths.lower)
    with gmpy2.context(precision=256, round=gmpy2.RoundToNearest):
        assert gmpy2.mpfr(upper_text) >= three_tenths.upper
        assert gmpy2.mpfr(lower_text) <= three_tenths.lower


def test_directed_trigonometry_contains_extrema_and_special_values() -> None:
    precision = 128
    pi = pi_interval(precision)
    sine_peak = sin_interval(pi / 2)
    cosine_trough = cos_interval(pi)
    assert sine_peak.lower <= 1 <= sine_peak.upper
    assert cosine_trough.lower <= -1 <= cosine_trough.upper

    wide = sin_interval(DirectedInterval.from_bounds("-10", "10", precision))
    assert wide.lower == -1
    assert wide.upper == 1


def test_low_precision_spectral_enclosure_contains_higher_precision_one() -> None:
    low_alpha = DirectedInterval.from_decimal("0.173", 96)
    high_alpha = DirectedInterval.from_decimal("0.173", 192)
    low_derivative, low_shift = directed_odd_fourier_matrices(9, low_alpha)
    high_derivative, high_shift = directed_odd_fourier_matrices(9, high_alpha)
    for row, column in ((0, 1), (2, 7), (8, 3)):
        assert low_derivative[row][column].lower <= high_derivative[row][column].lower
        assert high_derivative[row][column].upper <= low_derivative[row][column].upper
        assert low_shift[row][column].lower <= high_shift[row][column].lower
        assert high_shift[row][column].upper <= low_shift[row][column].upper


def test_directed_dft_encloses_known_resolved_mode() -> None:
    node_count = 9
    phases = np.arange(node_count, dtype=float) / node_count
    values = np.cos(4.0 * np.pi * phases)
    coefficients = directed_dft(values, precision=128)
    # The samples themselves are exact binary64 inputs. Their DFT differs
    # slightly from the analytic cosine coefficients, so compare with a
    # high-precision enclosure of the same binary samples.
    refined = directed_dft(values, precision=224)
    for mode in range(-4, 5):
        assert coefficients[mode].real.lower <= refined[mode].real.lower
        assert refined[mode].real.upper <= coefficients[mode].real.upper
        assert coefficients[mode].imag.lower <= refined[mode].imag.lower
        assert refined[mode].imag.upper <= coefficients[mode].imag.upper


def test_directed_validation_proves_only_the_finite_root() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    result = directed_fhn_validation(orbit, precision=96)
    assert result.finite.exact_finite_collocation_root_validated
    assert result.finite.exact_finite_bordered_inverse_validated
    assert float(result.finite.uniform_inverse_defect_upper) < 1.0e-5
    assert result.finite.uniform_inverse_norm_upper is not None
    assert float(result.finite.radii_margin_lower) > 0.0
    assert result.fourier.outside_collocation_band_l1_upper != "0"
    assert float(result.fourier.outside_collocation_band_l1_lower) > 0.0
    assert float(result.fourier.unweighted_l1_lower) <= float(
        result.fourier.unweighted_l1_upper
    )
    assert float(result.fourier.maximum_coefficient_lower) <= float(
        result.fourier.maximum_coefficient_upper
    )
    assert result.fourier.tail_derivative_neumann_gate

    # A finite nodal proof plus a small full-polynomial residual is not an
    # infinite RFDE proof without the coupled correction-tail estimates.
    assert not result.finite_tail_coupling_bound_supplied
    assert not result.nonlinear_correction_tail_bound_supplied
    assert not result.infinite_radii_polynomial_evaluated
    assert not result.periodic_rfde_orbit_validated
    assert not result.bordered_rfde_inverse_validated
    assert "finite_to_tail_cross_norm" in result.missing_infinite_bounds
    assert "quadratic_cubic_correction_tail" in result.missing_infinite_bounds


def test_tracked_result_preserves_finite_proof_and_infinite_refusal() -> None:
    result_path = (
        Path(__file__).resolve().parents[1]
        / "experiments/results/fhn_periodic_directed_validation.json"
    )
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    assert payload["provenance"]["gmpy2"] == "2.2.2"
    assert payload["provenance"]["rounding"].startswith("MPFR RoundDown")
    assert payload["backend_audit"]["python_modules_visible"]["gmpy2"]
    assert payload["scope"]["exact_finite_collocation_proof"]
    assert payload["scope"]["exact_finite_bordered_inverse_proof"]
    assert not payload["scope"]["infinite_dimensional_periodic_rfde_proof"]
    assert not payload["scope"]["issue_15_closed"]
    validation = payload["validation"]
    assert validation["finite"]["uniform_inverse_norm_upper"] is not None
    assert float(validation["fourier"]["outside_collocation_band_l1_lower"]) > 1.0e-6
    assert "finite_to_tail_cross_norm" in validation["missing_infinite_bounds"]
    assert not validation["infinite_radii_polynomial_evaluated"]
