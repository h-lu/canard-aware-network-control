from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_route_c_event_stage5c import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage5c_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8"))


def test_registered_stage5c_artifact_validates() -> None:
    validate_stage5c_result(_payload(), REPOSITORY)


def test_stage5c_claim_ledger_is_hostile_at_the_stable_sheet() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


def test_uniform_event_has_strict_endpoint_signs_and_speed() -> None:
    event = _payload()["certificate"]["uniform_event_bracket"]
    assert float(event["left_gap_for_all_J"]["upper"]) < 0.0
    assert float(event["right_gap_for_all_J"]["lower"]) > 0.0
    assert float(event["voltage_event_speed_on_whole_bracket"]["lower"]) > 0.0
    assert event["validated_cell_count"] == 3


def test_event_graph_has_two_strict_directed_faces() -> None:
    model = _payload()["certificate"]["uniform_event_time_model"]
    assert float(model["negative_graph_gap"]["upper"]) < 0.0
    assert float(model["positive_graph_gap"]["lower"]) > 0.0
    assert model["event_time_remainder_upper"] == "1/10000"


def test_four_implicit_event_derivatives_are_registered() -> None:
    certificate = _payload()["certificate"]
    center = certificate["center_event"]
    assert center["requested_endpoint_gap_margin_exact"] == "1/10000000000000000"
    assert float(center["lower_gap"]["upper"]) < -9.0e-17
    assert float(center["upper_gap"]["lower"]) > 9.0e-17
    rows = certificate["implicit_event_time_jet"]["rows"]
    assert [row["order"] for row in rows] == [1, 2, 3, 4]
    for row in rows:
        interval = row["scaled_xi_power_coefficient"]
        assert float(interval["lower"]) <= float(interval["upper"])


def test_common_event_history_is_continuous_but_not_promoted_to_a_J_jet() -> None:
    payload = _payload()["certificate"]
    history = payload["common_event_complete_history"]
    assert history["phase_space"] == "Y=C([-5*sqrt(5),0],R)xR"
    assert 0.0 < float(history["Y_max_radius_upper"]) < 0.02
    assert payload["claim_status"][
        "uniform_J_derivative_tube_for_event_aligned_complete_history_validated"
    ] is False


def test_stable_and_newton_fields_remain_null() -> None:
    interface = _payload()["certificate"]["stable_sheet_interface"]
    assert interface["stable_gap_endpoint_intervals"] is None
    assert interface["stable_gap_derivative_interval"] is None
    assert interface["interval_newton_image"] is None


def test_validator_rejects_old_fourier_candidate_as_exact_section_level() -> None:
    payload = _payload()
    mutated = copy.deepcopy(payload)
    mutated["certificate"]["route_c_section"]["phase_zero_voltage_level"] = {
        "lower": (
            "0.905393843282120025506287674943450838327407828420743243"
        ),
        "upper": (
            "0.905393843282120025506287674943450838327407845269167748"
        ),
    }
    from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
        canonical_sha256,
    )

    mutated["manifest"]["certificate_sha256"] = canonical_sha256(
        mutated["certificate"]
    )
    with pytest.raises(
        ValueError, match="exact-orbit Route-C level enclosure changed"
    ):
        validate_stage5c_result(mutated, REPOSITORY)


@pytest.mark.parametrize(
    "path,value",
    [
        (("uniform_event_bracket", "left_gap_for_all_J", "upper"), "0"),
        (("uniform_event_bracket", "voltage_event_speed_on_whole_bracket", "lower"), "0"),
        (("uniform_event_time_model", "positive_graph_gap", "lower"), "0"),
    ],
)
def test_validator_rejects_destroyed_strict_margins(
    path: tuple[str, ...], value: str
) -> None:
    payload = _payload()
    mutated = copy.deepcopy(payload)
    target = mutated["certificate"]
    for name in path[:-1]:
        target = target[name]
    target[path[-1]] = value
    # Rebind the certificate digest so the semantic gate, rather than the
    # digest gate, is the reason for rejection.
    from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
        canonical_sha256,
    )

    mutated["manifest"]["certificate_sha256"] = canonical_sha256(
        mutated["certificate"]
    )
    with pytest.raises(ValueError):
        validate_stage5c_result(mutated, REPOSITORY)
