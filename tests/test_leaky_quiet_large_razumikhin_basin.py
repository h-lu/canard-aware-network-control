from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path

import pytest

from canard_control.leaky_quiet_large_razumikhin_basin import (
    DECAY_RATE,
    EXPONENTIAL_DELAY_FACTOR_UPPER,
    FALSE_FLAGS,
    HISTORY_SUBLEVEL,
    MAXIMUM_DELAY_UPPER,
    PHYSICAL_DELAY_MULTIPLIERS,
    RAZUMIKHIN_RATIO,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    _alpha_interval,
    build_large_quiet_basin_certificate,
    exact_large_basin_defects,
    validate_large_quiet_basin_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_exact_radial_algebra():
    assert exact_large_basin_defects() == (0,) * 6


def test_cuberoot_and_delay_majorants_are_exactly_oriented():
    alpha = _alpha_interval(160)
    lower_numerator, lower_denominator = alpha.lower.as_integer_ratio()
    upper_numerator, upper_denominator = alpha.upper.as_integer_ratio()
    lower = Fraction(int(lower_numerator), int(lower_denominator))
    upper = Fraction(int(upper_numerator), int(upper_denominator))
    assert lower**3 < Fraction(3, 4) < upper**3

    largest_delay_multiplier = max(PHYSICAL_DELAY_MULTIPLIERS)
    assert largest_delay_multiplier**2 * 5 < MAXIMUM_DELAY_UPPER**2
    delay_rate_product = DECAY_RATE * MAXIMUM_DELAY_UPPER
    assert delay_rate_product == Fraction(9, 8000)
    assert EXPONENTIAL_DELAY_FACTOR_UPPER == 1 / (1 - delay_rate_product)
    assert EXPONENTIAL_DELAY_FACTOR_UPPER < RAZUMIKHIN_RATIO


def test_directed_large_basin_closes():
    certificate = build_large_quiet_basin_certificate()
    assert HISTORY_SUBLEVEL == Fraction(1, 125)
    assert float(certificate.maximum_normalized_derivative_upper) < 0
    assert float(certificate.derivative_rate_lower) > 1.0e-4
    assert certificate.ambiguous_endpoint_cell_count <= 4
    assert certificate.physical_delays == (
        "4*sqrt(5)",
        "5*sqrt(5)",
    )
    assert certificate.exact_symbolic_zero_defect_count == 6
    for name in TRUE_FLAGS:
        assert getattr(certificate, name) is True
    for name in FALSE_FLAGS:
        assert getattr(certificate, name) is False


def test_tracked_result_replays(payload):
    validate_large_quiet_basin_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"physical_pulse_onset_validated": True}
        ),
        lambda value: value["certificate"].update(
            {"history_sublevel": "1/100"}
        ),
        lambda value: value["certificate"].update(
            {"precision_bits": 160.0}
        ),
        lambda value: value["manifest"].update({"extra": "forbidden"}),
        lambda value: value["manifest"].update(
            {"default_command": "python forged.py"}
        ),
        lambda value: value["manifest"].update(
            {"arithmetic": "binary64 samples"}
        ),
        lambda value: value["manifest"].update(
            {"small_basin_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {"source": "0" * 64}
        ),
    ],
)
def test_tampering_is_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises(ValueError):
        validate_large_quiet_basin_result(changed, REPOSITORY)


def test_note_keeps_pulse_capture_open():
    text = (REPOSITORY / "docs/leaky-quiet-large-razumikhin-basin.md").read_text()
    assert "does **not** prove" in text
    assert "directed method-of-steps" in text
    assert "makes no claim about \\(J=0.30\\)" in text
