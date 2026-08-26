from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import shutil
from inspect import signature

import pytest

import canard_control.leaky_outer_signed_density_stage3i_tv as stage3i
from canard_control.leaky_outer_signed_density_stage3i_tv import (
    BASE_TRUE_FLAGS,
    CENTER_EXCESS_SEMANTICS,
    CENTER_TRANSFER_TARGET,
    CLOSURE_FLAGS,
    CONCLUSION_TARGET_OPEN_CONTRACTION_CLOSED,
    FALSE_FLAGS,
    LAG_SEAM_ENDPOINT_CONVENTION,
    RESULT_RELATIVE_PATH,
    ROW_SCOPE,
    STAGE3G_RESULT_RELATIVE_PATH,
    STAGE3G_RESULT_SHA256,
    STAGE3H_RESULT_RELATIVE_PATH,
    STAGE3H_RESULT_SHA256,
    TOTAL_ROW_BUDGET_SEMANTICS,
    _candidate_excess_records,
    _lag_chart_indices,
    _load_parent,
    _require_unique_disjoint_flags,
    _stage3i_geometry_preflight,
    _transfer_rows_from_excess_records,
    _validate_parent_artifact_lock,
    canonical_sha256,
    validate_outer_signed_density_stage3i_tv_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def _refresh_certificate_digest(value: dict) -> None:
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


def _reject_before_replay(
    changed: dict, monkeypatch: pytest.MonkeyPatch, match: str
) -> None:
    def forbidden(_: Path) -> object:
        raise AssertionError("an invalid Stage-3I payload reached full replay")

    monkeypatch.setattr(stage3i, "build_outer_signed_density_stage3i_tv", forbidden)
    with pytest.raises(ValueError, match=match):
        validate_outer_signed_density_stage3i_tv_result(changed, REPOSITORY)


def _parent_certificate(relative: str) -> dict:
    return json.loads((REPOSITORY / relative).read_text())["certificate"]


def test_frozen_stage3g_and_stage3h_parents_are_exact_and_source_bound() -> None:
    for label, relative, digest, schema in (
        (
            "Stage-3G",
            STAGE3G_RESULT_RELATIVE_PATH,
            STAGE3G_RESULT_SHA256,
            stage3i.STAGE3G_SCHEMA_ID,
        ),
        (
            "Stage-3H",
            STAGE3H_RESULT_RELATIVE_PATH,
            STAGE3H_RESULT_SHA256,
            stage3i.STAGE3H_SCHEMA_ID,
        ),
    ):
        path = REPOSITORY / relative
        assert sha256(path.read_bytes()).hexdigest() == digest
        parent = _load_parent(REPOSITORY, relative, digest)
        _validate_parent_artifact_lock(
            parent,
            REPOSITORY,
            label=label,
            schema_id=schema,
            result_relative_path=relative,
        )


def test_complete_directed_lag_geometry_preflight() -> None:
    stage3g = _parent_certificate(STAGE3G_RESULT_RELATIVE_PATH)
    geometry = stage3g["tensor_geometry"]
    period = float.fromhex(geometry["guide_period_binary64_hex"])
    h = float.fromhex(geometry["mesh_width_binary64_hex"])
    preflight = _stage3i_geometry_preflight(period, h)
    assert preflight["delta_history_rectangle_count"] == 25600
    assert preflight["seam_union_rectangle_count"] == 8800
    assert preflight["maximum_lag_chart_multiplicity"] == 16
    assert preflight["recovery_seam_subinterval_count"] == 20
    assert preflight["requested_lag_interval_count"] == 92900
    assert preflight["delay_mesh_widths"] == [16, 20]
    assert preflight["all_requested_lag_intervals_in_domain"] is True
    assert preflight["lag_seam_endpoint_convention"] == (
        LAG_SEAM_ENDPOINT_CONVENTION
    )


def test_lag_chart_domain_and_endpoint_convention_are_hostile() -> None:
    assert _lag_chart_indices(0, Fraction(1), Fraction(2)) == (1, 2)
    assert _lag_chart_indices(0, Fraction(48), Fraction(48)) == (47,)
    with pytest.raises(ValueError, match="reversed"):
        _lag_chart_indices(0, Fraction(2), Fraction(1))
    with pytest.raises(ValueError, match="left the Stage-3G domain"):
        _lag_chart_indices(0, Fraction(-1, 100), Fraction(1))
    with pytest.raises(ValueError, match="left the Stage-3G domain"):
        _lag_chart_indices(1, Fraction(1), Fraction(48))


def test_exact_target_delay_binding_and_denominator_guard_are_static() -> None:
    assert CENTER_TRANSFER_TARGET == "0.01"
    source = (REPOSITORY / stage3i.SOURCE_RELATIVE_PATH).read_text()
    assert "float(CENTER_TRANSFER_TARGET)" not in source
    assert "center_target.lower()" in source
    assert "alpha_denominator.lower() > 0" in source
    assert "the Stage-3I 16h/20h delay geometry changed" in source
    assert source.count("history_width = h_arb * _arb_fraction(") == 2
    assert "_exact_arb_float(float(history_upper" not in source
    environment = stage3i._expected_environment()
    assert environment["mpfr_directed_precision_bits"] == 192
    assert environment["mpfr"].startswith("MPFR ")
    assert environment["openblas_num_threads"] == "1"
    assert environment["omp_num_threads"] == "1"


def test_flag_registries_are_unique_disjoint_and_semantically_split() -> None:
    _require_unique_disjoint_flags(
        ("base", BASE_TRUE_FLAGS),
        ("closure", CLOSURE_FLAGS),
        ("false", FALSE_FLAGS),
    )
    assert "continuous_signed_density_total_variation_validated" in BASE_TRUE_FLAGS
    assert "voltage_exact_row_budget_validated" in BASE_TRUE_FLAGS
    assert "recovery_exact_row_budget_validated" in BASE_TRUE_FLAGS
    assert "continuous_center_signed_density_TV_reserve_validated" in CLOSURE_FLAGS
    assert "arbitrary_c0_linear_return_contraction_validated" in CLOSURE_FLAGS
    with pytest.raises(ValueError, match="duplicates"):
        _require_unique_disjoint_flags(("a", ("x", "x")), ("b", ("y",)))
    with pytest.raises(ValueError, match="overlap"):
        _require_unique_disjoint_flags(("a", ("x",)), ("b", ("x",)))


def test_once_only_transfer_formula_uses_serialized_candidate_slack() -> None:
    stage3h = _parent_certificate(STAGE3H_RESULT_RELATIVE_PATH)
    stage3g = _parent_certificate(STAGE3G_RESULT_RELATIVE_PATH)
    stage3f = _parent_certificate(stage3i.STAGE3F_RESULT_RELATIVE_PATH)
    stage2 = _parent_certificate(stage3i.STAGE2_RESULT_RELATIVE_PATH)
    excess = {"voltage": "0.009", "recovery": "0.008"}
    rows, _, _ = _transfer_rows_from_excess_records(
        excess, stage3h, stage3g, stage3f, stage2
    )
    for row_id in ("voltage", "recovery"):
        row = rows[row_id]
        assert row["candidate_row_excess_over_stage2_shadow_upper"] == excess[
            row_id
        ]
        assert Decimal(row["E_row_upper"]) > Decimal(excess[row_id])
        assert row["strictly_below_one"] is True


def test_parent_source_lock_rechecks_files_without_a_warm_cache(tmp_path: Path) -> None:
    payload = json.loads((REPOSITORY / STAGE3H_RESULT_RELATIVE_PATH).read_text())
    for relative in payload["manifest"]["source_sha256"]:
        source = REPOSITORY / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    _validate_parent_artifact_lock(
        payload,
        tmp_path,
        label="Stage-3H",
        schema_id=stage3i.STAGE3H_SCHEMA_ID,
        result_relative_path=STAGE3H_RESULT_RELATIVE_PATH,
    )
    relative = next(iter(payload["manifest"]["source_sha256"]))
    (tmp_path / relative).write_bytes((tmp_path / relative).read_bytes() + b"\n")
    with pytest.raises(ValueError, match="runtime source changed"):
        _validate_parent_artifact_lock(
            payload,
            tmp_path,
            label="Stage-3H",
            schema_id=stage3i.STAGE3H_SCHEMA_ID,
            result_relative_path=STAGE3H_RESULT_RELATIVE_PATH,
        )

    result_target = tmp_path / STAGE3H_RESULT_RELATIVE_PATH
    result_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPOSITORY / STAGE3H_RESULT_RELATIVE_PATH, result_target)
    _load_parent(
        tmp_path, STAGE3H_RESULT_RELATIVE_PATH, STAGE3H_RESULT_SHA256
    )
    result_target.write_bytes(result_target.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="parent changed"):
        _load_parent(
            tmp_path, STAGE3H_RESULT_RELATIVE_PATH, STAGE3H_RESULT_SHA256
        )


