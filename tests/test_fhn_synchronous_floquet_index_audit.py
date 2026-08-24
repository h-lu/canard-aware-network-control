"""Regression and hostile-scope tests for the Floquet-index audit."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.fhn_synchronous_floquet_index_audit import (
    FloquetDiagnosticRow,
    FloquetIndexSourceEvidence,
    audit_synchronous_floquet_index,
    compute_center_monodromy_diagnostic,
)


REPOSITORY = Path(__file__).resolve().parents[1]
BLOCH_RESULT = REPOSITORY / "experiments/results/fhn_bloch_outer_validation.json"
TRANSVERSE_RESULT = (
    REPOSITORY / "experiments/results/fhn_periodic_transverse_halanay.json"
)
CANDIDATE_RESULT = (
    REPOSITORY / "experiments/results/fhn_periodic_box_candidate.json"
)
AUDIT_RESULT = (
    REPOSITORY
    / "experiments/results/fhn_synchronous_floquet_index_audit.json"
)
AUDIT_NOTE = REPOSITORY / "docs/paper-iv-synchronous-floquet-index-audit.md"
EXPECTED_AUDIT_SHA256 = (
    "328a4207863279cd5136a159dbe1a7deecc50d1b3eb1be30b6fd34e66b2af024"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _bound_inputs():
    result = _load(AUDIT_RESULT)
    evidence = FloquetIndexSourceEvidence(**result["source_evidence"])
    rows = tuple(
        FloquetDiagnosticRow(**row)
        for row in result["certificate"]["diagnostic_rows"]
    )
    return _load(BLOCH_RESULT), _load(TRANSVERSE_RESULT), _load(CANDIDATE_RESULT), evidence, rows


def _audit(
    bloch: dict,
    transverse: dict,
    candidate: dict,
    evidence: FloquetIndexSourceEvidence,
    rows: tuple[FloquetDiagnosticRow, ...],
):
    return audit_synchronous_floquet_index(
        bloch,
        transverse,
        candidate,
        evidence,
        diagnostic_rows=rows,
    )


def test_tracked_audit_is_hash_and_source_bound() -> None:
    assert sha256(AUDIT_RESULT.read_bytes()).hexdigest() == EXPECTED_AUDIT_SHA256
    payload = _load(AUDIT_RESULT)
    provenance = payload["provenance"]
    assert sha256((REPOSITORY / provenance["generator"]).read_bytes()).hexdigest() == (
        provenance["generator_sha256"]
    )
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest


def test_audit_note_has_raw_safe_math_delimiters_and_no_controls() -> None:
    raw = AUDIT_NOTE.read_bytes()
    forbidden = set(range(0x00, 0x09)) | {0x0B, 0x0C} | set(
        range(0x0E, 0x20)
    ) | {0x7F}
    assert not any(byte in forbidden for byte in raw)
    text = raw.decode("utf-8")
    assert r"Let \(b=(\kappa _1,\kappa _3)\) range over" in text
    assert "Let (b=(\\kappa" not in text
    assert text.count(r"\(") == text.count(r"\)")
    assert text.count(r"\[") == text.count(r"\]")
    assert r"| 600 | \(0.9999998917\) | \(-0.7580502125\)" in text


def test_no_unit_circle_roots_are_not_promoted_to_stability() -> None:
    bloch, transverse, candidate, evidence, rows = _bound_inputs()
    certificate = _audit(bloch, transverse, candidate, evidence, rows)
    assert certificate.source_unit_multiplier_algebraically_simple
    assert certificate.source_all_nontrivial_unit_multipliers_excluded
    assert certificate.source_synchronous_orbital_hyperbolicity
    assert certificate.source_fixed_topology_transverse_variational_decay
    assert certificate.box_index_transport_ready_after_anchor_count
    assert not certificate.bound_source_ledger_contains_anchor_multiplier_count
    assert not certificate.bound_source_ledger_contains_argument_principle_winding
    assert not certificate.bound_source_ledger_contains_validated_gain_homotopy
    assert certificate.anchor_unstable_multiplier_count is None
    assert not certificate.synchronous_stable_index_validated
    assert not certificate.synchronous_attraction_validated
    assert not certificate.full_network_orbital_attraction_validated
    assert not certificate.quantitative_synchronous_decay_rate_validated


def test_diagnostic_converges_toward_a_stable_anchor_candidate_only() -> None:
    payload = _load(AUDIT_RESULT)
    certificate = payload["certificate"]
    rows = certificate["diagnostic_rows"]
    assert [row["step_count"] for row in rows] == [150, 250, 400, 600]
    neutral_errors = [float(row["neutral_multiplier_error_from_one"]) for row in rows]
    leading = [float(row["leading_nontrivial_multiplier_modulus"]) for row in rows]
    assert all(right < left for left, right in zip(neutral_errors, neutral_errors[1:]))
    assert abs(leading[-1] - 0.75805021) < 2.0e-7
    assert abs(leading[-1] - leading[-2]) < 2.0e-7
    assert all(row["observed_nontrivial_outside_unit_disk_count"] == 0 for row in rows)
    assert all(not row["outward_rounded"] for row in rows)
    assert all(row["operator_norm_error_bound"] is None for row in rows)
    assert all(row["contour_resolvent_bound"] is None for row in rows)
    assert certificate["diagnostic_consistent_with_zero_unstable_count"]
    assert not certificate["diagnostic_is_directed_proof"]


def test_small_monodromy_diagnostic_reproduces_the_leading_branch() -> None:
    rows = compute_center_monodromy_diagnostic(
        _load(CANDIDATE_RESULT), step_counts=(60, 90)
    )
    assert len(rows) == 2
    assert abs(float(rows[-1].leading_nontrivial_multiplier_real) + 0.75804) < 2e-5
    assert float(rows[-1].neutral_multiplier_error_from_one) < 3e-4
    assert all(row.observed_nontrivial_outside_unit_disk_count == 0 for row in rows)
    assert all(not row.outward_rounded for row in rows)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("source_evidence", "periodic_branch_validated"),
        ("local_transfer", "monodromy_compact"),
        ("local_transfer", "unit_multiplier_algebraically_simple_validated"),
        ("outer_arc", "all_nontrivial_unit_multipliers_excluded"),
        ("outer_arc", "synchronous_orbital_hyperbolicity_validated"),
        ("scope", "synchronous_orbital_hyperbolicity"),
    ),
)
def test_missing_bloch_theorem_evidence_is_refused(
    section: str, flag: str
) -> None:
    bloch, transverse, candidate, evidence, rows = _bound_inputs()
    bloch[section][flag] = False
    with pytest.raises(ValueError, match="required validated source flag"):
        _audit(bloch, transverse, candidate, evidence, rows)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("outer_arc", "attraction_validated"),
        ("scope", "attraction"),
        ("scope", "full_network_transverse_stability"),
    ),
)
def test_historical_bloch_scope_promotion_is_refused(
    section: str, flag: str
) -> None:
    bloch, transverse, candidate, evidence, rows = _bound_inputs()
    bloch[section][flag] = True
    with pytest.raises(ValueError, match="forged or promoted"):
        _audit(bloch, transverse, candidate, evidence, rows)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("certificate", "synchronous_attraction_validated"),
        ("certificate", "full_network_attraction_validated"),
        ("scope", "synchronous_attraction"),
        ("scope", "full_network_attraction"),
        ("scope", "general_network_topology"),
    ),
)
def test_transverse_scope_promotion_is_refused(
    section: str, flag: str
) -> None:
    bloch, transverse, candidate, evidence, rows = _bound_inputs()
    transverse[section][flag] = True
    with pytest.raises(ValueError, match="forged or promoted"):
        _audit(bloch, transverse, candidate, evidence, rows)


def test_mismatched_source_hashes_and_model_are_refused() -> None:
    bloch, transverse, candidate, evidence, rows = _bound_inputs()
    with pytest.raises(ValueError, match="Bloch evidence"):
        _audit(
            bloch,
            transverse,
            candidate,
            replace(evidence, bloch_result_sha256="0" * 64),
            rows,
        )
    with pytest.raises(ValueError, match="model evidence"):
        _audit(
            bloch,
            transverse,
            candidate,
            replace(evidence, model_id="generic-network"),
            rows,
        )


def test_self_declared_anchor_count_cannot_promote_attraction() -> None:
    bloch, transverse, candidate, evidence, rows = _bound_inputs()
    with pytest.raises(ValueError, match="no tracked directed anchor-index"):
        audit_synchronous_floquet_index(
            bloch,
            transverse,
            candidate,
            evidence,
            diagnostic_rows=rows,
            anchor_index_evidence={
                "unstable_multiplier_count": 0,
                "argument_principle_validated": True,
            },
        )


def test_floating_rows_cannot_be_relabelled_as_directed() -> None:
    bloch, transverse, candidate, evidence, rows = _bound_inputs()
    forged = (replace(rows[0], outward_rounded=True), *rows[1:])
    with pytest.raises(ValueError, match="must not be relabeled as directed"):
        _audit(bloch, transverse, candidate, evidence, forged)
    forged_bound = (
        replace(rows[0], operator_norm_error_bound="1e-8"),
        *rows[1:],
    )
    with pytest.raises(ValueError, match="must remain null"):
        _audit(bloch, transverse, candidate, evidence, forged_bound)


def test_ode_route_is_diagnostic_not_a_validated_homotopy() -> None:
    payload = _load(AUDIT_RESULT)["certificate"]
    assert float(payload["ode_anchor_nontrivial_multiplier_binary64"]) < 2e-11
    assert not payload["ode_anchor_direct_theorem_applies"]
    assert not payload["ode_to_target_homotopy_interval_validated"]
    assert float(payload["ode_to_target_c0_distance_binary64"]) > 0.88
    assert "one directed center-anchor certificate" in payload[
        "minimal_missing_certificate"
    ]


def test_scope_leaves_every_attraction_claim_false() -> None:
    scope = _load(AUDIT_RESULT)["scope"]
    assert scope["synchronous_orbital_hyperbolicity"]
    assert scope["fixed_topology_transverse_variational_decay"]
    assert scope["box_index_transport_ready_after_anchor_count"]
    for key in (
        "anchor_unstable_multiplier_count",
        "synchronous_stable_index",
        "synchronous_attraction",
        "quantitative_synchronous_decay_rate",
        "full_network_orbital_attraction",
        "nonlinear_synchronization",
        "general_network_topology",
        "issue_15_closed",
    ):
        assert not scope[key]
