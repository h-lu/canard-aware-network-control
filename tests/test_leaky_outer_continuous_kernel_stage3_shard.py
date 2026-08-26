from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.directed_interval import DirectedInterval
from canard_control.leaky_outer_continuous_kernel_stage3_shard import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    canonical_sha256,
    directed_picard_matrix_step,
    validate_continuous_kernel_stage3_shard_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_continuous_shard_replays(payload):
    validate_continuous_kernel_stage3_shard_result(payload, REPOSITORY)


def test_both_exact_ac_injection_shards_close(payload):
    certificate = payload["certificate"]
    shards = certificate["injection_shards"]
    assert [shard["delay_id"] for shard in shards] == ["tau_0", "tau_1"]
    for shard in shards:
        assert gmpy2.mpq(shard["minimum_delay_minus_elapsed_lower"]) > 8
        assert gmpy2.mpq(shard["path_expansion_radius_upper"]) < gmpy2.mpq(
            "0.02"
        )
        assert gmpy2.mpq(shard["endpoint_resolvent_inf_norm_upper"]) < gmpy2.mpq(
            "1.03"
        )
        assert gmpy2.mpq(shard["endpoint_density_inf_norm_upper"]) < gmpy2.mpq(
            "0.01"
        )
        for name in (
            "initial_dirac_jump_is_identity",
            "delayed_feedback_zero_on_cell",
            "interval_picard_endpoint_validated",
            "exact_ac_density_injection_validated",
            "composable_endpoint_interface_validated",
        ):
            assert shard[name] is True


def test_exact_orbit_period_uncertainty_is_visible(payload):
    certificate = payload["certificate"]
    stored = certificate["stored_period_interval"]
    exact = certificate["exact_period_interval"]
    assert gmpy2.mpq(exact["lower"]) < gmpy2.mpq(stored["lower"])
    assert gmpy2.mpq(exact["upper"]) > gmpy2.mpq(stored["upper"])
    assert certificate["exact_orbit_radius"] == "1e-8"


def test_public_picard_step_accepts_a_delayed_forcing_box():
    precision = 160
    zero = DirectedInterval.from_decimal(0, precision)
    one = DirectedInterval.from_decimal(1, precision)
    tenth = DirectedInterval.from_decimal("0.1", precision)
    matrix = ((one, zero), (zero, one))
    coefficient = ((zero, zero), (zero, zero))
    forcing = ((tenth, zero), (zero, tenth))
    step = DirectedInterval.from_decimal("0.01", precision)
    path, endpoint, expansion, norm = directed_picard_matrix_step(
        current_matrix=matrix,
        current_coefficient=coefficient,
        delayed_forcing=forcing,
        step=step,
    )
    assert expansion > 0
    assert endpoint[0][0].lower <= gmpy2.mpq("1.001") <= endpoint[0][0].upper
    assert endpoint[1][1].lower <= gmpy2.mpq("1.001") <= endpoint[1][1].upper
    assert norm > 1
    assert path[0][0].lower < 1 < path[0][0].upper


def test_global_transfer_and_contraction_remain_false(payload):
    certificate = payload["certificate"]
    claims = certificate["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    budget = certificate["global_transfer_budget"]
    assert budget["validated_theta_cell_count"] == 1
    assert not budget["full_period_density_propagation_complete"]
    assert not budget["returned_total_variation_accumulation_complete"]
    assert not budget["stage2_linear_gate_re_evaluated"]
    assert budget["voltage_shadow_transfer_error_upper"] is None
    assert budget["recovery_shadow_transfer_error_upper"] is None


def _refresh(value):
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"]["claim_status"].update(
            {"all_theta_cells_continuously_propagated": True}
        ),
        lambda value: value["certificate"]["global_transfer_budget"].update(
            {"voltage_shadow_transfer_error_upper": "0"}
        ),
        lambda value: value["certificate"]["injection_shards"][0].update(
            {"delayed_feedback_zero_on_cell": False}
        ),
        lambda value: value["certificate"]["injection_shards"][0].update(
            {"minimum_delay_minus_elapsed_lower": "-1"}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_mutations_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_continuous_kernel_stage3_shard_result(changed, REPOSITORY)


def test_note_preserves_local_shard_scope():
    text = (
        REPOSITORY / "docs/leaky-outer-continuous-kernel-stage3-shard.md"
    ).read_text()
    normalized = " ".join(text.split())
    assert "two rigorous, composable AC-density injection shards" in normalized
    assert "There is no omitted delayed term" in normalized
    assert "not re-evaluated" in normalized
    assert "No arbitrary-" in normalized and "contraction" in normalized
