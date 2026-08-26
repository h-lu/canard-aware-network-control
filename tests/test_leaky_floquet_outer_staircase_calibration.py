from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_floquet_outer_staircase_calibration import (
    FALSE_CLAIMS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STAIRCASE_BANDS,
    canonical_sha256,
    validate_outer_staircase_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_staircase_calibration_replays(payload):
    validate_outer_staircase_result(payload, REPOSITORY)


def test_exact_predetermined_ownership_contract(payload):
    calibration = payload["calibration"]
    assert calibration["staircase_band_count"] == len(STAIRCASE_BANDS) == 8
    assert calibration["local_root_count"] == 8
    assert calibration["complement_root_count"] == 9
    assert calibration["total_root_count"] == 17
    for name in (
        "exact_root_partition_validated",
        "every_local_upper_corner_strictly_inside_parent_disk",
        "local_roots_accepted_only_at_empty_path",
        "complement_descendants_always_use_full_neumann",
    ):
        assert calibration[name] is True
    assert float(calibration["parent_local_complex_exclusion_radius_lower"]) > 0.0028635


def test_low_band_contains_the_previous_pending_envelope(payload):
    calibration = payload["calibration"]
    assert float(calibration["low_band_real_ceiling"]) == 0.00274
    assert float(calibration["low_band_phase_upper"]) == 0.0008
    assert float(calibration["low_band_real_ceiling"]) > float(
        calibration["low_band_covers_previous_pending_real_upper"]
    )
    assert float(calibration["low_band_phase_upper"]) > float(
        calibration["low_band_covers_previous_pending_phase_upper"]
    )


def test_equal_budget_comparison_remains_claim_free(payload):
    calibration = payload["calibration"]
    runs = calibration["runs"]
    assert [run["maximum_processed_cells"] for run in runs] == [200, 5000]
    assert all(run["local_parent_leaf_count"] == 8 for run in runs)
    assert all(len(run["root_diagnostics"]) == 17 for run in runs)
    assert all(
        diagnostic["processed_cell_count"] > 0
        for diagnostic in runs[-1]["root_diagnostics"]
    )
    assert calibration["breadth_first_all_complement_roots_receive_budget"]
    assert not calibration["old_depth_first_pending_count_direct_comparison_valid"]
    assert calibration["final_accepted_area_exceeds_95_percent"]
    assert float(runs[-1]["accepted_normalized_area_decimal"]) > 0.958
    assert calibration["calibration_is_not_a_theorem_artifact"] is True
    for name in FALSE_CLAIMS:
        assert calibration[name] is False
    final = runs[-1]
    if final["pending_cell_count"]:
        assert not final["calibration_cover_complete"]
        assert not final["prefix_complete"]
        assert not final["exact_area_complete"]


def _refresh(value):
    value["manifest"]["calibration_sha256"] = canonical_sha256(
        value["calibration"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["calibration"].update(
            {"every_local_upper_corner_strictly_inside_parent_disk": False}
        ),
        lambda value: value["calibration"].update(
            {"complement_descendants_always_use_full_neumann": False}
        ),
        lambda value: value["calibration"].update(
            {"outer_attracting_floquet_index_validated": True}
        ),
        lambda value: value["calibration"].update(
            {"physical_pulse_onset_validated": True}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_mutations_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_outer_staircase_result(changed, REPOSITORY)


def test_note_preserves_calibration_scope():
    text = (
        REPOSITORY / "docs/leaky-floquet-outer-staircase-calibration.md"
    ).read_text()
    normalized = " ".join(text.split())
    assert "calibration, not a theorem artifact" in normalized
    assert "exact fraction arithmetic" in normalized
    assert "complete infinite-operator Neumann" in normalized
    assert "outer attracting Floquet index" in normalized
    assert "physical pulse onset" in normalized
