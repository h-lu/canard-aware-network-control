from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.directed_interval import DirectedInterval
from canard_control.leaky_outer_resolvent_stage3g_tensor import (
    COEFFICIENT_FIELDS,
    COMBINED_FIELDS,
    CONCLUSION,
    DEFECT_FIELDS,
    EXPECTED_COEFFICIENT_PATCH_COUNT,
    FALSE_FLAGS,
    GEOMETRY_FIELDS,
    GREEN_FIELDS,
    OUTER_RESULT_RELATIVE_PATH,
    OUTER_RESULT_SHA256,
    PRECISION_BITS,
    RECOVERY_RESIDUAL_TARGET,
    RESIDUAL_FIELDS,
    RESULT_RELATIVE_PATH,
    STAGE3D_REQUIRED_RUNTIME_SOURCES,
    STAGE3D_RESULT_RELATIVE_PATH,
    STAGE3D_RESULT_SHA256,
    STAGE3D_SCHEMA_ID,
    STAGE3F_RESULT_RELATIVE_PATH,
    STAGE3F_RESULT_SHA256,
    TRUE_FLAGS,
    VOLTAGE_RESIDUAL_TARGET,
    _arb_strict_upper_below,
    _directed_geometry_preflight,
    _load_parent,
    _pinned_outer_guide_period,
    _require_unique_integer_assignment,
    _require_unique_disjoint_flags,
    _validate_parent_artifact_lock,
    _validate_stage3f_target_ingress,
    canonical_sha256,
    validate_outer_resolvent_stage3g_tensor_result,
)
from flint import arb
from canard_control.leaky_pulse_separator_candidate import TAU_1


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_terminal_cover_constant_is_unique_and_pinned() -> None:
    source = (
        REPOSITORY
        / "src/canard_control/leaky_outer_resolvent_stage3g_tensor.py"
    ).read_text()
    _require_unique_integer_assignment(
        source, "TERMINAL_EXTENDED_RECTANGLE_COUNT", 40
    )
    for name, expected in (
        ("DELTA_CELL_COUNT", 20),
        ("LAG_CELL_COUNT", 48),
        ("ORDINARY_RECTANGLE_COUNT", 730),
    ):
        _require_unique_integer_assignment(source, name, expected)
    with pytest.raises(ValueError, match="occur exactly once"):
        _require_unique_integer_assignment(
            source + "\nTERMINAL_EXTENDED_RECTANGLE_COUNT = 20\n",
            "TERMINAL_EXTENDED_RECTANGLE_COUNT",
            40,
        )


def test_flag_registries_reject_duplicates_and_overlap() -> None:
    _require_unique_disjoint_flags(TRUE_FLAGS, FALSE_FLAGS)
    with pytest.raises(ValueError, match="true-flag.*duplicates"):
        _require_unique_disjoint_flags(("a", "a"), ("b",))
    with pytest.raises(ValueError, match="registries overlap"):
        _require_unique_disjoint_flags(("a",), ("a",))


def test_parent_source_lock_and_exact_target_ingress() -> None:
    stage3d = _load_parent(
        REPOSITORY, STAGE3D_RESULT_RELATIVE_PATH, STAGE3D_RESULT_SHA256
    )
    _validate_parent_artifact_lock(
        stage3d,
        REPOSITORY,
        label="Stage-3D",
        schema_id=STAGE3D_SCHEMA_ID,
        result_relative_path=STAGE3D_RESULT_RELATIVE_PATH,
        validate_sources=True,
        required_sources=STAGE3D_REQUIRED_RUNTIME_SOURCES,
    )
    changed_stage3d = deepcopy(stage3d)
    runtime_source = next(iter(STAGE3D_REQUIRED_RUNTIME_SOURCES))
    changed_stage3d["manifest"]["source_sha256"][runtime_source] = "0" * 64
    with pytest.raises(ValueError, match="runtime source changed"):
        _validate_parent_artifact_lock(
            changed_stage3d,
            REPOSITORY,
            label="Stage-3D",
            schema_id=STAGE3D_SCHEMA_ID,
            result_relative_path=STAGE3D_RESULT_RELATIVE_PATH,
            validate_sources=True,
            required_sources=STAGE3D_REQUIRED_RUNTIME_SOURCES,
        )
    stage3f = _load_parent(
        REPOSITORY, STAGE3F_RESULT_RELATIVE_PATH, STAGE3F_RESULT_SHA256
    )
    targets = _validate_stage3f_target_ingress(stage3f)
    assert (
        targets["rows"]["voltage"][
            "required_combined_p_bernstein_residual_upper"
        ]
        == VOLTAGE_RESIDUAL_TARGET
    )
    assert (
        targets["rows"]["recovery"][
            "required_combined_p_bernstein_residual_upper"
        ]
        == RECOVERY_RESIDUAL_TARGET
    )


