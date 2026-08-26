from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import inspect
import json
from pathlib import Path

import pytest

import canard_control.leaky_inner_stable_graph_enlargement_stage4k as stage4k
from canard_control.leaky_inner_stable_graph_enlargement_stage4k import (
    CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER,
    EXPECTED_STAGE4A_HEURISTIC_BLOCKS,
    FALSE_FLAGS,
    GENERATOR_RELATIVE_PATH,
    INFLATION_MULTIPLIERS,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STABLE_GRAPH_RADIUS,
    STABLE_SEED_RADIUS,
    STATUS,
    TERMINAL_RATE_SENSITIVITY,
    TERMINAL_RATE_SENSITIVITY_CEILING_ESTIMATE,
    TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE,
    TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE,
    TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS,
    TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS,
    TRUE_FLAGS,
    UNIT_UNSTABLE_GRAPH_RADIUS,
    UNBOUND_STAGE4E_ALPHA_LOWER,
    UNBOUND_STAGE5GA_PHYSICAL_TARGET_RADIUS,
    UNBOUND_STAGE5GB_EXPECTED_CONE_MARGIN,
    UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER,
    build_stage4k_diagnostic_result,
    canonical_sha256,
    validate_stage4k_diagnostic_result,
)
from canard_control.leaky_projected_return_hessian_stage4_contract import (
    HESSIAN_FIELD_NAMES,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "57119dc28bfa841b4f1a9dcddc3af542783493da94862ed2f7336202b05e2f5c"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _rehash_artifact(payload: dict[str, object]) -> None:
    payload["manifest"]["artifact_sha256"] = canonical_sha256(
        payload["artifact"]
    )


def _mutate(
    payload: dict[str, object], path: tuple[object, ...], value: object
) -> None:
    target: object = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def test_registered_stage4k_result_is_source_bound_and_fresh_replayed() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4k_diagnostic_result(payload, REPOSITORY, recompute=True)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_fresh_build_is_byte_for_byte_reproducible() -> None:
    expected = build_stage4k_diagnostic_result(REPOSITORY)
    assert expected == _payload()


def test_registered_design_and_all_six_blocks_are_exact() -> None:
    artifact = _payload()["artifact"]
    assert artifact["status"] == STATUS == "DIAGNOSTIC"
    design = artifact["recommended_design"]
    assert design["stable_seed_radius_r"] == STABLE_SEED_RADIUS == "0.0094"
    assert design["stable_graph_radius_R_s"] == STABLE_GRAPH_RADIUS == "0.0099"
    assert (
        design["unit_unstable_graph_radius_R_u_hat"]
        == UNIT_UNSTABLE_GRAPH_RADIUS
        == "0.00005"
    )
    assert design["sequence_weight_beta"] == "0.9999"
    assert design["graph_box_split_radius_sum"] == "0.00995"
    assert design["stable_power_rate_is_hypothetical"]
    assert not design["design_values_are_validated"]
    heuristic = artifact["stage4a_heuristic_ingress"]
    assert heuristic["six_block_candidate_upper"] == (
        EXPECTED_STAGE4A_HEURISTIC_BLOCKS
    )
    assert set(heuristic["six_block_candidate_upper"]) == set(
        HESSIAN_FIELD_NAMES
    )


def test_three_simultaneous_exact_majorants_close_only_diagnostically() -> None:
    rows = _payload()["artifact"]["exact_majorant_rows"]
    assert [row["multiplier"] for row in rows] == list(INFLATION_MULTIPLIERS)
    perron = []
    for row in rows:
        evaluation = row["exact_majorant_evaluation"]
        perron.append(Decimal(evaluation["perron_root_upper"]))
        assert evaluation["input_complete"]
        assert evaluation["contraction_closes"]
        assert evaluation["self_map_closes"]
        assert evaluation["split_ball_contains_graph_box"]
        assert evaluation["graph_certificate_closes"]
        interpretation = row["proof_interpretation"]
        assert interpretation["raw_evaluator_closes_numerically"]
        assert not interpretation["hessian_blocks_are_directed_uniform_bounds"]
        assert not interpretation["stable_power_rate_is_validated"]
        assert not interpretation["stable_power_constant_is_validated"]
        assert not interpretation["return_ball_is_validated"]
        assert not interpretation["strict_graph_certificate_closes"]
    assert perron[0] < perron[1] < perron[2] < Decimal("0.126")


def test_twofold_row_retains_registered_margins() -> None:
    row = _payload()["artifact"]["exact_majorant_rows"][-1]
    evaluation = row["exact_majorant_evaluation"]
    slacks = evaluation["self_map_slack_vector_lower"]
    assert Decimal(slacks["stable"]) > Decimal("0.000026")
    assert Decimal(slacks["unstable"]) > Decimal("0.000014")
    assert Decimal(evaluation["graph_height_upper"]) < Decimal("0.000036")
    assert Decimal(evaluation["graph_derivative_upper"]) < Decimal("0.0081")
    blocks = row["input_hessian_blocks"]
    assert blocks["stable_output_ss_upper"] == "0.0449373390057929145148"
    assert blocks["stable_output_uu_upper"] == "15.89363127345690251956"


def test_unbound_stage5gb_cone_only_drives_the_v2_design() -> None:
    artifact = _payload()["artifact"]
    cone = artifact["cone_compatibility_design_driver"]
    assert cone["status"] == "DIAGNOSTIC"
    assert cone["expected_stable_coordinate_upper"] == (
        UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER
    )
    assert cone["expected_numeric_margin"] == (
        UNBOUND_STAGE5GB_EXPECTED_CONE_MARGIN
    )
    assert Decimal(UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER) < Decimal(
        STABLE_SEED_RADIUS
    )
    assert cone["strict_expected_inequality_holds_numerically"]
    assert not cone["stage5gb_result_parent_bound"]
    assert not cone["cone_bound_is_directed_and_validated"]
    assert not cone["full_pulse_interval_seed_containment_validated"]
    assert not cone["entered_into_strict_proof_ingress"]
    assert all(
        "stage5g" not in path.lower()
        for path in artifact["parent_result_sha256"]
    )


def test_preferred_terminal_rate_sensitivity_is_exact_and_isolated() -> None:
    sensitivity = _payload()["artifact"]["terminal_rate_sensitivity"]
    assert sensitivity["status"] == "DIAGNOSTIC"
    assert (
        sensitivity["stable_power_rate_hypothesis"]
        == TERMINAL_RATE_SENSITIVITY
        == "0.1"
    )
    assert sensitivity["stable_seed_radius_r"] == "0.0094"
    assert (
        sensitivity["stable_graph_radius_R_s"]
        == TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS
        == "0.0097"
    )
    assert (
        sensitivity["unit_unstable_graph_radius_R_u_hat"]
        == TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
        == "0.00025"
    )
    assert sensitivity["graph_box_split_radius_sum"] == "0.00995"
    assert not sensitivity["entered_into_main_majorant_rows"]
    assert not sensitivity["entered_into_strict_proof_ingress"]
    evaluation = sensitivity["exact_majorant_evaluation"]
    slacks = evaluation["self_map_slack_vector_lower"]
    assert Decimal(evaluation["perron_root_upper"]) < Decimal("0.024589")
    assert Decimal(slacks["stable"]) > Decimal("0.0002966204")
    assert Decimal(slacks["unstable"]) > Decimal("0.0002122224")
    assert Decimal(evaluation["graph_height_upper"]) < Decimal("0.000037773")
    assert Decimal(evaluation["graph_derivative_upper"]) < Decimal("0.007376")
    assert sensitivity["simultaneous_multiplier_ceiling_estimate"] == (
        TERMINAL_RATE_SENSITIVITY_CEILING_ESTIMATE
    )
    assert sensitivity["limiting_gate"] == "unstable_self_map"
    assert sensitivity["limiting_block_family"] == "unstable-output C_u blocks"
    lower = sensitivity["ceiling_lower_probe"]
    upper = sensitivity["ceiling_upper_probe"]
    assert lower["multiplier"] == TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE
    assert upper["multiplier"] == TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE
    assert lower["exact_majorant_evaluation"]["graph_certificate_closes"]
    assert not upper["exact_majorant_evaluation"]["graph_certificate_closes"]
    assert Decimal(
        lower["exact_majorant_evaluation"]["self_map_slack_vector_lower"][
            "unstable"
        ]
    ) > 0
    assert Decimal(
        upper["exact_majorant_evaluation"]["self_map_slack_vector_lower"][
            "unstable"
        ]
    ) < 0


def test_conditional_physical_scaling_uses_graph_height_not_box_radius() -> None:
    artifact = _payload()["artifact"]
    scaling = artifact["coordinate_convention"][
        "conditional_unit_to_physical_scaling_interface"
    ]
    sensitivity = artifact["terminal_rate_sensitivity"]
    height = Decimal(
        sensitivity["exact_majorant_evaluation"]["graph_height_upper"]
    )
    assert scaling["formula"] == "|psi|<=H_graph_hat/alpha"
    assert Decimal(scaling["sensitivity_design_graph_height_upper"]) == height
    assert scaling["sensitivity_design_box_radius_R_u_hat"] == "0.00025"
    assert scaling["box_radius_is_not_substituted_for_graph_height"]
    assert height / Decimal(UNBOUND_STAGE4E_ALPHA_LOWER) < Decimal(
        CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER
    )
    assert Decimal(CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER) == Decimal(
        "0.0004871"
    )
    assert Decimal(CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER) < Decimal(
        UNBOUND_STAGE5GA_PHYSICAL_TARGET_RADIUS
    )
    for name in (
        "stage4e_alpha_parent_bound",
        "stage5ga_target_parent_bound",
        "sensitivity_graph_self_map_validated",
        "conditional_premises_validated",
        "physical_height_target_claim",
        "endpoint_stable_gap_signs_validated",
    ):
        assert not scaling[name]


def test_strict_proof_ingress_remains_completely_open() -> None:
    ingress = _payload()["artifact"]["strict_proof_ingress"]
    blocks = ingress["directed_uniform_hessian_blocks"]
    assert set(blocks) == set(HESSIAN_FIELD_NAMES)
    assert all(blocks[name] is None for name in HESSIAN_FIELD_NAMES)
    assert ingress["stable_power_rate_upper"] is None
    assert ingress["stable_power_constant_upper"] is None
    assert not ingress["k_s_equals_one_validated"]
    assert ingress["validated_return_map_split_ball_radius_lower"] is None
    assert ingress["return_tube_history_radius_upper"] is None
    assert not ingress["split_return_tube_validated"]
    assert not ingress["first_positive_return_and_no_earlier_hit_validated"]
    assert ingress["validated_full_pulse_stable_coordinate_upper"] is None
    assert not ingress["full_pulse_interval_stable_seed_containment_validated"]


def test_claim_ledger_forbids_graph_intersection_crossing_and_onset() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)
    for name in (
        "inner_local_stable_graph_quantitatively_validated",
        "selected_pulse_stable_graph_intersection_validated",
        "physical_pulse_separator_crossing_validated",
        "unique_physical_pulse_onset_validated",
    ):
        assert not claims[name]


