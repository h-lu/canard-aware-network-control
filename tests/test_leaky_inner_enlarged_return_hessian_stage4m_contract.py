from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

import pytest

import canard_control.leaky_inner_enlarged_return_hessian_stage4m_contract as stage4m
from canard_control.leaky_inner_enlarged_return_hessian_stage4m_contract import (
    COMMON_CAP_MULTIPLIER,
    FALSE_FLAGS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    SPLIT_RETURN_RADIUS,
    STABLE_GRAPH_RADIUS,
    TOP_KEYS,
    TRUE_FLAGS,
    UNIT_UNSTABLE_GRAPH_RADIUS,
    _numeric_core,
    canonical_sha256,
    validate_stage4m_result,
)
from canard_control.leaky_inner_stable_graph_enlargement_stage4k import (
    EXPECTED_STAGE4A_HEURISTIC_BLOCKS,
)
from canard_control.leaky_projected_return_hessian_stage4_contract import (
    HESSIAN_FIELD_NAMES,
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


def test_registered_stage4m_result_validates_and_fresh_replays() -> None:
    validate_stage4m_result(_payload(), REPOSITORY, recompute=True)


def test_parent_set_binds_stage4k_and_excludes_stage4l() -> None:
    payload = _payload()
    assert payload["contract"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert len(PARENT_RESULT_SHA256) == 1
    assert all("stage4l" not in path.lower() for path in PARENT_RESULT_SHA256)
    assert payload["contract"]["first_missing_parent"][
        "stage4l_can_substitute"
    ] is False


def test_preferred_b_geometry_is_exact_and_not_a_validated_domain() -> None:
    domain = _payload()["contract"]["anisotropic_domain"]
    assert domain["stable_radius_R_s"] == STABLE_GRAPH_RADIUS == "0.0097"
    assert (
        domain["unit_unstable_radius_R_u_hat"]
        == UNIT_UNSTABLE_GRAPH_RADIUS
        == "0.00025"
    )
    assert domain["split_radius_sum_exact"] == SPLIT_RETURN_RADIUS == "0.00995"
    assert Decimal(STABLE_GRAPH_RADIUS) + Decimal(
        UNIT_UNSTABLE_GRAPH_RADIUS
    ) == Decimal(SPLIT_RETURN_RADIUS)
    assert domain["validated_return_domain"] is False


def test_all_six_strict_caps_are_exact_common_products() -> None:
    ledger = _payload()["contract"]["common_cap_ledger"]
    assert ledger["common_multiplier_exact"] == COMMON_CAP_MULTIPLIER == "13.2353"
    records = ledger["records"]
    assert [record["block"] for record in records] == list(HESSIAN_FIELD_NAMES)
    for record in records:
        name = record["block"]
        expected = Fraction(Decimal(EXPECTED_STAGE4A_HEURISTIC_BLOCKS[name])) * Fraction(
            Decimal(COMMON_CAP_MULTIPLIER)
        )
        assert Fraction(Decimal(record["strict_cap_decimal_exact"])) == expected
        assert " < strict_cap_decimal_exact" in record[
            "strict_acceptance_inequality"
        ]
    assert ledger["caps_are_rfde_bounds"] is False


def test_all_six_caps_enter_the_same_exact_majorant() -> None:
    contract = _payload()["contract"]
    ledger = contract["common_cap_ledger"]
    majorant = contract["cap_majorant_evaluation"]
    caps = {
        record["block"]: record["strict_cap_decimal_exact"]
        for record in ledger["records"]
    }
    blocks = majorant["input_budget"]["hessian_blocks"]
    assert all(blocks[name] == caps[name] for name in HESSIAN_FIELD_NAMES)
    evaluation = majorant["exact_evaluation"]
    assert evaluation["graph_certificate_closes"] is True
    assert Decimal(evaluation["perron_root_upper"]) < Decimal("0.163")
    assert Decimal(evaluation["self_map_slack_vector_lower"]["stable"]) > 0
    assert Decimal(evaluation["self_map_slack_vector_lower"]["unstable"]) > 0
    interpretation = majorant["proof_interpretation"]
    assert interpretation["all_six_caps_inserted_simultaneously"] is True
    assert interpretation["hessian_caps_are_certified_blocks"] is False
    assert interpretation["graph_certificate_closes"] is False


def test_first_missing_parent_precedes_every_hessian_supremum() -> None:
    missing = _payload()["contract"]["first_missing_parent"]
    assert missing["required_parent_stage"] == (
        "Stage-4N nonlinear selected-return tube"
    )
    for key in (
        "required_parent_result_path",
        "required_parent_result_sha256",
        "nonlinear_flow_family_Y_tube_remainder_upper",
        "common_selected_event_window",
        "uniform_event_speed_lower",
        "complete_returned_history_tube_radius_upper",
        "no_earlier_hit_margin_lower",
    ):
        assert missing[key] is None
    assert "D2P(x)" in missing["blocking_reason"]


def test_complete_history_moving_event_terms_are_explicit() -> None:
    event = _payload()["contract"]["moving_event_return_hessian"]
    assert event["moving_event_terms_retained"] is True
    assert event["endpoint_only_correction_forbidden"] is True
    assert "dot U_h" in event["history_core"]
    assert "dot U_k" in event["history_core"]
    assert "ddot X" in event["history_core"]
    assert "T_hk" in event["complete_history_return_hessian"]
    assert "every theta in [-tau_max,0]" in event[
        "complete_history_return_hessian"
    ]


def test_fixed_projection_is_correlated_before_norm() -> None:
    contract = _payload()["contract"]
    coordinates = contract["coordinate_registration"]
    assert coordinates["fixed_projection"] == "P_s=I-q_hat*f_hat=I-q*f"
    assert coordinates["normalization_transfer_validated_here"] is False
    projection = contract["correlated_projection_order"]
    assert projection["fixed_projection_over_ball"] is True
    assert projection["moving_projection_forbidden"] is True
    assert projection["triangle_of_separately_normed_terms_forbidden"] is True
    assert "then take" in projection["stable_output"]
    assert "then take" in projection["unstable_output"]


def test_strict_numeric_ingress_and_downstream_claims_stay_open() -> None:
    contract = _payload()["contract"]
    ingress = contract["strict_numeric_ingress"]
    assert set(ingress["directed_uniform_hessian_blocks"]) == set(
        HESSIAN_FIELD_NAMES
    )
    assert all(
        ingress["directed_uniform_hessian_blocks"][name] is None
        for name in HESSIAN_FIELD_NAMES
    )
    assert ingress["majorant_with_certified_blocks"] is None
    claims = contract["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (
            (
                "contract",
                "strict_numeric_ingress",
                "directed_uniform_hessian_blocks",
                "stable_output_ss_upper",
            ),
            "0.1",
        ),
        (
            (
                "contract",
                "first_missing_parent",
                "uniform_event_speed_lower",
            ),
            "0.1",
        ),
        (
            (
                "contract",
                "claim_status",
                "all_six_projected_return_hessian_blocks_validated",
            ),
            True,
        ),
        (
            (
                "contract",
                "claim_status",
                "quantitative_inner_stable_graph_validated",
            ),
            True,
        ),
        (
            (
                "contract",
                "moving_event_return_hessian",
                "moving_event_terms_retained",
            ),
            False,
        ),
        (
            (
                "contract",
                "correlated_projection_order",
                "triangle_of_separately_normed_terms_forbidden",
            ),
            False,
        ),
    ),
)
def test_hostile_numeric_formula_and_claim_promotions_are_rejected(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4m_result(payload, REPOSITORY)


def test_hostile_cap_change_is_rejected_even_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["contract"]["common_cap_ledger"]["records"][0][
        "strict_cap_decimal_exact"
    ] = "1"
    payload["contract"]["cap_majorant_evaluation"]["input_budget"][
        "hessian_blocks"
    ]["stable_output_ss_upper"] = "1"
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4m_result(payload, REPOSITORY)


def test_hostile_stage4l_parent_insertion_is_rejected() -> None:
    payload = deepcopy(_payload())
    fake_path = "experiments/results/unpublished_stage4l.json"
    payload["contract"]["parent_result_sha256"][fake_path] = "0" * 64
    payload["manifest"]["parent_result_sha256"][fake_path] = "0" * 64
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4m_result(payload, REPOSITORY)


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
        / "experiments/leaky_inner_enlarged_return_hessian_stage4m_contract.py"
    ).read_text(encoding="utf-8")
    ast.parse(source)
    assert source.index("validate_stage4m_result(") < source.index(
        "tempfile.mkstemp("
    )
    assert "os.replace" in source
    assert source.count("os.fsync") >= 2


def test_fresh_interpreter_validation() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_enlarged_return_hessian_stage4m_contract "
        "import RESULT_RELATIVE_PATH, validate_stage4m_result; "
        "r=Path.cwd(); p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4m_result(p,r,recompute=True); print('STAGE4M_FRESH_OK')"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
        env={**dict(__import__("os").environ), "PYTHONPATH": "src"},
    )
    assert completed.stdout.strip() == "STAGE4M_FRESH_OK"


def test_result_builder_is_deterministic() -> None:
    first = stage4m.build_stage4m_result(REPOSITORY)
    second = stage4m.build_stage4m_result(REPOSITORY)
    assert first == second