def test_generator_is_fsync_atomic_and_validation_is_a_fresh_replay() -> None:
    generator = (REPOSITORY / stage3i.GENERATOR_RELATIVE_PATH).read_text()
    atomic = generator.index("def _atomic_write(")
    temporary = generator.index("NamedTemporaryFile(")
    replacement = generator.index("temporary_path.replace(result_path)")
    main = generator.index("def main()")
    assert atomic < temporary < replacement < main
    assert generator.count("os.fsync(") >= 2
    default_branch = generator.index(
        "else:\n        payload = build_outer_signed_density_stage3i_tv_result("
    )
    validation = generator.index(
        "validate_outer_signed_density_stage3i_tv_result(", default_branch
    )
    write = generator.index("_atomic_write(result_path, payload)", validation)
    assert default_branch < validation < write
    assert "--reissue-frozen-cells" in generator
    assert "result_path.read_bytes()" in generator
    source = (REPOSITORY / stage3i.SOURCE_RELATIVE_PATH).read_text()
    cache_clear = source.index("build_outer_signed_density_stage3i_tv.cache_clear()")
    replay = source.index(
        "asdict(build_outer_signed_density_stage3i_tv(repository))", cache_clear
    )
    assert cache_clear < replay
    assert "replay_numerics" not in signature(
        validate_outer_signed_density_stage3i_tv_result
    ).parameters
    with pytest.raises(ValueError, match="prefinal cell artifact changed"):
        stage3i.reissue_outer_signed_density_stage3i_tv_result(
            REPOSITORY, b"{}\n"
        )


