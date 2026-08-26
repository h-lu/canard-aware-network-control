from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_floquet_riesz_reduction import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TAIL_DIAGONAL_GAP_MULTIPLIER,
    TRUE_FLAGS,
    canonical_sha256,
    validate_leaky_floquet_riesz_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_tracked_reduction_validates(payload):
    validate_leaky_floquet_riesz_result(payload, REPOSITORY)


def test_both_branches_have_strict_tail_and_outer_gates(payload):
    branches = payload["artifact"]["branches"]
    assert set(branches) == {"inner_saddle_candidate", "outer_pulse"}
    for branch in branches.values():
        assert 0 < float(branch["tail_contraction_upper"]) < 1
        assert 0 < float(branch["outer_half_plane_contraction_upper"]) < 1
        assert branch["complex_finite_dimension"] == 258
        for name in TRUE_FLAGS:
            assert branch[name] is True
        for name in FALSE_FLAGS:
            assert branch[name] is False
        assert branch["directed_keyhole_zero_count"] is None


def test_pencil_sign_tail_gap_and_direct_sources_are_bound(payload):
    theorem = payload["artifact"]["theorem"]
    assert theorem["leaky_recovery_row"].endswith(
        "+T*epsilon*y_w"
    )
    assert TAIL_DIAGONAL_GAP_MULTIPLIER == 129
    assert theorem["tail_diagonal_gap"].endswith(">=129*pi")
    assert (
        "src/canard_control/leaky_periodic_validation.py"
        in SOURCE_MANIFEST
    )
    assert (
        "src/canard_control/fhn_periodic_infinite_validation.py"
        in SOURCE_MANIFEST
    )


def _alter_bound_and_refresh_self_hash(value):
    value["artifact"]["branches"]["outer_pulse"][
        "current_coefficient_uniform_wiener_upper"
    ] = "4.9"
    value["manifest"]["artifact_sha256"] = canonical_sha256(
        value["artifact"]
    )


def _alter_pencil_sign_and_refresh_self_hash(value):
    value["artifact"]["theorem"]["leaky_recovery_row"] = (
        "(d_theta+s)y_w-T*epsilon*y_v-T*epsilon*y_w"
    )
    value["manifest"]["artifact_sha256"] = canonical_sha256(
        value["artifact"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["artifact"]["branches"]["outer_pulse"].update(
            {"outer_attracting_floquet_index_validated": True}
        ),
        lambda value: value["artifact"]["branches"][
            "inner_saddle_candidate"
        ].update({"directed_keyhole_zero_count": 1}),
        lambda value: value["manifest"].update({"extra": "forbidden"}),
        lambda value: value["manifest"].update(
            {"arithmetic_scope": "binary64 determinant winding"}
        ),
        lambda value: value["manifest"].update(
            {"floquet_parent_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"].update(
            {"default_command": "python forged.py"}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {"src/canard_control/leaky_periodic_validation.py": "0" * 64}
        ),
        _alter_bound_and_refresh_self_hash,
        _alter_pencil_sign_and_refresh_self_hash,
    ],
)
def test_hostile_tampering_is_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises(ValueError):
        validate_leaky_floquet_riesz_result(changed, REPOSITORY)


def test_note_keeps_indices_open():
    text = (REPOSITORY / "docs/leaky-floquet-riesz-reduction.md").read_text()
    assert "neither unstable index is yet counted" in text
    assert "258" in text
    assert "physical pulse onset all remain unproved" in text
    assert "half-open" in text
