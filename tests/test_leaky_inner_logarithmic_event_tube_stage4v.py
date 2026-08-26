from __future__ import annotations

from decimal import Decimal, getcontext, setcontext
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_logarithmic_event_tube_stage4v import (
    CERTIFIED_LAMBDA,
    FALSE_FLAGS,
    OPEN_DOMAIN_LAMBDA,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage4v_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _restore_decimal_context():
    saved = getcontext().copy()
    try:
        yield
    finally:
        setcontext(saved)


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_result_validates_without_recompute(payload):
    validate_stage4v_result(payload, REPOSITORY, recompute=False)


def test_registered_result_matches_fresh_directed_recompute(payload):
    validate_stage4v_result(payload, REPOSITORY, recompute=True)


def test_claim_boundary_is_exact(payload):
    claims = payload["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


def test_scaled_domain_and_parent_bindings(payload):
    certificate = payload["certificate"]
    domain = certificate["scaled_domain"]
    assert domain["certified_closed_lambda"] == CERTIFIED_LAMBDA
    assert domain["strict_open_domain_lambda"] == OPEN_DOMAIN_LAMBDA
    assert Decimal(OPEN_DOMAIN_LAMBDA) > Decimal(CERTIFIED_LAMBDA)
    assert certificate["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert certificate["theorem_boundary"]["stage4u_result_used_as_parent"] is False


def test_directed_rate_and_bootstrap_are_strict(payload):
    certificate = payload["certificate"]
    rate = certificate["directed_orbit_rate_integral"]
    bootstrap = certificate["nonlinear_first_exit_bootstrap"]
    assert rate["cell_count"] == 1042
    assert Decimal(rate["one_binary_period_rate_integral_upper"]) < Decimal("6.36")
    assert Decimal(rate["rate_maximum_upper"]) < Decimal("0.776")
    assert Decimal(bootstrap["bootstrap_slack"]["lower"]) > 0
    assert Decimal(bootstrap["construction_lambda_ceiling"]["lower"]) > Decimal(
        OPEN_DOMAIN_LAMBDA
    )
    phase = rate["delayed_phase_bridge"]
    assert phase["binary_algebra_guard_is_phase_bridge"] is False
    assert Decimal(
        phase["additional_phase_coefficient_error_upper"]["lower"]
    ) > 0
    assert Decimal(phase["total_delayed_coefficient_error_used_upper"]) > Decimal(
        phase["inherited_delayed_coefficient_error_upper"]
    )


def test_event_and_patch_margins_are_strict(payload):
    event = payload["certificate"]["common_event_and_patch"]
    assert Decimal(event["endpoint_margin_beyond_half_gap"]["lower"]) > 0
    assert Decimal(event["terminal_patch_margin"]["lower"]) > 0
    assert Decimal(event["uniform_event_speed_lower"]["lower"]) > 0
    assert event["event_ordinal"] is None


def test_preferred_ball_is_not_promoted(payload):
    feasibility = payload["certificate"]["preferred_ball_feasibility"]
    claims = payload["certificate"]["claim_status"]
    assert feasibility["preferred_lambda_one_proved"] is False
    assert (
        feasibility["fixed_plus_minus_1e3_window_excludes_preferred_ball_proved"]
        is False
    )
    assert Decimal(
        feasibility["preferred_initial_energy_to_beta_ratio"]["lower"]
    ) > Decimal("200")
    assert Decimal(feasibility["formal_rhs_to_beta_ratio"]["lower"]) > Decimal(
        "1e7"
    )
    assert feasibility["formal_rhs_is_validated_flow_bound"] is False
    assert claims["preferred_lambda_one_ball_validated"] is False
    assert claims["biological_onset_or_control_validated"] is False
