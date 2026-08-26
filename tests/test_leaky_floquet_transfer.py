from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal, localcontext
from functools import cache
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.leaky_floquet_transfer import (
    CLAIM_STATUS,
    EXPECTED_ARTIFACT_SHA256,
    INNER_RESULT_RELATIVE_PATH,
    OUTER_RESULT_RELATIVE_PATH,
    build_leaky_period_column_transfer_audit,
    canonical_sha256,
    load_validated_leaky_orbit_evidence,
    validate_leaky_branch_floquet_transfer,
    validate_leaky_floquet_transfer_artifact,
)


_ROOT = Path(__file__).resolve().parents[1]
_RESULT = _ROOT / "experiments/results/leaky_floquet_transfer.json"


@cache
def _payload() -> dict[str, object]:
    return json.loads(_RESULT.read_text(encoding="utf-8"))


@cache
def _source(branch: str):
    return load_validated_leaky_orbit_evidence(_ROOT, branch)


@cache
def _certificate(branch: str):
    orbit, evidence = _source(branch)
    return validate_leaky_branch_floquet_transfer(orbit, evidence)


def test_tracked_artifact_body_and_source_manifest_validate() -> None:
    payload = _payload()
    assert canonical_sha256(payload["artifact"]) == EXPECTED_ARTIFACT_SHA256
    validate_leaky_floquet_transfer_artifact(
        payload, _ROOT, recompute=False
    )
    assert payload["artifact"]["claim_status"] == CLAIM_STATUS


def test_exact_period_column_audit_contains_both_changed_seams() -> None:
    audit = build_leaky_period_column_transfer_audit()
    assert audit.autonomous_retarded_rfde
    assert audit.physical_delays_fixed_when_period_varies
    assert "tau_j/T" in audit.normalized_period_column
    assert "epsilon*(v-a-w)" in audit.recovery_period_column
    assert audit.moving_delay_terms_present
    assert audit.jordan_identity == "L(theta X')=T*b"
    assert audit.bvp_fredholm_index_zero
    assert audit.history_regularization_bridge_registered
    assert audit.algebraic_simplicity_transfer_proved


@pytest.mark.parametrize(
    ("branch", "node_count", "minimum_local_radius"),
    (
        ("inner_saddle_candidate", 129, Decimal("0.0039")),
        ("outer_pulse", 257, Decimal("0.0028")),
    ),
)
def test_each_source_bound_branch_has_simple_neutral_multiplier_and_local_arc(
    branch: str,
    node_count: int,
    minimum_local_radius: Decimal,
) -> None:
    certificate = _certificate(branch)
    assert certificate.node_count == node_count
    assert Decimal(certificate.nonconstant_fourier_mode_lower) > 0
    assert (
        Decimal(certificate.minimum_period_lower)
        > Decimal(certificate.maximum_delay_upper)
    )
    assert certificate.monodromy_compact
    assert certificate.periodic_bvp_fredholm_index_zero
    assert certificate.regularity_bridge_to_history_monodromy
    assert certificate.exact_moving_delay_jordan_identity
    assert certificate.translation_multiplier_present
    assert certificate.translation_kernel_geometrically_simple_validated
    assert certificate.translation_jordan_vector_excluded
    assert certificate.neutral_multiplier_algebraically_simple_validated
    assert certificate.punctured_local_unit_circle_exclusion_validated
    assert Decimal(certificate.local_phase_radius_lower) > minimum_local_radius

    # The leaky recovery column, rather than the old non-leaky column, is
    # present in the tangent majorant.
    assert Decimal(certificate.recovery_input_column_upper) >= Decimal("1.2")

    # These are independent later gates, not consequences of simplicity.
    assert not certificate.remaining_positive_arc_directed_exclusion_validated
    assert not certificate.full_nontranslation_unit_circle_exclusion_validated
    assert not certificate.unstable_multiplier_count_validated
    assert not certificate.attracting_or_saddle_floquet_index_validated


