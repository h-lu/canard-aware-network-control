"""Operator-level regression tests for delayed Fourier--Floquet phases.

The physical product ``b(theta-alpha) y(theta-alpha)`` has two equivalent
representations.  These tests bind that identity to the coefficient semantics
used by the legacy FHN Bloch and right-half validators and reject the two
mixed conventions.
"""

from __future__ import annotations

import cmath
import inspect
import math

from canard_control.fhn_bloch_outer_validation import _center_voltage_entry
from canard_control.fhn_periodic_infinite_validation import _build_base_sequences
from canard_control.fhn_periodic_candidate import solve_fhn_periodic_orbit
from canard_control.fhn_synchronous_floquet_right_half_cover import (
    _candidate_matrices,
)


def _row_form(
    coefficient: complex,
    *,
    output_mode: int,
    alpha: float,
    bloch_phase: float,
) -> complex:
    """Unshifted coefficient with the total phase on the output mode."""

    return coefficient * cmath.exp(
        -1j * (2.0 * math.pi * output_mode + bloch_phase) * alpha
    )


def _column_form(
    coefficient: complex,
    *,
    coefficient_mode: int,
    input_mode: int,
    alpha: float,
    bloch_phase: float,
) -> complex:
    """Delay-shifted coefficient with the remaining input-mode phase."""

    shifted_coefficient = coefficient * cmath.exp(
        -2.0j * math.pi * coefficient_mode * alpha
    )
    return shifted_coefficient * cmath.exp(
        -1j * (2.0 * math.pi * input_mode + bloch_phase) * alpha
    )


def test_unshifted_row_and_shifted_column_forms_agree_entrywise() -> None:
    coefficients = {
        -3: -0.13 + 0.07j,
        -1: 0.29 - 0.11j,
        0: 0.37 + 0.05j,
        2: -0.19 - 0.23j,
        4: 0.08 + 0.17j,
    }
    alpha = 0.237_419
    bloch_phase = 0.613
    for output_mode in range(-5, 6):
        for input_mode in range(-5, 6):
            coefficient_mode = output_mode - input_mode
            if coefficient_mode not in coefficients:
                continue
            coefficient = coefficients[coefficient_mode]
            row = _row_form(
                coefficient,
                output_mode=output_mode,
                alpha=alpha,
                bloch_phase=bloch_phase,
            )
            column = _column_form(
                coefficient,
                coefficient_mode=coefficient_mode,
                input_mode=input_mode,
                alpha=alpha,
                bloch_phase=bloch_phase,
            )
            assert abs(row - column) < 3e-15


def test_both_mixed_phase_conventions_are_detectably_wrong() -> None:
    coefficient = 0.31 - 0.27j
    output_mode = 3
    input_mode = -2
    coefficient_mode = output_mode - input_mode
    alpha = 0.217
    bloch_phase = 0.47
    correct = _row_form(
        coefficient,
        output_mode=output_mode,
        alpha=alpha,
        bloch_phase=bloch_phase,
    )

    # Invalid mix 1: unshifted coefficient plus input/column phase.
    unshifted_column = coefficient * cmath.exp(
        -1j * (2.0 * math.pi * input_mode + bloch_phase) * alpha
    )
    # Invalid mix 2: shifted coefficient plus output/row phase.
    shifted_row = (
        coefficient
        * cmath.exp(-2.0j * math.pi * coefficient_mode * alpha)
        * cmath.exp(
            -1j * (2.0 * math.pi * output_mode + bloch_phase) * alpha
        )
    )

    assert abs(correct - unshifted_column) > 0.1
    assert abs(correct - shifted_row) > 0.1


def test_legacy_fhn_validators_bind_unshifted_coefficients_to_output_phase() -> None:
    center_source = inspect.getsource(_center_voltage_entry)
    assert "base.delayed_state_derivative" in center_source
    assert "output_mode, phase, tau, base.period" in center_source
    assert "input_mode, phase, tau, base.period" not in center_source

    right_half_source = inspect.getsource(_candidate_matrices)
    assert "candidate.delayed_finite" in right_half_source
    assert "rotation[:, None] * candidate.delayed_finite" in right_half_source
    assert "rotation[:, None] * candidate.delayed_finite_tail" in right_half_source
    assert "rotation[:, None] * candidate.delayed_tail_finite" in right_half_source


def test_tracked_base_keeps_shifted_and_unshifted_coefficient_semantics_distinct() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    base = _build_base_sequences(orbit, 100)
    assert base.delayed_state_derivative is not base.delayed_coefficients[0]
    assert base.delayed_state_derivative is not base.delayed_coefficients[1]

    # A nonconstant mode changes under each nonzero delay shift.  This guards
    # against silently relabeling one coefficient sequence as the other.
    nonzero_modes = [
        mode
        for mode, value in base.delayed_state_derivative.items()
        if mode != 0 and float(value.upper_abs()) > 1e-10
    ]
    assert nonzero_modes
    mode = max(
        nonzero_modes,
        key=lambda candidate: float(
            base.delayed_state_derivative[candidate].upper_abs()
        ),
    )
    for shifted in base.delayed_coefficients:
        unshifted_value = base.delayed_state_derivative[mode]
        shifted_value = shifted[mode]
        real_separated = (
            shifted_value.real.upper < unshifted_value.real.lower
            or unshifted_value.real.upper < shifted_value.real.lower
        )
        imag_separated = (
            shifted_value.imag.upper < unshifted_value.imag.lower
            or unshifted_value.imag.upper < shifted_value.imag.lower
        )
        assert real_separated or imag_separated