def test_note_states_the_diagnostic_boundary_and_open_inputs() -> None:
    note = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    compact = " ".join(note.split())
    for required in (
        "DIAGNOSTIC",
        "not a stable-graph certificate",
        "unbound design expectation",
        "0.0093802671 < r=0.0094",
        "0.0004871<0.001",
        "does not follow from the displayed rounded ingress",
        "None of the six numbers is a directed uniform bound",
        "strict_graph_certificate_closes=false",
        "no stable graph",
        "no selected pulse intersection",
        "no separator crossing",
        "no physical onset",
        "fresh replay",
        "atomically replaces",
    ):
        assert required in compact


def test_source_manifest_and_runtime_are_explicit() -> None:
    manifest = _payload()["manifest"]
    assert set(manifest["source_sha256"]) == set(SOURCE_MANIFEST)
    assert manifest["diagnostic_status"] == "DIAGNOSTIC"
    assert manifest["artifact_sha256"] == canonical_sha256(
        _payload()["artifact"]
    )
    runtime = manifest["runtime"]
    assert runtime["python"]
    assert runtime["python_implementation"]
    assert "Fraction" in runtime["arithmetic"]
    assert "atomic replacement" in runtime["installation"]


def test_validator_performs_a_fresh_replay_by_default(monkeypatch) -> None:
    calls: list[Path] = []
    original = stage4k.build_stage4k_diagnostic_artifact

    def wrapped(repository: Path):
        calls.append(repository.resolve())
        return original(repository)

    monkeypatch.setattr(stage4k, "build_stage4k_diagnostic_artifact", wrapped)
    assert inspect.signature(stage4k.validate_stage4k_diagnostic_result).parameters[
        "recompute"
    ].default is True
    stage4k.validate_stage4k_diagnostic_result(_payload(), REPOSITORY)
    assert calls == [REPOSITORY.resolve()]


