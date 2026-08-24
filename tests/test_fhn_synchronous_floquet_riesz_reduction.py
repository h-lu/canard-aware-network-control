from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.directed_interval import DirectedInterval
from canard_control.fhn_bloch_outer_validation import _finite_center_matrix
from canard_control.fhn_periodic_infinite_validation import _build_base_sequences
from canard_control.fhn_synchronous_floquet_riesz_reduction import (
    RieszReductionSourceEvidence,
    _determinant_phase,
    _finite_candidate_matrix,
    _orbit_from_payload,
    build_synchronous_floquet_riesz_reduction,
    compute_finite_winding_diagnostic,
    validate_synchronous_floquet_riesz_result_payload,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "experiments" / "results"


def _load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def _evidence() -> RieszReductionSourceEvidence:
    return RieszReductionSourceEvidence(
        parameter_box_result_sha256=(
            "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
        ),
        bloch_result_sha256=(
            "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
        ),
        index_audit_result_sha256=(
            "328a4207863279cd5136a159dbe1a7deecc50d1b3eb1be30b6fd34e66b2af024"
        ),
        candidate_result_sha256=(
            "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
        ),
        candidate_fingerprint=(
            "2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169"
        ),
        model_id="dual-scaffold-rank-one-two-module-fhn-two-delay",
    )


@pytest.fixture(scope="module")
def short_certificate():
    return build_synchronous_floquet_riesz_reduction(
        _load("fhn_bloch_outer_validation.json"),
        _load("fhn_synchronous_floquet_index_audit.json"),
        _load("fhn_periodic_box_candidate.json"),
        _evidence(),
        edge_subdivision_counts=(24, 48),
    )


def test_strict_tail_and_outer_reductions(short_certificate) -> None:
    certificate = short_certificate
    assert certificate.cutoff == 64
    assert certificate.complex_finite_dimension == 258
    assert Decimal(certificate.logarithmic_strip_imaginary_lower) == Decimal(
        "-" + certificate.logarithmic_strip_imaginary_upper
    )
    assert 0 < float(certificate.uniform_tail_contraction_upper) < 1
    assert 0 < float(certificate.outer_half_plane_contraction_upper) < 1
    assert certificate.tail_outer_norm_id == "complex-component-wiener-l1-modulus"
    assert float(certificate.complex_modulus_lower_order_norm_upper) < 7
    assert certificate.uniform_tail_block_invertible_on_closed_right_half_strip
    assert certificate.analytic_finite_schur_reduction_validated
    assert certificate.algebraic_multiplicity_preserved_by_schur_reduction
    assert not (
        certificate.general_multiplier_analytic_to_monodromy_multiplicity_bridge_validated
    )
    assert certificate.no_characteristic_values_at_or_beyond_outer_real_part
    assert certificate.local_complex_border_contraction_validated
    assert 0 < float(certificate.local_complex_exclusion_radius_lower)
    assert float(certificate.local_complex_keyhole_radius) < float(
        certificate.local_complex_exclusion_radius_lower
    )
    assert certificate.local_right_half_punctured_disk_excluded


def test_reduction_does_not_promote_the_missing_integer(short_certificate) -> None:
    certificate = short_certificate
    assert not certificate.exact_boundary_schur_to_candidate_finite_homotopy_validated
    assert not certificate.directed_finite_schur_winding_validated
    assert certificate.directed_nontranslation_right_half_strip_zero_count is None
    assert certificate.anchor_unstable_multiplier_count is None
    assert not certificate.synchronous_stable_index_validated
    assert not certificate.synchronous_attraction_validated
    assert not certificate.full_network_orbital_attraction_validated
    assert not certificate.diagnostic_is_directed_proof


def test_correct_slogdet_component_is_the_phase() -> None:
    positive = np.diag(np.array([2.0, 3.0], dtype=complex))
    negative = np.diag(np.array([-2.0, 3.0], dtype=complex))
    assert _determinant_phase(positive) == pytest.approx(0.0)
    assert abs(_determinant_phase(negative)) == pytest.approx(np.pi)
    # The log modulus of the first matrix is log(6), so this catches the
    # otherwise easy-to-miss ``slogdet(...)[1]`` error.
    assert _determinant_phase(positive) != pytest.approx(np.log(6.0))


def test_candidate_block_uses_exact_polynomial_convolution_without_aliasing() -> None:
    orbit = _orbit_from_payload(_load("fhn_periodic_box_candidate.json"))
    phase = 0.7
    exact_center = _finite_center_matrix(
        _build_base_sequences(orbit, 160),
        64,
        DirectedInterval.from_float(phase, 160),
    ).midpoint
    diagnostic = _finite_candidate_matrix(orbit, 1.0j * phase, cutoff=64)
    # Squaring at the 129 grid nodes would alias the genuine polynomial
    # modes 65,...,128 and misses this comparison by about 1e-9.
    assert np.max(np.abs(exact_center - diagnostic)) < 5e-13


def test_finite_winding_converges_but_remains_nondirected() -> None:
    orbit = _orbit_from_payload(_load("fhn_periodic_box_candidate.json"))
    rows = compute_finite_winding_diagnostic(
        orbit,
        keyhole_radius=0.0005,
        edge_subdivision_counts=(24, 48),
    )
    assert [row.determinant_phase_winding_binary64 for row in rows] == [0, 0]
    assert all(row.used_complex_slogdet_phase_not_log_modulus for row in rows)
    assert all(not row.outward_rounded_determinant_phase for row in rows)
    assert all(
        not row.exact_schur_to_candidate_boundary_homotopy_validated
        for row in rows
    )
    assert float(rows[-1].maximum_adjacent_principal_phase_increment_binary64) < (
        float(rows[0].maximum_adjacent_principal_phase_increment_binary64)
    )


def test_tracked_result_payload_is_semantically_valid() -> None:
    validate_synchronous_floquet_riesz_result_payload(
        _load("fhn_synchronous_floquet_riesz_reduction.json")
    )


def test_wrong_hash_and_promoted_source_are_rejected() -> None:
    bloch = _load("fhn_bloch_outer_validation.json")
    index = _load("fhn_synchronous_floquet_index_audit.json")
    candidate = _load("fhn_periodic_box_candidate.json")
    with pytest.raises(ValueError):
        build_synchronous_floquet_riesz_reduction(
            bloch,
            index,
            candidate,
            replace(_evidence(), bloch_result_sha256="0" * 64),
            edge_subdivision_counts=(24,),
        )
    forged_bloch = json.loads(json.dumps(bloch))
    forged_bloch["source_evidence"][
        "moving_delay_period_column_validated"
    ] = False
    with pytest.raises(ValueError):
        build_synchronous_floquet_riesz_reduction(
            forged_bloch,
            index,
            candidate,
            _evidence(),
            edge_subdivision_counts=(24,),
        )
    wrong_norm = json.loads(json.dumps(bloch))
    wrong_norm["local_transfer"]["norm_id"] = "wrong-complexification"
    with pytest.raises(ValueError):
        build_synchronous_floquet_riesz_reduction(
            wrong_norm,
            index,
            candidate,
            _evidence(),
            edge_subdivision_counts=(24,),
        )
    forged = json.loads(json.dumps(index))
    forged["certificate"]["synchronous_attraction_validated"] = True
    with pytest.raises(ValueError):
        build_synchronous_floquet_riesz_reduction(
            bloch,
            forged,
            candidate,
            _evidence(),
            edge_subdivision_counts=(24,),
        )


def test_result_validator_rejects_attraction_promotion() -> None:
    payload = _load("fhn_synchronous_floquet_riesz_reduction.json")
    payload["certificate"]["synchronous_attraction_validated"] = True
    with pytest.raises(ValueError):
        validate_synchronous_floquet_riesz_result_payload(payload)
