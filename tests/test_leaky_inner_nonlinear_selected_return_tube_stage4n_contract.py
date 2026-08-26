from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_contract as stage4n
from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_contract import (
    FALSE_FLAGS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    TOP_KEYS,
    TRUE_FLAGS,
    _numeric_core,
    canonical_sha256,
    validate_stage4n_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_digests(payload: dict[str, object]) -> None:
    contract = payload["contract"]
    payload["manifest"]["contract_sha256"] = canonical_sha256(contract)
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(contract)
    )


def test_registered_stage4n_result_validates_and_fresh_replays() -> None:
    validate_stage4n_result(_payload(), REPOSITORY, recompute=True)


def test_parent_is_stage4m_only_and_stage4l_is_excluded() -> None:
    payload = _payload()
    assert payload["contract"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert len(PARENT_RESULT_SHA256) == 1
    assert all("stage4l" not in path.lower() for path in PARENT_RESULT_SHA256)
    assert payload["contract"]["required_numeric_ingress"][
        "stage4l_numeric_parent"
    ] is None


def test_preferred_b_ball_is_inherited_exactly() -> None:
    domain = _payload()["contract"]["coordinate_and_domain_registration"]
    assert domain["stable_radius_R_s"] == "0.0097"
    assert domain["unit_unstable_radius_R_u_hat"] == "0.00025"
    assert domain["split_radius_sum"] == "0.00995"
    assert Decimal(domain["stable_radius_R_s"]) + Decimal(
        domain["unit_unstable_radius_R_u_hat"]
    ) == Decimal(domain["split_radius_sum"])
    assert domain["finite_node_initial_ball_forbidden"] is True
    assert domain["domain_validated_here"] is False


def test_selected_event_is_not_silently_promoted_to_first_return() -> None:
    selected = _payload()["contract"]["selected_return_definition"]
    assert selected["earlier_negative_crossing_is_not_selected_return"] is True
    assert selected["selected_does_not_mean_first_until_cover_closes"] is True
    assert "local patch" in selected["selected_event"]
    claims = _payload()["contract"]["claim_status"]
    assert claims["unique_selected_event_on_common_window_validated"] is False
    assert claims["first_positive_local_return_validated"] is False


def test_common_window_has_two_signs_and_one_uniform_speed_gate() -> None:
    window = _payload()["contract"]["common_event_window_contract"]
    assert "-delta_minus < 0" in window["left_endpoint_sign"]
    assert "delta_plus > 0" in window["right_endpoint_sign"]
    assert "a_star > 0" in window["speed_gate"]
    assert window["parameter_sampling_forbidden"] is True
    assert window["validated_here"] is False


def test_complete_returned_history_not_endpoint_or_nodes() -> None:
    tube = _payload()["contract"]["complete_returned_history_tube_contract"]
    assert "every theta in [-tau_max,0]" in tube["returned_history"]
    assert "[T_minus-tau_max,T_plus]" in tube["coverage_interval"]
    assert tube["moving_time_translation_retained"] is True
    assert tube["finite_history_nodes_or_endpoint_only_bound_forbidden"] is True
    assert tube["validated_here"] is False


def test_no_earlier_cover_is_oriented_local_and_disjunctive() -> None:
    contract = _payload()["contract"]["no_earlier_admissible_return_contract"]
    assert "Dg[F(X_t(x))]>0" in contract["admissible_return"]
    alternatives = contract["exclusion_alternatives"]
    assert "section gap" in alternatives
    assert "event speed is nonpositive" in alternatives
    assert "outside the local complete-history patch" in alternatives
    assert contract["negative_oriented_crossings_may_exist"] is True
    assert contract["single_global_sign_requirement"] is False
    assert contract["time_sampling_forbidden"] is True
    assert contract["validated_here"] is False


def test_event_graph_is_c2_and_keeps_common_denominator() -> None:
    graph = _payload()["contract"]["c2_event_graph_contract"]
    assert "C2" in graph["regularity"]
    assert "Dg[U_h(T)]" in graph["first_derivative"]
    assert "dot U_h" in graph["second_core"]
    assert "ddot X" in graph["second_core"]
    assert "same directed event-speed enclosure" in graph["common_denominator"]
    assert graph["endpoint_only_event_correction_forbidden"] is True
    assert graph["validated_here"] is False


def test_first_missing_error_is_full_ball_nonlinear_flow() -> None:
    first = _payload()["contract"]["first_missing_error_term"]
    assert first["name"] == "full_ball_nonlinear_mild_flow_remainder_in_Y"
    assert first["value_upper"] is None
    assert "Rs=0.0097" in first["domain"]
    assert "Ru_hat=0.00025" in first["domain"]
    assert first["finite_mesh_pilot_can_fill"] is False
    assert first["linear_stage4l_row_can_fill"] is False


def test_all_numeric_ingress_and_theorem_claims_stay_open() -> None:
    contract = _payload()["contract"]
    numeric = contract["required_numeric_ingress"]
    false_keys = {
        "all_delay_activation_and_history_seams_covered",
        "one_common_tube_used_for_event_and_return_history",
    }
    for key, value in numeric.items():
        if key in false_keys:
            assert value is False
        elif key == "evidence_status":
            assert value == "OPEN_NONCLOSING"
        else:
            assert value is None
    claims = contract["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


def test_handoff_supplies_domain_but_no_hessian_block() -> None:
    handoff = _payload()["contract"]["handoff_to_stage4m"]
    assert handoff["same_R_s"] == "0.0097"
    assert handoff["same_R_u_hat"] == "0.00025"
    assert handoff["same_split_radius"] == "0.00995"
    assert handoff["same_fixed_q_hat_f_hat_projection"] is True
    assert handoff["supplies_any_hessian_block_by_itself"] is False
    assert handoff[
        "stage4m_must_still_enclose_variations_and_six_correlated_outputs"
    ] is True


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (
            ("contract", "required_numeric_ingress", "T_minus"),
            "1",
        ),
        (
            (
                "contract",
                "required_numeric_ingress",
                "uniform_event_speed_lower_a_star",
            ),
            "0.1",
        ),
        (
            (
                "contract",
                "required_numeric_ingress",
                "all_delay_activation_and_history_seams_covered",
            ),
            True,
        ),
        (
            (
                "contract",
                "claim_status",
                "unique_selected_event_on_common_window_validated",
            ),
            True,
        ),
        (
            (
                "contract",
                "claim_status",
                "first_positive_local_return_validated",
            ),
            True,
        ),
        (
            (
                "contract",
                "claim_status",
                "stage4m_six_projected_return_hessian_blocks_validated",
            ),
            True,
        ),
        (
            (
                "contract",
                "complete_returned_history_tube_contract",
                "moving_time_translation_retained",
            ),
            False,
        ),
        (
            (
                "contract",
                "no_earlier_admissible_return_contract",
                "time_sampling_forbidden",
            ),
            False,
        ),
    ),
)
def test_hostile_numeric_coverage_and_claim_promotions_are_rejected(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4n_result(payload, REPOSITORY)


def test_hostile_stage4l_parent_insertion_is_rejected() -> None:
    payload = deepcopy(_payload())
    fake = "experiments/results/unpublished_stage4l.json"
    payload["contract"]["parent_result_sha256"][fake] = "0" * 64
    payload["manifest"]["parent_result_sha256"][fake] = "0" * 64
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4n_result(payload, REPOSITORY)


def test_manifest_digests_and_outer_schema_are_exact() -> None:
    payload = _payload()
    assert set(payload) == TOP_KEYS
    assert payload["manifest"]["contract_sha256"] == canonical_sha256(
        payload["contract"]
    )
    assert payload["manifest"]["numeric_core_sha256"] == canonical_sha256(
        _numeric_core(payload["contract"])
    )


def test_generator_validates_before_atomic_replace_and_fsyncs() -> None:
    source = (
        REPOSITORY
        / "experiments/"
        "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py"
    ).read_text(encoding="utf-8")
    ast.parse(source)
    assert source.index("validate_stage4n_result(") < source.index(
        "tempfile.mkstemp("
    )
    assert "os.replace" in source
    assert source.count("os.fsync") >= 2


def test_fresh_interpreter_validation() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_contract "
        "import RESULT_RELATIVE_PATH, validate_stage4n_result; "
        "r=Path.cwd(); p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4n_result(p,r,recompute=True); print('STAGE4N_FRESH_OK')"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    assert completed.stdout.strip() == "STAGE4N_FRESH_OK"


def test_result_builder_is_deterministic() -> None:
    assert stage4n.build_stage4n_result(REPOSITORY) == stage4n.build_stage4n_result(
        REPOSITORY
    )
