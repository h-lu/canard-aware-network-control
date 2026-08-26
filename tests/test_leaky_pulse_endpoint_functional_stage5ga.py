from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

import canard_control.leaky_pulse_endpoint_functional_stage5ga as stage5ga_module
from canard_control.leaky_pulse_endpoint_functional_stage5ga import (
    BRANCH,
    CERTIFICATE_KEYS,
    COORDINATE_REGISTRATION,
    ENDPOINT_CENTERS,
    ENDPOINT_EVALUATION_CONTRACT,
    FALSE_FLAGS,
    GENERATOR_RELATIVE_PATH,
    HISTORY_SPACE,
    MANIFEST_KEYS,
    MODEL_ID,
    NOTE_RELATIVE_PATH,
    PARAMETER_SCOPE,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SECTION_SPACE,
    STAGE5F_BRIDGE_INTERFACE,
    THEOREM_STATEMENT,
    TOP_KEYS,
    TRUE_FLAGS,
    VOLTAGE_ATOM_ZERO_IDENTITY,
    _conditional_graph_height_record,
    _numeric_core,
    _public_endpoint_arithmetic,
    _runtime_record,
    canonical_sha256,
    validate_stage5ga_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8"))


def _refresh_digests(payload: dict[str, object]) -> None:
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(payload["certificate"])
    )
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )


def test_registered_stage5ga_result_validates() -> None:
    validate_stage5ga_result(_payload(), REPOSITORY)


def test_exact_schemas_and_registered_coordinates_are_bound() -> None:
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
    assert certificate["section_tangent_space"] == SECTION_SPACE
    assert certificate["parameter_scope"] == PARAMETER_SCOPE
    assert certificate["coordinate_registration"] == COORDINATE_REGISTRATION
    assert certificate["endpoint_evaluation_contract"] == ENDPOINT_EVALUATION_CONTRACT
    assert certificate["voltage_atom_zero_identity"] == VOLTAGE_ATOM_ZERO_IDENTITY
    assert certificate["stage5f_bridge_interface"] == STAGE5F_BRIDGE_INTERFACE
    assert certificate["theorem_statement"] == THEOREM_STATEMENT
    assert manifest["certificate_sha256"] == canonical_sha256(certificate)
    assert manifest["numeric_core_sha256"] == canonical_sha256(
        _numeric_core(certificate)
    )
    assert {key: manifest[key] for key in _runtime_record()} == _runtime_record()


def test_endpoint_functional_signs_and_projection_bounds_are_strict() -> None:
    certificate = _payload()["certificate"]
    common = certificate["common_row_and_q_ledger"]
    endpoints = {row["name"]: row for row in certificate["endpoints"]}
    minus = endpoints["minus"]
    plus = endpoints["plus"]

    assert minus["chosen_residual_center_exact"] == ENDPOINT_CENTERS[-1]
    assert plus["chosen_residual_center_exact"] == ENDPOINT_CENTERS[1]
    assert Decimal(minus["functional_interval"]["lower"]) > Decimal("0.019")
    assert Decimal(plus["functional_interval"]["upper"]) < Decimal("-0.014")
    assert Decimal(minus["functional_radius_upper"]) < Decimal("0.0017")
    assert Decimal(plus["functional_radius_upper"]) < Decimal("0.0017")
    assert Decimal(minus["stable_projection_Y_norm_upper"]) < Decimal("0.009")
    assert Decimal(plus["stable_projection_Y_norm_upper"]) < Decimal("0.009")
    assert Decimal(common["direct_q_phys_Y_norm_upper"]) < Decimal("0.087")
    assert Decimal(common["direct_q_phys_Y_norm_upper"]) < Decimal(
        common["stage5f_registered_q_phys_Y_norm_upper"]
    )

    target = certificate["conditional_graph_height_target"]
    assert target["common_height_target_exact"] == "1/1000"
    assert Decimal(target["left_conditional_stable_gap_margin_lower"]) > Decimal(
        "0.018"
    )
    assert Decimal(target["right_conditional_stable_gap_margin_lower"]) > Decimal(
        "0.013"
    )
    assert target["quantitative_graph_supplied_here"] is False
    assert target["stable_gap_endpoint_signs_claimed_here"] is False


