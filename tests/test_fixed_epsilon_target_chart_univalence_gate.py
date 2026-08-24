"""Tests for the target-chart P-matrix univalence gate."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

import canard_control.fixed_epsilon_target_causal_tube_candidate as legacy
from canard_control.fixed_epsilon_target_chart_univalence_gate import (
    EXACT_TRUE_FLAGS,
    NUMERICAL_TRUE_FLAGS,
    OPEN_FLAGS,
    PMatrixIntervalCell,
    exact_history_gate,
    solve_target_c4_causal_tube,
    solve_target_variational_dde,
    validate_p_matrix_interval_cover,
    validate_target_chart_univalence_gate_audit,
    validate_target_chart_univalence_gate_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_target_chart_univalence_gate.json"
)


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _cell(
    t0: str, t1: str, l0: str, l1: str, margin: str = "0.1"
) -> PMatrixIntervalCell:
    return PMatrixIntervalCell(t0, t1, l0, l1, margin, margin, margin)


def test_exact_history_gate_has_rational_strict_margins() -> None:
    gate = exact_history_gate()
    assert gate.smooth_step_derivative_upper == "2"
    assert gate.preparation_bump_derivative_absolute_upper == "3"
    assert gate.first_principal_minor_lower == "7/20"
    assert gate.determinant_lower == "7/20"
    assert gate.history_frame_determinant == -1


def test_strict_interval_schema_accepts_an_exact_complete_cover() -> None:
    cells = [
        _cell("0", "1", "-1", "0", "0.2"),
        _cell("0", "1", "0", "1", "0.3"),
        _cell("1", "2", "-1", "0", "0.4"),
        _cell("1", "2", "0", "1", "0.5"),
    ]
    margins = validate_p_matrix_interval_cover(
        cells, time_nodes=("0", "1", "2"), lambda_nodes=("-1", "0", "1")
    )
    assert tuple(map(str, margins)) == ("0.2", "0.2", "0.2")


def test_interval_schema_rejects_holes_duplicates_and_nonstrict_data() -> None:
    complete = [
        _cell("0", "1", "-1", "0"),
        _cell("0", "1", "0", "1"),
        _cell("1", "2", "-1", "0"),
        _cell("1", "2", "0", "1"),
    ]
    with pytest.raises(ValueError, match="exact grid"):
        validate_p_matrix_interval_cover(
            complete[:-1],
            time_nodes=("0", "1", "2"),
            lambda_nodes=("-1", "0", "1"),
        )
    with pytest.raises(ValueError, match="duplicate"):
        validate_p_matrix_interval_cover(
            complete + [complete[0]],
            time_nodes=("0", "1", "2"),
            lambda_nodes=("-1", "0", "1"),
        )
    hostile = list(complete)
    hostile[0] = _cell("0", "1", "-1", "0", "0")
    with pytest.raises(ValueError, match="strict"):
        validate_p_matrix_interval_cover(
            hostile,
            time_nodes=("0", "1", "2"),
            lambda_nodes=("-1", "0", "1"),
        )
    with pytest.raises(ValueError, match="finite"):
        validate_p_matrix_interval_cover(
            complete,
            time_nodes=("0", "NaN", "2"),
            lambda_nodes=("-1", "0", "1"),
        )


def test_result_keeps_binary64_margins_separate_from_open_interval_gates() -> None:
    certificate = _result()["audit"]["certificate"]
    assert all(certificate[key] is True for key in EXACT_TRUE_FLAGS)
    assert all(certificate[key] is True for key in NUMERICAL_TRUE_FLAGS)
    assert all(certificate[key] is False for key in OPEN_FLAGS)
    physical = certificate["binary64_physical_gate"]
    history = certificate["binary64_c4_history_gate"]
    assert float(history["minimum_time_principal_minor"]) > 0.36
    assert float(history["minimum_lambda_principal_minor"]) > 0.97
    assert float(history["minimum_oriented_determinant"]) > 0.44
    assert float(physical["minimum_time_principal_minor"]) > 0.25
    assert float(physical["minimum_lambda_principal_minor"]) >= 1.0
    assert float(physical["minimum_oriented_determinant"]) > 1.49
    assert float(physical["maximum_raw_chart_determinant"]) < -0.11
    assert float(physical["maximum_early_x_time_derivative"]) < -0.44
    assert float(physical["minimum_late_entry_x_gap"]) > 0.46
    assert certificate["interval_cell_count"] == 0
    assert certificate["c4_history_interval_cell_count"] == 0


def test_combined_solvers_never_call_the_legacy_preparation(monkeypatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("legacy preparation was called")

    monkeypatch.setattr(legacy, "prepared_history_state", forbidden)
    monkeypatch.setattr(legacy, "prepared_history_transverse_derivative", forbidden)
    monkeypatch.setattr(legacy, "solve_target_causal_tube", forbidden)
    configuration = legacy.TargetTubeConfiguration(transverse_sample_count=5)
    base = solve_target_c4_causal_tube(4.0, configuration)
    variation = solve_target_variational_dde(base, 4.0)
    assert base.states(configuration.incoming_time - 0.25).shape == (5, 2)
    assert variation.variations(configuration.incoming_time - 0.25).shape == (5, 2)
    assert variation.variations(configuration.outgoing_time).shape == (5, 2)


def test_ledger_rejects_numerical_weakening_and_interval_promotion() -> None:
    audit = _result()["audit"]
    weakened = deepcopy(audit)
    weakened["certificate"][NUMERICAL_TRUE_FLAGS[0]] = False
    with pytest.raises(ValueError, match="binary64"):
        validate_target_chart_univalence_gate_audit(weakened)
    promoted = deepcopy(audit)
    promoted["certificate"][OPEN_FLAGS[0]] = True
    with pytest.raises(ValueError, match="promoted"):
        validate_target_chart_univalence_gate_audit(promoted)


def test_result_manifest_and_reference_revalidate() -> None:
    validate_target_chart_univalence_gate_result(_result(), REPOSITORY)
