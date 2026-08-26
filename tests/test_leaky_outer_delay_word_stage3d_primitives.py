from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_delay_word_stage3d_primitives import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    canonical_sha256,
    validate_outer_delay_word_stage3d_primitives_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_stage3d_result_replays(payload):
    validate_outer_delay_word_stage3d_primitives_result(payload, REPOSITORY)


def test_duffy_words_are_exactly_reduced_to_primitives(payload):
    identity = payload["certificate"]["primitive_identity"]
    assert identity["maximum_primitive_delay_depth"] == 2
    assert "H_j(t)-H_j(s+tau_j)" in identity["one_word"]
    assert "L_jk(t)-L_jk(a)" in identity["two_word"]
    assert "one-dimensional" in identity["duffy_reduction"]
    assert "only then" in identity["signed_ordering"]


def test_center_density_ladder_is_continuous_but_diagnostic(payload):
    rows = payload["certificate"]["pilot_levels"]
    assert [row["level_id"] for row in rows] == ["coarse", "fine"]
    for row in rows:
        assert row["continuous_history_density_evaluated_without_input_sampling"]
        assert row["signed_sum_before_absolute_quadrature"]
        assert row["diagnostic_only"]
        assert Decimal(row["center_voltage_return_norm_binary64"]["decimal"]) < Decimal("0.14")
        assert Decimal(row["center_recovery_return_norm_binary64"]["decimal"]) < Decimal("0.004")
        assert Decimal(
            row["fundamental_inverse_consistency_max_binary64"]["decimal"]
        ) < Decimal("1e-6")


def test_phase_projection_is_proved_but_nonlinear_chart_is_not(payload):
    certificate = payload["certificate"]
    phase = certificate["continuous_phase_projection"]
    assert Decimal(phase["exact_phase_speed_lower"]) > Decimal("0.9")
    assert Decimal(phase["continuous_projection_norm_upper"]) < Decimal("3")
    assert Decimal(
        phase["phase_chart_continuous_transfer_error_upper"]
    ) < Decimal("1")
    assert Decimal(phase["linear_projection_radius_margin_lower"]) > 0
    assert phase["continuous_linear_phase_projection_validated"]
    assert not phase["nonlinear_phase_chart_on_ambient_tube_validated"]
    errors = certificate["transfer_errors"]
    assert errors["E_phase"] == phase["phase_chart_continuous_transfer_error_upper"]
    assert errors["E_voltage"] is None
    assert errors["E_recovery"] is None


def test_coarse_growth_is_exposed_as_failure_not_transfer(payload):
    failure = payload["certificate"]["coarse_directed_failure"]
    assert failure["phase_partition_count"] == 512
    assert Decimal(failure["full_period_growth_upper"]) > 1
    assert failure["growth_exceeds_stage2_linear_margin"]
    assert failure["not_used_as_transfer_error"]
    frontier = payload["certificate"]["directed_bernstein_frontier"]
    assert frontier["current_reached_partition"] == 512
    assert frontier["current_reached_degree"] == 0
    assert frontier["failure_is_numerical_not_structural"]


def test_claim_ledger_preserves_open_return_claims(payload):
    claims = payload["certificate"]["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    gate = payload["certificate"]["transfer_gate"]
    assert not gate["linear_return_gate_evaluated"]
    assert not gate["arbitrary_c0_linear_contraction_closes"]
    assert gate["linearized_ambient_projection_gate_closes"]
    assert not gate["nonlinear_ambient_phase_chart_gate_closes"]


def _refresh(value):
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"]["claim_status"].update(
            {"arbitrary_c0_linear_return_contraction_validated": True}
        ),
        lambda value: value["certificate"]["transfer_errors"].update(
            {"E_voltage": "0"}
        ),
        lambda value: value["certificate"]["continuous_phase_projection"].update(
            {"nonlinear_phase_chart_on_ambient_tube_validated": True}
        ),
        lambda value: value["certificate"]["coarse_directed_failure"].update(
            {"not_used_as_transfer_error": False}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_promotions_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_outer_delay_word_stage3d_primitives_result(changed, REPOSITORY)


def test_note_has_no_control_characters_or_false_completion():
    text = (
        REPOSITORY / "docs/leaky-outer-delay-word-stage3d-primitives.md"
    ).read_text()
    assert "\t" not in text
    assert all(character in "\n\r" or ord(character) >= 32 for character in text)
    normalized = " ".join(text.split())
    assert "one-dimensional primitives" in normalized
    assert "linear tangent projection result" in normalized
    assert "all remain false" in normalized