def test_complete_cell_cover_and_signed_order(payload: dict) -> None:
    certificate = payload["certificate"]
    geometry = certificate["cell_geometry"]
    assert geometry["delta_subinterval_count"] == 160
    assert geometry["history_subinterval_count"] == 160
    assert geometry["delta_history_rectangle_count"] == 25600
    assert geometry["point_samples_used_as_proof"] is False
    assert geometry["all_requested_lag_intervals_in_domain"] is True
    rows = certificate["candidate_continuous_rows"]
    assert rows["both_injection_branches_summed_before_absolute_value"]
    assert rows["phase_subtraction_inside_each_density_interval"]
    assert certificate["row_scope"] == ROW_SCOPE


def test_one_sided_slack_and_unconditional_error_ledger(payload: dict) -> None:
    certificate = payload["certificate"]
    candidate = certificate["candidate_continuous_rows"]
    stage2 = _parent_certificate(stage3i.STAGE2_RESULT_RELATIVE_PATH)
    expected_excess = _candidate_excess_records(candidate, stage2)
    ledger = certificate["transfer_ledger"]
    assert ledger["candidate_row_excess_semantics"] == CENTER_EXCESS_SEMANTICS
    assert ledger["total_row_budget_semantics"] == TOTAL_ROW_BUDGET_SEMANTICS
    assert ledger["voltage_candidate_row_excess_over_shadow_upper"] == (
        expected_excess["voltage"]
    )
    assert ledger["recovery_candidate_row_excess_over_shadow_upper"] == (
        expected_excess["recovery"]
    )
    assert certificate["transfer_errors"]["E_voltage"] is not None
    assert certificate["transfer_errors"]["E_recovery"] is not None
    assert certificate["transfer_gate"]["linear_return_gate_evaluated"] is True
    assert certificate["transfer_gate"][
        "continuous_signed_density_total_variation_validated"
    ] is True


def test_claim_ledger_matches_two_distinct_outcomes(payload: dict) -> None:
    certificate = payload["certificate"]
    gate = certificate["transfer_gate"]
    claims = certificate["claim_status"]
    assert all(claims[name] is True for name in BASE_TRUE_FLAGS)
    assert claims["continuous_center_signed_density_TV_reserve_validated"] is gate[
        "continuous_center_signed_density_TV_reserve_validated"
    ]
    assert claims["arbitrary_c0_linear_return_contraction_validated"] is gate[
        "arbitrary_c0_linear_contraction_closes"
    ]
    assert all(claims[name] is False for name in FALSE_FLAGS)


