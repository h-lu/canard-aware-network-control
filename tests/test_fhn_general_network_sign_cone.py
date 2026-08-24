"""Regression and refusal tests for the general-network sign-cone theorem."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import pytest
import sympy as sp

from canard_control.fhn_general_network_sign_cone import (
    ASSUMPTIONS_ID,
    TRACKED_SEPARATOR_RESULT_SHA256,
    general_network_balance_audit,
    general_network_polynomial_audit,
    general_network_sign_cone_from_payload,
    load_general_network_sign_cone,
    load_general_network_sign_cone_result,
    reference_general_topology_audits,
    validate_general_network_sign_cone_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SEPARATOR_RESULT = REPOSITORY / "experiments/results/fhn_same_model_separator.json"
GENERAL_RESULT = (
    REPOSITORY / "experiments/results/fhn_general_network_sign_cone.json"
)
EXPECTED_GENERAL_RESULT_SHA256 = (
    "1dd606d7f4aec1ea857f1c53d4e60106fc2737089b67e989aa7b192fe3ca43fb"
)


def _separator_payload() -> dict:
    return json.loads(SEPARATOR_RESULT.read_text(encoding="utf-8"))


def _assert_exact_balance(audit: object) -> None:
    node_count = audit.node_count
    assert audit.pi_sum_residual == 0
    assert audit.scaffold_row_mass_residual == sp.zeros(node_count, 1)
    assert audit.scaffold_stationarity_residual == sp.zeros(1, node_count)
    assert all(
        item == sp.zeros(node_count, 1)
        for item in audit.delay_row_mass_residuals
    )
    assert all(
        item == sp.zeros(1, node_count)
        for item in audit.delay_stationarity_residuals
    )
    assert audit.alpha_sum_residual == 0
    assert audit.combined_delay_row_mass_residual == sp.zeros(node_count, 1)
    assert audit.combined_delay_stationarity_residual == sp.zeros(1, node_count)
    assert audit.synchronous_scaffold_residual == sp.zeros(node_count, 1)
    assert audit.mean_scaffold_residual == 0
    assert audit.scaffold_entrywise_nonnegative
    assert audit.delay_layers_entrywise_nonnegative
    assert audit.alphas_nonnegative
    assert audit.stationary_weight_strictly_positive


def test_exact_diverse_reference_topologies() -> None:
    audits = reference_general_topology_audits()
    assert tuple(audit.node_count for audit in audits) == (1, 3, 4, 5)
    assert audits[1].scaffold_rank == 3
    assert audits[2].scaffold_rank == 4
    for audit in audits:
        _assert_exact_balance(audit)


def test_exact_three_delay_directed_cycle() -> None:
    node_count = 5
    cycle = sp.zeros(node_count)
    for row in range(node_count):
        cycle[row, (row + 1) % node_count] = 1
    identity = sp.eye(node_count)
    alpha = (sp.Rational(1, 5), sp.Rational(3, 10), sp.Rational(1, 2))
    audit = general_network_balance_audit(
        cycle,
        [sp.Rational(1, node_count)] * node_count,
        [alpha[0] * identity, alpha[1] * cycle, alpha[2] * cycle**2],
        alpha,
    )
    _assert_exact_balance(audit)


def test_balance_audit_exposes_wrong_left_weight() -> None:
    scaffold = sp.Matrix([[sp.Rational(3, 4), sp.Rational(1, 4)], [1, 0]])
    audit = general_network_balance_audit(
        scaffold,
        [sp.Rational(1, 2), sp.Rational(1, 2)],
        [scaffold / 2, sp.eye(2) / 2],
        [sp.Rational(1, 2), sp.Rational(1, 2)],
    )
    assert audit.scaffold_row_mass_residual == sp.zeros(2, 1)
    assert audit.scaffold_stationarity_residual != sp.zeros(1, 2)


def test_balance_audit_exposes_signed_scaffold() -> None:
    signed = sp.Matrix([[2, -1], [-1, 2]])
    audit = general_network_balance_audit(
        signed,
        [sp.Rational(1, 2), sp.Rational(1, 2)],
        [sp.eye(2) / 2, sp.eye(2) / 2],
        [sp.Rational(1, 2), sp.Rational(1, 2)],
    )
    assert audit.scaffold_row_mass_residual == sp.zeros(2, 1)
    assert audit.scaffold_stationarity_residual == sp.zeros(1, 2)
    assert not audit.scaffold_entrywise_nonnegative


def test_exact_fhn_polynomial_constants() -> None:
    audit = general_network_polynomial_audit()
    assert audit.intrinsic_factor_residual == 0
    assert audit.control_secant_factor_residual == 0
    assert audit.control_derivative_residual == 0
    assert audit.positive_detector_growth == sp.Rational(143, 300)
    assert audit.negative_detector_growth == sp.Rational(83, 300)
    assert audit.positive_excursion_growth == sp.Rational(3, 50)
    assert audit.negative_excursion_growth == sp.Rational(39, 500)


def test_tracked_source_gives_topology_independent_constants() -> None:
    certificate = load_general_network_sign_cone(SEPARATOR_RESULT)
    assert certificate.separator_result_sha256 == TRACKED_SEPARATOR_RESULT_SHA256
    assert certificate.assumptions_id == ASSUMPTIONS_ID
    assert "J>=1;0<=tau_j<infinity" in certificate.assumptions_id
    assert Decimal(certificate.declared_initial_mean_magnitude_lower) == Decimal(
        "0.06"
    )
    assert Decimal(certificate.positive_detector_growth_lower) > Decimal("0.476")
    assert Decimal(certificate.negative_detector_growth_lower) > Decimal("0.276")
    assert Decimal(certificate.positive_detector_deadline_upper) < Decimal("6")
    assert Decimal(certificate.negative_detector_deadline_upper) < Decimal("10.2")
    assert Decimal(certificate.positive_excursion_growth_lower) > Decimal("0.059")
    assert Decimal(certificate.negative_excursion_growth_lower) > Decimal("0.077")
    assert Decimal(certificate.positive_excursion_deadline_upper) < Decimal("53.7")
    assert Decimal(certificate.negative_excursion_deadline_upper) < Decimal("38.5")
    assert certificate.positive_history_orthant_invariance_validated
    assert certificate.negative_history_orthant_invariance_validated
    assert certificate.topology_independent_collective_growth_validated
    assert certificate.arbitrary_finite_node_count_formula_validated
    assert certificate.nodewise_detector_first_hit_validated
    assert certificate.synchronized_scalar_restriction_form_validated
    assert certificate.staged_frequency_amplitude_reset_map_form_validated
    assert not certificate.irreducibility_or_unique_stationary_distribution_required
    assert not certificate.dobrushin_contraction_required
    assert not certificate.rank_one_topology_required
    assert not certificate.bounded_actuator_validated
    assert not certificate.transverse_attraction_validated
    assert not certificate.general_topology_canard_root_equivalence_validated
    assert not certificate.general_topology_three_output_target_ball_validated
    assert not certificate.asynchronous_frequency_amplitude_map_validated
    assert not certificate.strict_inward_orthant_boundary_validated


def test_public_deadlines_compose_safely() -> None:
    certificate = load_general_network_sign_cone(SEPARATOR_RESULT)
    with localcontext() as context:
        context.prec = 120
        mean = Decimal(certificate.declared_initial_mean_magnitude_lower)
        cases = (
            (
                Decimal(1),
                Decimal(certificate.positive_detector_growth_lower),
                Decimal(certificate.positive_detector_deadline_upper),
            ),
            (
                Decimal(1),
                Decimal(certificate.negative_detector_growth_lower),
                Decimal(certificate.negative_detector_deadline_upper),
            ),
            (
                Decimal(certificate.positive_excursion_face),
                Decimal(certificate.positive_excursion_growth_lower),
                Decimal(certificate.positive_excursion_deadline_upper),
            ),
            (
                -Decimal(certificate.negative_excursion_face),
                Decimal(certificate.negative_excursion_growth_lower),
                Decimal(certificate.negative_excursion_deadline_upper),
            ),
        )
        for face, growth, deadline in cases:
            assert deadline >= (face / mean).ln() / growth


@pytest.mark.parametrize("mean", ("0", "-0.1", "1", "1.2"))
def test_invalid_mean_magnitude_is_refused(mean: str) -> None:
    with pytest.raises(ValueError, match="strictly between"):
        general_network_sign_cone_from_payload(
            _separator_payload(),
            separator_result_sha256=TRACKED_SEPARATOR_RESULT_SHA256,
            initial_mean_magnitude_lower=mean,
        )


def test_source_loader_refuses_forged_separator(tmp_path: Path) -> None:
    forged = tmp_path / "separator.json"
    forged.write_bytes(SEPARATOR_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="separator result SHA-256"):
        load_general_network_sign_cone(forged)


def test_generated_result_is_hash_and_manifest_bound() -> None:
    payload = load_general_network_sign_cone_result(
        GENERAL_RESULT,
        expected_sha256=EXPECTED_GENERAL_RESULT_SHA256,
    )
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    evidence = payload["source_evidence"]
    assert evidence["separator_result_sha256"] == sha256(
        SEPARATOR_RESULT.read_bytes()
    ).hexdigest()


def test_generated_result_loader_refuses_forged_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "general.json"
    forged.write_bytes(GENERAL_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="general-network sign-cone result"):
        load_general_network_sign_cone_result(
            forged,
            expected_sha256=EXPECTED_GENERAL_RESULT_SHA256,
        )


def test_result_semantics_refuse_missing_or_promoted_claims() -> None:
    payload = json.loads(GENERAL_RESULT.read_text(encoding="utf-8"))
    missing = deepcopy(payload)
    missing["scope"]["topology_independent_nodewise_detector_first_hit"] = False
    with pytest.raises(ValueError, match="must be true"):
        validate_general_network_sign_cone_result_payload(missing)
    for name in (
        "bounded_actuator",
        "transverse_attraction",
        "full_network_periodic_hyperbolicity",
        "general_topology_canard_root_equivalence",
        "general_topology_three_output_target_ball",
        "asynchronous_frequency_amplitude_map",
        "strict_inward_orthant_boundary",
        "biological_basin",
        "hardware",
    ):
        promoted = deepcopy(payload)
        promoted["scope"][name] = True
        with pytest.raises(ValueError, match="must be false"):
            validate_general_network_sign_cone_result_payload(promoted)
