from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_nonlinear_tube_stage6a import (
    EXPECTED_NUMERIC_CORE_SHA256,
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_RELATIVE_PATH,
    TRUE_FLAGS,
    canonical_sha256,
    validate_stage6a_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def _refresh(payload: dict) -> None:
    digest = canonical_sha256(payload["certificate"])
    payload["manifest"]["numeric_core_sha256"] = digest
    payload["manifest"]["certificate_sha256"] = digest


def test_registered_stage6a_result_validates() -> None:
    validate_stage6a_result(_payload(), REPOSITORY)


def test_stage6a_frozen_numeric_core_is_filled() -> None:
    assert EXPECTED_NUMERIC_CORE_SHA256 != "TO_BE_FILLED"
    assert len(EXPECTED_NUMERIC_CORE_SHA256) == 64
    assert _payload()["manifest"]["numeric_core_sha256"] == (
        EXPECTED_NUMERIC_CORE_SHA256
    )


def test_stage6a_closes_only_the_tiny_nonlinear_outer_tube() -> None:
    certificate = _payload()["certificate"]
    claims = certificate["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    tube = certificate["nonlinear_return_tube"]
    assert tube["section_radius"] == "1e-335"
    assert tube["nonlinear_return_contraction_closes"] is True
    assert tube["full_history_invariance_closes"] is True
    assert tube["biological_attachment_closes"] is False


def test_stage6a_phase_cover_is_directed_and_complete() -> None:
    phase = _payload()["certificate"]["phase_cover"]
    assert phase["normalized_phase_cell_count"] == 256
    assert phase["middle_phase_cell_count"] == 254
    assert phase["point_samples_used_as_proof"] is False
    assert phase["candidate_coefficients_treated_as_exact_binary64_dyadics"] is True
    assert phase["period_correction_included_in_exact_history_transfer"] is True
    assert phase["all_middle_cells_separated"] is True
    assert phase["both_wrap_cells_strictly_positive"] is True


def test_stage6a_records_exact_first_biological_failure() -> None:
    audit = _payload()["certificate"]["nonlinear_return_tube"][
        "J_0p32_attachment_audit"
    ]
    assert audit["inside_stage6a_phase_chart_domain"] is False
    assert audit["same_exact_section_parent_gate"] is False
    assert audit["outer_capture_closes"] is False
    assert "ambient-to-section domain containment" in audit["first_failed_gate"]


def test_hostile_smaller_return_hessian_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["nonlinear_return_tube"][
        "return_second_derivative_upper"
    ] = "1"
    _refresh(payload)
    with pytest.raises(ValueError, match="frozen numeric core"):
        validate_stage6a_result(payload, REPOSITORY)


def test_hostile_larger_section_radius_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["nonlinear_return_tube"]["section_radius"] = "1e-4"
    _refresh(payload)
    with pytest.raises(ValueError, match="frozen numeric core"):
        validate_stage6a_result(payload, REPOSITORY)


def test_hostile_capture_promotion_is_rejected() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"]["outer_pulse_capture_validated"] = True
    _refresh(payload)
    with pytest.raises(ValueError, match="open biological claim"):
        validate_stage6a_result(payload, REPOSITORY)


def test_hostile_no_earlier_hit_removal_is_rejected() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["nonlinear_return_tube"][
        "no_earlier_local_hit_closes"
    ] = False
    _refresh(payload)
    with pytest.raises(ValueError, match="no_earlier_local_hit_closes"):
        validate_stage6a_result(payload, REPOSITORY)


def test_hostile_parent_digest_is_rejected() -> None:
    payload = deepcopy(_payload())
    key = next(iter(payload["certificate"]["parent_result_sha256"]))
    payload["certificate"]["parent_result_sha256"][key] = "0" * 64
    _refresh(payload)
    with pytest.raises(ValueError, match="parent map"):
        validate_stage6a_result(payload, REPOSITORY)


def test_stage6a_source_has_no_inner_graph_dependency() -> None:
    source = (REPOSITORY / SOURCE_RELATIVE_PATH).read_text()
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
    assert not any("inner" in name or "stable_graph" in name for name in imports)


def test_fourier_remainder_uses_exactly_one_factorial_denominator() -> None:
    source = (REPOSITORY / SOURCE_RELATIVE_PATH).read_text()
    tree = ast.parse(source)
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_fourier_taylor_polynomial"
    )
    factorial_calls = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "math"
        and node.func.attr == "factorial"
    ]
    assert len(factorial_calls) == 1
    assert source.count('"one_return_maps_tube_to_itself"') == 1


def test_generator_validates_before_atomic_write() -> None:
    source = (
        REPOSITORY / "experiments/leaky_outer_nonlinear_tube_stage6a.py"
    ).read_text()
    tree = ast.parse(source)
    main = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "main"
    )
    calls = [
        node
        for statement in main.body
        for node in ast.walk(statement)
        if isinstance(node, ast.Call)
    ]
    names = []
    for call in calls:
        if isinstance(call.func, ast.Name):
            names.append(call.func.id)
        elif isinstance(call.func, ast.Attribute):
            names.append(call.func.attr)
    assert names.index("validate_stage6a_result") < names.index("mkstemp")
    assert names.index("validate_stage6a_result") < names.index("replace")


def test_stage6a_fresh_recompute() -> None:
    validate_stage6a_result(_payload(), REPOSITORY, recompute=True)
