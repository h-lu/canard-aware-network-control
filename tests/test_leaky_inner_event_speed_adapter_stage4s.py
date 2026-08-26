from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal, ROUND_FLOOR, localcontext
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import canard_control.leaky_inner_event_speed_adapter_stage4s as stage4s
from canard_control.leaky_inner_event_speed_adapter_stage4s import (
    FALSE_FLAGS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    _numeric_core,
    canonical_sha256,
    validate_stage4s_event_speed_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_digests(payload: dict[str, object]) -> None:
    certificate = payload["certificate"]
    payload["manifest"]["certificate_sha256"] = canonical_sha256(certificate)
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(certificate)
    )


def test_registered_result_validates_and_fresh_replays() -> None:
    validate_stage4s_event_speed_result(_payload(), REPOSITORY, recompute=True)


def test_both_parent_results_are_byte_bound() -> None:
    payload = _payload()
    assert len(PARENT_RESULT_SHA256) == 2
    assert payload["certificate"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    for relative, digest in PARENT_RESULT_SHA256.items():
        assert stage4s._sha256_path(REPOSITORY / relative) == digest


def test_exact_preferred_b_radius_sum_and_strict_inclusion() -> None:
    radius = _payload()["certificate"]["exact_radius_adapter"]
    assert Decimal(radius["stable_radius_R_s"]) == Decimal("0.0097")
    assert Decimal(radius["unit_unstable_radius_R_u_hat"]) == Decimal(
        "0.00025"
    )
    assert (
        Decimal(radius["stable_radius_R_s"])
        + Decimal(radius["unit_unstable_radius_R_u_hat"])
        == Decimal(radius["preferred_b_radius_sum_exact"])
        == Decimal("0.00995")
    )
    assert Decimal(radius["strict_inclusion_slack_lower"]) > 0
    assert (
        Decimal(radius["preferred_b_radius_sum_exact"])
        < Decimal(radius["stage2_declared_ball_radius_lower"])
    )


def test_directed_event_speed_arithmetic_replays() -> None:
    speed = _payload()["certificate"]["directed_event_speed_adapter"]
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_FLOOR
        expected_variation = Decimal(speed["vector_field_lipschitz_upper"]) * Decimal(
            speed["smaller_complete_history_ball_radius"]
        )
        expected_speed = Decimal(speed["orbit_event_speed_lower"]) - expected_variation
    assert Decimal(speed["event_speed_variation_upper"]) == expected_variation
    assert Decimal(speed["smaller_ball_event_speed_lower"]) == expected_speed
    assert expected_speed == Decimal(
        "0.2069547790094916713843497979253308516874029625928539498445"
    )
    assert expected_speed > Decimal(
        speed["inherited_stage2_declared_ball_event_speed_lower"]
    )


def test_same_complete_history_norm_and_event_row_are_explicit() -> None:
    registration = _payload()["certificate"][
        "center_norm_and_event_row_registration"
    ]
    assert "C([-tau_max,0],R)_v" in registration["history_space"]
    assert "max" in registration["history_norm"]
    assert registration["stage2_event_functional"] == (
        "h_C(phi)=phi_v(0)-V_true(0)"
    )
    assert registration["stage4n_event_functional"] == (
        "g(phi)=phi_v(0)-X_{*,v}(0), an affine complete-history row"
    )
    assert registration["center_identity_status"] == "DECLARED_ROUTE_C_DEFINITION"
    assert registration["no_finite_node_norm_substitution"] is True


def test_initial_ball_inclusion_is_not_flow_invariance() -> None:
    certificate = _payload()["certificate"]
    radius = certificate["exact_radius_adapter"]
    conditional = certificate["conditional_stage4n_discharge"]
    assert radius["preferred_b_declared_initial_ball_inside_stage2_ball"] is True
    assert radius["stage4n_return_domain_validated"] is False
    assert conditional["common_window_containment_premise_validated"] is False
    assert conditional["returned_history_containment_premise_validated"] is False
    assert conditional["stage4n_speed_claim_promoted_here"] is False


def test_conditional_conclusion_carries_the_exact_positive_bound() -> None:
    conditional = _payload()["certificate"]["conditional_stage4n_discharge"]
    speed = _payload()["certificate"]["directed_event_speed_adapter"]
    bound = speed["smaller_ball_event_speed_lower"]
    assert bound in conditional["proved_conclusion_if_premise_holds"]
    assert bound in conditional[
        "endpoint_speed_conclusion_if_returned_history_premise_holds"
    ]
    assert Decimal(
        conditional["stage4n_uniform_event_speed_ingress_can_then_be_filled_with"]
    ) > 0


def test_claim_ledger_has_exact_truth_boundary() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert claims["directed_event_speed_lower_strictly_positive"] is True
    assert claims[
        "uniform_positive_event_speed_on_stage4n_window_validated"
    ] is False


@pytest.mark.parametrize(
    "flag",
    (
        "common_window_histories_lie_in_smaller_ball_validated",
        "uniform_positive_event_speed_on_stage4n_window_validated",
        "complete_returned_history_tube_validated",
        "unique_selected_event_on_common_window_validated",
        "c2_selected_return_map_validated",
        "quantitative_inner_stable_graph_validated",
        "unique_physical_pulse_onset_validated",
        "two_sided_basin_routing_validated",
        "frequency_amplitude_safety_radius_validated",
    ),
)
def test_hostile_open_gate_promotion_is_rejected(flag: str) -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][flag] = True
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_event_speed_result(payload, REPOSITORY)


def test_hostile_radius_change_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["exact_radius_adapter"][
        "preferred_b_radius_sum_exact"
    ] = "0.00994"
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_event_speed_result(payload, REPOSITORY)


def test_hostile_speed_increase_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["directed_event_speed_adapter"][
        "smaller_ball_event_speed_lower"
    ] = "0.21"
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_event_speed_result(payload, REPOSITORY)


def test_source_manifest_and_parent_ledger_are_explicit_and_complete() -> None:
    tree = ast.parse(
        (REPOSITORY / stage4s.SOURCE_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    assigned_names = {
        node.targets[0].id
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
    }
    assert {"SOURCE_MANIFEST", "PARENT_RESULT_SHA256"} <= assigned_names
    assert stage4s.SOURCE_MANIFEST == SOURCE_MANIFEST
    assert stage4s.PARENT_RESULT_SHA256 == PARENT_RESULT_SHA256
    assert len(SOURCE_MANIFEST) == 4


def test_manifest_hashes_every_declared_source() -> None:
    manifest = _payload()["manifest"]
    assert set(manifest["source_sha256"]) == set(SOURCE_MANIFEST)
    for relative in SOURCE_MANIFEST:
        assert manifest["source_sha256"][relative] == stage4s._sha256_path(
            REPOSITORY / relative
        )


def test_generation_is_deterministic_in_current_process() -> None:
    first = stage4s.build_stage4s_event_speed_result(REPOSITORY)
    second = stage4s.build_stage4s_event_speed_result(REPOSITORY)
    assert first == second == _payload()


def test_generation_is_deterministic_in_fresh_subprocess() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_event_speed_adapter_stage4s import "
        "build_stage4s_event_speed_result; "
        "print(json.dumps(build_stage4s_event_speed_result(Path('.')), "
        "sort_keys=True, separators=(',', ':')))"
    )
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(REPOSITORY / "src")
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert json.loads(completed.stdout) == _payload()
