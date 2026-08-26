from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

import canard_control.leaky_pulse_stable_gap_slope_bridge_stage5f as stage5f_module
from canard_control.leaky_pulse_stable_gap_slope_bridge_stage5f import (
    BRANCH,
    CENTERED_CHART,
    CERTIFICATE_KEYS,
    COORDINATE_COMPATIBILITY,
    EXPECTED_Q_NUMERIC_RECORDS,
    FALSE_FLAGS,
    GENERATOR_RELATIVE_PATH,
    HISTORY_SPACE,
    MANIFEST_KEYS,
    MODEL_ID,
    NOTE_RELATIVE_PATH,
    PARAMETER_SCOPE,
    PROJECTION_IDENTITY,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SECTION_TANGENT_SPACE,
    SELECTED_EVENT_SCOPE,
    THEOREM_STATEMENT,
    TOP_KEYS,
    TRUE_FLAGS,
    _clear_stage5f_replay_caches,
    _derive_bridge_records,
    _q_record_from_numeric,
    _runtime_record,
    _source_bound_q_norm_records,
    canonical_sha256,
    validate_stage5f_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8"))


def _refresh_digest(payload: dict[str, object]) -> None:
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )


def test_registered_stage5f_result_validates() -> None:
    validate_stage5f_result(_payload(), REPOSITORY)


def test_exact_schemas_and_coordinate_chart_are_bound() -> None:
    payload = _payload()
    certificate = payload["certificate"]
    manifest = payload["manifest"]
    assert set(payload) == set(TOP_KEYS)
    assert set(certificate) == set(CERTIFICATE_KEYS)
    assert set(manifest) == set(MANIFEST_KEYS)
    assert certificate["schema_id"] == manifest["schema_id"] == SCHEMA_ID
    assert certificate["model_id"] == MODEL_ID
    assert certificate["branch"] == BRANCH
    assert certificate["history_space"] == HISTORY_SPACE
    assert certificate["section_tangent_space"] == SECTION_TANGENT_SPACE
    assert certificate["centered_chart"] == CENTERED_CHART
    assert certificate["coordinate_compatibility"] == COORDINATE_COMPATIBILITY
    assert certificate["projection_identity"] == PROJECTION_IDENTITY
    assert certificate["selected_event_scope"] == SELECTED_EVENT_SCOPE
    assert certificate["parameter_scope"] == PARAMETER_SCOPE
    assert certificate["theorem_statement"] == THEOREM_STATEMENT
    assert manifest["certificate_sha256"] == canonical_sha256(certificate)
    assert {
        key: manifest[key] for key in _runtime_record()
    } == _runtime_record()


def test_bridge_closes_with_a_strict_negative_margin() -> None:
    certificate = _payload()["certificate"]
    q_record = certificate["q_phys_norm_enclosure"]
    stable = certificate["stable_projection_derivative"]
    gate = certificate["conditional_stable_gap_slope"]
    interval = gate["conditional_gap_derivative_interval"]
    assert {
        key: q_record[key] for key in EXPECTED_Q_NUMERIC_RECORDS
    } == EXPECTED_Q_NUMERIC_RECORDS
    assert Decimal(q_record["q_phys_history_norm_upper"]) < Decimal("1.383")
    assert Decimal(stable["stable_projection_pulse_derivative_norm_upper"]) < Decimal(
        "14.728"
    )
    assert Decimal(gate["maximum_admissible_graph_derivative_norm_lower"]) > Decimal(
        "16.65"
    )
    assert Decimal(interval["upper"]) < Decimal("-9.61")
    assert Decimal(gate["conditional_negative_margin_lower"]) > Decimal("9.61")


