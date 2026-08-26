from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_delay_word_stage3e_relative_residual import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    canonical_sha256,
    validate_outer_delay_word_stage3e_relative_residual_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_stage3e_result_replays(payload):
    validate_outer_delay_word_stage3e_relative_residual_result(
        payload, REPOSITORY
    )


def test_fundamental_relative_residual_closes(payload):
    row = payload["certificate"]["fundamental_certificate"]
    assert row["phase_cell_count"] == 1024
    assert row["fundamental_polynomial_degree"] == 24
    assert row["coefficient_taylor_degree"] == 12
    assert Decimal(row["minimum_polynomial_determinant_abs_lower"]) > 0
    assert Decimal(row["F_right_relative_error_upper"]) < 1
    assert Decimal(row["G_left_relative_error_upper"]) < 1
    assert row["determinant_nonvanishing_on_every_cell"]
    assert row["chart_interfaces_included"]
    assert row["source_replayed_binary_guide_is_nonclaim_center"]


def test_exact_orbit_ball_is_exposed_as_dominant(payload):
    row = payload["certificate"]["fundamental_certificate"]
    orbit = Decimal(row["exact_orbit_ball_exponent_upper"])
    polynomial = Decimal(row["central_polynomial_residual_exponent_upper"])
    taylor = Decimal(row["coefficient_taylor_remainder_exponent_upper"])
    assert orbit > polynomial
    assert orbit > taylor
    frontier = payload["certificate"]["signed_kernel_frontier"]
    assert frontier["more_partitioning_of_F_alone_is_not_the_next_bottleneck"]


def test_triangular_H_L_bound_is_rigorous_but_not_promoted(payload):
    triangular = payload["certificate"]["triangular_primitive_propagation"]
    assert triangular["triangular_majorant_validated"]
    assert not triangular["binary_stage3d_H_L_guides_transferred"]
    assert not triangular["signed_word_cancellation_retained"]
    assert not triangular["usable_as_E_voltage_or_E_recovery"]
    assert Decimal(triangular["H_transfer_error_upper"]) > 0
    assert Decimal(triangular["L_transfer_error_upper"]) > 0


def test_open_kernel_and_contraction_claims_remain_false(payload):
    certificate = payload["certificate"]
    claims = certificate["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert certificate["transfer_errors"]["E_voltage"] is None
    assert certificate["transfer_errors"]["E_recovery"] is None
    gate = certificate["transfer_gate"]
    assert gate["exact_F_G_transfer_validated"]
    assert not gate["binary_H_L_transfer_validated"]
    assert not gate["arbitrary_c0_linear_contraction_closes"]


def _refresh(value):
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"]["claim_status"].update(
            {"continuous_signed_density_total_variation_validated": True}
        ),
        lambda value: value["certificate"]["transfer_errors"].update(
            {"E_voltage": "0"}
        ),
        lambda value: value["certificate"]["triangular_primitive_propagation"].update(
            {"usable_as_E_voltage_or_E_recovery": True}
        ),
        lambda value: value["certificate"]["fundamental_certificate"].update(
            {"chart_interfaces_included": False}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_promotions_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_outer_delay_word_stage3e_relative_residual_result(
            changed, REPOSITORY
        )


def test_note_has_no_control_characters_or_false_completion():
    text = (
        REPOSITORY / "docs/leaky-outer-delay-word-stage3e-relative-residual.md"
    ).read_text()
    assert "\t" not in text
    assert all(character in "\n\r" or ord(character) >= 32 for character in text)
    normalized = " ".join(text.split())
    assert "one signed matrix polynomial" in normalized
    assert "not inserted as" in normalized
    assert "all remain false" in normalized
