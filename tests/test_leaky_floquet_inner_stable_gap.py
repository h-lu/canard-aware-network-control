from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import gmpy2
import pytest

from canard_control.directed_interval import DirectedInterval, pi_interval
from canard_control.leaky_floquet_compact_cover_engine import (
    Rectangle,
    rectangle_from_path,
    rectangle_strictly_inside_origin_disk,
    validate_cell,
)
from canard_control.leaky_floquet_inner_right_half_cover import (
    _prepare_inner_candidate,
)
from canard_control.leaky_floquet_inner_stable_gap import (
    ALWAYS_FALSE,
    CORRECTION_RADIUS,
    GAMMA,
    PINNED_OPENBLAS_NUM_THREADS,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STRUCTURAL_TRUE,
    TRUE_ON_COMPLETE,
    _rectangle_strictly_inside_full_origin_disk,
    _root_rectangles,
    _validate_parents,
    canonical_sha256,
    validate_inner_stable_gap_result,
)
from canard_control.leaky_floquet_left_strip_cover_engine import (
    _left_delay_modulus_upper,
    _left_orbit_corrections,
    _left_second_order_raw,
    _left_tail_frequency_upper,
    validate_left_cell,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH
EXPECTED_RESULT_SHA256 = (
    "9180fd43b6c19d8c6d8ee1e34a88cbdaee714a7f784b5ce862625a9f8015190a"
)


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def prepared():
    parent = _validate_parents(REPOSITORY, replay_parents=False)
    base = _build_leaky_base_sequences(parent.orbit, PRECISION_BITS)
    candidate = _prepare_inner_candidate(
        parent.orbit, base, PRECISION_BITS
    )
    correction = DirectedInterval.from_decimal(
        CORRECTION_RADIUS, PRECISION_BITS
    )
    return base, candidate, correction


def _refresh_certificate(value: dict) -> None:
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


def test_tracked_result_sha_is_registered() -> None:
    assert hashlib.sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256


def test_tracked_result_validates(payload: dict) -> None:
    validate_inner_stable_gap_result(
        payload, REPOSITORY, validate_parents=False
    )


def test_quantitative_gap_and_claim_boundary(payload: dict) -> None:
    certificate = payload["certificate"]
    assert certificate["gamma_lower"] == "0.001"
    assert certificate["binary_blas_thread_count"] == int(
        PINNED_OPENBLAS_NUM_THREADS
    )
    assert Decimal(certificate["stable_multiplier_spectral_radius_upper"]) < 1
    assert Decimal(certificate["one_minus_stable_multiplier_modulus_lower"]) > 0
    assert certificate["left_closed_strip_characteristic_value_count"] == 1
    assert certificate["left_open_strip_characteristic_value_count"] == 0
    assert certificate["shifted_closed_strip_characteristic_value_count"] == 2
    assert certificate[
        "shifted_closed_strip_nontranslation_characteristic_value_count"
    ] == 1
    assert certificate["accepted_leaf_count"] == 660
    assert certificate["processed_cell_count"] == 1318
    assert certificate["neutral_disk_leaf_count"] == 16
    assert certificate["neutral_root_owner_leaf_count"] == 1
    assert certificate["neumann_leaf_count"] == 644
    assert certificate["pending_cell_count"] == 0
    assert certificate["accepted_normalized_root_fraction"] == "2"
    assert Decimal(certificate["maximum_contraction_upper"]) < Decimal("0.995")
    assert certificate["worst_cell_finer_split_stress_strict"]
    for name in STRUCTURAL_TRUE + TRUE_ON_COMPLETE:
        assert certificate[name] is True
    for name in ALWAYS_FALSE:
        assert certificate[name] is False


def test_full_neutral_disk_is_strict(payload: dict) -> None:
    certificate = payload["certificate"]
    assert Decimal(certificate["neutral_full_disk_radius"]) > GAMMA
    assert Decimal(certificate["neutral_delay_exponential_modulus_upper"]) > 1
    assert Decimal(certificate["neutral_first_contraction_upper"]) < 0.5
    assert Decimal(certificate["neutral_second_contraction_upper"]) < 0.003
    assert certificate["neutral_full_complex_disk_uniqueness_validated"]
    assert certificate["neutral_full_disk_boundary_zero_free_validated"]


def test_left_disk_geometry_uses_the_farthest_real_corner() -> None:
    rectangle = Rectangle(
        "left_mutant",
        "",
        Decimal("-0.001"),
        Decimal(0),
        Decimal("0.0038"),
        Decimal("0.00385"),
    )
    radius = Decimal("0.0039")
    assert rectangle_strictly_inside_origin_disk(rectangle, radius)
    assert not _rectangle_strictly_inside_full_origin_disk(rectangle, radius)


def _worst_rectangle(payload: dict) -> Rectangle:
    certificate = payload["certificate"]
    roots = {
        root.root_id: root
        for root in _root_rectangles(
            Decimal(certificate["upper_phase_upper"])
        )
    }
    worst = certificate["worst_cell"]
    return rectangle_from_path(roots[worst["root_id"]], worst["path"])


def test_negative_cell_uses_dedicated_left_engine(
    payload: dict, prepared
) -> None:
    base, candidate, correction = prepared
    rectangle = _worst_rectangle(payload)
    assert rectangle.sigma_lower < 0
    with pytest.raises(ValueError, match="right half-plane"):
        validate_cell(
            rectangle,
            candidate,
            base,
            correction,
            PRECISION_BITS,
            Decimal("0.995"),
        )
    expected = payload["certificate"]["maximum_contraction_upper"]
    if os.environ.get("OPENBLAS_NUM_THREADS") == PINNED_OPENBLAS_NUM_THREADS:
        replay = validate_left_cell(
            rectangle,
            candidate,
            base,
            correction,
            PRECISION_BITS,
            Decimal("0.995"),
        )
        assert replay.validated
        actual = replay.worst.contraction_upper
    else:
        environment = dict(os.environ)
        environment["OPENBLAS_NUM_THREADS"] = PINNED_OPENBLAS_NUM_THREADS
        program = """
import json,sys
from decimal import Decimal
from pathlib import Path
from canard_control.directed_interval import DirectedInterval
from canard_control.leaky_floquet_compact_cover_engine import rectangle_from_path
from canard_control.leaky_floquet_inner_stable_gap import CORRECTION_RADIUS, PRECISION_BITS, RESULT_RELATIVE_PATH, _root_rectangles, _validate_parents
from canard_control.leaky_floquet_inner_right_half_cover import _prepare_inner_candidate
from canard_control.leaky_floquet_left_strip_cover_engine import validate_left_cell
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences
repository=Path(sys.argv[1])
payload=json.loads((repository/RESULT_RELATIVE_PATH).read_text())
parent=_validate_parents(repository,replay_parents=False)
base=_build_leaky_base_sequences(parent.orbit,PRECISION_BITS)
candidate=_prepare_inner_candidate(parent.orbit,base,PRECISION_BITS)
correction=DirectedInterval.from_decimal(CORRECTION_RADIUS,PRECISION_BITS)
roots={root.root_id:root for root in _root_rectangles(Decimal(payload['certificate']['upper_phase_upper']))}
worst=payload['certificate']['worst_cell']
rectangle=rectangle_from_path(roots[worst['root_id']],worst['path'])
replay=validate_left_cell(rectangle,candidate,base,correction,PRECISION_BITS,Decimal('0.995'))
print(replay.worst.contraction_upper)
"""
        completed = subprocess.run(
            [sys.executable, "-c", program, str(REPOSITORY)],
            cwd=REPOSITORY,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        actual = completed.stdout.strip()
    assert actual == expected


def test_nonpinned_direct_build_is_rejected() -> None:
    environment = dict(os.environ)
    environment["OPENBLAS_NUM_THREADS"] = "2"
    program = """
from pathlib import Path
from canard_control.leaky_floquet_inner_stable_gap import build_inner_stable_gap_certificate
try:
    build_inner_stable_gap_certificate(Path('.'), maximum_processed_cells=1, replay_parents=False)
except RuntimeError as error:
    assert 'fresh subprocess' in str(error)
else:
    raise SystemExit('nonpinned build was accepted')
"""
    completed = subprocess.run(
        [sys.executable, "-c", program],
        cwd=REPOSITORY,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


def test_tail_formation_uses_absolute_negative_real_part() -> None:
    precision = PRECISION_BITS
    sigma = DirectedInterval.from_decimal("-0.00075", precision)
    phase = DirectedInterval.from_decimal("0.25", precision)
    actual = _left_tail_frequency_upper(sigma, phase, 192, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        right_half_mutant = (
            sigma.upper
            + phase.upper_abs()
            + 2 * 192 * pi_interval(precision).upper
        )
    assert actual > right_half_mutant


def test_delay_orbit_taylor_and_tail_factors_reject_rhp_mutants(
    payload: dict, prepared
) -> None:
    base, _, correction = prepared
    rectangle = _worst_rectangle(payload)
    delay_modulus = _left_delay_modulus_upper(
        rectangle, base, correction, PRECISION_BITS
    )
    assert delay_modulus > 1
    negative_real = DirectedInterval.from_decimal(
        format(-rectangle.sigma_lower, "f"), PRECISION_BITS
    ).upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        center_period_mutant = gmpy2.exp(
            negative_real
            * max(
                base.parameters["tau_0"].upper / base.period.lower,
                base.parameters["tau_1"].upper / base.period.lower,
            )
        )
    assert delay_modulus > center_period_mutant
    fast_inverse = gmpy2.mpfr(
        payload["certificate"]["worst_cell"][
            "fast_tail_diagonal_inverse_split_upper"
        ],
        PRECISION_BITS,
    )
    actual = _left_orbit_corrections(
        base,
        correction,
        rectangle,
        fast_inverse,
        64,
        delay_modulus,
        PRECISION_BITS,
    )
    mutant = _left_orbit_corrections(
        base,
        correction,
        rectangle,
        fast_inverse,
        64,
        gmpy2.mpfr(1, PRECISION_BITS),
        PRECISION_BITS,
    )
    assert all(left >= right for left, right in zip(actual[:4], mutant[:4]))
    assert any(left > right for left, right in zip(actual[:4], mutant[:4]))
    actual_second = _left_second_order_raw(
        base,
        actual[4]["period_upper"],
        actual[4]["delayed_center"],
        delay_modulus,
        PRECISION_BITS,
    )
    mutant_second = _left_second_order_raw(
        base,
        actual[4]["period_upper"],
        actual[4]["delayed_center"],
        gmpy2.mpfr(1, PRECISION_BITS),
        PRECISION_BITS,
    )
    assert actual_second > mutant_second

    sqrt_two = DirectedInterval.from_decimal(2, PRECISION_BITS).sqrt().upper
    worst = payload["certificate"]["worst_cell"]
    slow_inverse = gmpy2.mpfr(
        worst["slow_tail_diagonal_inverse_split_upper"], PRECISION_BITS
    )
    h = gmpy2.mpfr(worst["split_parameter_radius_upper"], PRECISION_BITS)
    values = actual[4]
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        expected_tail_voltage = fast_inverse * (
            h
            + values["period_upper"]
            * (
                values["current_uniform"]
                + 2 * sqrt_two * delay_modulus * values["delayed_uniform"]
            )
        ) + slow_inverse * values["period_upper"] * values["epsilon"]
        mutant_tail_voltage = fast_inverse * (
            h
            + values["period_upper"]
            * (
                values["current_uniform"]
                + 2 * sqrt_two * values["delayed_uniform"]
            )
        ) + slow_inverse * values["period_upper"] * values["epsilon"]
    stored_tail_voltage = gmpy2.mpfr(
        worst["tail_to_tail_voltage_input_upper"], PRECISION_BITS
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        relative_replay_error = abs(
            stored_tail_voltage - expected_tail_voltage
        ) / expected_tail_voltage
    # The stored fast/slow inverse bounds have been decimalized and loaded
    # again, so exact equality is neither expected nor used.
    assert relative_replay_error < gmpy2.mpfr("1e-45")
    assert stored_tail_voltage > mutant_tail_voltage


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"gamma_lower": "0.01"}
        ),
        lambda value: value["certificate"].update(
            {"binary_blas_thread_count": 2}
        ),
        lambda value: value["certificate"].update(
            {"left_open_strip_characteristic_value_count": 1}
        ),
        lambda value: value["certificate"].update(
            {"left_closed_strip_characteristic_value_count": 0}
        ),
        lambda value: value["certificate"].update(
            {"shifted_closed_strip_characteristic_value_count": 3}
        ),
        lambda value: value["certificate"].update(
            {"stable_multiplier_spectral_radius_upper": "1"}
        ),
        lambda value: value["certificate"].update(
            {"neutral_first_contraction_upper": "1.1"}
        ),
        lambda value: value["certificate"].update(
            {"negative_real_delay_modulus_restored": False}
        ),
        lambda value: value["certificate"].update(
            {"negative_real_tail_frequency_absolute_value_restored": False}
        ),
        lambda value: value["certificate"].update(
            {"negative_real_delay_taylor_factor_restored": False}
        ),
        lambda value: value["certificate"].update(
            {"negative_real_full_disk_farthest_corner_used": False}
        ),
        lambda value: value["certificate"].update(
            {"source_validated_compact_history_monodromy_used": False}
        ),
        lambda value: value["certificate"].update(
            {
                "history_spectrum_to_fourier_characteristic_values_bridge_used": (
                    False
                )
            }
        ),
        lambda value: value["certificate"].update(
            {"leaf_partition_sha256": "0" * 64}
        ),
        lambda value: value["certificate"].update(
            {"neutral_root_owner_leaf_count": 2}
        ),
        lambda value: value["certificate"]["leaves"][0].update(
            {"proof_kind": "forged"}
        ),
        lambda value: value["manifest"].update(
            {"right_half_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
        lambda value: value["scope"].update(
            {"inner_stable_manifold_validated": True}
        ),
    ],
)
def test_hostile_tampering_is_rejected(payload: dict, mutation) -> None:
    changed = deepcopy(payload)
    mutation(changed)
    _refresh_certificate(changed)
    with pytest.raises(ValueError):
        validate_inner_stable_gap_result(
            changed, REPOSITORY, validate_parents=False
        )


def test_manifest_avoids_active_outer_or_old_fhn_phase_files(payload: dict) -> None:
    sources = payload["manifest"]["source_sha256"]
    active_outer = "src/canard_control/leaky_floquet_outer_" + "right_half_cover.py"
    assert active_outer not in sources
    assert "src/canard_control/fhn_synchronous_floquet_right_half_cover.py" not in sources
    assert "src/canard_control/fhn_bloch_outer_validation.py" not in sources


def test_note_states_gap_and_scope() -> None:
    text = " ".join(
        (REPOSITORY / "docs/leaky-floquet-inner-stable-gap.md")
        .read_text()
        .split()
    )
    assert "|\\mu|\\le e^{-0.001}<1" in text
    assert "full complex neutral disk" in text
    assert "not uniform on a parameter box" in text
    assert "does not construct a spectral projection" in text
    assert "physical-onset" in text
