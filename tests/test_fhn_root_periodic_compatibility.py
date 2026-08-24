"""Hostile tests for the lifted-root/periodic-model compatibility audit."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import sympy as sp
import pytest

from canard_control.fhn_root_periodic_compatibility import (
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    BALANCED_CHAIN_RESULT_SHA256,
    PERIODIC_BOX_RESULT_SHA256,
    PERIODIC_MODEL_DOC_SHA256,
    ROOT_CLASS_DOC_SHA256,
    ROOT_MODEL_SOURCE_SHA256,
    ROOT_RESPONSE_SOURCE_SHA256,
    ROOT_THEOREM_DOC_SHA256,
    compatibility_audit_is_exact,
    reference_compatibility_audit,
    reference_compatibility_certificate,
    validate_root_periodic_compatibility_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / "experiments/results/fhn_root_periodic_compatibility.json"
NOTE = REPOSITORY / "docs/paper-iv-root-periodic-model-compatibility.md"
EXPECTED_RESULT_SHA256 = (
    "600c8f45fd420b284299921142b3b0ab337f7427df8f9b92d53e3d0555365adf"
)
EXPECTED_NOTE_SHA256 = (
    "ee427b3a04eb2b9ebcd9dd108738eb539758f41d2d7c2924f9a9a7308005c8da"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_exact_model_comparison_refuses_literal_identity() -> None:
    audit = reference_compatibility_audit()
    assert compatibility_audit_is_exact(audit)
    assert audit.root_fold_voltage == sp.Matrix([sp.sqrt(6) / 2, 0])
    assert audit.periodic_fold_voltage == sp.Matrix([1, 1])
    assert audit.root_fast_fold_jacobian == sp.Matrix(
        [[-1, sp.Rational(1, 2)], [2, -1]]
    )
    assert audit.periodic_fast_fold_jacobian == sp.Matrix(
        [[-sp.Rational(3, 2), sp.Rational(3, 2)],
         [sp.Rational(3, 2), -sp.Rational(3, 2)]]
    )
    assert audit.fast_fold_jacobian_difference != sp.zeros(2, 2)
    assert audit.recovery_scaffold_difference != sp.zeros(2, 2)
    assert audit.unfolding_column_difference == sp.Matrix([0, -1])
    assert audit.root_current_linear_compensator == sp.Matrix(
        [
            [sp.Rational(1, 2), sp.Rational(1, 4)],
            [sp.Rational(2, 3), sp.Rational(2, 3)],
        ]
    )
    assert audit.periodic_current_linear_compensator == sp.eye(2)
    assert audit.current_linear_compensator_difference != sp.zeros(2, 2)


def test_lifted_layers_are_not_the_periodic_balanced_half_layers() -> None:
    audit = reference_compatibility_audit()
    assert audit.root_layer_0 != audit.periodic_layer_0
    assert audit.root_layer_1 != audit.periodic_layer_1
    assert audit.root_layer_0_half_row_mass_residual == sp.Matrix(
        [-sp.Rational(1, 4), -sp.Rational(1, 12)]
    )
    assert audit.root_layer_1_half_row_mass_residual == sp.Matrix(
        [0, sp.Rational(5, 12)]
    )
    assert audit.root_layer_0_half_left_balance_residual != sp.zeros(1, 2)
    assert audit.root_layer_1_half_left_balance_residual != sp.zeros(1, 2)


def test_lifted_eta_is_root_projected_invisible_but_periodic_sync_visible() -> None:
    audit = reference_compatibility_audit()
    assert audit.root_eta_action_on_root_critical == sp.Matrix([1, -2])
    assert audit.root_eta_root_critical_pairing == 0
    assert audit.root_eta_action_on_periodic_sync == sp.Matrix([1, -2])
    assert audit.root_eta_periodic_sync_pairing == -sp.Rational(1, 2)
    assert not audit.root_eta_preserves_periodic_synchrony
    assert not audit.root_eta_is_invisible_on_periodic_sync_branch


def test_exact_sync_invisibility_annihilates_direct_sync_critical_forcing() -> None:
    audit = reference_compatibility_audit()
    a, b, c, d = sp.symbols("a b c d", real=True)
    assert audit.generic_redistribution_sync_action == sp.Matrix(
        [a + b, c + d]
    )
    assert audit.generic_sync_invisible_substitution_action == sp.zeros(2, 1)
    # For two distinct fixed delays the eta perturbation is
    # T*1*(g(s_0)-g(s_1)); invisibility for arbitrary scalar histories is
    # therefore equivalent to T*1=0.
    assert sp.solve(
        list(audit.generic_redistribution_sync_action), (b, d), dict=True
    ) == [{b: -a, d: -c}]


def test_certificate_keeps_the_two_positive_parent_links_but_refuses_composition() -> None:
    certificate = reference_compatibility_certificate()
    assert certificate.same_nodewise_voltage_recovery_state_type_validated
    assert certificate.same_local_fhn_cubic_term_validated
    assert certificate.balanced_control_and_autonomous_handoff_same_baseline_validated
    assert (
        certificate.balanced_synchronous_restriction_matches_periodic_scalar_rfde_validated
    )
    assert (
        certificate.controlled_onset_to_autonomous_finite_excursion_in_balanced_model_inherited
    )
    assert not certificate.same_literal_rfde_validated
    assert not certificate.lifted_eta_preserves_periodic_synchrony_validated
    assert not certificate.periodic_branch_validated_in_eta_neighborhood
    assert not certificate.lifted_selected_root_theorem_applies_to_dual_scaffold_periodic_model
    assert not certificate.three_input_three_output_parameter_linked_theorem_validated
    assert not certificate.canard_root_to_handoff_trajectory_link_validated
    assert not certificate.autonomous_onset_validated


def test_all_parent_hashes_are_pinned_to_current_files() -> None:
    pairs = (
        ("docs/paper-ii-lifted-two-module-class.md", ROOT_CLASS_DOC_SHA256),
        (
            "docs/paper-ii-selected-root-lift-and-symmetry-breaking.md",
            ROOT_THEOREM_DOC_SHA256,
        ),
        (
            "src/canard_control/lifted_two_module_network.py",
            ROOT_MODEL_SOURCE_SHA256,
        ),
        (
            "src/canard_control/lifted_selected_root_response.py",
            ROOT_RESPONSE_SOURCE_SHA256,
        ),
        ("docs/two-module-reference.md", PERIODIC_MODEL_DOC_SHA256),
        (
            "experiments/results/fhn_periodic_parameter_box.json",
            PERIODIC_BOX_RESULT_SHA256,
        ),
        (
            "experiments/results/fhn_balanced_control_chain.json",
            BALANCED_CHAIN_RESULT_SHA256,
        ),
        (
            "experiments/results/fhn_autonomous_handoff_excursion.json",
            AUTONOMOUS_HANDOFF_RESULT_SHA256,
        ),
    )
    for relative, expected in pairs:
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == expected


def test_generated_payload_validates_and_rejects_false_promotion() -> None:
    payload = _payload()
    validate_root_periodic_compatibility_payload(payload)
    hostile = deepcopy(payload)
    hostile["scope"]["same_literal_rfde"] = True
    with pytest.raises(ValueError, match="promoted"):
        validate_root_periodic_compatibility_payload(hostile)
    hostile = deepcopy(payload)
    hostile["scope"]["three_input_three_output_parameter_linked_theorem"] = True
    with pytest.raises(ValueError, match="promoted"):
        validate_root_periodic_compatibility_payload(hostile)
    hostile = deepcopy(payload)
    hostile["exact_audit"]["root_eta_periodic_sync_pairing"] = "0"
    with pytest.raises(ValueError, match="exact_audit"):
        validate_root_periodic_compatibility_payload(hostile)
    hostile = deepcopy(payload)
    hostile["scope"]["universal_eta_no_go"] = True
    with pytest.raises(ValueError, match="unpinned"):
        validate_root_periodic_compatibility_payload(hostile)
    hostile = deepcopy(payload)
    hostile["parent_claim_checks"][
        "handoff_same_delayed_baseline_validated"
    ] = False
    with pytest.raises(ValueError, match="parent claim checks"):
        validate_root_periodic_compatibility_payload(hostile)
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256


def test_generated_record_is_byte_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "compatibility.json"
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY / "experiments/fhn_root_periodic_compatibility.py"),
            "--output",
            str(output),
        ],
        cwd=REPOSITORY,
        check=True,
        stdout=subprocess.DEVNULL,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_states_the_exact_incompatibility_and_claim_boundary() -> None:
    text = NOTE.read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    assert "not the same RFDE" in normalized
    assert "does not preserve the validated completely synchronous branch" in normalized
    assert "parameter-linked" in normalized
    assert "trajectory-linked" in normalized
    assert "controlled onset" in normalized
    assert "autonomous onset" in normalized