def test_exact_arb_target_comparison_does_not_round_through_binary64() -> None:
    assert _arb_strict_upper_below(arb("1e-7"), VOLTAGE_RESIDUAL_TARGET)
    assert not _arb_strict_upper_below(
        arb(VOLTAGE_RESIDUAL_TARGET), VOLTAGE_RESIDUAL_TARGET
    )
    source = (
        REPOSITORY
        / "src/canard_control/leaky_outer_resolvent_stage3g_tensor.py"
    ).read_text()
    assert "float(VOLTAGE_RESIDUAL_TARGET)" not in source
    assert "float(RECOVERY_RESIDUAL_TARGET)" not in source
    assert "Path(__file__).resolve().parents[2]" not in source
    assert ".is_positive()" not in source
    assert arb("1e-12").lower() > 0


def test_builder_and_validator_nested_schemas_match_statically() -> None:
    source = (
        REPOSITORY
        / "src/canard_control/leaky_outer_resolvent_stage3g_tensor.py"
    ).read_text()
    tree = ast.parse(source)
    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    def final_return(name: str) -> ast.Dict:
        function = functions[name]
        statement = next(
            item for item in reversed(function.body) if isinstance(item, ast.Return)
        )
        assert isinstance(statement.value, ast.Dict)
        return statement.value

    def literal_keys(node: ast.Dict) -> set[str]:
        return {
            key.value
            for key in node.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, str)
        }

    preflight_keys = literal_keys(final_return("_directed_geometry_preflight"))
    build_return = final_return("_build_tensor_certificate")
    sections = {
        key.value: value
        for key, value in zip(build_return.keys, build_return.values, strict=True)
        if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }
    assert isinstance(sections["geometry"], ast.Dict)
    assert literal_keys(sections["geometry"]) | preflight_keys == set(
        GEOMETRY_FIELDS
    )
    for name, expected in (
        ("coefficient", COEFFICIENT_FIELDS),
        ("residual", RESIDUAL_FIELDS),
        ("defects", DEFECT_FIELDS),
        ("green", GREEN_FIELDS),
        ("combined", COMBINED_FIELDS),
    ):
        assert isinstance(sections[name], ast.Dict)
        assert literal_keys(sections[name]) == set(expected)


def test_directed_geometry_preflight_and_hostile_periods() -> None:
    h = float(TAU_1) / 20
    guide_period = 47.6 * h
    valid_period = DirectedInterval.symmetric_radius(
        guide_period, "1e-12", PRECISION_BITS
    )
    geometry = _directed_geometry_preflight(valid_period, h, guide_period)
    assert geometry["ordinary_rectangle_count"] == 730
    assert geometry["terminal_extended_rectangle_count"] == 40
    assert geometry["tensor_patch_count"] == 12320
    assert geometry["period_strictly_between_47h_and_48h"]
    assert geometry["guide_period_inside_directed_period_interval"]
    assert geometry["terminal_extension_strictly_between_zero_and_0p85"]
    assert geometry["terminal_extension_within_solver_horizon"]

    outside_guide = 46.9 * h
    outside_period = DirectedInterval.symmetric_radius(
        outside_guide, "1e-12", PRECISION_BITS
    )
    with pytest.raises(ArithmeticError, match="47h<T<48h"):
        _directed_geometry_preflight(outside_period, h, outside_guide)
    long_guide = 47.4 * h
    too_long_extension = DirectedInterval.symmetric_radius(
        long_guide, "1e-12", PRECISION_BITS
    )
    with pytest.raises(ArithmeticError, match="0<49h-T<0.85"):
        _directed_geometry_preflight(too_long_extension, h, long_guide)
    with pytest.raises(ValueError, match="occur exactly once"):
        _require_unique_integer_assignment(
            "TERMINAL_EXTENDED_RECTANGLE_COUNT = 20\n",
            "TERMINAL_EXTENDED_RECTANGLE_COUNT",
            40,
        )