def test_claim_boundary_keeps_every_nonlinear_antecedent_open() -> None:
    certificate = _payload()["certificate"]
    claims = certificate["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert len(certificate["conditional_stable_gap_slope"]["open_antecedents"]) == 3
    assert certificate["selected_event_scope"]["ordinal_third_crossing_validated"] is False
    assert certificate["conditional_stable_gap_slope"]["theorem_status"].startswith(
        "PROVED conditional implication"
    )


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (("certificate", "centered_chart", "centered_pulse_history"), "K(J)"),
        (
            ("certificate", "coordinate_compatibility", "normalization"),
            "a different finite-row normalization",
        ),
        (
            ("certificate", "selected_event_scope", "ordinal_third_crossing_validated"),
            True,
        ),
        (
            ("certificate", "parameter_scope", "interval_exact"),
            "I_J=[0,1]",
        ),
        (
            ("certificate", "claim_status", "quantitative_inner_stable_graph_validated"),
            True,
        ),
        (
            ("certificate", "theorem_statement"),
            "A unique physical pulse onset and two-sided routing are proved.",
        ),
        (
            (
                "certificate",
                "conditional_stable_gap_slope",
                "conditional_gap_derivative_interval",
                "upper",
            ),
            "0",
        ),
        (("certificate", "q_phys_norm_enclosure", "q_phys_history_norm_upper"), "1"),
    ),
)
def test_validator_rejects_hostile_mutations_even_with_refreshed_digest(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5f_result(payload, REPOSITORY)


def test_validator_rejects_coordinated_parent_and_downstream_mutation() -> None:
    payload = deepcopy(_payload())
    certificate = payload["certificate"]
    certificate["parent_action"]["action_upper"] = "-300"
    stable, gate = _derive_bridge_records(
        certificate["parent_action"], certificate["q_phys_norm_enclosure"]
    )
    certificate["stable_projection_derivative"] = stable
    certificate["conditional_stable_gap_slope"] = gate
    _refresh_digest(payload)
    with pytest.raises(ValueError, match="differs from Stage 5E"):
        validate_stage5f_result(payload, REPOSITORY)


def test_validator_rejects_extra_keys_and_stale_digest() -> None:
    extra = deepcopy(_payload())
    extra["certificate"]["unregistered_claim"] = True
    _refresh_digest(extra)
    with pytest.raises(ValueError, match="keys changed"):
        validate_stage5f_result(extra, REPOSITORY)

    stale = deepcopy(_payload())
    stale["certificate"]["theorem_statement"] += " altered"
    with pytest.raises(ValueError, match="digest"):
        validate_stage5f_result(stale, REPOSITORY)


def test_runtime_manifest_and_current_environment_are_both_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    changed_manifest = deepcopy(_payload())
    changed_manifest["manifest"]["numpy"] = "0"
    with pytest.raises(ValueError, match="numpy replay ledger"):
        validate_stage5f_result(changed_manifest, REPOSITORY)

    hostile_runtime = _runtime_record()
    hostile_runtime["mpfr"] = "MPFR 0"
    monkeypatch.setattr(stage5f_module, "_runtime_record", lambda: hostile_runtime)
    with pytest.raises(RuntimeError, match="replay environment changed"):
        validate_stage5f_result(_payload(), REPOSITORY)


def test_default_validation_calls_both_parent_validators(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    original_stage5e = stage5f_module.validate_stage5e_result
    original_stage4e = stage5f_module.validate_stage4e_result

    def stage5e_probe(*args: object, **kwargs: object) -> None:
        calls.append("stage5e")
        original_stage5e(*args, **kwargs)

    def stage4e_probe(*args: object, **kwargs: object) -> None:
        calls.append("stage4e")
        original_stage4e(*args, **kwargs)

    monkeypatch.setattr(stage5f_module, "validate_stage5e_result", stage5e_probe)
    monkeypatch.setattr(stage5f_module, "validate_stage4e_result", stage4e_probe)
    validate_stage5f_result(_payload(), REPOSITORY)
    assert calls == ["stage5e", "stage4e"]


def test_recompute_clears_q_cache_and_matches_registered_certificate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    original = stage5f_module._clear_stage5f_replay_caches

    def probe() -> None:
        calls.append("clear")
        original()

    monkeypatch.setattr(stage5f_module, "_clear_stage5f_replay_caches", probe)
    validate_stage5f_result(_payload(), REPOSITORY, recompute=True)
    assert calls == ["clear"]


def test_q_cache_poisoning_fails_closed_and_clear_restores_replay() -> None:
    cached = _source_bound_q_norm_records(str(REPOSITORY.resolve()))
    assert cached == EXPECTED_Q_NUMERIC_RECORDS
    cached["q_phys_history_norm_upper"] = "0"
    with pytest.raises(ArithmeticError, match="q-norm replay changed"):
        stage5f_module.build_stage5f_bridge_certificate(REPOSITORY)
    _clear_stage5f_replay_caches()
    restored = _source_bound_q_norm_records(str(REPOSITORY.resolve()))
    assert restored == EXPECTED_Q_NUMERIC_RECORDS
    assert _q_record_from_numeric(restored)["positive_phase_wiener_guard_retained"] is True


def test_note_keeps_centered_conditional_boundary() -> None:
    note = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    compact_note = " ".join(note.split())
    for required in (
        "H(J):=",
        "if and only if $H(J)=0$",
        "cannot be imported",
        "selected late time",
        "I_J=\\left[\\frac{6021}{20000},\\frac{753}{2500}\\right]",
        "not been proved to be the ordinal third crossing",
        "**OPEN antecedents:**",
        "**NOT CLAIMED:**",
        "physical onset",
    ):
        assert required in compact_note
    assert "H(J)=f(\\kappa(J))-\\psi(P_s\\kappa(J))=0" not in compact_note


def test_generator_validates_before_atomic_replace() -> None:
    source = (REPOSITORY / GENERATOR_RELATIVE_PATH).read_text(encoding="utf-8")
    tree = ast.parse(source)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    ]

    def call_name(node: ast.Call) -> str:
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            prefix = node.func.value.id if isinstance(node.func.value, ast.Name) else ""
            return f"{prefix}.{node.func.attr}"
        return ""

    positions = {call_name(node): (node.lineno, node.col_offset) for node in calls}
    assert positions["validate_stage5f_result"] < positions["tempfile.mkstemp"]
    assert positions["tempfile.mkstemp"] < positions["os.replace"]
    assert "os.fsync" in positions