@pytest.mark.parametrize(
    "branch", ("inner_saddle_candidate", "outer_pulse")
)
def test_stored_local_arc_has_exact_decimal_strict_slack(branch: str) -> None:
    stored = _payload()["artifact"]["branches"][branch]
    with localcontext() as context:
        context.prec = 100
        inverse = Decimal(stored["bordered_inverse_norm_upper"])
        first = Decimal(stored["bloch_first_order_coefficient_upper"])
        second = Decimal(stored["bloch_second_order_coefficient_upper"])
        period = Decimal(stored["minimum_period_lower"])
        delta = Decimal(stored["local_phase_radius_lower"])
        assert inverse * first * delta < Decimal("0.500000000000001")
        assert inverse * second * delta < period / Decimal(2)
        assert delta * 2 <= Decimal(
            stored["first_local_phase_threshold_lower"]
        )
        assert delta * 2 <= Decimal(
            stored["second_local_phase_threshold_lower"]
        )


def test_source_artifacts_remain_pretransfer_and_cannot_self_promote() -> None:
    for relative in (
        INNER_RESULT_RELATIVE_PATH,
        OUTER_RESULT_RELATIVE_PATH,
    ):
        artifact = json.loads((_ROOT / relative).read_text())["artifact"]
        wrapper = (
            artifact.get("directed_radii_prototype")
            or artifact.get("directed_radii_certificate")
        )
        floquet = wrapper["validation"]["floquet"]
        assert not floquet[
            "fredholm_to_monodromy_multiplicity_transfer_registered"
        ]
        assert not floquet["neutral_multiplier_algebraically_simple_validated"]
        assert not floquet["nontranslation_unit_circle_exclusion_validated"]
        assert not floquet["unstable_multiplier_count_validated"]


@pytest.mark.parametrize(
    ("field", "message"),
    (
        ("periodic_rfde_orbit_validated", "validated periodic RFDE orbit"),
        (
            "phase_bordered_rfde_inverse_validated",
            "validated phase-bordered RFDE inverse",
        ),
        (
            "moving_delay_period_column_validated",
            "exact moving-delay period column",
        ),
        (
            "recovery_leak_period_column_validated",
            "exact recovery-leak period column",
        ),
    ),
)
def test_transfer_refuses_each_missing_theorem_seam(
    field: str,
    message: str,
) -> None:
    orbit, evidence = _source("inner_saddle_candidate")
    with pytest.raises(ValueError, match=message):
        validate_leaky_branch_floquet_transfer(
            orbit, replace(evidence, **{field: False}), precision=80
        )


def test_transfer_refuses_evidence_for_a_different_polynomial() -> None:
    orbit, evidence = _source("inner_saddle_candidate")
    state = np.array(orbit.state, copy=True)
    state[0, 0] = np.nextafter(state[0, 0], np.inf)
    with pytest.raises(ValueError, match="different orbit"):
        validate_leaky_branch_floquet_transfer(
            replace(orbit, state=state), evidence, precision=80
        )


def test_artifact_refuses_a_promoted_global_floquet_flag() -> None:
    changed = deepcopy(_payload())
    changed["artifact"]["branches"]["outer_pulse"][
        "full_nontranslation_unit_circle_exclusion_validated"
    ] = True
    changed["manifest"]["artifact_sha256"] = canonical_sha256(
        changed["artifact"]
    )
    with pytest.raises(ValueError, match="registered body"):
        validate_leaky_floquet_transfer_artifact(changed, _ROOT)


def test_artifact_refuses_a_source_hash_change() -> None:
    changed = deepcopy(_payload())
    changed["manifest"]["source_sha256"][
        "src/canard_control/rfde_floquet_transfer.py"
    ] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        validate_leaky_floquet_transfer_artifact(changed, _ROOT)


def test_full_source_orbit_and_directed_endpoint_replay() -> None:
    """Expensive replay: both upstream validators and all bounds rerun."""

    validate_leaky_floquet_transfer_artifact(
        _payload(), _ROOT, recompute=True
    )