def test_auxiliary_reserve_failure_is_decoupled_from_contraction(
    payload: dict,
) -> None:
    certificate = payload["certificate"]
    ledger = certificate["transfer_ledger"]
    gate = certificate["transfer_gate"]
    claims = certificate["claim_status"]
    assert ledger["candidate_row_excess_target_closes"] is False
    assert gate["continuous_center_signed_density_TV_reserve_validated"] is False
    assert all(
        ledger["rows"][row_id]["strictly_below_one"] is True
        for row_id in ("voltage", "recovery")
    )
    assert all(
        Decimal(ledger["rows"][row_id]["stage2_shadow_plus_E_upper"]) < 1
        for row_id in ("voltage", "recovery")
    )
    assert ledger["arbitrary_c0_linear_contraction_closes"] is True
    assert gate["arbitrary_c0_linear_contraction_closes"] is True
    assert claims["arbitrary_c0_linear_return_contraction_validated"] is True
    assert certificate["conclusion"] == (
        CONCLUSION_TARGET_OPEN_CONTRACTION_CLOSED
    )


def test_nonlinear_claims_remain_false(payload: dict) -> None:
    gate = payload["certificate"]["transfer_gate"]
    assert gate["nonlinear_outer_attraction_closes"] is False
    claims = payload["certificate"]["claim_status"]
    assert claims["outer_pulse_capture_validated"] is False
    assert claims["physical_pulse_onset_validated"] is False


def test_result_replays_source_bound_and_fresh(payload: dict) -> None:
    validate_outer_signed_density_stage3i_tv_result(payload, REPOSITORY)


def test_source_manifest_and_environment_hostiles(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    source = next(iter(changed["manifest"]["source_sha256"]))
    changed["manifest"]["source_sha256"][source] = "0" * 64
    _reject_before_replay(changed, monkeypatch, "source changed")

    changed = deepcopy(payload)
    changed["manifest"]["environment"]["arb_precision_bits"] = 191
    _reject_before_replay(changed, monkeypatch, "environment changed")

    changed = deepcopy(payload)
    changed["manifest"]["extra"] = None
    _reject_before_replay(changed, monkeypatch, "manifest schema changed")


def test_parent_geometry_and_range_seam_hostiles(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["parent_result_sha256"][
        STAGE3H_RESULT_RELATIVE_PATH
    ] = "0" * 64
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "parent digest map changed")

    changed = deepcopy(payload)
    geometry = changed["certificate"]["cell_geometry"]
    geometry["seam_union_rectangle_count"] -= 1
    geometry["requested_lag_interval_count"] += 1
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "directed lag geometry changed")

    changed = deepcopy(payload)
    changed["certificate"]["cell_geometry"][
        "lag_seam_endpoint_convention"
    ] += "; both lower charts"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "directed lag geometry changed")


def test_target_candidate_slack_and_transfer_formula_hostiles(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["transfer_ledger"][
        "candidate_row_excess_target"
    ] = 0.01
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "center-reserve semantics changed")

    changed = deepcopy(payload)
    candidate = changed["certificate"]["candidate_continuous_rows"]
    candidate["voltage_history_density_TV_upper"] = str(
        Decimal(candidate["voltage_history_density_TV_upper"]) + 1
    )
    candidate["voltage_total_row_upper"] = str(
        Decimal(candidate["voltage_total_row_upper"]) + 1
    )
    stage2 = _parent_certificate(stage3i.STAGE2_RESULT_RELATIVE_PATH)
    excess = _candidate_excess_records(candidate, stage2)
    changed["certificate"]["transfer_ledger"][
        "voltage_candidate_row_excess_over_shadow_upper"
    ] = excess["voltage"]
    changed["certificate"]["transfer_ledger"][
        "candidate_row_excess_target_closes"
    ] = False
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "once-only transfer formula")

    changed = deepcopy(payload)
    changed["certificate"]["transfer_ledger"]["rows"]["voltage"][
        "candidate_residual_and_atom_transfer_upper"
    ] = "0"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "once-only transfer formula")


def test_gate_claim_conclusion_and_nested_schema_hostiles(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["transfer_gate"][
        "nonlinear_outer_attraction_closes"
    ] = True
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "transfer gate ledger changed")

    changed = deepcopy(payload)
    changed["certificate"]["transfer_ledger"][
        "arbitrary_c0_linear_contraction_closes"
    ] = False
    changed["certificate"]["transfer_gate"][
        "arbitrary_c0_linear_contraction_closes"
    ] = False
    changed["certificate"]["claim_status"][
        "arbitrary_c0_linear_return_contraction_validated"
    ] = False
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "linear contraction ledger")

    changed = deepcopy(payload)
    changed["certificate"]["claim_status"]["physical_pulse_onset_validated"] = (
        True
    )
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "claim ledger changed")

    changed = deepcopy(payload)
    changed["certificate"]["conclusion"] += "; nonlinear onset proved"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "conclusion changed")

    changed = deepcopy(payload)
    changed["certificate"]["candidate_continuous_rows"]["extra"] = "0"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "candidate rows schema changed")
