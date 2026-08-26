from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_dobrushin_complete_line_inverse import (
    OPEN_FLAGS,
    PROVED_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    build_leaky_complete_line_inverse_result,
    validate_leaky_complete_line_inverse_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_tracked_complete_line_result_validates(payload):
    validate_leaky_complete_line_inverse_result(payload, REPOSITORY)


def test_exact_claim_boundary(payload):
    certificate = payload["certificate"]
    for name in PROVED_FLAGS:
        assert certificate[name] is True
    for name in OPEN_FLAGS:
        assert certificate[name] is False
    assert certificate["complete_line_green_norm_upper"] == "10"
    assert certificate["forcing_space"] == "C_b(R,E_{N,perp})"
    assert certificate["green_operator_mapping"].startswith(
        "G_perp:C_b(R,E_{N,perp})->C_b(R,X_{N,lambda})"
    )
    assert "no N-uniform equivalence with Euclidean" in certificate[
        "dimension_uniformity_scope"
    ]
    assert "graph norm" in certificate["transverse_lin_operator_spaces"]


def test_json_tuple_fields_are_canonical_arrays(payload):
    assert isinstance(payload["certificate"]["transferred_data"], list)
    assert isinstance(payload["certificate"]["canonical_lin_hypotheses"], list)
    replay = build_leaky_complete_line_inverse_result(REPOSITORY)
    assert replay == payload


def test_parent_and_all_local_sources_are_bound(payload):
    manifest = payload["manifest"]
    assert set(manifest["source_sha256"]) == set(SOURCE_MANIFEST)
    assert manifest["halanay_parent_result"].endswith(
        "leaky_dobrushin_transverse_halanay.json"
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"scalar_leaky_simple_canard_root_validated": True}
        ),
        lambda value: value["certificate"].update(
            {"conditional_scalar_simple_root_data_transfer_exactly": False}
        ),
        lambda value: value["certificate"].update(
            {"complete_line_green_norm_upper": "9"}
        ),
        lambda value: value["manifest"].update(
            {"halanay_parent_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"].update({"extra": "forbidden"}),
        lambda value: value["manifest"].update(
            {"default_command": "python forged.py"}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
        lambda value: value["certificate"]["transferred_data"].reverse(),
        lambda value: value["certificate"].update(
            {"green_operator_mapping": "G backwards in time"}
        ),
    ],
)
def test_hostile_tampering_is_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises(ValueError):
        validate_leaky_complete_line_inverse_result(changed, REPOSITORY)


def test_note_keeps_scalar_canard_and_onset_open():
    text = (
        REPOSITORY / "docs/leaky-dobrushin-complete-line-inverse.md"
    ).read_text()
    assert "scalar complete-history canard root" in text
    assert "has not yet been proved" in text
    assert "physical pulse onset" in text
    assert "At no point is the RFDE semiflow inverted backward" in text
    assert "does not cover independently chosen endpoint rules" in text
    assert "additional asynchronous roots" in text
