from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_event_aligned_parameter_jet_contract import (
    FALSE_FLAGS,
    JET_EQUATION_CONTRACT,
    RESULT_RELATIVE_PATH,
    canonical_sha256,
    validate_event_aligned_jet_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "12993314508d7b31de1ef7e5988b9dbd0798347eee73309d381774faa0d21646"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_event_jet_contract_is_source_bound() -> None:
    payload = _payload()
    validate_event_aligned_jet_result(payload, REPOSITORY)
    assert sha256((REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()).hexdigest() == (
        EXPECTED_RESULT_SHA256
    )


def test_factorial_jet_equations_have_all_orders_and_bell_coefficients() -> None:
    equations = _payload()["contract"]["jet_equations"]
    assert equations == JET_EQUATION_CONTRACT
    assert set(equations["equations"]) == {"z0", "z1", "z2", "z3", "z4"}
    assert "4*B_2[z_1,z_3]" in equations["equations"]["z4"]
    assert "3*B_2[z_2,z_2]" in equations["equations"]["z4"]
    assert "6*B_3[z_1,z_1,z_2]" in equations["equations"]["z4"]


def test_event_history_stable_gap_and_newton_gates_are_registered() -> None:
    contract = _payload()["contract"]
    event = contract["implicit_event_jet"]
    history = contract["common_event_history_pullback"]
    stable = contract["stable_gap_and_interval_newton"]
    assert event["first_derivative"] == "tau_1=-g_J/g_t"
    assert "g_t*tau_k" in event["orders_three_and_four_rule"]
    assert "theta->v(T(delta)+theta" in history["definition"]
    assert stable["stable_gap"] == "H(J)=f_u*y_u(J)-h_s(y_s(J))"
    assert stable["interval_newton"] == "N(I)=m-H(m)/H'(I), where m=mid(I)"


def test_every_strict_numerical_input_is_null_and_claims_are_false() -> None:
    contract = _payload()["contract"]

    def leaves(value: object) -> list[object]:
        if isinstance(value, dict):
            answer: list[object] = []
            for item in value.values():
                answer.extend(leaves(item))
            return answer
        return [value]

    assert leaves(contract["numerical_inputs"])
    assert all(value is None for value in leaves(contract["numerical_inputs"]))
    for name in FALSE_FLAGS:
        assert not contract["claim_status"][name]


def test_hostile_equation_mutation_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["contract"]["jet_equations"]["equations"]["z4"] = "dot(z_4)=0"
    payload["manifest"]["contract_sha256"] = canonical_sha256(
        payload["contract"]
    )
    with pytest.raises(ValueError, match="coefficient equations"):
        validate_event_aligned_jet_result(payload, REPOSITORY)


def test_hostile_numeric_population_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["contract"]["numerical_inputs"]["event"][
        "uniform_speed_lower"
    ] = "0.2"
    payload["manifest"]["contract_sha256"] = canonical_sha256(
        payload["contract"]
    )
    with pytest.raises(ValueError, match="unvalidated numerical input"):
        validate_event_aligned_jet_result(payload, REPOSITORY)


def test_hostile_onset_promotion_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["contract"]["claim_status"][
        "unique_local_physical_pulse_onset_validated"
    ] = True
    payload["manifest"]["contract_sha256"] = canonical_sha256(
        payload["contract"]
    )
    with pytest.raises(ValueError, match="open event-jet claim"):
        validate_event_aligned_jet_result(payload, REPOSITORY)


def test_hostile_source_hash_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    source = next(iter(payload["manifest"]["source_sha256"]))
    payload["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source changed"):
        validate_event_aligned_jet_result(payload, REPOSITORY)


def test_note_forbids_finite_section_and_basin_promotions() -> None:
    note = (
        REPOSITORY
        / "docs/leaky-pulse-event-aligned-parameter-jet-contract.md"
    ).read_text(encoding="utf-8")
    assert "sampled" in note
    assert "history mesh is not a" in note
    assert "finite-section endpoint signs remain forbidden" in note
    assert "still do not identify the basins" in note
    assert "Every strict numerical field is `null`" in note
