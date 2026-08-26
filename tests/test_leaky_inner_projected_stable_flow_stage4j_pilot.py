from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_projected_stable_flow_stage4j_pilot import (
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    canonical_sha256,
    validate_stage4j_pilot_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "34f59e23c092eb0f15dc8a4e63d73b2b6d9f7cbcd58f25a2b4315d8bb525dafe"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4j_pilot_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4j_pilot_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_same_double_projected_complete_object_is_used() -> None:
    artifact = _payload()["artifact"]
    residual = artifact["common_projected_residual_pilot"]
    claims = artifact["claim_status"]
    assert residual["double_projection_formula"] == "P_t A P_s"
    assert claims["same_double_projected_object_used_for_khat_and_residual"]
    assert claims["projected_initial_defect_sampled"]
    assert claims["unadvanced_translation_identity_block_included"]
    assert (
        artifact["complete_history_khat_pilot"]["sampled_argmax_block"]
        == "unadvanced_translation_identity"
    )


def test_sampled_radii_budget_is_numerically_wide_but_not_directed() -> None:
    artifact = _payload()["artifact"]
    residual = artifact["common_projected_residual_pilot"]
    terminal = artifact["terminal_event_budget_pilot"]
    assert 15.0 < float(
        artifact["complete_history_khat_pilot"]["sampled_khat_binary64"]
    ) < 20.0
    assert float(residual["sampled_delta_binary64"]) < 1.0e-3
    assert float(terminal["sampled_terminal_ms_proxy_binary64"]) < 0.01
    assert terminal["directed_kint_upper"] is None
    assert terminal["directed_preprojection_delta_t_upper"] is None
    assert terminal["directed_epsilon_pi_t_upper"] is None
    assert terminal["directed_terminal_ms_upper"] is None


def test_all_residual_sources_are_explicitly_in_the_sampled_sum() -> None:
    residual = _payload()["artifact"]["common_projected_residual_pilot"]
    names = (
        "sampled_differential_integral_supremum_binary64",
        "sampled_projected_initial_defect_binary64",
        "sampled_history_transport_boundary_defect_binary64",
        "sampled_delay_activation_jump_proxy_binary64",
        "sampled_ordinary_cell_seam_conversion_proxy_binary64",
    )
    total = sum(float(residual[name]) for name in names)
    assert abs(total - float(residual["sampled_delta_binary64"])) < 1.0e-15
    assert residual[
        "sampled_delta_sum_includes_initial_boundary_activation_and_cell_seams"
    ]
    assert float(
        residual["sampled_delay_activation_right_residual_binary64"]
    ) > float(residual["sampled_delay_activation_jump_proxy_binary64"])


def test_trapezoid_is_exposed_as_nonproof_quadrature() -> None:
    artifact = _payload()["artifact"]
    discretization = artifact["pilot_discretization"]
    rows = artifact["transported_covector_oracles"]["rows"]
    assert not discretization["finite_history_nodes_promoted_to_operator_bound"]
    assert max(
        float(row["pilot_trapezoid_vs_high_order"]) for row in rows
    ) > 1.0e-8
    assert max(
        float(row["high_order_defect_from_phase_zero_direct_action"])
        for row in rows
    ) < 2.0e-12


def test_terminal_event_projection_is_applied_only_once() -> None:
    terminal = _payload()["artifact"]["terminal_event_budget_pilot"]
    assert terminal["event_projection_location"] == "terminal_time_only"
    assert not terminal["moving_pi_t_used"]
    assert 2.0 < float(terminal["directed_c_pi_t_upper"]) < 2.1


def test_claim_ledger_preserves_all_theorem_boundaries() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_note_names_the_exact_remaining_continuous_gate() -> None:
    prose = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "source-bound diagnostic / OPEN directed certificate" in prose
    assert "doubly projected object" in prose
    assert "unadvanced translation/identity block" in prose
    assert "inadmissible as proof evidence" in prose
    assert "Taylor--Bernstein enclosure" in prose


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            (
                "artifact",
                "pilot_discretization",
                "finite_history_nodes_promoted_to_operator_bound",
            ),
            True,
        ),
        (
            (
                "artifact",
                "common_projected_residual_pilot",
                "double_projection_formula",
            ),
            "P_t A",
        ),
        (
            (
                "artifact",
                "common_projected_residual_pilot",
                "sampled_projected_initial_defect_binary64",
            ),
            "0",
        ),
        (
            (
                "artifact",
                "common_projected_residual_pilot",
                "sampled_delay_activation_jump_proxy_binary64",
            ),
            "1",
        ),
        (
            (
                "artifact",
                "common_projected_residual_pilot",
                "directed_delta_upper",
            ),
            "0.001",
        ),
        (
            (
                "artifact",
                "terminal_event_budget_pilot",
                "moving_pi_t_used",
            ),
            True,
        ),
        (
            (
                "artifact",
                "terminal_event_budget_pilot",
                "directed_terminal_ms_upper",
            ),
            "0.01",
        ),
        (
            (
                "artifact",
                "claim_status",
                "phase_fixed_one_step_stable_map_norm_upper_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_promotions_or_omissions_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    payload["manifest"]["artifact_sha256"] = canonical_sha256(
        payload["artifact"]
    )
    with pytest.raises(ValueError):
        validate_stage4j_pilot_result(payload, REPOSITORY)


def test_non_numeric_directed_field_is_rejected_semantically() -> None:
    payload = deepcopy(_payload())
    payload["artifact"]["terminal_event_budget_pilot"][
        "directed_c_pi_t_upper"
    ] = None
    payload["manifest"]["artifact_sha256"] = canonical_sha256(
        payload["artifact"]
    )
    with pytest.raises(ValueError):
        validate_stage4j_pilot_result(payload, REPOSITORY)
