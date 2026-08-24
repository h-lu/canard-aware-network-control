"""Tests for the target-amplitude prepared causal-tube candidate."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from canard_control.fixed_epsilon_frozen_graph_operator import (
    FlowSlots,
    uncut_physical_transform,
)
from canard_control.fixed_epsilon_target_causal_tube_candidate import (
    CONDITIONAL_THEOREM_FLAGS,
    NUMERICAL_TRUE_FLAGS,
    OPEN_FLAGS,
    PARENT_CLAIM_CHECK_KEYS,
    PARENT_SHA256,
    TARGET_RHO,
    TargetTubeConfiguration,
    prepared_history_derivative,
    prepared_history_state,
    preparation_bump,
    preparation_bump_derivative,
    solve_target_causal_tube,
    validate_target_causal_tube_audit,
    validate_target_causal_tube_result,
    verify_target_causal_tube_parent_evidence,
)
from canard_control.fixed_epsilon_two_sided_candidate import _entry_template


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_target_causal_tube_candidate.py"
)
GENERATOR = (
    REPOSITORY
    / "experiments/fixed_epsilon_target_causal_tube_candidate.py"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_target_causal_tube_candidate.json"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-target-causal-tube-candidate.md"


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_preparation_bump_has_the_required_one_sided_endpoint_jet() -> None:
    assert preparation_bump(-2.0) == 0.0
    assert preparation_bump(-1.0) == 0.0
    assert preparation_bump(0.0) == 0.0
    assert preparation_bump_derivative(-2.0) == 0.0
    assert preparation_bump_derivative(-1.0) == 0.0
    assert preparation_bump_derivative(0.0) == 1.0
    for hostile in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="must be finite"):
            preparation_bump(hostile)
        with pytest.raises(ValueError, match="must be finite"):
            preparation_bump_derivative(hostile)
    with pytest.raises(ValueError, match="only for r<=0"):
        preparation_bump(math.nextafter(0.0, math.inf))


def test_zero_transverse_history_replays_the_pinned_entry_template() -> None:
    config = TargetTubeConfiguration()
    for time in np.linspace(config.oldest_retained_time, config.incoming_time, 51):
        expected = _entry_template(
            float(time),
            config.phase_shift,
            config.nu,
            config.section_half_width,
            config.eta,
        )
        assert prepared_history_state(time, 0.0, config) == pytest.approx(
            expected, rel=0.0, abs=3e-15
        )


def test_transverse_preparation_is_exactly_endpoint_compatible() -> None:
    config = TargetTubeConfiguration()
    time = config.incoming_time
    for transverse in np.linspace(
        -config.transverse_radius, config.transverse_radius, 11
    ):
        current = prepared_history_state(time, transverse, config)
        slots = FlowSlots(
            current=current,
            delay_4=prepared_history_state(time - 4.0, transverse, config),
            delay_5=prepared_history_state(time - 5.0, transverse, config),
            delay_theta=prepared_history_state(
                time - config.theta, transverse, config
            ),
        )
        physical = uncut_physical_transform(
            slots,
            rho=config.rho,
            nu=config.nu,
            eta=config.eta,
        )
        derivative = prepared_history_derivative(time, transverse, config)
        assert derivative == pytest.approx(physical, rel=0.0, abs=3e-15)


def test_method_of_steps_retains_same_transverse_label_in_every_slot() -> None:
    solution = solve_target_causal_tube(maximum_step=0.04)
    config = solution.configuration
    assert TARGET_RHO == pytest.approx(1.0 / math.sqrt(5.0))
    for time in (-3.0, -1.25, 1.0, 2.75, 3.0):
        slots = solution.slot_states(time)
        expected = (
            solution.states(time),
            solution.states(time - 4.0),
            solution.states(time - 5.0),
            solution.states(time - config.theta),
        )
        for actual, reference in zip(slots, expected, strict=True):
            assert actual.shape == (config.transverse_sample_count, 2)
            assert np.all(np.isfinite(actual))
            assert np.array_equal(actual, reference)


def test_recorded_candidate_separates_numerics_from_theorem_gates() -> None:
    certificate = _result()["audit"]["certificate"]
    assert all(certificate[key] is True for key in NUMERICAL_TRUE_FLAGS)
    assert all(certificate[key] is True for key in CONDITIONAL_THEOREM_FLAGS)
    assert all(certificate[key] is False for key in OPEN_FLAGS)
    assert float(certificate["minimum_sampled_sigma_clock"]) < -0.8
    assert float(certificate["maximum_sampled_sigma_clock"]) > 1.4
    assert (
        float(certificate["minimum_sampled_absolute_chart_determinant"])
        > 0.11
    )
    assert certificate["strict_sampled_boundary_segment_intersections"] == 0
    assert float(certificate["minimum_current_old_cutoff_weight"]) == 1.0
    assert float(certificate["minimum_all_delayed_old_cutoff_weight"]) < 0.38
    assert float(certificate["maximum_old_clocked_tail_operator_defect"]) > 0.3
    assert float(certificate["delay_theta_hull"]["normal_minimum"]) < -1.56
    assert float(certificate["maximum_sampled_dde_derivative_residual"]) < 3e-10
    assert (
        float(
            certificate["refinement_rows"][-2][
                "maximum_state_change_to_next"
            ]
        )
        < 3e-14
    )


def test_conditional_embedding_theorem_records_the_derivative_loss() -> None:
    certificate = _result()["audit"]["certificate"]
    assert "Psi in C^{k+1} implies" in certificate["conditional_regularities"]
    assert "C2 gives Q0 in C1 and C4 gives Q0 in C3" in certificate[
        "conditional_regularities"
    ]
    extension = certificate["conditional_complete_cutoff_extension"]
    assert "chi in C_c^infinity(Omega)" in extension
    assert "complete C_b^1" in extension
    assert "complete C_b^3" in extension
    assert "Phi_{Q_tilde}^{-tau}" in certificate[
        "conditional_flow_shift_identity"
    ]
    assert "T_phys(Q_tilde)" in certificate[
        "conditional_graph_fixed_identity"
    ]
    assert "no global fixed point" in certificate[
        "conditional_graph_fixed_identity"
    ]
    assert certificate["conditional_intrinsic_coordinate_identities"] == [
        "D t_tube[Q_tilde]=1 on the retained agreement tube",
        "D lambda_tube[Q_tilde]=0 on the retained agreement tube",
    ]
    assert "locally invariant nonstrict faces" in certificate[
        "conditional_lambda_face_barriers"
    ][-1]
    assert certificate[
        "target_c4_chart_and_seam_compatibility_validated"
    ] is False
    assert certificate["target_candidate_class_self_map_validated"] is False
    assert certificate["target_strict_lambda_barrier_margin_validated"] is False
    assert certificate["target_global_graph_fixed_point_validated"] is False


def test_boolean_ledger_rejects_promotion_and_weakening() -> None:
    audit = _result()["audit"]
    weakened = deepcopy(audit)
    weakened["certificate"][NUMERICAL_TRUE_FLAGS[0]] = False
    with pytest.raises(ValueError, match="flag was weakened"):
        validate_target_causal_tube_audit(weakened)

    conditional_weakened = deepcopy(audit)
    conditional_weakened["certificate"][CONDITIONAL_THEOREM_FLAGS[0]] = False
    with pytest.raises(ValueError, match="conditional local-graph theorem"):
        validate_target_causal_tube_audit(conditional_weakened)

    promoted = deepcopy(audit)
    promoted["certificate"][OPEN_FLAGS[0]] = True
    with pytest.raises(ValueError, match="gate was promoted"):
        validate_target_causal_tube_audit(promoted)

    wrong_type = deepcopy(audit)
    wrong_type["certificate"]["transverse_sample_count"] = 41.0
    with pytest.raises(ValueError, match="wrong type"):
        validate_target_causal_tube_audit(wrong_type)


def test_parent_hashes_and_scope_checks_are_exact() -> None:
    hashes, checks = verify_target_causal_tube_parent_evidence(REPOSITORY)
    assert hashes == PARENT_SHA256
    assert set(checks) == PARENT_CLAIM_CHECK_KEYS
    assert all(checks.values())


def test_result_manifest_and_full_reference_revalidate() -> None:
    payload = _result()
    validate_target_causal_tube_result(payload, REPOSITORY)
    manifest = payload["manifest"]
    assert manifest["proof_source_sha256"] == _digest(SOURCE)
    assert manifest["generator_sha256"] == _digest(GENERATOR)
    assert manifest["note_sha256"] == _digest(NOTE)


def test_generator_replays_committed_result_bytes(tmp_path: Path) -> None:
    replay = tmp_path / "target-causal-tube.json"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
        cwd=REPOSITORY,
        env={**dict(__import__("os").environ), "PYTHONPATH": "src"},
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_note_states_the_actual_failure_and_remaining_interval_gate() -> None:
    note = NOTE.read_text(encoding="utf-8")
    normalized = " ".join(note.split())
    assert "fixed point of the old clocked-tail operator" in normalized
    assert "is **not** a" in normalized
    assert "does not restore the old phase clock" in normalized
    assert "neither a \\(C^4\\) chart seam nor a" in normalized
    assert "a complete extension of an embedded solution family" in normalized
    assert "\\mathcal T_{\\rm phys}(\\widetilde Q)=\\widetilde Q" in normalized
    assert "the proposition does not assert a global fixed point" in normalized
    assert "causal slot representation" in normalized
    assert "not a self-map of any candidate class" in normalized
    assert "invariant nonstrict barriers" in normalized
    assert "interval or Taylor-model arithmetic" in normalized
    assert "not an actual validated target fixed graph" in normalized