def test_generator_validates_before_fsync_atomic_replace() -> None:
    source = (REPOSITORY / GENERATOR_RELATIVE_PATH).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "tempfile.mkstemp(" in source
    assert "os.replace(temporary, destination)" in source
    assert source.count("os.fsync(") >= 2
    build = source.index("payload = build_stage4k_diagnostic_result(")
    validate = source.index("validate_stage4k_diagnostic_result(", build)
    install = source.index("_atomic_write(destination, payload)", validate)
    assert build < validate < install
    assert "recompute=True" in source
    assert tree is not None


@pytest.mark.parametrize(
    ("path", "value", "message"),
    (
        (("artifact", "status"), "PROVED", "identity"),
        (
            (
                "artifact",
                "stage4a_heuristic_ingress",
                "directed_uniform_bound",
            ),
            True,
            "heuristic row was promoted",
        ),
        (
            (
                "artifact",
                "strict_proof_ingress",
                "directed_uniform_hessian_blocks",
                "stable_output_ss_upper",
            ),
            EXPECTED_STAGE4A_HEURISTIC_BLOCKS["stable_output_ss_upper"],
            "heuristic Hessian block entered strict ingress",
        ),
        (
            (
                "artifact",
                "strict_proof_ingress",
                "stable_power_rate_upper",
            ),
            "0.1",
            "unproved Stage-4K numeric input was filled",
        ),
        (
            (
                "artifact",
                "strict_proof_ingress",
                "stable_power_constant_upper",
            ),
            "1",
            "unproved Stage-4K numeric input was filled",
        ),
        (
            (
                "artifact",
                "strict_proof_ingress",
                "split_return_tube_validated",
            ),
            True,
            "proof flag was promoted",
        ),
        (
            (
                "artifact",
                "strict_proof_ingress",
                "validated_full_pulse_stable_coordinate_upper",
            ),
            UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER,
            "unproved Stage-4K numeric input was filled",
        ),
        (
            (
                "artifact",
                "cone_compatibility_design_driver",
                "cone_bound_is_directed_and_validated",
            ),
            True,
            "unbound Stage-5G-b cone was promoted",
        ),
        (
            (
                "artifact",
                "terminal_rate_sensitivity",
                "entered_into_strict_proof_ingress",
            ),
            True,
            "terminal-rate sensitivity was promoted",
        ),
        (
            (
                "artifact",
                "coordinate_convention",
                "conditional_unit_to_physical_scaling_interface",
                "physical_height_target_claim",
            ),
            True,
            "conditional scaling was promoted",
        ),
        (
            (
                "artifact",
                "exact_majorant_rows",
                2,
                "proof_interpretation",
                "strict_graph_certificate_closes",
            ),
            True,
            "numeric closure was promoted",
        ),
        (
            (
                "artifact",
                "claim_status",
                "inner_local_stable_graph_quantitatively_validated",
            ),
            True,
            "proof gate was promoted",
        ),
        (
            (
                "artifact",
                "claim_status",
                "selected_pulse_stable_graph_intersection_validated",
            ),
            True,
            "proof gate was promoted",
        ),
        (
            (
                "artifact",
                "claim_status",
                "unique_physical_pulse_onset_validated",
            ),
            True,
            "proof gate was promoted",
        ),
    ),
)
def test_hostile_proof_promotions_are_rejected_after_rehash(
    path: tuple[object, ...], value: object, message: str
) -> None:
    payload = deepcopy(_payload())
    _mutate(payload, path, value)
    _rehash_artifact(payload)
    with pytest.raises(ValueError, match=message):
        validate_stage4k_diagnostic_result(
            payload, REPOSITORY, recompute=False
        )


