from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from canard_control.directed_interval import DirectedInterval
from canard_control.leaky_floquet_compact_cover_engine import (
    Rectangle,
    rectangle_from_path,
)
from canard_control.leaky_floquet_inner_stable_gap import (
    CORRECTION_RADIUS,
    PINNED_OPENBLAS_NUM_THREADS,
    RESULT_RELATIVE_PATH as BASE_GAP_RESULT_RELATIVE_PATH,
    _prepare_inner_candidate,
    _rectangle_strictly_inside_full_origin_disk,
)
from canard_control.leaky_floquet_inner_strong_stable_gap import (
    ALWAYS_FALSE,
    BASE_GAMMA,
    GAMMA,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STRUCTURAL_TRUE,
    TRUE_ON_COMPLETE,
    _root_rectangles,
    _validate_base_gap,
    canonical_sha256,
    validate_inner_strong_stable_gap_result,
)
from canard_control.leaky_floquet_left_strip_cover_engine import (
    validate_left_cell,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH
EXPECTED_RESULT_SHA256 = (
    "e61792cd946103b33da8209cae1c3123baa07b14aa6ccef4ae63b1c9a14848cc"
)


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def prepared():
    _, parent = _validate_base_gap(REPOSITORY, replay_parents=False)
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
    validate_inner_strong_stable_gap_result(
        payload, REPOSITORY, validate_parents=False
    )


def test_strong_gap_counts_and_claim_boundary(payload: dict) -> None:
    certificate = payload["certificate"]
    assert certificate["base_gamma_lower"] == "0.001"
    assert certificate["gamma_lower"] == "0.01"
    assert certificate["binary_blas_thread_count"] == int(
        PINNED_OPENBLAS_NUM_THREADS
    )
    assert Decimal(certificate["stable_multiplier_spectral_radius_upper"]) < 1
    assert Decimal(certificate["one_minus_stable_multiplier_modulus_lower"]) > 0
    assert certificate["extension_closed_slab_characteristic_value_count"] == 0
    assert certificate["combined_left_closed_strip_characteristic_value_count"] == 1
    assert certificate["combined_left_open_strip_characteristic_value_count"] == 0
    assert certificate["combined_shifted_closed_strip_characteristic_value_count"] == 2
    assert certificate["combined_shifted_nontranslation_characteristic_value_count"] == 1
    assert certificate["accepted_leaf_count"] == 5254
    assert certificate["processed_cell_count"] == 10506
    assert certificate["neutral_parent_leaf_count"] == 50
    assert certificate["neumann_leaf_count"] == 5204
    assert certificate["pending_cell_count"] == 0
    assert certificate["accepted_normalized_root_fraction"] == "2"
    assert Decimal(certificate["maximum_contraction_upper"]) < Decimal("0.995")
    assert certificate["worst_cell_finer_split_stress_strict"]
    for name in STRUCTURAL_TRUE + TRUE_ON_COMPLETE:
        assert certificate[name] is True
    for name in ALWAYS_FALSE:
        assert certificate[name] is False


def test_extension_geometry_and_parent_seam(payload: dict) -> None:
    certificate = payload["certificate"]
    roots = _root_rectangles(Decimal(certificate["upper_phase_upper"]))
    assert roots[0].sigma_lower == -GAMMA
    assert roots[0].sigma_upper == -BASE_GAMMA
    assert roots[1].sigma_lower == -GAMMA
    assert roots[1].sigma_upper == -BASE_GAMMA
    assert Decimal(certificate["maximum_extension_delay_modulus_upper"]) > 1
    base_payload = json.loads(
        (REPOSITORY / BASE_GAP_RESULT_RELATIVE_PATH).read_text()
    )
    assert Decimal(certificate["maximum_extension_delay_modulus_upper"]) > Decimal(
        base_payload["certificate"]["maximum_left_delay_modulus_upper"]
    )


def test_every_local_leaf_is_strictly_in_parent_disk_and_excludes_zero(
    payload: dict,
) -> None:
    certificate = payload["certificate"]
    roots = {
        root.root_id: root
        for root in _root_rectangles(
            Decimal(certificate["upper_phase_upper"])
        )
    }
    local = 0
    for leaf in certificate["leaves"]:
        if leaf["proof_kind"] != "neutral_parent_zero_free":
            continue
        local += 1
        rectangle = rectangle_from_path(
            roots[leaf["root_id"]], leaf["path"]
        )
        assert _rectangle_strictly_inside_full_origin_disk(
            rectangle, Decimal("0.0039")
        )
        assert rectangle.sigma_upper <= -BASE_GAMMA < 0
    assert local == certificate["neutral_parent_leaf_count"]


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


def test_worst_cell_replays_only_on_pinned_blas(
    payload: dict, prepared
) -> None:
    base, candidate, correction = prepared
    rectangle = _worst_rectangle(payload)
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
from canard_control.leaky_floquet_inner_stable_gap import CORRECTION_RADIUS, _prepare_inner_candidate
from canard_control.leaky_floquet_inner_strong_stable_gap import PRECISION_BITS, RESULT_RELATIVE_PATH, _root_rectangles, _validate_base_gap
from canard_control.leaky_floquet_left_strip_cover_engine import validate_left_cell
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences
repository=Path(sys.argv[1])
payload=json.loads((repository/RESULT_RELATIVE_PATH).read_text())
_,parent=_validate_base_gap(repository,replay_parents=False)
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


def test_nonpinned_direct_strong_build_is_rejected() -> None:
    environment = dict(os.environ)
    environment["OPENBLAS_NUM_THREADS"] = "2"
    program = """
from pathlib import Path
from canard_control.leaky_floquet_inner_strong_stable_gap import build_inner_strong_stable_gap_certificate
try:
    build_inner_strong_stable_gap_certificate(Path('.'), maximum_processed_cells=1, replay_parents=False)
except RuntimeError as error:
    assert 'fresh subprocess' in str(error)
else:
    raise SystemExit('nonpinned strong build was accepted')
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


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update({"gamma_lower": "0.1"}),
        lambda value: value["certificate"].update({"binary_blas_thread_count": 2}),
        lambda value: value["certificate"].update(
            {"extension_closed_slab_characteristic_value_count": 1}
        ),
        lambda value: value["certificate"].update(
            {"combined_left_open_strip_characteristic_value_count": 1}
        ),
        lambda value: value["certificate"].update(
            {"combined_shifted_closed_strip_characteristic_value_count": 3}
        ),
        lambda value: value["certificate"].update(
            {"stable_multiplier_spectral_radius_upper": "1"}
        ),
        lambda value: value["certificate"].update(
            {"base_compact_history_monodromy_bridge_used": False}
        ),
        lambda value: value["certificate"].update(
            {"negative_real_delay_modulus_restored": False}
        ),
        lambda value: value["certificate"].update(
            {"tail_diagonal_edge_monotonicity_validated": False}
        ),
        lambda value: value["certificate"].update(
            {"leaf_partition_sha256": "0" * 64}
        ),
        lambda value: value["certificate"].update(
            {"neutral_parent_leaf_count": 49}
        ),
        lambda value: value["certificate"]["leaves"][0].update(
            {"proof_kind": "forged"}
        ),
        lambda value: value["manifest"].update(
            {"base_gap_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
        lambda value: value["scope"].update(
            {"stable_boundary_power_bound_validated": True}
        ),
    ],
)
def test_hostile_tampering_is_rejected(payload: dict, mutation) -> None:
    changed = deepcopy(payload)
    mutation(changed)
    _refresh_certificate(changed)
    with pytest.raises(ValueError):
        validate_inner_strong_stable_gap_result(
            changed, REPOSITORY, validate_parents=False
        )


def test_manifest_avoids_active_outer_or_old_fhn_phase_files(payload: dict) -> None:
    sources = payload["manifest"]["source_sha256"]
    active_outer = "src/canard_control/leaky_floquet_outer_" + "right_half_cover.py"
    assert active_outer not in sources
    assert "src/canard_control/fhn_synchronous_floquet_right_half_cover.py" not in sources
    assert "src/canard_control/fhn_bloch_outer_validation.py" not in sources


def test_note_states_strength_and_scope() -> None:
    text = " ".join(
        (REPOSITORY / "docs/leaky-floquet-inner-strong-stable-gap.md")
        .read_text()
        .split()
    )
    assert "\\rho_s\\le e^{-0.01}<1" in text
    assert "extension rather than replacement" in text.lower()
    assert "not, by itself, a bound on powers" in text
    assert "does not make the estimate uniform on a parameter box" in text
