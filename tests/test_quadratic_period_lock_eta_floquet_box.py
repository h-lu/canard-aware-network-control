"""Hostile checks for the explicit nonzero-eta Floquet box."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.quadratic_period_lock_eta_floquet_box import (
    ETA_RADIUS,
    TRACKED_DOBRUSHIN_ATTRACTION_SHA256,
    TRACKED_PARENT_LEAF_COUNT,
    TRACKED_PARENT_LEAF_DIGEST,
    TRACKED_RIGHT_HALF_SHA256,
    load_eta_floquet_result,
    validate_eta_floquet_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/quadratic_period_lock_eta_floquet_box.json"
)
NOTE = REPOSITORY / "docs/quadratic-period-lock-eta-floquet-stability.md"
EXPECTED_RESULT_SHA256 = (
    "6a7743a9c3ec17d93c423a9f6d65b4b0f83bd9602542ba0db835b1fa07584790"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_generated_result_is_hash_and_source_bound() -> None:
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    payload = load_eta_floquet_result(
        RESULT,
        expected_sha256=EXPECTED_RESULT_SHA256,
    )
    certificate = payload["certificate"]
    assert certificate["right_half_result_sha256"] == TRACKED_RIGHT_HALF_SHA256
    assert (
        certificate["dobrushin_attraction_result_sha256"]
        == TRACKED_DOBRUSHIN_ATTRACTION_SHA256
    )
    assert certificate["parent_leaf_count"] == TRACKED_PARENT_LEAF_COUNT
    assert certificate["parent_leaf_digest"] == TRACKED_PARENT_LEAF_DIGEST

    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest


def test_leafwise_eta_budget_and_public_recomposition_are_strict() -> None:
    certificate = _payload()["certificate"]
    worst = certificate["worst_leaf"]
    with localcontext() as context:
        context.prec = 300
        eta = Decimal(ETA_RADIUS)
        minimum = Decimal(certificate["minimum_leaf_eta_radius_lower"])
        leaf_radius = Decimal(worst["eta_radius_lower"])
        q_replayed = Decimal(worst["replayed_base_contraction_upper"])
        slope = Decimal(worst["eta_slope_upper"])
        selected = Decimal(worst["selected_eta_contraction_upper"])
        assert eta < minimum
        assert minimum == leaf_radius
        assert selected >= q_replayed + eta * slope
        assert selected < 1
        assert leaf_radius * slope <= 1 - q_replayed

    assert worst["root_id"] == "main_upper"
    assert worst["path"] == (
        "x0x0x0x0x0x0y0x0y0x0y0x0y0x0y0x0y0x0y0x0y1x1y0x1y0x0y0x1y0x1y0"
    )
    assert Decimal(worst["finite_preconditioner_norm_upper"]) > Decimal(2048)
    assert Decimal(worst["tail_preconditioner_norm_upper"]) < Decimal("0.003")


def test_translation_tail_outer_and_full_network_margins_close() -> None:
    certificate = _payload()["certificate"]
    for name in (
        "bordered_neumann_contraction_upper",
        "local_first_contraction_upper",
        "local_second_contraction_upper",
        "tail_contraction_at_eta_upper",
        "outer_contraction_at_eta_upper",
    ):
        assert Decimal(0) < Decimal(certificate[name]) < Decimal(1)
    assert Decimal(certificate["bordered_neumann_contraction_upper"]) < Decimal(
        "0.004"
    )
    assert Decimal(certificate["tail_contraction_at_eta_upper"]) < Decimal(
        "0.273"
    )
    assert Decimal(certificate["outer_contraction_at_eta_upper"]) < Decimal(
        "0.862"
    )
    assert certificate[
        "translation_multiplier_algebraically_simple_on_eta_box"
    ]
    assert certificate["active_horizon_equals_period"]
    assert certificate["monodromy_square_compact"]
    assert certificate["monodromy_power_compact"]
    assert certificate["translation_generalized_history_bootstrap"]
    assert certificate["translation_bridge_instantiated"]
    assert certificate["every_parent_leaf_base_contraction_recomputed"]
    assert certificate[
        "synchronous_nontranslation_right_half_zero_free_on_eta_box"
    ]
    assert certificate["dobrushin_transverse_rate_unchanged_on_eta_box"]
    assert certificate["full_network_local_orbital_attraction_on_eta_box"]


@pytest.mark.parametrize(
    "flag",
    (
        "joint_gain_eta_box_validated",
        "fixed_epsilon_root_response_nonzero_validated",
        "uniform_nonlinear_basin_validated",
        "biological_pulse_capture_validated",
    ),
)
def test_unsupported_certificate_promotions_are_refused(flag: str) -> None:
    hostile = deepcopy(_payload())
    hostile["certificate"][flag] = True
    with pytest.raises(ValueError, match="unsupported eta scope was promoted"):
        validate_eta_floquet_payload(hostile)


@pytest.mark.parametrize(
    "flag",
    (
        "joint_gain_eta_box",
        "fixed_epsilon_root_response_nonzero",
        "uniform_nonlinear_basin",
        "biological_pulse_capture",
    ),
)
def test_unsupported_scope_promotions_are_refused(flag: str) -> None:
    hostile = deepcopy(_payload())
    hostile["scope"][flag] = True
    with pytest.raises(ValueError, match="scope changed"):
        validate_eta_floquet_payload(hostile)


def test_inward_leaf_rounding_and_parent_rebinding_are_refused() -> None:
    hostile = deepcopy(_payload())
    worst = hostile["certificate"]["worst_leaf"]
    worst["selected_eta_contraction_upper"] = worst[
        "parent_contraction_upper"
    ]
    with pytest.raises(ValueError, match="worst eta contraction does not recompose"):
        validate_eta_floquet_payload(hostile)

    hostile = deepcopy(_payload())
    hostile["source_evidence"]["right_half_result_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source evidence changed"):
        validate_eta_floquet_payload(hostile)

    hostile = deepcopy(_payload())
    hostile["certificate"]["right_half_result_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="certificate parent hash changed"):
        validate_eta_floquet_payload(hostile)


def test_public_local_formulas_refuse_mutation() -> None:
    hostile = deepcopy(_payload())
    hostile["certificate"]["local_second_contraction_upper"] = "0.1"
    with pytest.raises(ValueError, match="second local eta contraction"):
        validate_eta_floquet_payload(hostile)

    hostile = deepcopy(_payload())
    hostile["certificate"]["tail_contraction_at_eta_upper"] = "0.1"
    with pytest.raises(ValueError, match="tail eta contraction"):
        validate_eta_floquet_payload(hostile)


def test_period_column_is_T_free_and_second_remainder_keeps_one_half() -> None:
    payload = _payload()
    certificate = payload["certificate"]
    with localcontext() as context:
        context.prec = 300
        epsilon = Decimal(certificate["epsilon"])
        eta = Decimal(certificate["eta_radius"])
        centered = Decimal(certificate["centered_voltage_wiener_upper"])
        tangent = Decimal(certificate["orbit_tangent_wiener_upper"])
        period = Decimal(certificate["exact_period_upper"])
        carrier = Decimal(certificate["carrier_coefficient_wiener_upper"])
        period_slope = Decimal(
            certificate["bordered_period_column_eta_slope_upper"]
        )
        assert period_slope == 2 * epsilon * centered * tangent
        assert period_slope != 2 * epsilon * period * centered * tangent

        parent_second = Decimal(
            certificate["parent_local_second_order_coefficient_upper"]
        )
        expected_increment = eta * carrier * tangent / 2
        perturbed_second = parent_second + expected_increment
        d_eta = Decimal(certificate["perturbed_bordered_inverse_norm_upper"])
        radius = Decimal(certificate["local_radius"])
        period_lower = Decimal(certificate["minimum_period_lower"])
        stored = Decimal(certificate["local_second_contraction_upper"])
        assert stored >= d_eta * perturbed_second * radius / period_lower

    hostile = deepcopy(payload)
    hostile["certificate"]["bordered_period_column_eta_slope_upper"] = format(
        period_slope * period,
        "f",
    )
    with pytest.raises(ValueError, match="T-free period-column slope"):
        validate_eta_floquet_payload(hostile)


def test_note_states_the_operator_bound_and_exact_scope() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "\\Delta_\\eta\\mathcal L_s",
        "There is no factor \\(T_*\\) in (2.3)",
        "all four maps",
        "32,046 terminal rectangles",
        "3.318187791963341834382515964",
        "\\boxed{|\\eta|\\le3\\times10^{-6}}",
        "\\(M_\\eta^2=U_\\eta(2T_*,0)\\) is compact",
        "eta-zero nilpotent extension",
        "each fixed finite admitted topology",
        "Joint microscopic gain--eta box",
        "Not proved by this Floquet theorem",
    ):
        assert phrase in text
