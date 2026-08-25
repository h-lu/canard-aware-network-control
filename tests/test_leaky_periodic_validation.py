from __future__ import annotations

import numpy as np
import pytest

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
)
from canard_control.fhn_periodic_infinite_validation import (
    _build_base_sequences,
    _coefficient_column_outputs,
    _finite_coefficient_matrix,
    _nonlinear_coefficients,
    _sequence_box_norm_upper,
    _tail_from_finite_upper,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
    _floquet_contract,
    _leaky_coefficient_column_outputs,
    _leaky_finite_coefficient_matrix,
    _leaky_nonlinear_coefficients,
    _leaky_tail_to_tail_upper,
    build_leaky_machinery_reuse_audit,
    evaluate_leaky_periodic_radii_candidate,
)
from canard_control.leaky_periodic_majorant_audit import (
    analytic_tail_preconditioner_norm_upper,
    build_leaky_periodic_majorant_formula_audit,
    leak_derivative_variation_z1_increment_upper,
)


def _small_orbit() -> PeriodicOrbitCandidate:
    count = 5
    phases = np.arange(count, dtype=float) / count
    state = np.column_stack(
        (
            0.9 + 0.2 * np.cos(2 * np.pi * phases),
            0.4 + 0.1 * np.sin(2 * np.pi * phases),
        )
    )
    parameters = FHNPeriodicParameters(
        epsilon=0.2,
        unfolding=0.25,
        theta_0=4.0,
        theta_1=5.0,
        kappa_1=0.004,
        kappa_3=0.005,
    )
    return PeriodicOrbitCandidate(
        parameters=parameters,
        phase_nodes=phases,
        state=state,
        period=20.0,
        collocation_residual_inf=1.0,
        oversampled_residual_inf=1.0,
        newton_iterations=0,
        final_step_inf=0.0,
        spectral_tail_l1=0.0,
    )


def _midpoint(value) -> complex:
    return complex(
        float(value.real.midpoint_nearest()),
        float(value.imag.midpoint_nearest()),
    )


def test_old_validator_slow_residual_is_the_wrong_equation() -> None:
    orbit = _small_orbit()
    old = _build_base_sequences(orbit, precision=100)
    leaky = _build_leaky_base_sequences(orbit, precision=100)
    period = orbit.period
    epsilon = orbit.parameters.epsilon

    for mode, recovery in leaky.recovery.items():
        observed = _midpoint(leaky.residual_recovery[mode]) - _midpoint(
            old.residual_recovery[mode]
        )
        expected = period * epsilon * _midpoint(recovery)
        assert abs(observed - expected) < 2.0e-12

    assert any(
        abs(
            _midpoint(leaky.residual_recovery[mode])
            - _midpoint(old.residual_recovery[mode])
        )
        > 1.0e-6
        for mode in leaky.recovery
    )


def test_leak_adds_T_epsilon_to_the_recovery_diagonal() -> None:
    orbit = _small_orbit()
    base = _build_leaky_base_sequences(orbit, precision=100)
    _, old_slow, _ = _coefficient_column_outputs(
        base,
        [0, 1],
        input_component=1,
        input_mode=1,
        input_part="real",
    )
    _, leaky_slow, _ = _leaky_coefficient_column_outputs(
        base,
        [0, 1],
        input_component=1,
        input_mode=1,
        input_part="real",
    )
    observed = _midpoint(leaky_slow[1]) - _midpoint(old_slow[1])
    assert abs(observed - orbit.period * orbit.parameters.epsilon) < 1.0e-12
    assert abs(_midpoint(leaky_slow[0]) - _midpoint(old_slow[0])) < 1.0e-12


def test_leak_adds_epsilon_w_to_the_period_column_mode_by_mode() -> None:
    orbit = _small_orbit()
    old_base = _build_base_sequences(orbit, precision=100)
    leaky_base = _build_leaky_base_sequences(orbit, precision=100)
    _, old_slow, _ = _coefficient_column_outputs(
        old_base, [0, 1, 2], input_component=None
    )
    _, leaky_slow, _ = _leaky_coefficient_column_outputs(
        leaky_base, [0, 1, 2], input_component=None
    )
    epsilon = orbit.parameters.epsilon
    for mode in (0, 1, 2):
        observed = _midpoint(leaky_slow[mode]) - _midpoint(old_slow[mode])
        expected = epsilon * _midpoint(leaky_base.recovery.get(mode))
        assert abs(observed - expected) < 2.0e-12


def test_full_finite_matrix_difference_has_only_the_two_leak_blocks() -> None:
    orbit = _small_orbit()
    precision = 100
    cutoff = 6
    old_base = _build_base_sequences(orbit, precision)
    leaky_base = _build_leaky_base_sequences(orbit, precision)
    old_matrix, _, layout = _finite_coefficient_matrix(old_base, cutoff)
    leaky_matrix, _, leaky_layout = _leaky_finite_coefficient_matrix(
        leaky_base, cutoff
    )
    assert leaky_layout == layout
    expected = np.zeros_like(old_matrix)
    diagonal = orbit.period * orbit.parameters.epsilon
    for mode in range(cutoff + 1):
        for part in (("real",) if mode == 0 else ("real", "imag")):
            index = layout.state_index(1, mode, part)
            expected[index, index] = diagonal
        coefficient = (
            _midpoint(leaky_base.recovery[mode])
            if mode in leaky_base.recovery
            else 0.0j
        )
        weight = 1 if mode == 0 else 2
        expected[
            layout.state_index(1, mode, "real"), layout.period_index
        ] = orbit.parameters.epsilon * weight * coefficient.real
        if mode:
            expected[
                layout.state_index(1, mode, "imag"), layout.period_index
            ] = orbit.parameters.epsilon * weight * coefficient.imag
    assert np.max(np.abs((leaky_matrix - old_matrix) - expected)) < 2.0e-15


