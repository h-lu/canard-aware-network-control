"""Tests for the rigorous target second-method-step cover."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import gmpy2
import pytest

import canard_control.fixed_epsilon_target_first_step_cover as first
from canard_control.fixed_epsilon_target_second_step_cover import (
    FALSE_METHOD_FLAGS,
    OPEN_FLAGS,
    RIGOROUS_TRUE_FLAGS,
    _point,
    _restrict_polynomial_to_half,
    _symmetric_ball_box,
    aggregate_second_step_shards,
    build_target_second_method_step_cover_certificate_from_shards,
    exact_second_step_cover_defects,
    probe_second_step_cover,
    shard_relative_path,
    validate_second_step_shard_payload,
    validate_target_second_method_step_cover_audit,
    validate_target_second_method_step_cover_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / "experiments/results/fixed_epsilon_target_second_step_cover.json"


def _shards(precision: int) -> list[dict[str, object]]:
    return [
        json.loads(
            (REPOSITORY / shard_relative_path(precision, index)).read_text(
                encoding="utf-8"
            )
        )
        for index in range(20)
    ]


def _canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    ).hexdigest()


@pytest.fixture(scope="module")
def certificate():
    return build_target_second_method_step_cover_certificate_from_shards(
        REPOSITORY
    )


def test_exact_slot_log_norm_gronwall_and_partition_audit_is_zero() -> None:
    defects = exact_second_step_cover_defects()
    assert len(defects) == 16
    assert all(defect == 0 for defect in defects)


def test_exact_half_cell_polynomial_reparameterization() -> None:
    precision = 192
    polynomial = tuple(_point(value, precision) for value in ("1", "-2", "3", "-4"))
    zero_half = _restrict_polynomial_to_half(polynomial, 0)
    one_half = _restrict_polynomial_to_half(polynomial, 1)
    for half, restricted in ((0, zero_half), (1, one_half)):
        for endpoint in (0, 1):
            value = first._polynomial(restricted, _point(endpoint, precision))
            source = first._polynomial(
                polynomial,
                _point(half + endpoint, precision) / _point(2, precision),
            )
            assert value.lower <= source.lower <= source.upper <= value.upper


def test_euclidean_ball_box_uses_declared_precision_directed_endpoints() -> None:
    precision = 192
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        radius = gmpy2.mpfr("1.23456789012345678901234567890123456789e-10")
    box = _symmetric_ball_box(radius, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        exact_lower = -radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        exact_upper = gmpy2.mpfr(radius)
    assert box.lower.precision == precision
    assert box.upper.precision == precision
    assert box.lower <= exact_lower
    assert box.upper >= exact_upper


def test_all_pinned_shards_close_and_have_exact_source_counts() -> None:
    for precision in (192, 256):
        payloads = _shards(precision)
        for index, payload in enumerate(payloads):
            probe = validate_second_step_shard_payload(
                payload, precision=precision, label_index=index
            )
            assert probe.first_failure is None
            assert probe.completed_second_time_cells == 400
            assert (
                probe.delay_four_previous_solution_cell_count,
                probe.delay_five_affine_history_cell_count,
                probe.delay_five_c4_patch_cell_count,
                probe.delay_five_previous_solution_cell_count,
            ) == (400, 100, 100, 200)


def test_hostile_aggregator_rejects_missing_swapped_and_tampered_shards() -> None:
    payloads = _shards(192)
    with pytest.raises(ValueError, match="exactly twenty"):
        aggregate_second_step_shards(payloads[:-1], precision=192)

    swapped = deepcopy(payloads)
    swapped[0], swapped[1] = swapped[1], swapped[0]
    with pytest.raises(ValueError, match="label index"):
        aggregate_second_step_shards(swapped, precision=192)

    body_tampered = deepcopy(payloads[0])
    body_tampered["body"]["probe"]["minimum_time_minor"] = "0.2"
    with pytest.raises(ValueError, match="body digest"):
        validate_second_step_shard_payload(
            body_tampered, precision=192, label_index=0
        )

    digest_tampered = deepcopy(payloads[0])
    digest_tampered["body"]["probe"]["proof_cell_digest_sha256"] = "0" * 64
    digest_tampered["body_sha256"] = _canonical_sha256(digest_tampered["body"])
    with pytest.raises(ValueError, match="pinned run"):
        validate_second_step_shard_payload(
            digest_tampered, precision=192, label_index=0
        )

    sign_tampered = deepcopy(payloads[0])
    sign_tampered["body"]["probe"]["minimum_time_minor"] = "0"
    sign_tampered["body_sha256"] = _canonical_sha256(sign_tampered["body"])
    with pytest.raises(ValueError, match="not strictly positive"):
        validate_second_step_shard_payload(
            sign_tampered,
            precision=192,
            label_index=0,
            require_pinned_digest=False,
        )


def test_aggregate_has_full_grid_and_strict_global_margins(certificate) -> None:
    assert certificate.physical_time_interval == ("1", "3")
    assert certificate.full_physical_time_interval == ("-3", "3")
    assert certificate.regularity_breakpoints == ("1.5", "2")
    for probe, precision in (
        (certificate.primary, 192),
        (certificate.refinement, 256),
    ):
        assert probe.precision_bits == precision
        assert probe.completed_label_cells == 20
        assert probe.completed_second_time_cells == 8000
        assert probe.first_failure is None
        assert Decimal(probe.minimum_time_minor) > Decimal("0.114")
        assert Decimal(probe.minimum_label_minor) > Decimal("1.289")
        assert Decimal(probe.minimum_oriented_determinant) > Decimal("2.13")
        assert Decimal(probe.maximum_raw_determinant) < Decimal("-0.164")
        assert Decimal(probe.minimum_late_entry_x_gap) > Decimal("0.461")
        assert Decimal(probe.minimum_central_picard_gap) > Decimal("5.6e-7")
        assert Decimal(probe.minimum_first_variation_picard_gap) > Decimal("4.7e-5")
        assert Decimal(probe.minimum_second_variation_picard_gap) > Decimal("0.0043")


def test_claim_ledger_promotes_full_physical_but_not_open_collar(certificate) -> None:
    assert all(getattr(certificate, name) for name in RIGOROUS_TRUE_FLAGS)
    assert all(not getattr(certificate, name) for name in FALSE_METHOD_FLAGS)
    assert all(not getattr(certificate, name) for name in OPEN_FLAGS)
    assert certificate.full_physical_strip_interval_cover_validated
    assert certificate.physical_cross_separation_interval_validated
    assert not certificate.expanded_open_collar_interval_validated
    assert not certificate.target_chart_global_embedding_validated


def test_audit_rejects_replay_independence_and_open_claim_promotions(certificate) -> None:
    audit = {"certificate": asdict(certificate)}
    validate_target_second_method_step_cover_audit(audit)

    independent = deepcopy(audit)
    independent["certificate"][
        "independent_second_interval_kernel_replay_validated"
    ] = True
    with pytest.raises(ValueError, match="forbidden second-step method"):
        validate_target_second_method_step_cover_audit(independent)

    promoted = deepcopy(audit)
    promoted["certificate"]["expanded_open_collar_interval_validated"] = True
    with pytest.raises(ValueError, match="open target-chart claim"):
        validate_target_second_method_step_cover_audit(promoted)


def test_generated_result_and_all_source_hashes_validate(certificate) -> None:
    del certificate
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_target_second_method_step_cover_result(payload, REPOSITORY)


def test_result_manifest_rejects_extra_tampered_and_runtime_fields() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    corrupted = deepcopy(payload)
    corrupted["manifest"]["shards"][0]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="shard source manifest"):
        validate_target_second_method_step_cover_result(corrupted, REPOSITORY)

    extra = deepcopy(payload)
    extra["manifest"]["unreviewed_extra"] = "accepted"
    with pytest.raises(ValueError, match="manifest schema"):
        validate_target_second_method_step_cover_result(extra, REPOSITORY)

    command = deepcopy(payload)
    command["manifest"]["default_command"] = "python unbound.py"
    with pytest.raises(ValueError, match="command changed"):
        validate_target_second_method_step_cover_result(command, REPOSITORY)

    arithmetic = deepcopy(payload)
    arithmetic["manifest"]["arithmetic"] = "binary64 samples"
    with pytest.raises(ValueError, match="arithmetic changed"):
        validate_target_second_method_step_cover_result(arithmetic, REPOSITORY)

    runtime = deepcopy(payload)
    runtime["manifest"]["mpfr"] = "unknown"
    with pytest.raises(ValueError, match="runtime changed"):
        validate_target_second_method_step_cover_result(runtime, REPOSITORY)


def test_small_kernel_smoke_uses_claim_bearing_intervals() -> None:
    probe = probe_second_step_cover(
        128,
        label_start_index=0,
        maximum_label_cells=1,
        maximum_second_time_cells=1,
    )
    assert probe.first_failure is None
    assert probe.completed_second_time_cells == 1
    assert Decimal(probe.minimum_time_minor) > 0
    assert Decimal(probe.minimum_oriented_determinant) > 0


def test_note_states_exact_delay_breaks_and_replay_limit() -> None:
    text = (
        REPOSITORY / "docs/fixed-epsilon-target-second-step-cover.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(text.split())
    assert "t=3/2" in compact
    assert "t=2" in compact
    assert "logarithmic norm" in text
    assert "8,000 second-step rectangles" in text
    assert "not an independent implementation" in compact
    assert "enlarged label collar" in text