def test_hostile_numeric_change_is_rejected_by_fresh_replay_after_rehash() -> None:
    payload = deepcopy(_payload())
    path = (
        "artifact",
        "exact_majorant_rows",
        0,
        "exact_majorant_evaluation",
        "weighted_row_sum_upper",
    )
    _mutate(payload, path, "0.1")
    _rehash_artifact(payload)
    with pytest.raises(ValueError, match="fresh replay"):
        validate_stage4k_diagnostic_result(
            payload, REPOSITORY, recompute=True
        )


@pytest.mark.parametrize(
    ("field", "old_value"),
    (
        ("stable_seed_radius_r", "0.0090"),
        ("stable_graph_radius_R_s", "0.0095"),
    ),
)
def test_hostile_retired_v1_radii_are_rejected(
    field: str, old_value: str
) -> None:
    payload = deepcopy(_payload())
    payload["artifact"]["recommended_design"][field] = old_value
    _rehash_artifact(payload)
    with pytest.raises(ValueError, match="recommended design changed"):
        validate_stage4k_diagnostic_result(
            payload, REPOSITORY, recompute=False
        )


def test_hostile_source_manifest_change_is_rejected() -> None:
    payload = deepcopy(_payload())
    relative = SOURCE_MANIFEST[0]
    payload["manifest"]["source_sha256"][relative] = "0" * 64
    with pytest.raises(ValueError, match="source changed"):
        validate_stage4k_diagnostic_result(
            payload, REPOSITORY, recompute=False
        )
