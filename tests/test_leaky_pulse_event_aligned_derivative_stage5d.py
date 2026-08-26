from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.leaky_pulse_event_aligned_derivative_stage5d import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage5d_result,
)
from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    canonical_sha256,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _rebind(payload: dict) -> None:
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )


def test_registered_stage5d_result_is_source_bound() -> None:
    validate_stage5d_result(_payload(), REPOSITORY)


def test_first_variation_closes_without_differentiating_state_remainder() -> None:
    fixed = _payload()["certificate"]["fixed_time_first_variation"]
    assert fixed["all_cells_closed"]
    assert fixed["closed_cell_count"] == 1152
    assert not fixed["state_remainder_derivative_used"]
    assert gmpy2.mpq(fixed["minimum_cell_closure_gap_lower"]) > 0
    assert gmpy2.mpq(fixed["maximum_scaled_P_error_radius_upper"]) < gmpy2.mpq(
        "9e-8"
    )
    assert gmpy2.mpq(fixed["maximum_tail_derivative_source_upper"]) > gmpy2.mpq(
        "1e-8"
    )
    assert gmpy2.mpq(
        fixed["maximum_linearization_mismatch_source_upper"]
    ) > 0
    assert gmpy2.mpq(fixed["maximum_total_source_upper"]) > gmpy2.mpq(
        fixed["maximum_tail_derivative_source_upper"]
    )
    assert "partial_xi Tail" in fixed["exact_error_equation"]


def test_event_time_derivative_is_strictly_positive_on_full_interval() -> None:
    event = _payload()["certificate"]["event_time_first_derivative"]
    assert event["event_graph_parameter_subdivision_count"] == 128
    assert gmpy2.mpq(event["event_scaled_voltage_variation_Wv"]["upper"]) < 0
    assert gmpy2.mpq(event["uniform_positive_voltage_speed"]["lower"]) > 0
    assert gmpy2.mpq(event["T_J_interval"]["lower"]) > 300
    assert gmpy2.mpq(event["T_J_interval"]["upper"]) < 500


def test_complete_history_derivative_retains_translation_and_signed_recovery() -> None:
    history = _payload()["certificate"]["continuous_Y_derivative"]
    assert history["phase_space"] == "Y=C([-5*sqrt(5),0],R)xR"
    assert history["event_current_voltage_D_J_exact"] == "0"
    assert gmpy2.mpq(
        history["event_current_recovery_D_J_interval"]["upper"]
    ) < 0
    assert gmpy2.mpq(history["Y_norm_upper"]) < 143
    translation = history["voltage_translation_z_t_times_T_J_interval"]
    assert gmpy2.mpq(translation["lower"]) < 0 < gmpy2.mpq(
        translation["upper"]
    )


def test_fixed_center_action_is_a_modulus_bound_not_a_fake_sign() -> None:
    certificate = _payload()["certificate"]
    action = certificate["fixed_center_route_c_functional_action"]
    assert action["oriented_interval"] is None
    assert gmpy2.mpq(action["normalized_action_modulus_upper"]) < gmpy2.mpq(
        action["global_operator_norm_fallback_upper"]
    )
    assert not certificate["stable_gap_interface"][
        "oriented_functional_action_sign_available"
    ]


def test_stage5d_claim_ledger_keeps_stable_sheet_and_onset_open() -> None:
    certificate = _payload()["certificate"]
    claims = certificate["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    interface = certificate["stable_gap_interface"]
    assert interface["stable_gap_endpoint_intervals"] is None
    assert interface["stable_gap_derivative_interval"] is None
    assert interface["interval_newton_image"] is None
    assert interface["pulse_parameter_Jc"] is None


@pytest.mark.parametrize(
    ("path", "value", "message"),
    (
        (
            ("fixed_time_first_variation", "state_remainder_derivative_used"),
            True,
            "state remainder was illicitly differentiated",
        ),
        (
            ("event_time_first_derivative", "T_J_interval", "lower"),
            "0",
            "event-time monotonicity was lost",
        ),
        (
            (
                "continuous_Y_derivative",
                "event_current_recovery_D_J_interval",
                "upper",
            ),
            "0",
            "recovery monotonicity was lost",
        ),
        (
            (
                "fixed_center_route_c_functional_action",
                "oriented_interval",
            ),
            {"lower": "1", "upper": "2"},
            "oriented Stage-4D action was silently manufactured",
        ),
        (
            ("stable_gap_interface", "stable_gap_derivative_interval"),
            {"lower": "1", "upper": "2"},
            "open stable-sheet or onset field was populated",
        ),
    ),
)
def test_validator_rejects_hostile_promotions(
    path: tuple[str, ...], value: object, message: str
) -> None:
    payload = deepcopy(_payload())
    target = payload["certificate"]
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    _rebind(payload)
    with pytest.raises(ValueError, match=message):
        validate_stage5d_result(payload, REPOSITORY)
