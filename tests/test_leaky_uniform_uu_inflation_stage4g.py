from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.leaky_uniform_uu_inflation_stage4g import (
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage4g_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "9ce03324bf37270b59d6dd06cf6b79762a47c48c932497c570c30f11a4f94469"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4g_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4g_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_exact_budget_requires_lipschitz_below_2409() -> None:
    budget = _payload()["artifact"]["exact_radius_budget"]
    cap_lower = gmpy2.mpq(budget["required_lipschitz_cap_lower"])
    cap_upper = gmpy2.mpq(budget["required_lipschitz_cap_upper"])
    increment = gmpy2.mpq(budget["guaranteed_increment_budget_lower"])
    assert gmpy2.mpq(2408) < cap_lower <= cap_upper < gmpy2.mpq(2409)
    assert gmpy2.mpq(4) < increment < gmpy2.mpq(5)
    assert budget["cap_is_a_sufficient_threshold_not_a_validated_bound"]


def test_scalar_mean_flow_attempt_is_directed_but_fails_local_ball() -> None:
    attempt = _payload()["artifact"]["directed_scalar_mean_flow_attempt"]
    assert attempt["cell_count"] == 1042
    assert attempt["tau0_aligned_cell_count"] == 512
    assert attempt["tau1_aligned_cell_count"] == 640
    assert attempt["all_current_cells_self_closed"]
    assert not attempt["mesh_spread_used_as_error"]
    assert not attempt["local_return_tube_gate_closes"]
    failure = attempt["first_local_ball_failure"]
    assert failure["cell_index"] == 581
    assert gmpy2.mpq(failure["voltage_coordinate_radius_upper"]) > gmpy2.mpq(
        "0.01"
    )
    assert gmpy2.mpq(attempt["maximum_p_radius_upper"]) > 10
    assert gmpy2.mpq(
        attempt["maximum_voltage_coordinate_radius_upper"]
    ) > 2


def test_complete_history_decomposition_includes_event_and_moving_projection() -> None:
    decomposition = _payload()["artifact"][
        "full_history_lipschitz_decomposition"
    ]
    pieces = decomposition["required_lipschitz_pieces"]
    assert {"L_base_flow", "L_UV", "L_event", "L_q", "L_f", "L_normalization"} == set(
        pieces
    )
    assert "D_x q" in decomposition["exact_first_difference_identity"]
    assert "D_x f" in decomposition["exact_quotient_derivative"]
    assert not decomposition["stage4b_design_targets_used_as_bounds"]
    assert not decomposition[
        "independent_triangle_bounds_on_quotient_terms_allowed"
    ]


def test_minimal_failure_does_not_claim_impossibility() -> None:
    artifact = _payload()["artifact"]
    failure = artifact["frozen_minimal_failure"]
    downstream = artifact["downstream_status"]
    assert failure["this_does_not_disprove_a_sharper_signed_bound"]
    assert failure["required_signed_ingress_parent"] is None
    assert "(tau0,tau0)" in failure[
        "nonzero_forward_delay_words_over_one_period"
    ]
    assert downstream["validated_complete_history_lipschitz_upper"] is None
    assert downstream["uniform_stable_output_uu_upper"] is None
    assert not downstream[
        "uniform_stable_output_uu_strictly_below_twelve"
    ]
    assert not downstream["quantitative_stable_graph"]
    assert not downstream["physical_pulse_onset"]


def test_claim_ledger_separates_audit_from_uniform_theorem() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_note_states_failure_and_scope_boundary() -> None:
    prose = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "2408.441718672103" in prose
    assert "upper bounds, not observations" in prose
    assert "does not provide" in prose or "Not proved" in prose
    assert "five Stage-4B design targets" in prose
    assert "total variation" in prose


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            (
                "artifact",
                "directed_scalar_mean_flow_attempt",
                "local_return_tube_gate_closes",
            ),
            True,
        ),
        (
            (
                "artifact",
                "full_history_lipschitz_decomposition",
                "stage4b_design_targets_used_as_bounds",
            ),
            True,
        ),
        (
            (
                "artifact",
                "frozen_minimal_failure",
                "this_does_not_disprove_a_sharper_signed_bound",
            ),
            False,
        ),
        (
            (
                "artifact",
                "downstream_status",
                "uniform_stable_output_uu_upper",
            ),
            "11.99",
        ),
        (
            (
                "artifact",
                "claim_status",
                "uniform_split_ball_stable_output_uu_below_twelve_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "claim_status",
                "inner_local_stable_graph_quantitatively_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_promotions_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        validate_stage4g_result(payload, REPOSITORY)
