from __future__ import annotations

import json
from pathlib import Path

import pytest

import canard_control.leaky_pulse_oriented_adjoint_action_stage5e as stage5e_module
from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
)
from canard_control.leaky_pulse_oriented_adjoint_action_stage5e import (
    CONDITIONAL_TRUE_FLAGS,
    COVERAGE_LEDGER,
    FALSE_FLAGS,
    JOINT_ENVELOPE_NAMES,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    _complex_record,
    _interval_record,
    _oriented_arithmetic,
    _parse_interval_record,
    validate_stage5e_result,
)
from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    canonical_sha256,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8"))


def _refresh_digest(payload: dict[str, object]) -> None:
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )


def _recompute_downstream(payload: dict[str, object]) -> None:
    certificate = payload["certificate"]
    action = certificate["correlated_history_action"]
    budget = action["named_error_budget"]
    oriented = certificate["oriented_action"]
    arithmetic = _oriented_arithmetic(
        {
            name: str(budget["joint_envelope_upper"][name])
            for name in JOINT_ENVELOPE_NAMES
        },
        str(oriented["same_row_denominator_modulus_lower"]),
    )
    budget["total_numerator_radius_upper"] = arithmetic["numerator"]
    oriented["numerator_residual_modulus_upper"] = arithmetic["numerator"]
    oriented["quotient_radius_upper"] = arithmetic["radius"]
    oriented["physical_real_interval"] = {
        "lower": arithmetic["lower"],
        "upper": arithmetic["upper"],
    }
    excludes = not (
        float(arithmetic["lower"]) <= 0 <= float(arithmetic["upper"])
    )
    oriented["physical_real_interval_excludes_zero"] = excludes
    for name in CONDITIONAL_TRUE_FLAGS:
        certificate["claim_status"][name] = excludes
    certificate["stable_gap_interface"][
        "oriented_fixed_functional_action_excludes_zero"
    ] = excludes
    _refresh_digest(payload)


def test_stage5e_result_validates() -> None:
    validate_stage5e_result(_payload(), REPOSITORY)


def test_claim_flag_groups_are_unique_and_pairwise_disjoint() -> None:
    groups = (TRUE_FLAGS, CONDITIONAL_TRUE_FLAGS, FALSE_FLAGS)
    assert all(len(group) == len(set(group)) for group in groups)
    assert all(
        not (set(groups[left]) & set(groups[right]))
        for left in range(len(groups))
        for right in range(left + 1, len(groups))
    )
    assert "oriented_physical_functional_action_interval_validated" in TRUE_FLAGS
    assert (
        "oriented_physical_functional_action_interval_validated"
        not in CONDITIONAL_TRUE_FLAGS
    )


def test_neumann_tail_json_list_has_canonical_tuple_equivalence() -> None:
    payload = _payload()
    tail = payload["certificate"]["correlated_history_action"][
        "neumann_tail_residual_history"
    ]
    assert isinstance(tail, list)
    variant = json.loads(json.dumps(payload))
    variant["certificate"]["correlated_history_action"][
        "neumann_tail_residual_history"
    ] = tuple(tail)
    assert variant != payload
    assert canonical_sha256(variant) == canonical_sha256(payload)


def test_recompute_clears_all_four_stage5e_propagation_caches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    class CacheProbe:
        def __init__(self, name: str) -> None:
            self.name = name

        def cache_clear(self) -> None:
            calls.append(self.name)

    names = (
        "build_stage5e_certificate",
        "build_sensitivity_error_propagation",
        "build_remainder_propagation",
        "build_coefficient_propagation",
    )
    for name in names:
        monkeypatch.setattr(stage5e_module, name, CacheProbe(name))
    stage5e_module._clear_stage5e_replay_caches()
    assert calls == list(names)


def test_physical_phase_is_explicit_and_raw_quotient_is_not_real() -> None:
    certificate = _payload()["certificate"]
    phase = certificate["physical_phase_orientation"]
    assert phase["gamma_definition"] == "gamma=chi(q_tilde)/|chi(q_tilde)|"
    assert phase["q_phys_definition"] == "q_phys=q_tilde/gamma"
    assert phase["raw_complex_quotient_is_real"] is False
    modulus = phase["test_component_modulus_interval"]
    assert float(modulus["lower"]) > 0


def test_correlated_action_keeps_every_mandatory_piece() -> None:
    action = _payload()["certificate"]["correlated_history_action"]
    assert action["center_c_star_exact"] == "-252"
    assert action["finite_parameter_sampling_used"] is False
    assert isinstance(action["neumann_tail_residual_history"], list)
    assert action["neumann_tail_step_count"] == len(
        action["neumann_tail_residual_history"]
    )
    for name in (
        "event_translation_retained",
        "recovery_atom_retained",
        "voltage_current_atom_exactly_zero_after_section_and_q_section",
        "finite_row_retained",
        "neumann_tail_retained",
        "density_direct_and_omitted_dictionaries_kept_separate",
        "delay_and_history_seams_retained",
    ):
        assert action[name] is True
    budget = action["named_error_budget"]
    assert set(budget["joint_envelope_upper"]) == set(JOINT_ENVELOPE_NAMES)
    assert budget["coverage_ledger"] == COVERAGE_LEDGER
    assert budget["coverage_ledger_is_nested_or_overlapping_and_not_additive"] is True
    assert budget["sum_identity"] == "r_A=r_joint_guide+r_joint_measure"
    components = budget["common_measure_difference_components"]
    assert components["neumann_tail_remainder_covered"] is True
    assert components["finite_row_enclosure_covered"] is True
    assert components["periodic_orbit_and_advanced_covariance_covered"] is True
    assert components["guide_exact_atom_density_difference_covered"] is True


