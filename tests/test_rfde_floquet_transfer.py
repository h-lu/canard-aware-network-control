from __future__ import annotations

from dataclasses import replace
from functools import cache
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.fhn_unsquared_amplitude_transfer import (
    orbit_from_binary64_candidate_payload,
)
from canard_control.rfde_floquet_transfer import (
    DirectedBlochCell,
    PhaseBorderedOrbitEvidence,
    check_directed_bloch_arc_contract,
    periodic_orbit_candidate_fingerprint,
    validate_fhn_center_floquet_transfer,
)


_ROOT = Path(__file__).resolve().parents[1]
_CANDIDATE_PATH = (
    _ROOT / "experiments/results/fhn_periodic_box_candidate.json"
)
_VALIDATION_PATH = (
    _ROOT / "experiments/results/fhn_periodic_parameter_box.json"
)
_REPLAY_PATH = (
    _ROOT / "experiments/results/fhn_unsquared_amplitude_transfer.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tracked_center_evidence(orbit) -> PhaseBorderedOrbitEvidence:
    validation = json.loads(
        _VALIDATION_PATH.read_text(encoding="utf-8")
    )["validation"]["continuation"]
    replay = json.loads(_REPLAY_PATH.read_text(encoding="utf-8"))[
        "source_evidence"
    ]
    if (
        replay["candidate_result_sha256"] != _sha256(_CANDIDATE_PATH)
        or replay["parameter_box_result_sha256"]
        != _sha256(_VALIDATION_PATH)
        or replay["parameter_validation_exact_replay"] is not True
    ):
        raise ValueError("tracked candidate-validation replay is inconsistent")
    return PhaseBorderedOrbitEvidence(
        correction_radius=validation["chosen_radius"],
        bordered_inverse_norm_upper=validation[
            "uniform_bordered_inverse_norm_upper"
        ],
        periodic_rfde_orbit_validated=validation[
            "parameter_box_orbit_validated"
        ],
        bordered_rfde_inverse_validated=validation[
            "parameter_box_bordered_inverse_validated"
        ],
        # This is the exact source formula audited in the center proof, not
        # a flag inferred from the floating period column.
        moving_delay_period_column_validated=True,
        candidate_fingerprint=periodic_orbit_candidate_fingerprint(orbit),
        candidate_result_sha256=_sha256(_CANDIDATE_PATH),
        validation_result_sha256=_sha256(_VALIDATION_PATH),
        candidate_validation_replay_sha256=_sha256(_REPLAY_PATH),
    )


@cache
def _center_orbit():
    payload = json.loads(_CANDIDATE_PATH.read_text(encoding="utf-8"))
    return orbit_from_binary64_candidate_payload(payload)


@cache
def _center_certificate():
    orbit = _center_orbit()
    return validate_fhn_center_floquet_transfer(
        orbit,
        _tracked_center_evidence(orbit),
    )


def test_center_bordered_inverse_proves_simple_unit_multiplier() -> None:
    certificate = _center_certificate()

    assert float(certificate.nonconstant_fourier_mode_lower) > 0.67
    assert (
        float(certificate.minimum_period_lower)
        > float(certificate.maximum_delay_upper)
    )
    assert certificate.monodromy_compact
    assert certificate.regularity_bridge_to_validated_fourier_domain
    assert certificate.unit_multiplier_geometrically_simple_validated
    assert certificate.unit_multiplier_algebraically_simple_validated

    # This is a directed quantitative neighborhood, not merely the
    # nonconstructive isolation supplied by algebraic simplicity.
    assert float(certificate.local_phase_radius_lower) > 7.0e-4
    assert certificate.local_unit_circle_exclusion_validated

    # The positive outer arc still needs actual directed Bloch cells.
    assert not certificate.outer_arc_directed_exclusion_validated
    assert not certificate.full_unit_circle_exclusion_validated
    assert not certificate.full_floquet_hyperbolicity_validated


def test_center_proof_carrier_is_the_exact_tracked_binary_payload() -> None:
    """The theorem entrance must not rerun a BLAS-dependent Newton solve."""

    orbit = _center_orbit()
    evidence = _tracked_center_evidence(orbit)

    assert len(orbit.state) == 129
    assert evidence.candidate_result_sha256 == (
        "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
    )
    assert evidence.validation_result_sha256 == (
        "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
    )
    assert evidence.candidate_validation_replay_sha256 == (
        "28e74d2316f7e9324f03874c3294d27d83708c9dbb3f4eefaf04925f55bbba60"
    )
    assert evidence.candidate_fingerprint == (
        "2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169"
    )


@pytest.mark.parametrize(
    ("field", "message"),
    (
        (
            "periodic_rfde_orbit_validated",
            "validated periodic RFDE orbit",
        ),
        (
            "bordered_rfde_inverse_validated",
            "validated phase-bordered RFDE inverse",
        ),
        (
            "moving_delay_period_column_validated",
            "exact moving-delay period column",
        ),
    ),
)
def test_transfer_refuses_each_missing_theorem_seam(
    field: str,
    message: str,
) -> None:
    orbit = _center_orbit()
    evidence = replace(_tracked_center_evidence(orbit), **{field: False})
    with pytest.raises(ValueError, match=message):
        validate_fhn_center_floquet_transfer(orbit, evidence, precision=80)


def test_transfer_refuses_evidence_from_a_different_candidate() -> None:
    tracked = _center_orbit()
    changed_state = np.array(tracked.state, copy=True)
    changed_state[0, 0] = np.nextafter(changed_state[0, 0], np.inf)
    orbit = replace(tracked, state=changed_state)
    evidence = _tracked_center_evidence(tracked)
    with pytest.raises(ValueError, match="different candidate"):
        validate_fhn_center_floquet_transfer(orbit, evidence, precision=80)


def test_pair_consistency_cannot_promote_an_untracked_candidate() -> None:
    tracked = _center_orbit()
    changed_state = np.array(tracked.state, copy=True)
    changed_state[0, 0] = np.nextafter(changed_state[0, 0], np.inf)
    orbit = replace(tracked, state=changed_state)
    evidence = _tracked_center_evidence(orbit)

    with pytest.raises(ValueError, match="tracked center polynomial"):
        validate_fhn_center_floquet_transfer(orbit, evidence, precision=80)


@pytest.mark.parametrize(
    ("field", "message"),
    (
        (
            "candidate_result_sha256",
            "candidate is not the tracked theorem artifact",
        ),
        (
            "validation_result_sha256",
            "validation is not the tracked theorem artifact",
        ),
        (
            "candidate_validation_replay_sha256",
            "candidate-validation replay is not tracked",
        ),
    ),
)
def test_transfer_refuses_an_untracked_theorem_artifact(
    field: str,
    message: str,
) -> None:
    orbit = _center_orbit()
    evidence = replace(
        _tracked_center_evidence(orbit), **{field: "0" * 64}
    )
    with pytest.raises(ValueError, match=message):
        validate_fhn_center_floquet_transfer(orbit, evidence, precision=80)


def test_transfer_refuses_untracked_inverse_data() -> None:
    orbit = _center_orbit()
    evidence = replace(
        _tracked_center_evidence(orbit),
        bordered_inverse_norm_upper="23",
    )
    with pytest.raises(ValueError, match="tracked center theorem"):
        validate_fhn_center_floquet_transfer(orbit, evidence)


def _cell(
    lower: str,
    upper: str,
    *,
    finite_to_finite: str = "0.1",
    tail_from_finite: str = "0.2",
    finite_from_tail: str = "0.3",
    tail_to_tail: str = "0.4",
) -> DirectedBlochCell:
    return DirectedBlochCell(
        phase_lower=lower,
        phase_upper=upper,
        finite_to_finite_upper=finite_to_finite,
        tail_from_finite_upper=tail_from_finite,
        finite_from_tail_upper=finite_from_tail,
        tail_to_tail_upper=tail_to_tail,
    )


def test_directed_bloch_cells_must_cover_the_whole_outer_arc() -> None:
    certificate = check_directed_bloch_arc_contract(
        (_cell("0.001", "1.0"), _cell("1.1", "3.2")),
        required_lower="0.001",
        required_upper="3.14159",
        precision=100,
    )
    assert not certificate.connected_cover
    assert certificate.strict_block_contract
    assert not certificate.bookkeeping_contract_satisfied
    assert not certificate.outer_arc_exclusion_validated


def test_directed_bloch_cells_require_strict_four_block_contractions() -> None:
    certificate = check_directed_bloch_arc_contract(
        (
            _cell("0.001", "1.5"),
            _cell(
                "1.5",
                "3.2",
                finite_from_tail="0.61",
                tail_to_tail="0.4",
            ),
        ),
        required_lower="0.001",
        required_upper="3.14159",
        precision=100,
    )
    assert certificate.connected_cover
    assert not certificate.strict_block_contract
    assert not certificate.bookkeeping_contract_satisfied
    assert not certificate.outer_arc_exclusion_validated


def test_bare_connected_cells_satisfy_only_a_conditional_contract() -> None:
    certificate = check_directed_bloch_arc_contract(
        (_cell("0.0009", "1.5"), _cell("1.5", "3.2")),
        required_lower="0.001",
        required_upper="3.14159",
        precision=100,
    )
    assert certificate.connected_cover
    assert certificate.strict_block_contract
    assert certificate.bookkeeping_contract_satisfied
    assert not certificate.outer_arc_exclusion_validated
    assert float(certificate.maximum_contraction_upper) < 1
