from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_parameter_jet_center_pilot import (
    PROOF_FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    canonical_sha256,
    validate_center_jet_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "5743c16636e449c921cea45f1b8000c4a043200630d973f7cdfdecd20b740819"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _number(record: dict[str, str]) -> Decimal:
    return Decimal(record["decimal"])


def test_registered_center_jet_pilot_is_source_bound() -> None:
    payload = _payload()
    validate_center_jet_result(payload, REPOSITORY)
    assert sha256((REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()).hexdigest() == (
        EXPECTED_RESULT_SHA256
    )


def test_five_orders_are_jointly_sampled_on_the_full_two_origin_mesh() -> None:
    pilot = _payload()["pilot"]
    assert pilot["coefficient_guide"]["orders"] == [0, 1, 2, 3, 4]
    assert pilot["common_sample_mesh"]["point_count"] == 1153
    assert pilot["common_sample_mesh"]["cell_count"] == 1152
    assert len(pilot["refinements"]) == 3
    assert pilot["joint_state_order"] == [
        "a0_voltage",
        "a0_recovery",
        "a1_voltage",
        "a1_recovery",
        "a2_voltage",
        "a2_recovery",
        "a3_voltage",
        "a3_recovery",
        "a4_voltage",
        "a4_recovery",
    ]


def test_wide_scaled_correlated_terms_form_a_descending_hierarchy() -> None:
    rows = _payload()["pilot"]["coefficient_guide"][
        "maximum_absolute_wide_half_width_scaled_term_by_order_component"
    ]
    voltage = [_number(row["voltage"]) for row in rows]
    assert voltage[1] < Decimal("0.00735")
    assert voltage[2] < Decimal("0.000102")
    assert voltage[3] < Decimal("1.38e-6")
    assert voltage[4] < Decimal("1.9e-8")
    assert voltage[1] > voltage[2] > voltage[3] > voltage[4] > 0


def test_refinement_envelope_is_tight_but_explicitly_nonrigorous() -> None:
    envelope = _payload()["pilot"]["mesh_refinement_envelope"]
    assert not envelope["rigorous_solution_enclosure"]
    adjacent = envelope["adjacent_refinement_differences"]
    assert adjacent[-1]["left"] == "medium"
    assert adjacent[-1]["right"] == "fine"
    assert _number(adjacent[-1]["joint_maximum_relative_difference"]) < Decimal(
        "1.7e-9"
    )


def test_fourth_order_wide_endpoint_reconstruction_is_a_diagnostic_only() -> None:
    reconstruction = _payload()["pilot"]["wide_endpoint_reconstruction"]
    assert reconstruction["degree"] == 4
    assert reconstruction["diagnostic_only_no_order_five_bound"]
    assert [row["side"] for row in reconstruction["rows"]] == ["lower", "upper"]
    for row in reconstruction["rows"]:
        assert _number(row["maximum_absolute_state_difference"]["joint"]) < Decimal(
            "2.8e-10"
        )


def test_every_stage5_proof_input_and_claim_remains_open() -> None:
    pilot = _payload()["pilot"]
    assert all(value is None for value in pilot["open_stage5_inputs"].values())
    for name in PROOF_FALSE_FLAGS:
        assert not pilot["claim_status"][name]


def test_hostile_envelope_promotion_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["pilot"]["mesh_refinement_envelope"][
        "rigorous_solution_enclosure"
    ] = True
    payload["manifest"]["pilot_sha256"] = canonical_sha256(payload["pilot"])
    with pytest.raises(ValueError, match="promoted to a rigorous enclosure"):
        validate_center_jet_result(payload, REPOSITORY)


def test_hostile_event_promotion_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["pilot"]["claim_status"]["route_c_event_bracket_validated"] = True
    payload["manifest"]["pilot_sha256"] = canonical_sha256(payload["pilot"])
    with pytest.raises(ValueError, match="proof claim was promoted"):
        validate_center_jet_result(payload, REPOSITORY)


def test_hostile_source_hash_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    source = next(iter(payload["manifest"]["source_sha256"]))
    payload["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source changed"):
        validate_center_jet_result(payload, REPOSITORY)


def test_note_explains_the_breakthrough_without_promoting_it() -> None:
    note = (
        REPOSITORY / "docs/leaky-pulse-parameter-jet-center-pilot.md"
    ).read_text(encoding="utf-8")
    assert "descending hierarchy" in note
    assert "strong feasibility evidence" in note
    assert "It" in note
    assert "is not such a bound" in note
    assert "pointwise mesh agreement does not control" in note
    assert "All event, stable-sheet, onset, and routing flags" in note