def test_stage5e_does_not_promote_stable_gap_newton_or_onset() -> None:
    certificate = _payload()["certificate"]
    claims = certificate["claim_status"]
    for name in FALSE_FLAGS:
        assert claims[name] is False
    interface = certificate["stable_gap_interface"]
    assert interface["oriented_fixed_functional_action_interval_available"] is True
    assert (
        interface["oriented_fixed_functional_action_excludes_zero"]
        is certificate["oriented_action"]["physical_real_interval_excludes_zero"]
    )
    assert interface["quantitative_inner_stable_graph_available"] is False
    assert interface["stable_gap_derivative_interval"] is None
    assert interface["stable_gap_endpoint_intervals"] is None
    assert interface["interval_newton_image"] is None
    assert interface["pulse_parameter_Jc"] is None
    assert interface["onset_or_routing_conclusion"] is None


@pytest.mark.parametrize(
    "field",
    (
        "event_translation_retained",
        "recovery_atom_retained",
        "voltage_current_atom_exactly_zero_after_section_and_q_section",
        "finite_row_retained",
        "neumann_tail_retained",
        "density_direct_and_omitted_dictionaries_kept_separate",
        "delay_and_history_seams_retained",
    ),
)
def test_hostile_omission_is_rejected(field: str) -> None:
    payload = _payload()
    payload["certificate"]["correlated_history_action"][field] = False
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_raw_reality_promotion_is_rejected() -> None:
    payload = _payload()
    payload["certificate"]["physical_phase_orientation"][
        "raw_complex_quotient_is_real"
    ] = True
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    ("field", "hostile_value"),
    (
        ("oriented_fixed_functional_action_interval_available", False),
        ("quantitative_inner_stable_graph_available", True),
        ("stable_gap_derivative_interval", {"lower": "-1", "upper": "-1/2"}),
        ("stable_gap_endpoint_intervals", {"left": "-1", "right": "1"}),
        ("interval_newton_image", {"lower": "0", "upper": "1"}),
        ("pulse_parameter_Jc", "0.301"),
        ("onset_or_routing_conclusion", "onset proved"),
    ),
)
def test_hostile_stable_interface_promotion_is_rejected(
    field: str, hostile_value: object
) -> None:
    payload = _payload()
    payload["certificate"]["stable_gap_interface"][field] = hostile_value
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_stable_interface_exclusion_mismatch_is_rejected() -> None:
    payload = _payload()
    interface = payload["certificate"]["stable_gap_interface"]
    field = "oriented_fixed_functional_action_excludes_zero"
    interface[field] = not interface[field]
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_gamma_box_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    gamma_real = payload["certificate"]["physical_phase_orientation"][
        "gamma_box"
    ]["real"]
    gamma_real["lower"] = "0"
    gamma_real["upper"] = "0"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_coordinated_phase_triple_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    phase = payload["certificate"]["physical_phase_orientation"]
    test_record = phase["test_component_box"]
    test_box = DirectedComplexInterval(
        _parse_interval_record(test_record["real"], "hostile phase real"),
        _parse_interval_record(test_record["imag"], "hostile phase imag"),
    )
    scaled_box = DirectedComplexInterval(test_box.real * 2, test_box.imag * 2)
    scaled_modulus_record = _interval_record(
        DirectedInterval(
            scaled_box.lower_abs(), scaled_box.upper_abs(), PRECISION_BITS
        )
    )
    scaled_modulus = _parse_interval_record(
        scaled_modulus_record, "hostile phase modulus"
    )
    phase["test_component_box"] = _complex_record(scaled_box)
    phase["test_component_modulus_interval"] = scaled_modulus_record
    phase["gamma_box"] = _complex_record(
        DirectedComplexInterval(
            scaled_box.real / scaled_modulus,
            scaled_box.imag / scaled_modulus,
        )
    )
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_c_times_q_residual_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    payload["certificate"]["correlated_history_action"][
        "center_c_star_exact"
    ] = "-251"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_exact_voltage_atom_identity_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    payload["certificate"]["correlated_history_action"][
        "exact_section_identities"
    ]["q_phys_v_at_zero"] = "1e-30"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_density_piece_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    payload["certificate"]["correlated_history_action"][
        "density_dictionary_count"
    ] = 3
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize("joint_name", JOINT_ENVELOPE_NAMES)
def test_hostile_joint_envelope_shrink_is_rejected_with_consistent_downstream(
    joint_name: str,
) -> None:
    payload = _payload()
    payload["certificate"]["correlated_history_action"]["named_error_budget"][
        "joint_envelope_upper"
    ][joint_name] = "0"
    _recompute_downstream(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_denominator_is_rejected_with_consistent_downstream() -> None:
    payload = _payload()
    payload["certificate"]["oriented_action"][
        "same_row_denominator_modulus_lower"
    ] = "0.0004"
    _recompute_downstream(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_coverage_ledger_mutation_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    payload["certificate"]["correlated_history_action"]["named_error_budget"][
        "coverage_ledger"
    ]["r_tail"]["joint_envelope"] = "r_joint_guide"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    "hash_group",
    ("parent_sha256", "source_sha256", "dependency_source_sha256"),
)
def test_hostile_manifest_hash_deletion_is_rejected_after_digest_refresh(
    hash_group: str,
) -> None:
    payload = _payload()
    hashes = payload["manifest"][hash_group]
    del hashes[next(iter(hashes))]
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    ("top_group", "operation"),
    (
        ("certificate", "extra"),
        ("certificate", "missing"),
        ("manifest", "extra"),
        ("manifest", "missing"),
    ),
)
def test_hostile_top_level_schema_mutation_is_rejected_after_digest_refresh(
    top_group: str, operation: str
) -> None:
    payload = _payload()
    mapping = payload[top_group]
    if operation == "extra":
        mapping["hostile_extra"] = True
    elif top_group == "certificate":
        del mapping["model_id"]
    else:
        del mapping["default_command"]
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    "path",
    (
        ("physical_phase_orientation",),
        ("physical_phase_orientation", "test_component_box"),
        ("correlated_history_action",),
        ("correlated_history_action", "guide_action_complex_box"),
        ("correlated_history_action", "named_error_budget"),
        (
            "correlated_history_action",
            "named_error_budget",
            "common_measure_difference_components",
        ),
        ("oriented_action",),
        ("stable_gap_interface",),
    ),
)
def test_hostile_nested_schema_extra_is_rejected_after_digest_refresh(
    path: tuple[str, ...],
) -> None:
    payload = _payload()
    mapping = payload["certificate"]
    for key in path:
        mapping = mapping[key]
    mapping["hostile_extra"] = True
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_model_id_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    payload["certificate"]["model_id"] = "different-model"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_theorem_onset_promotion_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    payload["certificate"]["theorem_statement"] = "This proves physical onset."
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    "field",
    ("projection_identity", "q_phys_reality_reason"),
)
def test_hostile_phase_theorem_text_is_rejected_after_digest_refresh(
    field: str,
) -> None:
    payload = _payload()
    payload["certificate"]["physical_phase_orientation"][field] = "changed"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_diagnostic_promotion_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    payload["certificate"]["physical_phase_orientation"][
        "diagnostic_only_not_error_evidence"
    ] = False
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    "field", ("complex_disk_statement", "real_intersection_statement")
)
def test_hostile_oriented_statement_is_rejected_after_digest_refresh(
    field: str,
) -> None:
    payload = _payload()
    payload["certificate"]["oriented_action"][field] = "changed"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_parent_measure_shrink_is_rejected_with_consistent_downstream() -> None:
    payload = _payload()
    action = payload["certificate"]["correlated_history_action"]
    action["stage4e_complete_measure_difference_upper"] = "0"
    action["named_error_budget"]["joint_envelope_upper"][
        "r_joint_measure"
    ] = "0"
    _recompute_downstream(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    "field",
    (
        "finite_adjoint_l1_error_upper",
        "adjoint_fourier_tail_l1_error_upper",
        "adjoint_density_basis_shift_upper",
        "density_convolution_rounding_guard_upper",
    ),
)
def test_hostile_parent_measure_component_is_rejected_after_digest_refresh(
    field: str,
) -> None:
    payload = _payload()
    components = payload["certificate"]["correlated_history_action"][
        "named_error_budget"
    ]["common_measure_difference_components"]
    components[field] = "0"
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_coverage_statement_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    components = payload["certificate"]["correlated_history_action"][
        "named_error_budget"
    ]["common_measure_difference_components"]
    components["coverage_statement"] = "This proves physical onset."
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    ("field", "hostile_value"),
    (
        ("parameter_subdivision_count", 127),
        ("history_subdivision_count", 511),
        ("history_subdivisions_per_delay_piece", 255),
        ("minimum_event_speed_lower", "0"),
        ("maximum_correlated_residual_Y_norm_upper", "0"),
    ),
)
def test_hostile_count_or_positive_ingress_is_rejected_after_digest_refresh(
    field: str, hostile_value: object
) -> None:
    payload = _payload()
    payload["certificate"]["correlated_history_action"][field] = hostile_value
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)


def test_hostile_neumann_tail_count_is_rejected_after_digest_refresh() -> None:
    payload = _payload()
    action = payload["certificate"]["correlated_history_action"]
    action["neumann_tail_step_count"] += 1
    _refresh_digest(payload)
    with pytest.raises(ValueError):
        validate_stage5e_result(payload, REPOSITORY)
