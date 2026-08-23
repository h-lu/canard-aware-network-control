import sympy as sp

from canard_control.outer_selection_coherence import (
    anchored_trace_jet_log_bound,
    incoherent_selection_jet_log,
    outer_selection_coherence_audit,
    tame_envelope_log,
)


def test_bounded_backward_extension_does_not_select_a_curve() -> None:
    result = outer_selection_coherence_audit()
    epsilon = result.epsilon
    nu = result.unfolding
    a = result.amplitude_action
    b = result.frequency_action

    assert result.repelling_equation_residual == 0
    assert sp.simplify(
        result.first_eta_jet_at_zero
        - (1 + nu) * sp.exp((b - a) / epsilon)
    ) == 0
    assert sp.simplify(
        result.second_eta_jet_at_zero
        - sp.exp((2 * b - a) / epsilon)
    ) == 0
    assert sp.simplify(
        result.mixed_nu_eta_jet_at_zero
        - sp.exp((b - a) / epsilon)
    ) == 0


def test_exponentially_close_choices_can_violate_every_declared_tame_scale(
) -> None:
    fixed_tame_data = {
        "p": 20.0,
        "algebraic_loss": 50.0,
        "polynomial_loss": 12.0,
        "exponential_loss": 30.0,
    }
    # Proposition 2.1 is asymptotic.  These values are below the crossover
    # for the deliberately large fixed tame constants above.
    for delta in (0.04, 0.03, 0.02):
        bad_first_jet = incoherent_selection_jet_log(
            delta,
            amplitude_action=1.0,
            frequency_action=2.0,
            eta_order=1,
        )
        tame = tame_envelope_log(delta, **fixed_tame_data)
        assert bad_first_jet > tame


def test_anchored_tame_boundary_is_superalgebraically_suppressed() -> None:
    for target_order in (1.0, 10.0, 50.0):
        delta = 0.02
        propagated = anchored_trace_jet_log_bound(
            delta,
            normal_action=0.5,
            boundary_algebraic_loss=20.0,
            slow_delay=2.0,
            history_rate=3.0,
        )
        algebraic_target = -target_order * sp.log(1.0 / delta)
        assert propagated < float(algebraic_target)


def test_selection_diagnostic_rejects_invalid_domains() -> None:
    for delta in (-0.1, 0.0, 1.0, 2.0):
        try:
            incoherent_selection_jet_log(
                delta,
                amplitude_action=1.0,
                frequency_action=2.0,
                eta_order=1,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("invalid delta was accepted")
