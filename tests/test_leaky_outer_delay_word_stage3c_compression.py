from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_delay_word_stage3c_compression import (
    FALSE_FLAGS,
    FINITE_SECTION_STEPS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    canonical_sha256,
    validate_outer_delay_word_stage3c_compression_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_stage3c_compression_replays(payload):
    validate_outer_delay_word_stage3c_compression_result(payload, REPOSITORY)


def test_exact_word_lists_replace_the_nominal_grid(payload):
    certificate = payload["certificate"]
    branches = certificate["history_density_word_branches"]
    assert branches[0]["possible_word_ids"] == [
        "empty", "0", "1", "00", "01", "10", "11"
    ]
    assert branches[1]["possible_word_ids"] == [
        "empty", "0", "1", "00", "01", "10", "11"
    ]
    assert certificate["recovery_scalar_word_branch"]["possible_word_ids"] == [
        "empty", "0", "1", "00", "01", "10", "11"
    ]
    assert certificate["history_density_word_term_count"] == 14
    assert certificate["recovery_scalar_word_term_count"] == 7
    assert certificate["total_phase_fixed_word_term_count"] == 21
    assert Decimal(certificate["nominal_tile_to_word_term_ratio_lower"]) > 40000
    for branch in branches + [certificate["recovery_scalar_word_branch"]]:
        assert Decimal(
            branch["three_minimum_delays_exceed_horizon_margin_lower"]
        ) > 0
        assert branch["complete_finite_word_list_validated"]


def test_binary_low_rank_and_sign_data_remain_diagnostic(payload):
    rows = payload["certificate"]["shadow_compression_diagnostics"]
    assert [row["step_count"] for row in rows] == list(FINITE_SECTION_STEPS)
    for row in rows:
        ratio = float.fromhex(
            row["rank_one_row_residual_ratio_binary64"]["binary64_hex"]
        )
        assert 0 < ratio < 0.001
        assert row["every_sign_change_inside_two_declared_windows"]
        assert row["normalized_sign_template_on_three_safe_regions"] == [1, -1, 1]
        assert row["normalized_sign_template_common_to_every_output_row"]
        assert row["diagnostic_only"]


def test_strict_numeric_budgets_are_positive_but_not_filled(payload):
    certificate = payload["certificate"]
    budget = certificate["strict_transfer_error_budget"]
    assert Decimal(budget["voltage_error_strict_ceiling"]) > Decimal("0.87")
    assert Decimal(budget["recovery_error_strict_ceiling"]) > Decimal("0.99")
    assert Decimal(budget["phase_error_strict_ceiling"]) > Decimal("1.8")
    gap = certificate["minimum_remaining_gap"]
    assert gap["maximum_nested_integral_dimension"] == 2
    assert gap["all_length_three_words_excluded"]
    assert all(
        value is None for value in gap["continuous_transfer_errors"].values()
    )
    assert not gap["linear_gate_re_evaluated"]
    assert not gap["phase_entry_gate_re_evaluated"]


def test_claim_ledger_preserves_every_open_global_claim(payload):
    claims = payload["certificate"]["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


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
        lambda value: value["certificate"]["minimum_remaining_gap"][
            "continuous_transfer_errors"
        ].update({"E_voltage": "0"}),
        lambda value: value["certificate"]["history_density_word_branches"][0].update(
            {"possible_word_ids": ["empty"]}
        ),
        lambda value: value["certificate"]["shadow_compression_diagnostics"][0].update(
            {"diagnostic_only": False}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_promotions_and_word_erasure_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_outer_delay_word_stage3c_compression_result(changed, REPOSITORY)


def test_note_has_no_control_character_or_false_promotion():
    text = (
        REPOSITORY / "docs/leaky-outer-delay-word-stage3c-compression.md"
    ).read_text()
    assert "\t" not in text
    assert all(character in "\n\r" or ord(character) >= 32 for character in text)
    normalized = " ".join(text.split())
    assert "14 history-density word terms" in normalized
    assert "seven scalar-column word terms" in normalized
    assert "remain null" in normalized
    assert "all remain false" in normalized
