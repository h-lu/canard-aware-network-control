from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/leaky_floquet_outer_right_half_cover_calibration.json"
)


def _sha256(relative: str) -> str:
    return sha256((REPOSITORY / relative).read_bytes()).hexdigest()


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_calibration_is_source_bound_but_not_a_theorem_artifact() -> None:
    payload = _payload()
    calibration = payload["calibration"]
    manifest = payload["manifest"]
    assert calibration["schema_id"] == (
        "leaky-floquet-outer-right-half-cover-calibration-v1"
    )
    assert calibration["calibration_is_not_a_theorem_artifact"]
    for path_key, digest_key in (
        ("engine_source", "engine_source_sha256"),
        ("shared_arithmetic_source", "shared_arithmetic_source_sha256"),
        ("riesz_result", "riesz_result_sha256"),
        ("outer_orbit_result", "outer_orbit_result_sha256"),
        ("calibration_note", "calibration_note_sha256"),
    ):
        assert _sha256(manifest[path_key]) == manifest[digest_key]


def test_true_rectilinear_core_has_one_fixed_local_leaf() -> None:
    payload = _payload()
    ownership = payload["calibration"]["local_ownership"]
    assert ownership == {
        "complement_descendants_always_use_full_neumann": True,
        "local_leaf_count_required": 1,
        "local_path": "",
        "local_root_id": "neutral_core",
        "neutral_core_size": "0.002",
        "superseded_circular_shortcut_rejected": True,
    }
    for run in payload["calibration"]["runs"]:
        assert run["local_disk_leaf_count"] == 1
        assert run["accepted_leaf_count"] == (
            run["local_disk_leaf_count"] + run["neumann_leaf_count"]
        )


def test_equal_budget_threshold_relaxation_is_ineffective() -> None:
    calibration = _payload()["calibration"]
    runs = {
        (run["processed_cell_count"], run["acceptance_threshold"]): run
        for run in calibration["runs"]
    }
    low = runs[(5000, "0.999")]
    high = runs[(5000, "0.9999")]
    assert low["accepted_leaf_count"] == high["accepted_leaf_count"] == 2482
    assert low["pending_cell_count"] == high["pending_cell_count"] == 39
    low_area = Fraction(low["accepted_normalized_area_fraction"])
    high_area = Fraction(high["accepted_normalized_area_fraction"])
    with localcontext() as context:
        context.prec = 80
        ratio = (
            Decimal(high_area.numerator)
            / Decimal(high_area.denominator)
            / (Decimal(low_area.numerator) / Decimal(low_area.denominator))
        )
        percent = (ratio - 1) * 100
    comparison = calibration["threshold_comparison"]
    assert ratio == Decimal(
        comparison["accepted_normalized_area_ratio_09999_over_0999"]
    )
    assert percent == Decimal(
        comparison["accepted_normalized_area_relative_gain_percent"]
    )
    assert percent < Decimal("0.022")
    assert not comparison["brute_force_300000_run_started"]


def test_binary_grushin_numbers_do_not_promote_any_claim() -> None:
    payload = _payload()
    diagnostic = payload["calibration"][
        "nonclaim_binary64_grushin_diagnostic"
    ]
    assert not diagnostic["rigorous_or_directed"]
    assert Decimal(diagnostic["finite_smallest_singular_value"]) < Decimal(
        "1e-12"
    )
    assert Decimal(diagnostic["finite_second_smallest_singular_value"]) > 1
    assert Decimal(diagnostic["candidate_effective_slope_modulus"]) > 0
    for value in payload["claim_ledger"].values():
        assert value is False or value is None
    assert payload["claim_ledger"][
        "outer_directed_nontranslation_right_half_zero_count"
    ] is None