def test_claim_boundary_keeps_graph_crossing_and_onset_open() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    for required_open in (
        "quantitative_inner_stable_graph_validated",
        "full_interval_stable_coordinate_graph_domain_containment_validated",
        "stable_gap_endpoint_signs_validated",
        "unique_selected_event_stable_sheet_crossing_validated",
        "ordinal_third_crossing_validated",
        "unique_physical_pulse_onset_validated",
        "two_sided_basin_routing_validated",
        "frequency_amplitude_safety_radius_validated",
    ):
        assert claims[required_open] is False


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (
            ("certificate", "coordinate_registration", "centered_history"),
            "K(J) without subtracting X_*",
        ),
        (
            (
                "certificate",
                "endpoint_evaluation_contract",
                "inner_orbit_uncertainty_retained",
            ),
            False,
        ),
        (
            (
                "certificate",
                "endpoint_evaluation_contract",
                "residual_formed_before_norm_or_absolute_value",
            ),
            False,
        ),
        (
            ("certificate", "branch_regularity", "event_switching_inside_window"),
            True,
        ),
        (
            (
                "certificate",
                "voltage_atom_zero_identity",
                "unstable_column_section",
            ),
            "q_phys_v(0) is small",
        ),
        (
            (
                "certificate",
                "claim_status",
                "quantitative_inner_stable_graph_validated",
            ),
            True,
        ),
        (
            (
                "certificate",
                "claim_status",
                "stable_gap_endpoint_signs_validated",
            ),
            True,
        ),
        (
            (
                "certificate",
                "claim_status",
                "unique_selected_event_stable_sheet_crossing_validated",
            ),
            True,
        ),
        (
            (
                "certificate",
                "claim_status",
                "unique_physical_pulse_onset_validated",
            ),
            True,
        ),
        (
            ("certificate", "endpoints", 0, "chosen_residual_center_exact"),
            "0.02",
        ),
        (
            ("certificate", "endpoints", 0, "exact_endpoint_included"),
            False,
        ),
        (
            ("certificate", "endpoints", 1, "functional_sign"),
            "modulus_only",
        ),
    ),
)
def test_hostile_mutations_are_rejected_even_after_digest_refresh(
    path: tuple[object, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage5ga_result(payload, REPOSITORY)


def test_one_endpoint_only_is_rejected() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["endpoints"] = payload["certificate"]["endpoints"][:1]
    _refresh_digests(payload)
    with pytest.raises(ValueError, match="exactly two endpoint"):
        validate_stage5ga_result(payload, REPOSITORY)


def test_coordinated_smaller_direct_q_bound_is_rejected() -> None:
    payload = deepcopy(_payload())
    certificate = payload["certificate"]
    common = certificate["common_row_and_q_ledger"]
    # This hostile edit is internally propagated through every downstream
    # projection bound and both public digests.  It still lacks a 512-segment
    # source replay and must fail against the independently frozen numeric core.
    common["direct_q_phys_Y_norm_upper"] = "0.01"
    for endpoint in certificate["endpoints"]:
        endpoint.update(_public_endpoint_arithmetic(endpoint, common))
    certificate["conditional_graph_height_target"] = (
        _conditional_graph_height_record(certificate["endpoints"])
    )
    _refresh_digests(payload)
    with pytest.raises(ValueError, match="frozen numeric core"):
        validate_stage5ga_result(payload, REPOSITORY)


def test_coordinated_denominator_change_is_rejected() -> None:
    payload = deepcopy(_payload())
    certificate = payload["certificate"]
    common = certificate["common_row_and_q_ledger"]
    common["denominator_modulus_lower"] = "0.0004"
    for endpoint in certificate["endpoints"]:
        endpoint.update(_public_endpoint_arithmetic(endpoint, common))
    certificate["conditional_graph_height_target"] = (
        _conditional_graph_height_record(certificate["endpoints"])
    )
    _refresh_digests(payload)
    with pytest.raises(ValueError, match="frozen numeric core"):
        validate_stage5ga_result(payload, REPOSITORY)


def test_conditional_height_target_cannot_be_promoted_to_a_graph() -> None:
    payload = deepcopy(_payload())
    target = payload["certificate"]["conditional_graph_height_target"]
    target["quantitative_graph_supplied_here"] = True
    target["stable_gap_endpoint_signs_claimed_here"] = True
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage5ga_result(payload, REPOSITORY)


def test_manifest_parent_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    parent = next(iter(payload["manifest"]["parent_sha256"]))
    payload["manifest"]["parent_sha256"][parent] = "0" * 64
    with pytest.raises(ValueError, match="parent hash manifest"):
        validate_stage5ga_result(payload, REPOSITORY)


def test_runtime_manifest_and_current_runtime_are_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["mpfr"] = "MPFR 0"
    with pytest.raises(ValueError, match="runtime ledger"):
        validate_stage5ga_result(payload, REPOSITORY)

    hostile = _runtime_record()
    hostile["gmpy2"] = "0"
    monkeypatch.setattr(stage5ga_module, "_runtime_record", lambda: hostile)
    with pytest.raises(RuntimeError, match="replay environment changed"):
        validate_stage5ga_result(_payload(), REPOSITORY)


def test_default_validation_calls_all_eight_parent_validators(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    names = (
        "validate_directed_jet_result",
        "validate_stage3_stable_projection_result",
        "validate_stage4d_result",
        "validate_stage4e_result",
        "validate_stage5c_result",
        "validate_stage5d_result",
        "validate_stage5e_result",
        "validate_stage5f_result",
    )
    calls: list[str] = []
    for name in names:
        original = getattr(stage5ga_module, name)

        def probe(*args: object, _name: str = name, _original=original, **kwargs: object) -> None:
            calls.append(_name)
            _original(*args, **kwargs)

        monkeypatch.setattr(stage5ga_module, name, probe)
    validate_stage5ga_result(_payload(), REPOSITORY)
    assert calls == list(names)


def test_fresh_recompute_matches_the_registered_certificate() -> None:
    validate_stage5ga_result(_payload(), REPOSITORY, recompute=True)


def test_note_preserves_the_endpoint_only_claim_boundary() -> None:
    note = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    compact = " ".join(note.split())
    for required in (
        "**PROVED endpoint theorem / no stable graph or crossing theorem.**",
        "one-sided",
        "512 directed history cells",
        "No binary64 midpoint is used as proof data",
        "does not claim stable-gap signs",
        "The following remain **OPEN**",
        "biological onset",
    ):
        assert required in compact


def test_generator_validates_before_atomic_replace() -> None:
    source = (REPOSITORY / GENERATOR_RELATIVE_PATH).read_text(encoding="utf-8")
    tree = ast.parse(source)
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]

    def call_name(node: ast.Call) -> str:
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            prefix = node.func.value.id if isinstance(node.func.value, ast.Name) else ""
            return f"{prefix}.{node.func.attr}"
        return ""

    positions = {call_name(node): (node.lineno, node.col_offset) for node in calls}
    assert positions["validate_stage5ga_result"] < positions["tempfile.mkstemp"]
    assert positions["tempfile.mkstemp"] < positions["os.replace"]
    assert "os.fsync" in positions
