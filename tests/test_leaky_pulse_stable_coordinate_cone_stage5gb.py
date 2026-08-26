from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path

import pytest

import canard_control.leaky_pulse_stable_coordinate_cone_stage5gb as stage5gb_module
from canard_control.leaky_pulse_stable_coordinate_cone_stage5gb import (
    BRANCH,
    CERTIFICATE_KEYS,
    CONDITIONAL_GRAPH_INTERFACE,
    COORDINATE_REGISTRATION,
    FALSE_FLAGS,
    GENERATOR_RELATIVE_PATH,
    HISTORY_SPACE,
    MANIFEST_KEYS,
    MODEL_ID,
    NOTE_RELATIVE_PATH,
    PARAMETER_SCOPE,
    PARENT_INGRESS,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SECTION_SPACE,
    THEOREM_STATEMENT,
    TOP_KEYS,
    TRUE_FLAGS,
    _arithmetic_records,
    _numeric_core,
    _runtime_record,
    canonical_sha256,
    validate_stage5gb_result,
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


def _inputs_from_certificate(certificate: dict[str, object]) -> dict[str, str]:
    derivative = certificate["derivative_ledger"]
    endpoints = {row["name"]: row for row in certificate["endpoints"]}
    action = certificate["conditional_stable_gap_slope"][
        "parent_functional_action_interval"
    ]
    return {
        "residual_Y_norm_upper": derivative["correlated_residual_Y_norm_upper"],
        "functional_deviation_upper": derivative[
            "functional_deviation_from_center_upper"
        ],
        "functional_action_lower": action["lower"],
        "functional_action_upper": action["upper"],
        "direct_q_norm_upper": derivative["direct_q_phys_Y_norm_upper"],
        "coarse_q_norm_upper": derivative["stage5f_coarse_q_phys_Y_norm_upper"],
        "endpoint_minus_J": endpoints["minus"]["J_endpoint_exact"],
        "endpoint_plus_J": endpoints["plus"]["J_endpoint_exact"],
        "endpoint_minus_norm_upper": endpoints["minus"][
            "stable_projection_Y_norm_upper"
        ],
        "endpoint_plus_norm_upper": endpoints["plus"][
            "stable_projection_Y_norm_upper"
        ],
    }


def test_registered_stage5gb_result_validates() -> None:
    validate_stage5gb_result(_payload(), REPOSITORY)


def test_exact_schema_coordinates_and_parent_interface_are_bound() -> None:
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
    assert certificate["parent_ingress"] == PARENT_INGRESS
    assert certificate["conditional_graph_interface"] == CONDITIONAL_GRAPH_INTERFACE
    assert certificate["theorem_statement"] == THEOREM_STATEMENT
    assert manifest["certificate_sha256"] == canonical_sha256(certificate)
    assert manifest["numeric_core_sha256"] == canonical_sha256(
        _numeric_core(certificate)
    )
    assert {key: manifest[key] for key in _runtime_record()} == _runtime_record()


def test_exact_rational_cone_and_conditional_slope_are_strict() -> None:
    certificate = _payload()["certificate"]
    derivative = certificate["derivative_ledger"]
    endpoints = {row["name"]: row for row in certificate["endpoints"]}
    cone = certificate["two_ended_cone"]
    slope = certificate["conditional_stable_gap_slope"]

    residual = Fraction(derivative["correlated_residual_Y_norm_upper"])
    direct_q = Fraction(derivative["direct_q_phys_Y_norm_upper"])
    deviation = Fraction(derivative["functional_deviation_from_center_upper"])
    exact_derivative = residual + direct_q * deviation
    assert Fraction(derivative["stable_projection_derivative_norm_exact_fraction"]) == (
        exact_derivative
    )
    assert exact_derivative < 6
    assert Decimal(derivative["direct_q_phys_Y_norm_upper"]) < Decimal(
        derivative["stage5f_coarse_q_phys_Y_norm_upper"]
    )

    minus = Fraction(endpoints["minus"]["stable_projection_Y_norm_upper"])
    plus = Fraction(endpoints["plus"]["stable_projection_Y_norm_upper"])
    width = Fraction(3, 20_000)
    meeting = (plus - minus + exact_derivative * width) / (2 * exact_derivative)
    radius = (minus + plus + exact_derivative * width) / 2
    assert Fraction(cone["meeting_point_exact_fraction"]) == meeting
    assert Fraction(cone["cone_radius_exact_fraction"]) == radius
    assert 0 < meeting < width
    assert radius < Fraction(47, 5_000)
    assert Decimal(cone["target_margin_lower"]) > 0

    action_lower = Fraction(slope["parent_functional_action_interval"]["lower"])
    action_upper = Fraction(slope["parent_functional_action_interval"]["upper"])
    exact_slope = slope["conditional_gap_derivative_exact_interval"]
    assert Fraction(exact_slope["lower"]) == action_lower - 16 * exact_derivative
    assert Fraction(exact_slope["upper"]) == action_upper + 16 * exact_derivative
    assert Decimal(
        slope["conditional_gap_derivative_directed_interval"]["upper"]
    ) < Decimal("-149")
    assert Decimal(
        slope["conditional_gap_derivative_directed_interval"]["lower"]
    ) < Decimal("-354")
    assert Decimal(
        slope["maximum_admissible_graph_derivative_norm_lower"]
    ) > Decimal("41")
    assert slope["quantitative_graph_supplied_here"] is False
    assert slope["graph_derivative_norm_hypothesis_validated_here"] is False
    assert slope["unconditional_gap_derivative_claimed_here"] is False


def test_claim_boundary_keeps_graph_crossing_and_onset_open() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    for required_open in (
        "quantitative_inner_stable_graph_validated",
        "future_graph_domain_contains_radius_47_over_5000_ball_validated",
        "full_interval_stable_coordinate_in_future_graph_domain_validated",
        "graph_derivative_norm_16_validated",
        "stable_gap_endpoint_signs_validated",
        "unconditional_stable_gap_derivative_excludes_zero_validated",
        "unique_selected_event_stable_sheet_crossing_validated",
        "unique_physical_pulse_onset_validated",
        "two_sided_basin_routing_validated",
        "frequency_amplitude_safety_radius_validated",
    ):
        assert claims[required_open] is False


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (
            ("certificate", "coordinate_registration", "normalization"),
            "a differently scaled q/f pair",
        ),
        (
            ("certificate", "parent_ingress", "stage5d_event_translation_retained"),
            False,
        ),
        (
            ("certificate", "two_ended_cone", "interval_width_W_exact"),
            "3/40000",
        ),
        (
            (
                "certificate",
                "two_ended_cone",
                "meeting_point_strictly_inside_interval",
            ),
            False,
        ),
        (
            ("certificate", "two_ended_cone", "argument"),
            "sampled interpolation",
        ),
        (
            ("certificate", "two_ended_cone", "finite_parameter_sampling_used"),
            True,
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
            (
                "certificate",
                "conditional_stable_gap_slope",
                "unconditional_gap_derivative_claimed_here",
            ),
            True,
        ),
    ),
)
def test_hostile_claim_and_interface_mutations_are_rejected_after_digest_refresh(
    path: tuple[object, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage5gb_result(payload, REPOSITORY)


def test_one_endpoint_only_is_rejected() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["endpoints"] = payload["certificate"]["endpoints"][:1]
    _refresh_digests(payload)
    with pytest.raises(ValueError, match="both endpoint"):
        validate_stage5gb_result(payload, REPOSITORY)


def test_old_coarse_q_cannot_be_relabelled_as_the_direct_norm() -> None:
    payload = deepcopy(_payload())
    certificate = payload["certificate"]
    derivative = certificate["derivative_ledger"]
    # Refresh both public digests after relabelling the old Wiener value as the
    # direct norm.  Normal validation must still recover the actual direct norm
    # from Stage 5G-a and reject this edited ledger.
    derivative["direct_q_phys_Y_norm_upper"] = derivative[
        "stage5f_coarse_q_phys_Y_norm_upper"
    ]
    _refresh_digests(payload)
    with pytest.raises(ValueError, match="derivative arithmetic"):
        validate_stage5gb_result(payload, REPOSITORY)


def test_manifest_parent_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    parent = next(iter(payload["manifest"]["parent_sha256"]))
    payload["manifest"]["parent_sha256"][parent] = "0" * 64
    with pytest.raises(ValueError, match="parent hash manifest"):
        validate_stage5gb_result(payload, REPOSITORY)


def test_runtime_manifest_and_current_runtime_are_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["mpfr"] = "MPFR 0"
    with pytest.raises(ValueError, match="runtime ledger"):
        validate_stage5gb_result(payload, REPOSITORY)

    hostile = _runtime_record()
    hostile["gmpy2"] = "0"
    monkeypatch.setattr(stage5gb_module, "_runtime_record", lambda: hostile)
    with pytest.raises(RuntimeError, match="replay environment changed"):
        validate_stage5gb_result(_payload(), REPOSITORY)


def test_default_validation_calls_all_four_parent_validators(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    names = (
        "validate_stage5d_result",
        "validate_stage5e_result",
        "validate_stage5f_result",
        "validate_stage5ga_result",
    )
    calls: list[str] = []
    for name in names:
        original = getattr(stage5gb_module, name)

        def probe(
            *args: object,
            _name: str = name,
            _original=original,
            **kwargs: object,
        ) -> None:
            calls.append(_name)
            _original(*args, **kwargs)

        monkeypatch.setattr(stage5gb_module, name, probe)
    validate_stage5gb_result(_payload(), REPOSITORY)
    assert calls == list(names)


def test_fresh_recompute_matches_the_registered_certificate() -> None:
    validate_stage5gb_result(_payload(), REPOSITORY, recompute=True)


def test_note_preserves_ball_conditional_slope_and_open_graph_boundary() -> None:
    note = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    compact = " ".join(note.split())
    for required in (
        "**PROVED stable-coordinate ball / no stable graph or crossing theorem.**",
        "Banach-space fundamental theorem of calculus",
        "No finite parameter sample",
        "conditional implications",
        "does not claim an unconditional stable-gap derivative",
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
    assert positions["validate_stage5gb_result"] < positions["tempfile.mkstemp"]
    assert positions["tempfile.mkstemp"] < positions["os.replace"]
    assert "os.fsync" in positions
