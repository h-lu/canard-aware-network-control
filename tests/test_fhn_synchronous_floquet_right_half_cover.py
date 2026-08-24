from __future__ import annotations

from decimal import Decimal
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.fhn_synchronous_floquet_right_half_cover import (
    _binary_complex_max_split_upper,
    _binary_complex_matrix_split_l1_upper,
    _binary_complex_product_split_l1_upper,
    _binary_complex_split_upper,
    validate_right_half_cover_payload,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "experiments"
    / "results"
    / "fhn_synchronous_floquet_right_half_cover.json"
)
EXPECTED_RESULT_SHA256 = (
    "6795e6f19f31ffb6bfcf9abd24efb1c5dde4dccf54d896d01298b3e8f9a0d1c3"
)


def _load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_tracked_artifact_sha_is_locked() -> None:
    assert hashlib.sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256


def test_tracked_cover_is_complete_and_strict() -> None:
    payload = _load()
    validate_right_half_cover_payload(payload)
    certificate = payload["certificate"]
    assert certificate["root_rectangle_count"] == 2
    assert certificate["pending_cell_count"] == 0
    assert certificate["accepted_leaf_count"] == len(certificate["leaves"])
    assert certificate["prefix_complete_dyadic_cover_validated"]
    assert certificate["half_square_strictly_inside_local_disk"]
    assert certificate["negative_half_strip_mode_reversal_conjugacy_validated"]
    assert Decimal(certificate["maximum_contraction_upper"]) < 1
    assert Decimal(certificate["minimum_contraction_margin_lower"]) > 0
    assert max(
        Decimal(leaf["contraction_upper"]) for leaf in certificate["leaves"]
    ) == Decimal(certificate["maximum_contraction_upper"])
    assert Decimal(certificate["worst_cell"]["contraction_upper"]) == Decimal(
        certificate["maximum_contraction_upper"]
    )


def test_zero_free_cover_gives_exact_integer_zero_without_forging_old_homotopy() -> None:
    certificate = _load()["certificate"]
    assert certificate["entire_keyhole_region_zero_free_validated"]
    assert certificate[
        "cellwise_left_preconditioned_full_operator_neumann_homotopy_validated"
    ]
    assert not certificate[
        "exact_schur_to_candidate_finite_homotopy_validated"
    ]
    assert certificate["schur_boundary_winding_deduced_exactly_lower"] == 0
    assert certificate["schur_boundary_winding_deduced_exactly_upper"] == 0
    assert certificate["directed_nontranslation_right_half_strip_zero_count"] == 0
    assert certificate[
        "spectral_set_correspondence_used_without_general_multiplicity_bridge"
    ]


def test_attraction_scope_is_fixed_rank_one_not_general_network_control() -> None:
    payload = _load()
    certificate = payload["certificate"]
    scope = payload["scope"]
    assert certificate[
        "synchronous_nontranslation_unstable_index_zero_validated"
    ]
    assert certificate["synchronous_linear_orbital_attraction_validated"]
    assert certificate[
        "hale_verduyn_lunel_hyperbolic_periodic_orbit_theorem_applied"
    ]
    assert certificate["synchronous_nonlinear_orbital_attraction_validated"]
    assert certificate[
        "fixed_rank_one_full_network_linear_orbital_attraction_validated"
    ]
    assert certificate[
        "fixed_rank_one_full_network_nonlinear_orbital_attraction_validated"
    ]
    assert not certificate["general_network_topology_validated"]
    assert not certificate["biological_pulse_capture_validated"]
    assert scope["fixed_rank_one_full_network_nonlinear_orbital_attraction"]
    assert not scope["general_network_topology"]
    assert not scope["biological_pulse_capture"]


def test_every_leaf_uses_two_strict_input_column_bounds() -> None:
    for leaf in _load()["certificate"]["leaves"]:
        finite = Decimal(leaf["finite_input_column_sum_upper"])
        tail = Decimal(leaf["tail_input_column_sum_upper"])
        contraction = Decimal(leaf["contraction_upper"])
        assert finite < 1
        assert tail < 1
        assert contraction == max(finite, tail)


def test_split_tail_inverse_is_not_replaced_by_euclidean_modulus() -> None:
    sigma = 128.0
    omega = 129.0 * np.pi
    split_inverse = (sigma + abs(omega)) / (sigma * sigma + omega * omega)
    euclidean_inverse = 1.0 / np.hypot(sigma, omega)
    assert split_inverse > euclidean_inverse


def test_four_real_gemm_auditor_bounds_stored_complex_products() -> None:
    rng = np.random.default_rng(20260824)
    left = rng.normal(size=(7, 5)) + 1.0j * rng.normal(size=(7, 5))
    right = rng.normal(size=(5, 6)) + 1.0j * rng.normal(size=(5, 6))
    upper = _binary_complex_product_split_l1_upper(left, right, 160)
    stored = _binary_complex_matrix_split_l1_upper(left @ right, 160)
    assert float(upper) >= float(stored)


def test_binary_component_split_helpers_do_not_round_down_before_mpfr() -> None:
    value = complex(1.0, 2.0**-54)
    component = _binary_complex_split_upper(value, 160)
    maximum = _binary_complex_max_split_upper(np.asarray([value]), 160)
    assert component > 1
    assert maximum > 1


def test_validator_rejects_partition_and_scope_forgery() -> None:
    payload = _load()
    forged = json.loads(json.dumps(payload))
    forged["certificate"]["leaves"].pop()
    with pytest.raises(ValueError):
        validate_right_half_cover_payload(forged)
    forged = json.loads(json.dumps(payload))
    forged["certificate"]["general_network_topology_validated"] = True
    with pytest.raises(ValueError):
        validate_right_half_cover_payload(forged)
    forged = json.loads(json.dumps(payload))
    forged["certificate"][
        "exact_schur_to_candidate_finite_homotopy_validated"
    ] = True
    with pytest.raises(ValueError):
        validate_right_half_cover_payload(forged)
    forged = json.loads(json.dumps(payload))
    forged["certificate"]["half_square_radius"] = "0.0005"
    with pytest.raises(ValueError):
        validate_right_half_cover_payload(forged)
    forged = json.loads(json.dumps(payload))
    forged["scope"]["general_network_topology"] = True
    with pytest.raises(ValueError):
        validate_right_half_cover_payload(forged)
    forged = json.loads(json.dumps(payload))
    forged["certificate"]["candidate_result_sha256"] = "0" * 64
    with pytest.raises(ValueError):
        validate_right_half_cover_payload(forged)
    forged = json.loads(json.dumps(payload))
    forged["provenance"]["openblas_num_threads"] = "1"
    with pytest.raises(ValueError):
        validate_right_half_cover_payload(forged)
