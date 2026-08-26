from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_signed_stable_flow_stage4h import (
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage4h_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "6577a7fcba9888b5126adcd894a361c9436b29a6f619b04f3d54ce5c3218fc15"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4h_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4h_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_exact_four_word_support_is_not_a_numeric_truncation() -> None:
    words = _payload()["artifact"]["exact_four_word_reduction"]
    assert words["current_resolvent_words"] == [
        "empty",
        "(0)",
        "(1)",
        "(0,0)",
    ]
    assert words["initial_voltage_density_words"] == [
        "(0)",
        "(1)",
        "(0,0)",
    ]
    assert words["period_less_than_tau0_plus_tau1"]
    assert words["period_less_than_three_tau0"]
    assert "not a numerical truncation" in words["word_support_status"]


def test_signed_deflation_and_event_projection_precede_tv() -> None:
    split = _payload()["artifact"]["continuous_history_split"]
    assert "before total variation" in split["stable_projection_identity"]
    assert split["phase_fixed_voltage_row"].startswith("S_v(t)-")
    event = _payload()["artifact"]["phase_fixed_one_step_diagnostic"]
    assert float(
        event["sampled_phase_fixed_one_step_stable_map_norm_binary64"]
    ) < 0.02
    assert float(
        event["sampled_phase_fixed_separate_triangle_norm_binary64"]
    ) > 1.0
    assert float(event["cancellation_factor_triangle_over_signed_binary64"]) > 100


def test_source_bound_values_are_not_promoted() -> None:
    artifact = _payload()["artifact"]
    numerics = artifact["source_bound_numerics"]
    event = artifact["phase_fixed_one_step_diagnostic"]
    intermediate = artifact["intermediate_signed_flow_diagnostic"]
    obstruction = artifact["directed_ingress_obstruction"]
    assert not numerics["nested_mesh_spread_is_interval_error"]
    assert not numerics["finite_history_nodes_used_as_operator_bound"]
    assert event["directed_upper"] is None
    assert not event["phase_fixed_one_step_stable_map_norm_upper_validated"]
    assert not event["k_s_equals_one_validated"]
    assert intermediate["directed_upper"] is None
    assert not intermediate["intermediate_stable_flow_norm_upper_validated"]
    assert not obstruction["directed_error_budget_available"]
    assert not obstruction["stable_power_ingress_closed"]


def test_split_tube_linear_budget_has_correct_unit_q_scaling() -> None:
    tube = _payload()["artifact"]["split_tube_linear_budget_diagnostic"]
    assert "q^Sigma/||q^Sigma||_Y" in tube["coordinate_normalization"]
    assert float(tube["sampled_stable_contribution_binary64"]) > 0
    assert float(tube["sampled_unstable_contribution_binary64"]) > 0
    assert float(tube["sampled_linear_tube_total_binary64"]) < 0.01
    assert float(
        tube[
            "sampled_remaining_nonlinear_and_directed_error_margin_binary64"
        ]
    ) > 0
    assert tube["sampled_linear_tube_inside_section_radius"]
    assert not tube["diagnostic_promoted_to_split_return_tube"]


def test_claim_ledger_preserves_every_open_graph_gate() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_note_states_the_precise_remaining_gate() -> None:
    prose = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "exactly finite" in prose
    assert "common outward piecewise-polynomial enclosure" in prose
    assert "does not prove" in prose
    assert "leaves every such proof flag false" in prose


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            (
                "artifact",
                "source_bound_numerics",
                "nested_mesh_spread_is_interval_error",
            ),
            True,
        ),
        (
            (
                "artifact",
                "phase_fixed_one_step_diagnostic",
                "directed_upper",
            ),
            "0.01",
        ),
        (
            (
                "artifact",
                "phase_fixed_one_step_diagnostic",
                "k_s_equals_one_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "directed_ingress_obstruction",
                "stable_power_ingress_closed",
            ),
            True,
        ),
        (
            (
                "artifact",
                "split_tube_linear_budget_diagnostic",
                "diagnostic_promoted_to_split_return_tube",
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
        validate_stage4h_result(payload, REPOSITORY)
