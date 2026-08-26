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

import canard_control.leaky_inner_explicit_lambda_event_tube_stage4u as stage4u
from canard_control.leaky_inner_explicit_lambda_event_tube_stage4u import (
    CERTIFIED_LAMBDA,
    FALSE_FLAGS,
    OPEN_DOMAIN_LAMBDA,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    _numeric_core,
    canonical_sha256,
    validate_stage4u_result,
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
    validate_stage4u_result(_payload(), REPOSITORY, recompute=True)


def test_parent_set_is_exact_includes_stage4m_and_excludes_stage4s_a() -> None:
    payload = _payload()
    assert payload["certificate"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert len(PARENT_RESULT_SHA256) == 7
    assert all("stage4s_event_tube" not in name for name in PARENT_RESULT_SHA256)
    assert any("stage4n_feasibility" in name for name in PARENT_RESULT_SHA256)
    assert any("stage4m_contract" in name for name in PARENT_RESULT_SHA256)
    assert any("stage4r" in name for name in PARENT_RESULT_SHA256)
    assert any("reduced_history" in name for name in PARENT_RESULT_SHA256)


def test_clean_closed_scale_has_a_strictly_larger_open_domain() -> None:
    domain = _payload()["certificate"]["scaled_domain"]
    assert CERTIFIED_LAMBDA == "9e-31"
    assert OPEN_DOMAIN_LAMBDA == "9.1e-31"
    assert domain["certified_closed_lambda_lower"] == CERTIFIED_LAMBDA
    assert domain["strict_open_domain_lambda"] == OPEN_DOMAIN_LAMBDA
    assert Decimal(OPEN_DOMAIN_LAMBDA) > Decimal(CERTIFIED_LAMBDA) > 0
    assert domain[
        "arbitrary_continuous_reduced_y_stable_histories_included"
    ] is True
    assert domain["arbitrary_full_x_two_component_histories_included"] is False
    assert domain["normalization_adapter_numerically_promoted"] is False
    assert domain["coordinate_open_domain"] == (
        "D_open=j^{-1}(W_open intersect Sigma_loc), open in M"
    )
    assert "D_diamond" in domain["explicit_coordinate_diamond_subset"]


def test_corrected_two_period_gronwall_bootstrap_closes() -> None:
    row = _payload()["certificate"]["corrected_gronwall_bootstrap"]
    assert row["comparison_horizon"] == "all physical times 0<=t<=T_plus"
    assert "exact periodicity" in row["periodic_coefficient_extension"]
    assert row["centered_voltage_coordinate"] == "B=sup|v_*-1|"
    assert row["corrected_hessian_row_formula"] == (
        "H_beta=2*(1+B+beta)+12*epsilon*kappa3*(B+beta)"
    )
    assert Decimal(row["corrected_hessian_row_at_beta"]["lower"]) > Decimal("3")
    assert Decimal(row["flow_row_upper"]["upper"]) < Decimal("1.777")
    assert Decimal(row["complete_history_flow_gain"]["upper"]) > Decimal("1e28")
    assert Decimal(row["bootstrap_slack_beta_minus_deviation"]["lower"]) > 0
    ceiling = Decimal(row["strict_open_lambda_ceiling"]["lower"])
    assert Decimal("9.13e-31") < ceiling < Decimal("9.14e-31")
    assert ceiling > Decimal(OPEN_DOMAIN_LAMBDA)


def test_half_endpoint_margins_speed_and_patch_all_close() -> None:
    certificate = _payload()["certificate"]
    event = certificate["common_event_certificate"]
    history = certificate["complete_history_and_patch"]
    exact = certificate["exact_center_window"]
    assert Decimal(event["endpoint_gap_lower"]["lower"]) > Decimal(
        event["advertised_half_gap_target"]["upper"]
    )
    assert Decimal(
        event["endpoint_margin_beyond_half_target"]["lower"]
    ) > 0
    assert Decimal(event["uniform_event_speed_lower"]["lower"]) > Decimal("0.24")
    assert Decimal(event["uniform_event_speed_lower"]["lower"]) > Decimal(
        event["advertised_half_center_speed_target"]["upper"]
    )
    assert Decimal(history["terminal_patch_margin"]["lower"]) > Decimal("0.009")
    assert Decimal(history["initial_patch_margin"]["lower"]) > Decimal("0.009")
    assert Decimal(exact["T_minus_minus_2_tau_max"]["lower"]) > Decimal("14")
    assert event["event_ordinal"] is None


def test_history_translation_activation_seams_and_moving_time_are_explicit() -> None:
    history = _payload()["certificate"]["complete_history_and_patch"]
    assert "exact arbitrary initial-history translate" in history[
        "initial_translation_rule"
    ]
    assert "t=tau_j activation face" in history["activation_and_seam_rule"]
    assert "no time or history-node sampling" in history[
        "activation_and_seam_rule"
    ]
    assert "[T_minus-tau_max,T_plus]" in history["physical_cover"]
    assert "Psi_{T(y)}(y)-Psi_{T(y)}(Y_*)" in history[
        "moving_event_history_bound"
    ]


def test_reduced_full_bridge_does_not_claim_same_radius_in_full_x() -> None:
    bridge = _payload()["certificate"]["reduced_full_bridge_and_regularity"]
    assert bridge["full_x_same_radius_claimed"] is False
    assert bridge["smoothing_gate"] == "T_minus>2*tau_max"
    assert "parameter domain W_open subset Y" in bridge["stage4r_application"]
    assert bridge["ambient_C2_event_time"] == "T_tilde:W_open->R is C2"
    assert "D_open->R" in bridge["coordinate_C2_restriction"]
    assert bridge["coordinate_output_domain"] == "D_out=chi(Sigma_loc)"
    assert "D_open->D_out" in bridge["induced_return"]
    assert "finite-evaluation polynomial" in bridge["full_field_regularity"]
    assert "event domain V=X" in bridge["full_event_functional"]


def test_stage4m_section_splitting_is_directly_bound_and_used() -> None:
    payload = _payload()["certificate"]
    domain = payload["scaled_domain"]
    history = payload["complete_history_and_patch"]
    claims = payload["claim_status"]
    assert "E_s=ker(f_hat) in Sigma_0" in domain["coordinate_space"]
    assert "q_hat in Sigma_0" in domain["fixed_coordinate_injection"]
    assert "f_hat(q_hat)=1 exactly" in domain["fixed_coordinate_injection"]
    assert "direct Stage-4M parent" in history["initial_section_membership"]
    assert claims["stage4m_exact_section_splitting_semantics_validated"] is True
    assert claims[
        "scaled_ball_contains_arbitrary_full_x_two_component_histories_validated"
    ] is False


def test_claim_ledger_keeps_every_downstream_gate_false() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert claims["explicit_lambda_lower_bound_validated"] is True
    assert claims["preferred_lambda_one_ball_validated"] is False
    assert claims["same_scaled_ball_self_map_validated"] is False
    assert claims["six_projected_return_hessian_blocks_validated"] is False
    assert claims["biological_onset_or_control_validated"] is False


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (("certificate", "scaled_domain", "certified_closed_lambda_lower"), "1"),
        (
            (
                "certificate",
                "corrected_gronwall_bootstrap",
                "centered_voltage_coordinate",
            ),
            "B=sup|v_*|",
        ),
        (
            (
                "certificate",
                "corrected_gronwall_bootstrap",
                "bootstrap_slack_beta_minus_deviation",
                "lower",
            ),
            "-1",
        ),
        (
            (
                "certificate",
                "complete_history_and_patch",
                "activation_and_seam_rule",
            ),
            "sample a grid",
        ),
        (
            (
                "certificate",
                "scaled_domain",
                "coordinate_open_domain",
            ),
            "D_open=W_open",
        ),
        (
            (
                "certificate",
                "reduced_full_bridge_and_regularity",
                "coordinate_output_domain",
            ),
            "D_out=D_open",
        ),
        (
            (
                "certificate",
                "claim_status",
                "same_scaled_ball_self_map_validated",
            ),
            True,
        ),
        (
            (
                "certificate",
                "claim_status",
                "six_projected_return_hessian_blocks_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_numeric_semantic_and_downstream_promotions_are_rejected(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for name in path[:-1]:
        target = target[name]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4u_result(payload, REPOSITORY, recompute=False)


def test_manifest_digests_are_exact() -> None:
    payload = _payload()
    assert payload["manifest"]["certificate_sha256"] == canonical_sha256(
        payload["certificate"]
    )
    assert payload["manifest"]["numeric_core_sha256"] == canonical_sha256(
        _numeric_core(payload["certificate"])
    )


def test_generator_validates_before_atomic_replace_and_fsyncs() -> None:
    source = (REPOSITORY / "experiments/leaky_inner_explicit_lambda_event_tube_stage4u.py").read_text(
        encoding="utf-8"
    )
    ast.parse(source)
    assert source.index("validate_stage4u_result(") < source.index("tempfile.mkstemp(")
    assert "os.replace" in source
    assert source.count("os.fsync") >= 2


def test_fresh_interpreter_validation() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_explicit_lambda_event_tube_stage4u "
        "import RESULT_RELATIVE_PATH, validate_stage4u_result; "
        "r=Path.cwd(); p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4u_result(p,r,recompute=True); print('STAGE4U_FRESH_OK')"
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
    assert completed.stdout.strip() == "STAGE4U_FRESH_OK"


def test_result_builder_is_deterministic() -> None:
    assert stage4u.build_stage4u_result(REPOSITORY) == stage4u.build_stage4u_result(
        REPOSITORY
    )