def test_pinned_outer_period_recomputes_complete_geometry() -> None:
    outer = _load_parent(
        REPOSITORY, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256
    )
    period = _pinned_outer_guide_period(outer)
    h = float(TAU_1) / 20
    geometry = _directed_geometry_preflight(
        DirectedInterval.from_float(period, PRECISION_BITS), h, period
    )
    assert geometry["guide_period_binary64_hex"] == period.hex()
    assert geometry["ordinary_rectangle_count"] == 730
    assert geometry["terminal_extended_rectangle_count"] == 40
    assert geometry["tensor_patch_count"] == 12320


def test_complete_rectangle_cover(payload: dict) -> None:
    geometry = payload["certificate"]["tensor_geometry"]
    assert geometry["ordinary_rectangle_count"] == 730
    assert geometry["terminal_extended_rectangle_count"] == 40
    assert geometry["physical_terminal_clipped_domain_subset_of_validated_rectangle"]
    assert geometry["tensor_patch_count"] == 12320
    ratio = geometry["period_mesh_ratio_interval"]
    assert Decimal(ratio["lower"]) > 47
    assert Decimal(ratio["upper"]) < 48
    extension = geometry["terminal_extension_length_interval"]
    assert (
        0
        < Decimal(extension["lower"])
        <= Decimal(extension["upper"])
        < Decimal("0.85")
    )
    assert Decimal(extension["upper"]) < Decimal(
        geometry["terminal_extension_solver_horizon_lower"]
    )
    assert Decimal(geometry["terminal_extension_solver_margin_lower"]) > 0


def test_residual_is_directed_and_nonempty(payload: dict) -> None:
    residual = payload["certificate"]["resolvent_residual"]
    assert residual["arb_precision_bits"] == 192
    assert residual["signed_matrix_residual_before_row_norm"]
    assert Decimal(residual["full_matrix_row_residual_upper"]) > 0
    assert Decimal(residual["voltage_terminal_row_tail_upper"]) >= 0


def test_coefficient_patch_cache_is_complete(payload: dict) -> None:
    coefficient = payload["certificate"]["coefficient_remainder"]
    assert EXPECTED_COEFFICIENT_PATCH_COUNT == 48 * 3 * (2 * 4 - 1)
    assert (
        coefficient["cached_coefficient_patch_count"]
        == EXPECTED_COEFFICIENT_PATCH_COUNT
    )


def test_interface_atoms_are_not_omitted(payload: dict) -> None:
    defects = payload["certificate"]["chart_defects"]
    assert Decimal(defects["initial_boundary_matrix_row_defect_upper"]) >= 0
    assert Decimal(defects["summed_lag_interface_matrix_row_jump_upper"]) >= 0
    assert Decimal(defects["boundary_plus_interface_atom_upper"]) >= 0


def test_green_target_bootstrap_closes(payload: dict) -> None:
    green = payload["certificate"]["green_bootstrap"]
    assert green["strict_exact_arb_target_comparison"] is True
    assert green["full_green_target_closes"] is True
    assert green["full_boundary_target_closes"] is True
    assert green["target_bootstrap_closes"] is True
    assert Decimal(green["bootstrapped_exact_green_upper"]) < Decimal("60000")
    assert Decimal(green["bootstrapped_exact_boundary_upper"]) < Decimal("70000")


def test_both_joint_augmented_residual_targets_close(payload: dict) -> None:
    combined = payload["certificate"]["phase_combination_target"]
    assert combined["targets_exactly_ingressed_from_stage3f"] is True
    assert combined["strict_exact_arb_target_comparison"] is True
    assert combined["voltage_target_closes"] is True
    assert combined["recovery_target_closes"] is True
    assert Decimal(combined["voltage_effective_residual_upper"]) < Decimal(
        combined["voltage_target"]
    )
    assert Decimal(combined["recovery_effective_residual_upper"]) < Decimal(
        combined["recovery_target"]
    )


