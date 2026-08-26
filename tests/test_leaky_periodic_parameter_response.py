"""Replay and hostile-tamper tests for the leaky response artifact."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

import numpy as np
import pytest

from canard_control.leaky_periodic_parameter_response import (
    ARITHMETIC_SCOPE,
    CLAIM_STATUS,
    CONTROL_ORDER,
    EXPECTED_ARTIFACT_SHA256,
    OUTPUT_ORDER,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    canonical_sha256,
    _parameter_rhs,
    _validate_directed_box_semantics,
    validate_parameter_response_artifact,
)
from canard_control.leaky_periodic_branch_artifact import (
    _binary64_array,
    _collocation_system,
    validate_leaky_periodic_branch_artifact,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH
EXPECTED_RESULT_SHA256: str | None = (
    "beebd506ef157aebefb926bfcbac25e8c236c4319f8a5bddd48abe3c1ae78226"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def _number(record: dict) -> float:
    return float.fromhex(record["binary64_hex"])


def _matrix(record: list[list[dict]]) -> np.ndarray:
    return np.asarray(
        [[_number(value) for value in row] for row in record], dtype=float
    )


def test_response_artifact_is_source_bound_and_replays_centers() -> None:
    raw = RESULT.read_bytes()
    assert isinstance(EXPECTED_RESULT_SHA256, str)
    assert sha256(raw).hexdigest() == EXPECTED_RESULT_SHA256
    payload = json.loads(raw)
    validate_parameter_response_artifact(payload, REPOSITORY)
    artifact = payload["artifact"]
    assert artifact["claim_status"] == CLAIM_STATUS
    assert artifact["control_order"] == list(CONTROL_ORDER)
    assert artifact["output_order"] == list(OUTPUT_ORDER)
    assert canonical_sha256(artifact) == EXPECTED_ARTIFACT_SHA256
    for relative in SOURCE_MANIFEST:
        assert payload["manifest"]["source_sha256"][relative] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()


def test_correct_a_column_is_not_the_old_kappa1_column() -> None:
    artifact = _payload()["artifact"]
    formulas = artifact["parameter_column_formulas"]
    assert "slow right-hand side -T*epsilon*1" in formulas["unfolding_a"]
    assert "fast right-hand side T*epsilon*C(v)" in formulas["kappa_3"]
    assert "kappa_1" not in artifact["control_order"]


def test_parameter_rhs_support_and_sign_match_residual_differences() -> None:
    parent_path = REPOSITORY / (
        "experiments/results/"
        "autonomous_leaky_recovery_inner_branch_artifact.json"
    )
    parent = json.loads(parent_path.read_text(encoding="utf-8"))
    orbit = validate_leaky_periodic_branch_artifact(parent, REPOSITORY)
    reference = _binary64_array(
        parent["artifact"]["collocation"]["phase_reference_binary64"],
        "inner phase reference",
        2,
    )
    rhs, _ = _parameter_rhs(orbit)
    count = len(orbit.state)
    assert np.count_nonzero(rhs[:count, 0]) == 0
    assert np.all(rhs[count : 2 * count, 0] < 0.0)
    assert np.count_nonzero(rhs[count:, 1]) == 0

    step = 1.0e-6
    for column, parameter_name in enumerate(("unfolding", "kappa_3")):
        residuals = []
        for sign in (-1.0, 1.0):
            parameters = replace(
                orbit.parameters,
                **{
                    parameter_name: (
                        getattr(orbit.parameters, parameter_name)
                        + sign * step
                    )
                },
            )
            residual, _ = _collocation_system(
                orbit.state, orbit.period, parameters, reference
            )
            residuals.append(residual)
        residual_derivative = (residuals[1] - residuals[0]) / (2.0 * step)
        assert np.max(np.abs(residual_derivative + rhs[:, column])) < 3e-8


@pytest.mark.parametrize(
    ("branch", "expected_sign", "determinant_floor"),
    [
        ("inner_saddle_candidate", -1, 0.22),
        ("outer_pulse", 1, 1.08),
    ],
)
def test_center_and_sampled_response_margins_are_nonzero_but_numerical(
    branch: str, expected_sign: int, determinant_floor: float
) -> None:
    result = _payload()["artifact"]["branches"][branch]
    center = result["center_response"]
    matrix = _matrix(center["response_matrix"])
    determinant = _number(center["determinant"])
    assert np.linalg.det(matrix) == pytest.approx(determinant, abs=2e-14)
    assert int(np.sign(determinant)) == expected_sign
    sampled = result["sampled_box"]
    assert sampled["all_sampled_extrema_simple"]
    assert sampled["all_sampled_determinants_same_nonzero_sign"]
    assert sampled["determinant_sign"] == expected_sign
    assert _number(sampled["minimum_sampled_absolute_determinant"]) > (
        determinant_floor
    )
    margin = result["numerical_nonzero_margin"]
    assert margin["strictly_positive"]
    assert not margin["rigorous_interval_margin"]
    assert _number(margin["padded_margin"]) > determinant_floor


def test_resolution_and_centered_difference_ladders_converge() -> None:
    branches = _payload()["artifact"]["branches"]
    inner = branches["inner_saddle_candidate"]
    outer = branches["outer_pulse"]
    assert _number(
        inner["resolution_summary"]["determinant_span"]
    ) < 3e-11
    assert _number(
        outer["resolution_summary"]["determinant_span"]
    ) < 2e-11
    for branch in (inner, outer):
        errors = [
            _number(item["matrix_disagreement_inf"])
            for item in branch["centered_difference_ladder"]
        ]
        assert all(left > right for left, right in zip(errors, errors[1:]))
        assert errors[-1] < 5e-4
        center = branch["center_response"]
        assert _number(center["forward_adjoint_disagreement_inf"]) < 5e-10
        assert _number(center["sensitivity_linear_residual_inf"]) < 2e-9


def test_claim_ledger_keeps_sampled_and_directed_boxes_distinct() -> None:
    claim = _payload()["artifact"]["claim_status"]
    for name in (
        "exact_rfde_response_derivative_enclosed",
        "uniform_frequency_amplitude_local_inverse_validated",
    ):
        assert not claim[name]
    assert claim["uniform_common_parameter_box_orbits_validated"]
    assert claim["uniform_common_parameter_box_bordered_inverses_validated"]
    assert claim["uniform_simple_extrema_validated"]
    box = _payload()["artifact"]["common_sampled_box"]
    assert not box["continuum_between_samples_enclosed"]
    directed = _payload()["artifact"]["directed_common_box"]
    assert directed["uniform_orbit_and_bordered_inverse_validated"]
    assert directed["uniform_simple_extrema_validated"]
    assert not directed["exact_first_sensitivities_validated"]
    assert not directed["exact_response_determinant_or_inverse_validated"]


def test_directed_common_box_records_each_branch_gate_separately() -> None:
    directed = _payload()["artifact"]["directed_common_box"]
    thresholds = {
        "inner_saddle_candidate": {
            "residual": 4.9e-8,
            "defect": 0.0316,
            "variation": 0.0601,
            "contraction": 0.0917,
            "margin": 9.0e-6,
        },
        "outer_pulse": {
            "residual": 8.5e-7,
            "defect": 0.0813,
            "variation": 0.161,
            "contraction": 0.2422,
            "margin": 6.7e-6,
        },
    }
    for branch, bounds in thresholds.items():
        certificate = directed["branches"][branch]
        continuation = certificate["continuation"]
        extrema = certificate["extrema"]
        assert continuation["half_width_unfolding_a"] == "1e-10"
        assert continuation["half_width_kappa_3"] == "1e-10"
        assert continuation["parameter_box_orbit_validated"]
        assert continuation["parameter_box_bordered_inverse_validated"]
        assert (
            float(continuation["preconditioned_box_residual_upper"])
            < bounds["residual"]
        )
        assert (
            float(continuation["full_point_defect_upper"])
            < bounds["defect"]
        )
        assert (
            float(continuation["derivative_variation_upper"])
            < bounds["variation"]
        )
        assert (
            float(continuation["uniform_contraction_upper"])
            < bounds["contraction"]
        )
        assert float(continuation["radii_margin_lower"]) > bounds["margin"]
        assert extrema["extrema_validated"]
        assert extrema["all_complement_cells_strict"]
        assert float(extrema["complement_derivative_gap_lower"]) > 0.0
        assert float(extrema["maximum_curvature_upper"]) < 0.0
        assert float(extrema["minimum_curvature_lower"]) > 0.0
        assert certificate["uniform_orbit_and_bordered_inverse_validated"]
        assert certificate["uniform_simple_extrema_validated"]
        assert not certificate["exact_response_derivative_enclosed"]
        assert not certificate["frequency_amplitude_local_inverse_validated"]


def test_directed_extrema_and_orbit_balls_are_disjoint() -> None:
    payload = _payload()["artifact"]["directed_common_box"]
    for certificate in payload["branches"].values():
        extrema = certificate["extrema"]
        maximum = (
            float(extrema["maximum_phase_lower"]),
            float(extrema["maximum_phase_upper"]),
        )
        minimum = (
            float(extrema["minimum_phase_lower"]),
            float(extrema["minimum_phase_upper"]),
        )
        assert maximum[1] < minimum[0] or minimum[1] < maximum[0]

    inner_parent = json.loads(
        (
            REPOSITORY
            / "experiments/results/"
            "autonomous_leaky_recovery_inner_branch_artifact.json"
        ).read_text(
            encoding="utf-8"
        )
    )
    outer_parent = json.loads(
        (
            REPOSITORY
            / "experiments/results/"
            "autonomous_leaky_recovery_outer_high_resolution.json"
        ).read_text(
            encoding="utf-8"
        )
    )
    inner_period = _number(inner_parent["artifact"]["collocation"]["period"])
    outer_period = _number(
        outer_parent["artifact"]["resolutions"]["257"]["period"]
    )
    radii = sum(
        float(certificate["continuation"]["chosen_radius"])
        for certificate in payload["branches"].values()
    )
    assert abs(inner_period - outer_period) > radii


def test_directed_semantic_gate_rejects_bad_radii_and_overlapping_windows() -> None:
    directed = deepcopy(_payload()["artifact"]["directed_common_box"])
    directed["branches"]["outer_pulse"]["continuation"][
        "radii_margin_lower"
    ] = "-1"
    with pytest.raises(ValueError, match="orbit gate disagrees"):
        _validate_directed_box_semantics(directed)

    directed = deepcopy(_payload()["artifact"]["directed_common_box"])
    extrema = directed["branches"]["outer_pulse"]["extrema"]
    extrema["minimum_phase_lower"] = extrema["maximum_phase_lower"]
    extrema["minimum_phase_upper"] = extrema["maximum_phase_upper"]
    extrema["minimum_curvature_window_lower"] = extrema[
        "minimum_phase_lower"
    ]
    extrema["minimum_curvature_window_upper"] = extrema[
        "minimum_phase_upper"
    ]
    with pytest.raises(ValueError, match="windows overlap"):
        _validate_directed_box_semantics(directed)


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (
            (
                "artifact",
                "claim_status",
                "uniform_frequency_amplitude_local_inverse_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "branches",
                "outer_pulse",
                "center_response",
                "response_matrix",
                0,
                0,
                "binary64_hex",
            ),
            "0x0.0p+0",
        ),
        (("manifest", "artifact_sha256"), "0" * 64),
    ],
)
def test_validator_rejects_body_and_claim_tampering(
    path: tuple[object, ...], replacement: object
) -> None:
    tampered = deepcopy(_payload())
    target = tampered
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    with pytest.raises(ValueError):
        validate_parameter_response_artifact(
            tampered, REPOSITORY, replay_centers=False
        )


def test_validator_rejects_source_hash_tampering() -> None:
    tampered = deepcopy(_payload())
    source = SOURCE_MANIFEST[0]
    tampered["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        validate_parameter_response_artifact(
            tampered, REPOSITORY, replay_centers=False
        )


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    [
        ("default_command", "python unbound.py", "manifest command changed"),
        ("arithmetic_scope", "binary64 only", "arithmetic scope changed"),
    ],
)
def test_validator_rejects_manifest_scalar_tampering(
    field: str, replacement: str, message: str
) -> None:
    tampered = deepcopy(_payload())
    tampered["manifest"][field] = replacement
    with pytest.raises(ValueError, match=message):
        validate_parameter_response_artifact(
            tampered, REPOSITORY, replay_centers=False
        )


def test_validator_rejects_extra_manifest_and_runtime_tampering() -> None:
    extra = deepcopy(_payload())
    extra["manifest"]["unreviewed_extra"] = True
    with pytest.raises(ValueError, match="manifest schema changed"):
        validate_parameter_response_artifact(
            extra, REPOSITORY, replay_centers=False
        )

    runtime = deepcopy(_payload())
    runtime["manifest"]["environment"]["gmpy2"] = "hostile"
    with pytest.raises(ValueError, match="environment changed"):
        validate_parameter_response_artifact(
            runtime, REPOSITORY, replay_centers=False
        )


def test_rebind_existing_preserves_registered_body(tmp_path: Path) -> None:
    rebound = tmp_path / "response.json"
    rebound.write_bytes(RESULT.read_bytes())
    environment = {**os.environ, "PYTHONPATH": "src"}
    subprocess.run(
        [
            "/usr/bin/python3",
            "experiments/autonomous_leaky_recovery_parameter_response.py",
            "--rebind-existing",
            "--output",
            str(rebound),
        ],
        cwd=REPOSITORY,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    original = _payload()
    replayed = json.loads(rebound.read_text(encoding="utf-8"))
    assert replayed["artifact"] == original["artifact"]
    assert replayed["manifest"]["arithmetic_scope"] == ARITHMETIC_SCOPE
    validate_parameter_response_artifact(replayed, REPOSITORY)