def test_leak_changes_no_finite_to_tail_cross_block_and_tail_formula_is_exact() -> None:
    import gmpy2

    from canard_control.directed_interval import DirectedInterval, pi_interval

    orbit = _small_orbit()
    precision = 100
    cutoff = 6
    old_base = _build_base_sequences(orbit, precision)
    leaky_base = _build_leaky_base_sequences(orbit, precision)
    _, _, layout = _finite_coefficient_matrix(old_base, cutoff)
    assert _tail_from_finite_upper(
        old_base, layout
    ) == _tail_from_finite_upper(leaky_base, layout)

    current = _sequence_box_norm_upper(
        leaky_base.current_coefficient, precision
    )
    delayed = [
        _sequence_box_norm_upper(sequence, precision)
        for sequence in leaky_base.delayed_coefficients
    ]
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    denominator = (pi_interval(precision) * (2 * (cutoff + 1))).lower
    epsilon = leaky_base.parameters["epsilon"].upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage_column = current + sqrt_two * sum(
            delayed, gmpy2.mpfr(0, precision)
        ) + epsilon
        recovery_column = 1 + epsilon
        expected = (
            leaky_base.period.upper
            * max(voltage_column, recovery_column)
            / denominator
        )
    assert _leaky_tail_to_tail_upper(leaky_base, cutoff) == expected


def test_leaky_z1_majorant_adds_the_recovery_column_allowance() -> None:
    orbit = _small_orbit()
    base = _build_leaky_base_sequences(orbit, precision=100)
    inverse_norm = __import__("gmpy2").mpfr(2, 100)
    old = _nonlinear_coefficients(base, 6, inverse_norm, "1e-5")
    leaky = _leaky_nonlinear_coefficients(
        base, 6, inverse_norm, "1e-5"
    )
    expected = inverse_norm * base.parameters["epsilon"].upper
    assert float(leaky[0] - old[0] - expected) == pytest.approx(
        0.0, abs=1.0e-25
    )
    assert leaky[1:] == old[1:]


def test_leaky_z1_uses_the_full_finite_tail_preconditioner_norm() -> None:
    import gmpy2

    precision = 100
    finite = gmpy2.mpfr("1e-8", precision)
    epsilon = gmpy2.mpfr("0.2", precision)
    tail = analytic_tail_preconditioner_norm_upper(6, precision)
    increment = leak_derivative_variation_z1_increment_upper(
        epsilon, finite, 6, precision
    )
    assert tail > finite
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower_product = tail * epsilon
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        loose_product = (
            tail * epsilon * gmpy2.mpfr("1.0000000000000001", precision)
        )
    assert increment >= lower_product
    assert increment < loose_product


def test_formula_audit_closes_only_the_leaky_majorant_adaptation() -> None:
    audit = build_leaky_periodic_majorant_formula_audit()
    assert audit.formula_adaptation_independently_audited
    assert audit.recovery_residual_identity_proved
    assert audit.recovery_state_columns_proved
    assert audit.recovery_period_column_proved
    assert audit.finite_tail_cross_blocks_unchanged_proved
    assert audit.recovery_tail_column_bound_proved
    assert audit.nonlinear_z1_increment_proved
    assert len(audit.excluded_claims) == 4


def test_reuse_audit_refuses_old_parameter_box_and_floquet_artifacts() -> None:
    audit = build_leaky_machinery_reuse_audit()
    assert not audit.old_nonleaky_validator_directly_applies
    assert not audit.parameter_box_coordinates_match
    assert audit.branch_specific_replay_artifacts_available
    assert audit.registered_branch_replay_artifacts == (
        "inner_saddle_candidate",
        "outer_pulse",
    )
    assert audit.missing_branch_replay_artifacts == ()
    assert not audit.old_floquet_artifacts_transfer_to_leaky_orbits
    assert len(audit.exact_reusable_components) == 5
    assert len(audit.model_dependent_replacements) == 6
    assert audit.directed_outer_periodic_orbit_validated
    assert audit.directed_inner_periodic_orbit_validated
    assert not audit.directed_outer_floquet_index_validated
    assert not audit.directed_inner_floquet_index_validated


def test_floquet_contract_never_promotes_a_bordered_inverse_to_an_index() -> None:
    contract = _floquet_contract(True, True)
    assert contract.translation_identity_exact_for_validated_orbit
    assert contract.phase_bordered_rfde_inverse_validated
    assert not contract.fredholm_to_monodromy_multiplicity_transfer_registered
    assert not contract.neutral_multiplier_algebraically_simple_validated
    assert not contract.nontranslation_unit_circle_exclusion_validated
    assert not contract.unstable_multiplier_count_validated
    assert not contract.attracting_or_saddle_index_validated
    with pytest.raises(ValueError, match="without its orbit"):
        _floquet_contract(False, True)


def test_prototype_rejects_bad_branch_before_heavy_arithmetic() -> None:
    with pytest.raises(ValueError, match="branch must identify"):
        evaluate_leaky_periodic_radii_candidate(
            _small_orbit(), branch="unregistered", cutoff=6, precision=80
        )


def test_prototype_requires_the_full_cubic_support() -> None:
    with pytest.raises(ValueError, match="cubic residual support"):
        evaluate_leaky_periodic_radii_candidate(
            _small_orbit(), branch="outer_pulse", cutoff=5, precision=80
        )