def test_unproved_transfer_claims_stay_false(payload: dict) -> None:
    certificate = payload["certificate"]
    claims = certificate["claim_status"]
    assert set(claims) == set(TRUE_FLAGS + FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert certificate["transfer_errors"]["E_voltage"] is None
    assert certificate["transfer_errors"]["E_recovery"] is None
    assert certificate["transfer_gate"]["arbitrary_c0_linear_contraction_closes"] is False


def test_result_replays_source_bound(payload: dict) -> None:
    validate_outer_resolvent_stage3g_tensor_result(payload, REPOSITORY)


def test_source_tampering_is_rejected(payload: dict) -> None:
    changed = deepcopy(payload)
    source = next(iter(changed["manifest"]["source_sha256"]))
    changed["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)


def test_manifest_and_environment_schema_tampering_is_rejected(
    payload: dict,
) -> None:
    changed = deepcopy(payload)
    changed["manifest"]["unexpected"] = True
    with pytest.raises(ValueError, match="manifest schema"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)

    changed = deepcopy(payload)
    changed["manifest"]["environment"]["arb_precision_bits"] = 191
    with pytest.raises(ValueError, match="environment changed"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)


def test_geometry_gate_tampering_is_rejected_before_replay(payload: dict) -> None:
    changed = deepcopy(payload)
    geometry = changed["certificate"]["tensor_geometry"]
    geometry["guide_period_binary64_hex"] = "0x1.0000000000000p+4"
    geometry["period_mesh_ratio_interval"] = {
        "lower": "47.6",
        "upper": "47.7",
    }
    geometry["period_minus_47h_lower"] = "0.3"
    geometry["48h_minus_period_lower"] = "0.2"
    geometry["terminal_extension_length_interval"] = {
        "lower": "0.7",
        "upper": "0.7",
    }
    geometry["terminal_extension_solver_margin_lower"] = "0.1"
    changed["manifest"]["certificate_sha256"] = canonical_sha256(
        changed["certificate"]
    )
    with pytest.raises(ValueError, match="directed geometry preflight changed"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)


def test_coefficient_count_and_conclusion_tampering_are_rejected(
    payload: dict,
) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["coefficient_remainder"][
        "cached_coefficient_patch_count"
    ] = 987
    changed["manifest"]["certificate_sha256"] = canonical_sha256(
        changed["certificate"]
    )
    with pytest.raises(ValueError, match="coefficient remainder ledger"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)

    changed = deepcopy(payload)
    changed["certificate"]["conclusion"] = (
        CONCLUSION + "; physical pulse onset validated"
    )
    changed["manifest"]["certificate_sha256"] = canonical_sha256(
        changed["certificate"]
    )
    with pytest.raises(ValueError, match="conclusion changed"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)


def test_parent_and_exact_target_tampering_is_rejected_before_replay(
    payload: dict,
) -> None:
    changed = deepcopy(payload)
    parent = next(iter(changed["certificate"]["parent_result_sha256"]))
    changed["certificate"]["parent_result_sha256"][parent] = "0" * 64
    changed["manifest"]["certificate_sha256"] = canonical_sha256(
        changed["certificate"]
    )
    with pytest.raises(ValueError, match="parent digest map"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)

    changed = deepcopy(payload)
    changed["certificate"]["phase_combination_target"]["voltage_target"] = (
        "1.5760374644724814e-06"
    )
    changed["manifest"]["certificate_sha256"] = canonical_sha256(
        changed["certificate"]
    )
    with pytest.raises(ValueError, match="target ingress"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)


def test_numeric_gate_flag_mismatch_is_rejected_before_replay(payload: dict) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["phase_combination_target"][
        "voltage_target_closes"
    ] = False
    changed["manifest"]["certificate_sha256"] = canonical_sha256(
        changed["certificate"]
    )
    with pytest.raises(ValueError, match="joint residual gate"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)


def test_claim_promotion_is_rejected(payload: dict) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["claim_status"][
        "arbitrary_c0_linear_return_contraction_validated"
    ] = True
    changed["manifest"]["certificate_sha256"] = canonical_sha256(
        changed["certificate"]
    )
    with pytest.raises(ValueError, match="open Stage-3G claim was promoted"):
        validate_outer_resolvent_stage3g_tensor_result(changed, REPOSITORY)
    RESIDUAL_FIELDS,
