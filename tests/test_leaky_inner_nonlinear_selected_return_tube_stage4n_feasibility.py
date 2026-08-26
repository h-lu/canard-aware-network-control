from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal, localcontext
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility as stage4n
from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility import (
    FALSE_FLAGS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    _numeric_core,
    canonical_sha256,
    validate_stage4n_feasibility_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_digests(payload: dict[str, object]) -> None:
    pilot = payload["pilot"]
    payload["manifest"]["pilot_sha256"] = canonical_sha256(pilot)
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(pilot)
    )


def test_registered_result_validates_and_fresh_replays() -> None:
    validate_stage4n_feasibility_result(_payload(), REPOSITORY, recompute=True)


def test_all_five_parent_results_are_exactly_bound() -> None:
    payload = _payload()
    assert payload["pilot"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert len(PARENT_RESULT_SHA256) == 5
    assert any("stage4i" in name for name in PARENT_RESULT_SHA256)
    assert any("stage4l" in name for name in PARENT_RESULT_SHA256)
    assert any("stage4n_contract" in name for name in PARENT_RESULT_SHA256)


def test_preferred_b_ball_is_used_without_domain_promotion() -> None:
    domain = _payload()["pilot"]["anisotropic_domain"]
    assert domain["stable_radius_R_s"] == "0.0097"
    assert domain["unit_unstable_radius_R_u_hat"] == "0.00025"
    assert domain["split_radius_sum"] == "0.00995"
    assert Decimal(domain["stable_radius_R_s"]) + Decimal(
        domain["unit_unstable_radius_R_u_hat"]
    ) == Decimal(domain["split_radius_sum"])
    assert domain["arbitrary_continuous_stable_histories_included"] is True
    assert domain["domain_validated_by_this_pilot"] is False


def test_stage4i_sharpened_gronwall_is_the_primary_failure() -> None:
    pilot = _payload()["pilot"]
    row = pilot["stage4i_sharpened_generic_gronwall"]
    assert Decimal(
        row["stage4i_sharpened_flow_row_sum_on_input_radius_tube"]["lower"]
    ) > Decimal("1.78")
    assert Decimal(
        row["optimistic_generic_flow_gain_through_period_lower"]["lower"]
    ) > Decimal("1e14")
    assert Decimal(
        row["deviation_to_registered_strip_margin_factor"]["lower"]
    ) > Decimal("6e11")
    assert Decimal(row["decimal_order_failure_lower"]) > Decimal("11.8")
    assert row["closure_passes"] is False
    assert pilot["first_numeric_explosion"]["source"] == (
        "stage4i_sharpened_generic_gronwall"
    )


def test_sharpened_hessian_row_keeps_centered_voltage_semantics() -> None:
    """B bounds |v-1|, so the current Hessian must retain the +1 shift."""

    row = _payload()["pilot"]["stage4i_sharpened_generic_gronwall"]
    assert row["exact_inner_voltage_bound_coordinate"] == "centered z=v-1"
    assert row["field_hessian_row_formula"] == (
        "2*(1+B+r)+12*epsilon*kappa3*(B+r), with B=sup|v_*-1|"
    )
    with localcontext() as context:
        context.prec = 96
        centered = Decimal(row["exact_inner_centered_voltage_abs_upper"])
        radius = Decimal(row["input_radius"])
        expected = (
            Decimal(2) * (Decimal(1) + centered + radius)
            + Decimal(12)
            * Decimal("0.2")
            * Decimal("0.005")
            * (centered + radius)
        )
    recorded = Decimal(
        row["field_hessian_row_sum_on_input_radius_tube"]["lower"]
    )
    assert recorded <= expected
    assert Decimal(
        row["field_hessian_row_sum_on_input_radius_tube"]["upper"]
    ) >= expected
    # The old shifted-coordinate mistake gave a value near 1.10.
    assert recorded > Decimal("3.08")


def test_stage4i_four_word_primitives_are_quantitatively_registered() -> None:
    ingress = _payload()["pilot"]["parent_ingress"]
    assert ingress["stage4i_primitive_fields"] == ["F", "G", "C0", "C1", "C00"]
    assert Decimal(ingress["stage4i_maximum_guide_entry_upper"]["F"]) < Decimal(
        "8.4"
    )
    assert Decimal(ingress["stage4i_maximum_error_radius_upper"]["F"]) < Decimal(
        "0.0005"
    )
    raw = ingress["stage4i_raw_physical_frame_primitive_error_no_go"]
    assert raw["usable_for_signed_stable_certificate"] is False
    assert Decimal(raw["final_error_radius_upper"]["F"]) > Decimal("3e7")


def test_stage6a_style_row_is_strictly_worse_but_secondary() -> None:
    pilot = _payload()["pilot"]
    sharp = pilot["stage4i_sharpened_generic_gronwall"]
    coarse = pilot["stage6a_style_generic_gronwall"]
    assert Decimal(coarse["flow_row_sum"]["lower"]) > Decimal(
        sharp["stage4i_sharpened_flow_row_sum_on_input_radius_tube"]["upper"]
    )
    assert Decimal(coarse["decimal_order_failure_lower"]) > Decimal("32")
    assert coarse["closure_passes"] is False
    assert coarse["used_as_primary_no_go"] is False


def test_no_go_is_not_misreported_as_true_flow_lower_bound() -> None:
    row = _payload()["pilot"]["stage4i_sharpened_generic_gronwall"]
    assert "does not lower-bound the true nonlinear flow deviation" in row[
        "scope_of_no_go"
    ]


def test_mild_kernel_interface_requires_signed_continuous_history_cover() -> None:
    kernel = _payload()["pilot"]["signed_mild_flow_kernel_interface"]
    assert kernel["stage4i_four_words_supply_algebraic_skeleton"] is True
    assert kernel["stage4i_primitives_supply_this_kernel_bound"] is False
    assert kernel["stage4l_terminal_row_supplies_this_intermediate_bound"] is False
    assert kernel["initial_history_translation_before_delay_activation_retained"] is True
    assert kernel["complete_theta_range"] == "-tau_max<=theta<=0"
    assert kernel["actual_intermediate_kernel_upper"] is None
    assert "(t,s,theta)" in kernel["required_sharp_kernel"]


def test_conditional_terminal_kernel_target_is_quantitative_but_unproved() -> None:
    target = _payload()["pilot"]["conditional_terminal_kernel_target"]
    value = Decimal(target["strict_kernel_target_lower"])
    assert Decimal("188.9") < value < Decimal("189")
    assert target["actual_signed_event_aligned_kernel_upper"] is None
    assert target["target_is_conditional_design_arithmetic_only"] is True
    assert target["target_proves_event_existence"] is False
    assert target["target_proves_any_stage4m_hessian_block"] is False
    assert target["stage4m_six_separate_caps_still_required"] is True


def test_terminal_target_arithmetic_has_strict_positive_slack() -> None:
    target = _payload()["pilot"]["conditional_terminal_kernel_target"]
    image = Decimal(target["linear_terminal_complete_history_image_upper"]["upper"])
    slack = Decimal(target["nonlinear_terminal_remainder_slack"]["lower"])
    assert image < Decimal("0.0006")
    assert slack > Decimal("0.00935")
    assert image + slack <= Decimal(target["conditional_local_patch_radius"])


def test_event_history_and_no_earlier_ledger_remain_open() -> None:
    ledger = _payload()["pilot"]["open_event_and_history_ledger"]
    text = {
        "event_semantics",
        "no_earlier_semantics",
        "coverage_semantics",
    }
    for name, value in ledger.items():
        if name in text:
            assert isinstance(value, str) and value
        elif name == "evidence_status":
            assert value == "OPEN_AFTER_GENERIC_GRONWALL_FAILURE"
        else:
            assert value is None
    assert "positive-oriented" in ledger["event_semantics"]
    assert "negative crossings may remain" in ledger["no_earlier_semantics"]
    assert "[T_minus-tau_max,T_plus]" in ledger["coverage_semantics"]


def test_claim_ledger_has_no_event_return_or_hessian_promotion() -> None:
    claims = _payload()["pilot"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert claims["common_event_window_validated"] is False
    assert claims["complete_returned_history_tube_validated"] is False
    assert claims["six_projected_return_hessian_blocks_validated"] is False
    assert claims["quantitative_inner_stable_graph_validated"] is False


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (
            ("pilot", "claim_status", "common_event_window_validated"),
            True,
        ),
        (
            (
                "pilot",
                "claim_status",
                "sharp_signed_intermediate_second_variation_kernel_validated",
            ),
            True,
        ),
        (
            (
                "pilot",
                "claim_status",
                "six_projected_return_hessian_blocks_validated",
            ),
            True,
        ),
        (
            (
                "pilot",
                "signed_mild_flow_kernel_interface",
                "actual_intermediate_kernel_upper",
            ),
            "10",
        ),
        (
            (
                "pilot",
                "conditional_terminal_kernel_target",
                "actual_signed_event_aligned_kernel_upper",
            ),
            "100",
        ),
        (
            (
                "pilot",
                "open_event_and_history_ledger",
                "uniform_event_speed_lower",
            ),
            "0.1",
        ),
        (
            (
                "pilot",
                "stage4i_sharpened_generic_gronwall",
                "closure_passes",
            ),
            True,
        ),
        (
            (
                "pilot",
                "stage4i_sharpened_generic_gronwall",
                "exact_inner_voltage_bound_coordinate",
            ),
            "uncentered v",
        ),
        (
            (
                "pilot",
                "stage4i_sharpened_generic_gronwall",
                "field_hessian_row_sum_on_input_radius_tube",
            ),
            {"lower": "1.09", "upper": "1.10"},
        ),
    ),
)
def test_hostile_claim_kernel_and_event_promotions_are_rejected(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for name in path[:-1]:
        target = target[name]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4n_feasibility_result(
            payload, REPOSITORY, recompute=False
        )


def test_hostile_parent_hash_change_is_rejected() -> None:
    payload = deepcopy(_payload())
    name = next(iter(PARENT_RESULT_SHA256))
    payload["pilot"]["parent_result_sha256"][name] = "0" * 64
    payload["manifest"]["parent_result_sha256"][name] = "0" * 64
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4n_feasibility_result(
            payload, REPOSITORY, recompute=False
        )


def test_manifest_digests_are_exact() -> None:
    payload = _payload()
    assert payload["manifest"]["pilot_sha256"] == canonical_sha256(
        payload["pilot"]
    )
    assert payload["manifest"]["numeric_core_sha256"] == canonical_sha256(
        _numeric_core(payload["pilot"])
    )


def test_generator_validates_before_atomic_replace_and_fsyncs() -> None:
    source = (
        REPOSITORY
        / "experiments/"
        "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py"
    ).read_text(encoding="utf-8")
    ast.parse(source)
    assert source.index("validate_stage4n_feasibility_result(") < source.index(
        "tempfile.mkstemp("
    )
    assert "os.replace" in source
    assert source.count("os.fsync") >= 2


def test_source_does_not_import_stage6a_result_as_numeric_parent() -> None:
    source = (
        REPOSITORY
        / "src/canard_control/"
        "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py"
    ).read_text(encoding="utf-8")
    assert "leaky_outer_nonlinear_tube_stage6a" not in source
    assert all("stage6a" not in name.lower() for name in PARENT_RESULT_SHA256)


def test_fresh_interpreter_validation() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility "
        "import RESULT_RELATIVE_PATH, validate_stage4n_feasibility_result; "
        "r=Path.cwd(); p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4n_feasibility_result(p,r,recompute=True); "
        "print('STAGE4N_FEASIBILITY_FRESH_OK')"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONPATH": "src",
            "OPENBLAS_NUM_THREADS": "8",
            "OMP_NUM_THREADS": "1",
        },
    )
    assert completed.stdout.strip() == "STAGE4N_FEASIBILITY_FRESH_OK"


def test_result_builder_is_deterministic() -> None:
    assert stage4n.build_stage4n_feasibility_result(
        REPOSITORY
    ) == stage4n.build_stage4n_feasibility_result(REPOSITORY)
