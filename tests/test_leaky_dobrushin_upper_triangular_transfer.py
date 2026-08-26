from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import shutil

import pytest

from canard_control.leaky_dobrushin_collective_defect import (
    RESULT_RELATIVE_PATH as DEFECT_RESULT_RELATIVE_PATH,
    SOURCE_RELATIVE_PATH as DEFECT_SOURCE_RELATIVE_PATH,
    canonical_sha256 as defect_canonical_sha256,
)

from canard_control.leaky_dobrushin_upper_triangular_transfer import (
    OPEN_FLAGS,
    PARENT_RESULTS,
    PROVED_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    build_upper_triangular_transfer_result,
    validate_upper_triangular_transfer_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_tracked_upper_triangular_result_replays(payload):
    validate_upper_triangular_transfer_result(payload, REPOSITORY)
    assert build_upper_triangular_transfer_result(REPOSITORY) == payload


def test_exact_claim_boundary(payload):
    certificate = payload["certificate"]
    for name in PROVED_FLAGS:
        assert certificate[name] is True
    for name in OPEN_FLAGS:
        assert certificate[name] is False
    assert certificate["complete_line_green_norm_upper"] == "10"
    assert certificate["delay_balance_defect_range"] == "0<=delta_B<=1"
    assert certificate[
        "componentwise_resolved_linear_accumulated_bound_proved"
    ] is True
    assert certificate["imbalance_linear_coefficient_exact"] == "391/20000"
    assert certificate["imbalance_accumulated_coefficient_exact"] == (
        "391/20000*[delta0*(10+4*sqrt(5))+delta1*(10+5*sqrt(5))]"
    )
    assert certificate["imbalance_accumulated_delta_b_worst_exact"] == (
        "391*(2+sqrt(5))/4000"
    )
    assert certificate["quadratic_accumulated_coefficient_exact"] == (
        "703/40+27*sqrt(5)/800"
    )
    assert certificate[
        "quadratic_accumulated_coefficient_rational_upper"
    ] == "56483/3200"
    assert "M(t-tau0)" in certificate[
        "componentwise_pointwise_collective_forcing_bound"
    ]
    assert "H_M(t)" in certificate["pointwise_collective_forcing_bound"]
    assert "391*(2+sqrt(5))/4000" in certificate[
        "delta_b_only_accumulated_collective_forcing_bound"
    ]
    assert "upper triangular" in certificate["strict_boundary"] or (
        "left balance" in certificate["strict_boundary"]
    )


def test_exact_witness_is_nonbalanced_but_synchrony_invariant(payload):
    witness = payload["certificate"]["nonbalanced_exact_witness"]
    assert witness["dobrushin_tau_Q"] == "1/2"
    assert witness["B0_is_not_left_balanced"] is True
    assert witness["B1_is_left_balanced"] is True
    assert witness["P_B0_one"] == ["0", "0"]
    assert witness["piT_B0_P"] == ["-1/2", "1/2"]
    assert witness["strictly_upper_triangular_coupling_nonzero"] is True
    assert witness["delay_balance_defect_delta0"] == "1/2"
    assert witness["delay_balance_defect_delta1"] == "0"
    assert witness["delay_balance_defect_delta_B"] == "1/2"


def test_claim_ledgers_are_unique_and_disjoint():
    assert len(PROVED_FLAGS) == len(set(PROVED_FLAGS))
    assert len(OPEN_FLAGS) == len(set(OPEN_FLAGS))
    assert set(PROVED_FLAGS).isdisjoint(OPEN_FLAGS)


def test_all_sources_and_parents_are_exactly_bound(payload):
    manifest = payload["manifest"]
    assert set(manifest["source_sha256"]) == set(SOURCE_MANIFEST)
    assert set(manifest["parent_result_sha256"]) == set(PARENT_RESULTS)


def test_validator_replays_live_parent_after_warm_cache(
    tmp_path: Path,
):
    copied = tmp_path / "repository"
    shutil.copytree(
        REPOSITORY,
        copied,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            ".pytest_cache",
            "build",
            "output",
            "tmp",
            "manuscript",
            "__pycache__",
            "*.pyc",
        ),
    )
    child = json.loads((copied / RESULT_RELATIVE_PATH).read_bytes())
    validate_upper_triangular_transfer_result(child, copied)

    parent_source = copied / DEFECT_SOURCE_RELATIVE_PATH
    parent_source.write_bytes(
        parent_source.read_bytes() + b"\n# hostile live-source mutation\n"
    )
    parent_path = copied / DEFECT_RESULT_RELATIVE_PATH
    parent = json.loads(parent_path.read_bytes())
    parent["certificate"]["collective_scalar_shadowing_tube_proved"] = True
    parent["manifest"]["certificate_sha256"] = defect_canonical_sha256(
        parent["certificate"]
    )
    parent["manifest"]["source_sha256"] = sha256(
        parent_source.read_bytes()
    ).hexdigest()
    parent_path.write_text(
        json.dumps(parent, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    child["manifest"]["parent_result_sha256"][
        DEFECT_RESULT_RELATIVE_PATH
    ] = sha256(parent_path.read_bytes()).hexdigest()
    with pytest.raises(ValueError):
        validate_upper_triangular_transfer_result(child, copied)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"physical_pulse_onset_or_two_sided_routing_validated": True}
        ),
        lambda value: value["certificate"].update(
            {"delay_layer_left_balance_not_required_proved": False}
        ),
        lambda value: value["certificate"].update(
            {"complete_line_green_norm_upper": "9"}
        ),
        lambda value: value["certificate"].update(
            {"delay_balance_defect_range": "0<=delta_B<=2"}
        ),
        lambda value: value["certificate"]["nonbalanced_exact_witness"].update(
            {"piT_B0_P": ["0", "0"]}
        ),
        lambda value: value["certificate"].update(
            {"quadratic_accumulated_coefficient_exact": "703/40"}
        ),
        lambda value: value["certificate"].update(
            {"pointwise_collective_forcing_bound": "uses only M(t)"}
        ),
        lambda value: value["manifest"].update({"extra": "forbidden"}),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
        lambda value: value["manifest"]["parent_result_sha256"].update(
            {PARENT_RESULTS[0]: "0" * 64}
        ),
    ],
)
def test_hostile_mutations_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises(ValueError):
        validate_upper_triangular_transfer_result(changed, REPOSITORY)


def test_note_states_triangular_mechanism_and_open_boundary():
    text = (REPOSITORY / SOURCE_MANIFEST[2]).read_text()
    assert "upper triangular" in text.lower()
    assert "direct sum" in text.lower()
    assert "row-mass identity" in text
    assert "nonnegativity supplies" in text
    assert "391}{2000" in text
    assert "391(2+\\sqrt5)}{4000" in text
    assert "27\\sqrt5}{800" in text
    assert "cannot in general be replaced" in text
    assert "proved topology-uniform estimate" in text
    assert "cannot infer" in text
    assert "purely quadratic enlarged-class estimate" in text
    assert "scalar leaky root" in text
    assert "physical pulse onset" in text
