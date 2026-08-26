from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_continuous_kernel_stage3b_frontier import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STAGE3_RESULT_RELATIVE_PATH,
    STAGE3_RESULT_SHA256,
    TRUE_FLAGS,
    canonical_sha256,
    validate_continuous_kernel_stage3b_frontier_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_stage3b_frontier_replays(payload):
    validate_continuous_kernel_stage3b_frontier_result(payload, REPOSITORY)


def test_both_branches_cross_a_genuinely_nonzero_delayed_tile(payload):
    sweeps = payload["certificate"]["branch_sweeps"]
    assert [row["injection_delay_id"] for row in sweeps] == ["tau_0", "tau_1"]
    for row in sweeps:
        crossing = row["first_delayed_crossing_elapsed_cell"]
        assert Decimal(crossing["lower"]) > Decimal("8")
        assert Decimal(crossing["upper"]) > Decimal(crossing["lower"])
        assert Decimal(
            row["first_delayed_forcing_inf_norm_lower_witness"]
        ) > Decimal("4e-4")
        assert Decimal(row["first_delayed_forcing_inf_norm_upper"]) < Decimal(
            "4.6e-4"
        )
        assert row["first_nonzero_delayed_forcing_tile_validated"]


def test_coarse_bridge_is_rigorous_but_not_a_transfer_error(payload):
    sweeps = payload["certificate"]["branch_sweeps"]
    for row in sweeps:
        assert row["coarse_preboundary_tile_count"] == 18
        assert Decimal(row["homogeneous_boundary_growth_upper"]) > Decimal(
            "1e7"
        )
        assert Decimal(row["uncertainty_predecessor_growth_upper"]) >= 1
        assert Decimal(row["uncertainty_bridge_growth_upper"]) >= Decimal(
            row["homogeneous_boundary_growth_upper"]
        )
        assert row["coarse_bridge_not_usable_as_shadow_transfer_error"]


def test_density_tv_uses_the_invariant_path_not_only_the_endpoint(payload):
    for row in payload["certificate"]["branch_sweeps"]:
        endpoint = Decimal(
            row["delayed_crossing_endpoint_density_inf_norm_upper"]
        )
        path = Decimal(row["delayed_crossing_path_density_inf_norm_upper"])
        local_tv = Decimal(
            row["uncorrected_output_diagonal_tile_mass_upper"]
        )
        assert path >= endpoint
        assert local_tv >= Decimal("0.001") * path
        assert local_tv > Decimal("25")


def test_tight_failure_frontier_and_adaptive_depth_are_explicit(payload):
    sweeps = payload["certificate"]["branch_sweeps"]
    assert [row["tight_picard_accepted_tile_count"] for row in sweeps] == [8, 7]
    assert [row["tight_picard_failure_tile_index"] for row in sweeps] == [8, 7]
    for row in sweeps:
        assert Decimal(row["tight_picard_failure_endpoint_norm_upper"]) > Decimal(
            "1e6"
        )
        assert Decimal(row["tight_picard_failure_endpoint_width_upper"]) > Decimal(
            "1e6"
        )
        assert row["failure_step_norm_minimum_dyadic_depth"] >= 1
        assert Decimal(row["failure_step_norm_child_width_upper"]) < Decimal(
            "0.5"
        )


def test_remaining_two_dimensional_queue_is_not_hidden(payload):
    frontier = payload["certificate"]["global_frontier"]
    assert frontier["validated_theta_band_count"] == 1
    assert frontier["total_theta_band_count_at_width_1e_minus_3"] == 11181
    assert frontier["remaining_theta_band_count"] == 11180
    assert frontier["unstarted_branch_theta_chain_count"] == 22360
    assert frontier["current_band_remaining_elapsed_tile_count"] == 31
    assert (
        frontier["nominal_coarse_remaining_2d_tile_count_before_tau1_alignment"]
        > 22360
    )
    assert frontier[
        "tau1_alignment_and_adaptive_child_tiles_not_in_nominal_count"
    ]


def test_parent_and_global_claim_ledgers_remain_exact(payload):
    certificate = payload["certificate"]
    assert (
        certificate["parent_result_sha256"][STAGE3_RESULT_RELATIVE_PATH]
        == STAGE3_RESULT_SHA256
    )
    claims = certificate["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    frontier = certificate["global_frontier"]
    assert frontier["voltage_shadow_transfer_error_upper"] is None
    assert frontier["recovery_shadow_transfer_error_upper"] is None
    assert frontier["phase_chart_shadow_transfer_error_upper"] is None
    assert not frontier["returned_time_window_reached"]
    assert not frontier["phase_subtracted_tv_complete"]


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
        lambda value: value["certificate"]["global_frontier"].update(
            {"voltage_shadow_transfer_error_upper": "0"}
        ),
        lambda value: value["certificate"]["branch_sweeps"][0].update(
            {"first_delayed_forcing_inf_norm_lower_witness": "0"}
        ),
        lambda value: value["certificate"]["branch_sweeps"][1].update(
            {"tight_picard_failure_tile_index": -1}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_promotions_and_frontier_erasure_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_continuous_kernel_stage3b_frontier_result(changed, REPOSITORY)


def test_notes_have_no_control_character_or_global_promotion():
    for relative in (
        "docs/leaky-outer-continuous-kernel-stage3-shard.md",
        "docs/leaky-outer-continuous-kernel-stage3b-frontier.md",
    ):
        text = (REPOSITORY / relative).read_text()
        assert "\t" not in text
        assert all(
            character in "\n\r" or ord(character) >= 32 for character in text
        )
    note = (
        REPOSITORY / "docs/leaky-outer-continuous-kernel-stage3b-frontier.md"
    ).read_text()
    normalized = " ".join(note.split())
    assert "first genuinely delayed forcing" in normalized
    assert "cannot be inserted as" in normalized
    assert "remain empty" in normalized
    assert "all remain false" in normalized
