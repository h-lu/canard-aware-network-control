from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path

import gmpy2
import pytest

import canard_control.leaky_pulse_quiet_capture as capture
from canard_control.leaky_pulse_quiet_capture import (
    FALSE_FLAGS,
    GRID_DENOMINATOR,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    _forward_nodes,
    build_pulse_quiet_capture_certificate,
    exact_pulse_capture_defects,
    validate_pulse_quiet_capture_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


@pytest.fixture(scope="module")
def certificate():
    return build_pulse_quiet_capture_certificate()


def test_exact_error_split_and_log_norm_algebra():
    assert exact_pulse_capture_defects() == (0,) * 8


def test_negative_p12_magnitude_is_rounded_outward(monkeypatch):
    monkeypatch.setattr(capture, "P11", Fraction(1))
    monkeypatch.setattr(capture, "P12", Fraction(-2, 3))
    monkeypatch.setattr(capture, "P22", Fraction(1))
    bound = capture._p_box_norm_upper(
        gmpy2.mpfr(1), gmpy2.mpfr(1), 64
    )
    numerator, denominator = bound.as_integer_ratio()
    bound_squared = Fraction(int(numerator), int(denominator)) ** 2
    assert bound_squared >= Fraction(10, 3)


def test_exact_union_grid_and_delayed_translation_counts(certificate):
    assert GRID_DENOMINATOR == 24
    assert len(_forward_nodes()) == certificate.grid_cell_count + 1
    assert certificate.grid_cell_count == 7728
    assert certificate.forced_cell_count > 0
    assert (
        certificate.delay_four_initial_history_cell_count
        + certificate.delay_four_translated_cell_count
        == certificate.grid_cell_count
    )
    assert (
        certificate.delay_five_initial_history_cell_count
        + certificate.delay_five_translated_cell_count
        == certificate.grid_cell_count
    )


def test_directed_capture_has_strict_margins(certificate):
    assert float(certificate.minimum_cell_closure_gap_lower) > 0
    assert float(certificate.retained_history_p_norm_margin_lower) > 0.01
    assert float(certificate.maximum_retained_total_lyapunov_upper) < 1 / 125
    assert float(certificate.maximum_validated_p_error_radius_upper) < 1e-18
    assert certificate.retained_history_cell_count == 240
    for name in TRUE_FLAGS:
        assert getattr(certificate, name) is True
    for name in FALSE_FLAGS:
        assert getattr(certificate, name) is False


def test_tracked_result_replays(payload):
    validate_pulse_quiet_capture_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"unique_physical_pulse_onset_validated": True}
        ),
        lambda value: value["certificate"].update(
            {"retained_history_p_norm_margin_lower": "1"}
        ),
        lambda value: value["manifest"].update({"extra": "forbidden"}),
        lambda value: value["manifest"].update(
            {"arithmetic": "binary64 point samples"}
        ),
        lambda value: value["manifest"].update(
            {"default_command": "python unbound.py"}
        ),
        lambda value: value["manifest"].update({"gmpy2": "hostile"}),
        lambda value: value["manifest"].update(
            {"large_basin_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"].update(
            {"pulse_terminal_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {"source": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {"large_basin_source": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {"quiet_p_source": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {"extra": "0" * 64}
        ),
        lambda value: value["certificate"].update(
            {"precision_bits": 192.0}
        ),
    ],
)
def test_tampering_is_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises(ValueError):
        validate_pulse_quiet_capture_result(changed, REPOSITORY)


def test_note_keeps_onset_and_outer_capture_open():
    text = (REPOSITORY / "docs/leaky-pulse-quiet-capture.md").read_text()
    assert "does **not** prove an onset" in text
    assert "outer periodic orbit" in text
    assert "complete retained history" in text
    assert "not replaced by the nearest MPFR guide center" in text
