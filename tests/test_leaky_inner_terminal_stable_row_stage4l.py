from __future__ import annotations

import ast
from copy import deepcopy
import inspect
import json
from pathlib import Path

import gmpy2
import pytest

import canard_control.leaky_inner_terminal_stable_row_stage4l as stage4l
from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    FALSE_FLAGS,
    GENERATOR_RELATIVE_PATH,
    LP_RATE_UPPER,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STATUS,
    TARGET_RHO_TERM,
    TRUE_FLAGS,
    canonical_sha256,
    validate_stage4l_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACT_SHA256: str | None = (
    "b27631b62d437bf12431d751d4dad79570a03fa9a66fc0115d90f49768e058fc"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _rehash(payload: dict[str, object]) -> None:
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


def test_registered_stage4l_result_is_source_bound() -> None:
    assert EXPECTED_ARTIFACT_SHA256 is not None
    payload = _payload()
    validate_stage4l_result(payload, REPOSITORY, recompute=False)
    assert payload["manifest"]["artifact_sha256"] == EXPECTED_ARTIFACT_SHA256


def test_terminal_row_closes_below_point_one_and_supplies_k_s_one() -> None:
    artifact = _payload()["artifact"]
    ledger = artifact["directed_error_ledger"]
    power = artifact["stable_power_certificate"]
    assert artifact["status"] == STATUS == "PROVED_DISCRETE_LINEAR_INGRESS"
    assert gmpy2.mpq(
        ledger["phase_fixed_terminal_stable_row_norm_upper"]
    ) < gmpy2.mpq(TARGET_RHO_TERM)
    assert gmpy2.mpq(ledger["strict_slack_to_target_lower"]) > gmpy2.mpq(
        "0.09"
    )
    assert power["registered_stable_rate_upper"] == LP_RATE_UPPER == "0.1"
    assert power["stable_power_constant_upper"] == "1"
    assert power["k_s_equals_one_validated"]
    assert power["output_belongs_to_E_s_by_exact_intertwining"]
    assert not power["numerical_left_projection_applied"]


def test_common_row_precedes_norm_and_uses_exact_section_quotient() -> None:
    row = _payload()["artifact"]["terminal_grid_and_common_row"]
    assert row["common_row"] == "R_theta Pi_T U(T,0)(I-q f)"
    assert row["double_rank_one_formed_before_every_modulus"]
    assert row["terminal_event_correction_included"]
    assert row["current_voltage_atom_removed_by_exact_section_quotient"]
    assert row["current_recovery_atom_retained"]
    assert not row["finite_node_maximum_used"]
    assert not row["gaussian_quadrature_used"]
    assert row["continuous_output_phase_supremum"]
    assert row["outward_absolute_density_integration"]


def test_true_period_support_covers_T_plus_and_exactly_four_words() -> None:
    support = _payload()["artifact"]["true_period_and_word_support"]
    assert support["tau0_exact"] == "4*sqrt(5)"
    assert support["tau1_exact"] == "5*sqrt(5)"
    assert support["exact_active_words"] == [
        "empty",
        "(0)",
        "(1)",
        "(0,0)",
    ]
    assert all(
        gmpy2.mpq(value) > 0
        for value in support["directed_margin_lower"].values()
    )
    assert support["returned_history_has_no_unadvanced_identity_block"]
    assert support["centre_period_is_not_claimed_exact"]
    assert support["centre_grid_extended_to_true_T_plus_by_lipschitz_remainder"]
    assert support["complete_true_returned_history_covered"]
    assert gmpy2.mpq(support["activation_displacement_upper"]) < gmpy2.mpq(
        support["activation_padding_binary64"]
    )


def test_continuous_bernstein_cover_and_error_ledger_are_complete() -> None:
    artifact = _payload()["artifact"]
    center = artifact["directed_common_center"]
    ledger = artifact["directed_error_ledger"]
    assert center["returned_output_cell_count"] == 641
    assert center["input_history_cell_count"] == 640
    assert center["bernstein_rectangle_count_including_recovery"] == 410880
    assert center["activation_ambiguous_rectangle_count"] > 1000
    assert len(center["output_cell_rows"]) == 641
    assert gmpy2.mpq(
        center["center_common_row_upper_binary64_with_local_ball_guards"]
    ) < gmpy2.mpq("0.005")
    for key in (
        "centre_common_row_upper",
        "independent_binary_bernstein_guard_upper",
        "stage4i_primitive_event_measure_error_upper",
        "rank_one_normalization_and_event_error_upper",
        "raw_terminal_event_ratio_error_upper",
        "true_T_plus_and_coordinate_shift_error_upper",
    ):
        assert gmpy2.mpq(ledger[key]) >= 0
    assert ledger["all_terms_nonnegative_and_summed_outward"]
    assert not ledger["stage4j_projected_residual_used"]
    assert not ledger["unknown_terminal_norm_used_in_own_error"]
    assert not ledger["unknown_k_s_used_in_own_error"]


def test_binary64_gamma_and_time_shift_ledgers_are_explicit() -> None:
    row = _payload()["artifact"]["terminal_grid_and_common_row"]
    binary = row["binary_rounding_certificate"]
    assert binary["binary64_unit_roundoff_exact"].startswith("1.110223024625")
    assert binary["maximum_real_operations_per_guarded_kernel"] == 131072
    assert binary["derived_worst_case_real_operation_count"] < 131072
    assert binary["derived_operation_count_at_most_registered_maximum"]
    assert binary["all_ballpoly_and_bivariate_arrays_audited"]
    assert binary["actual_intermediate_envelope_strictly_below_analytic_cap"]
    assert gmpy2.mpq(
        binary["actual_all_intermediate_ball_envelope_upper_binary64"]
    ) < gmpy2.mpq(binary["analytic_binary_kernel_envelope_cap"])
    assert binary["local_guard_strictly_exceeds_gamma_n"]
    assert binary["final_guard_strictly_exceeds_unguarded_error"]
    assert binary["numpy_nextafter_is_not_the_rounding_proof"]
    assert binary["ieee_gamma_ledger_is_the_rounding_proof"]
    lipschitz = row["true_coordinate_lipschitz_certificate"]
    assert gmpy2.mpq(
        lipschitz["combined_analytic_candidate_upper"]
    ) < gmpy2.mpq(lipschitz["registered_lipschitz_cap"])
    assert not lipschitz["self_referential_error_propagation_used"]


def test_claim_ledger_keeps_first_return_nonlinear_graph_and_onset_false() -> None:
    artifact = _payload()["artifact"]
    claims = artifact["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)
    scope = artifact["scope_boundary"]
    for name in (
        "first_positive_return",
        "no_earlier_section_hit",
        "nonlinear_return_tube",
        "uniform_hessian_blocks",
        "stable_graph",
        "pulse_graph_intersection",
        "crossing",
        "onset",
        "two_sided_routing",
        "network_safety",
    ):
        assert not scope[name]


def test_source_manifest_runtime_and_atomic_generator_are_explicit() -> None:
    payload = _payload()
    manifest = payload["manifest"]
    assert set(manifest["source_sha256"]) == set(SOURCE_MANIFEST)
    assert manifest["artifact_sha256"] == canonical_sha256(payload["artifact"])
    assert manifest["proof_status"] == STATUS
    runtime = manifest["runtime"]
    assert runtime["openblas_num_threads"] == "8"
    assert runtime["omp_num_threads"] == "1"
    assert "gamma_n" in runtime["arithmetic"]
    source = (REPOSITORY / GENERATOR_RELATIVE_PATH).read_text(encoding="utf-8")
    assert ast.parse(source) is not None
    assert "tempfile.mkstemp(" in source
    assert "os.replace(temporary, destination)" in source
    assert source.count("os.fsync(") >= 2
    build = source.index("payload = build_stage4l_result(")
    validate = source.index("validate_stage4l_result(", build)
    install = source.index("_atomic_write(destination, payload)", validate)
    assert build < validate < install
    assert "recompute=True" in source


def test_validator_fresh_replays_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[Path] = []
    original = stage4l.build_stage4l_artifact

    def wrapped(repository: Path):
        calls.append(repository.resolve())
        return original(repository)

    monkeypatch.setattr(stage4l, "build_stage4l_artifact", wrapped)
    assert inspect.signature(stage4l.validate_stage4l_result).parameters[
        "recompute"
    ].default is True
    stage4l.validate_stage4l_result(_payload(), REPOSITORY)
    assert calls == [REPOSITORY.resolve()]


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (("artifact", "analytic_discrete_lemma", "normalized_left_row"), "f=f_0"),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "double_rank_one_formed_before_every_modulus",
            ),
            False,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "terminal_event_correction_included",
            ),
            False,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "current_voltage_atom_removed_by_exact_section_quotient",
            ),
            False,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "finite_node_maximum_used",
            ),
            True,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "binary_rounding_certificate",
                "ieee_gamma_ledger_is_the_rounding_proof",
            ),
            False,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "binary_rounding_certificate",
                "derived_operation_count_at_most_registered_maximum",
            ),
            False,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "binary_rounding_certificate",
                "operation_count_derivation",
                "positive_640_cell_density_reduction_real_ops",
            ),
            1,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "binary_rounding_certificate",
                "all_ballpoly_and_bivariate_arrays_audited",
            ),
            False,
        ),
        (
            (
                "artifact",
                "terminal_grid_and_common_row",
                "binary_rounding_certificate",
                "actual_all_intermediate_ball_envelope_upper_binary64",
            ),
            "4096",
        ),
        (
            (
                "artifact",
                "true_period_and_word_support",
                "exact_active_words",
            ),
            ["empty", "(0)", "(1)"],
        ),
        (
            (
                "artifact",
                "true_period_and_word_support",
                "centre_grid_extended_to_true_T_plus_by_lipschitz_remainder",
            ),
            False,
        ),
        (
            (
                "artifact",
                "directed_error_ledger",
                "stage4j_projected_residual_used",
            ),
            True,
        ),
        (
            (
                "artifact",
                "directed_error_ledger",
                "unknown_k_s_used_in_own_error",
            ),
            True,
        ),
        (
            (
                "artifact",
                "stable_power_certificate",
                "stable_power_constant_upper",
            ),
            "2",
        ),
        (("artifact", "scope_boundary", "first_positive_return"), True),
        (("artifact", "scope_boundary", "nonlinear_return_tube"), True),
        (("artifact", "scope_boundary", "stable_graph"), True),
        (("artifact", "scope_boundary", "crossing"), True),
        (("artifact", "scope_boundary", "onset"), True),
        (
            (
                "artifact",
                "claim_status",
                "unique_physical_pulse_onset_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_omissions_circularity_and_promotions_are_rejected(
    path: tuple[object, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    _mutate(payload, path, value)
    _rehash(payload)
    with pytest.raises(ValueError):
        validate_stage4l_result(payload, REPOSITORY, recompute=False)


def test_note_states_exact_scope_and_proof_mechanism() -> None:
    note = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    compact = " ".join(note.split())
    for required in (
        "PROVED DISCRETE LINEAR INGRESS",
        "0.009896427481610001 <0.1",
        "K_s=1",
        "double rank-one",
        "current-voltage",
        "true period",
        r"true \(T_+\)",
        "not justified by `nextafter` alone",
        "without circularity",
        "first-positive-return identification",
        "no nonlinear return tube",
        "no stable graph",
        "atomically replaces",
    ):
        assert required in compact

    for required_literal in (
        r"\(\tau_0=4\sqrt5\)",
        r"\(\tau_1=5\sqrt5\)",
        r"\(1.456\times 10^{-11}\)",
        r"\(5.97\times 10^{-8}\)",
        r"\(10^{-10}\)",
        r"\(10^{-5}\)",
        "18.18620994912992100",
        "0.000010000000000001",
        "0.004059226965383500",
        r"6.506172913144082\times10^{-7}",
        "0.009896427481610003",
    ):
        assert required_literal in note
    assert (
        "641 returned-history phase cells plus one recovery-output row, "
        "against 640 input-history cells, hence 410,880"
    ) in compact
    for obsolete_or_malformed in (
        "18.18620994912992099",
        "0.004059226949567234",
        r"6.506172638844078\times10^{-7}",
        "\tau_0",
        "\tau_1",
        "(1.456 times 10^{-11})",
        "(5.97 times 10^{-8})",
    ):
        assert obsolete_or_malformed not in note

    artifact = _payload()["artifact"]
    center = artifact["directed_common_center"]
    ledger = artifact["directed_error_ledger"]
    period = artifact["true_period_and_word_support"]
    grid = artifact["terminal_grid_and_common_row"]
    binary = grid["binary_rounding_certificate"]
    advertised_upper_bounds = (
        ("0.009896427481610001", ledger["phase_fixed_terminal_stable_row_norm_upper"]),
        ("0.004362999710080374", ledger["centre_common_row_upper"]),
        ("0.000010000000000001", ledger["independent_binary_bernstein_guard_upper"]),
        ("0.001463546183857267", ledger["stage4i_primitive_event_measure_error_upper"]),
        ("0.004059226965383500", ledger["rank_one_normalization_and_event_error_upper"]),
        ("6.506172913144082e-7", ledger["raw_terminal_event_ratio_error_upper"]),
        ("4.004997545987388e-9", ledger["true_T_plus_and_coordinate_shift_error_upper"]),
        ("18.18620994912992100", period["true_period_upper"]),
        ("4.0050e-12", period["combined_coordinate_shift_upper"]),
        ("594.72", grid["true_coordinate_lipschitz_certificate"]["combined_analytic_candidate_upper"]),
        ("1.456e-11", binary["gamma_n_upper"]),
        ("2347", binary["actual_all_intermediate_ball_envelope_upper_binary64"]),
        ("5.97e-8", binary["unguarded_reduction_error_upper"]),
    )
    for displayed, certified in advertised_upper_bounds:
        assert gmpy2.mpq(displayed) >= gmpy2.mpq(certified)

    displayed_ledger_sum = sum(
        (
            gmpy2.mpq("0.004362999710080374"),
            gmpy2.mpq("0.000010000000000001"),
            gmpy2.mpq("0.001463546183857267"),
            gmpy2.mpq("0.004059226965383500"),
            gmpy2.mpq("6.506172913144082e-7"),
            gmpy2.mpq("4.004997545987388e-9"),
        ),
        gmpy2.mpq(0),
    )
    assert displayed_ledger_sum <= gmpy2.mpq("0.009896427481610003")
    assert displayed_ledger_sum >= gmpy2.mpq(
        ledger["phase_fixed_terminal_stable_row_norm_upper"]
    )

    advertised_lower_bounds = (
        ("18.18620994912592099", period["true_period_lower"]),
        ("7.005870061626971", period["directed_margin_lower"]["T_minus_tau_max_lower"]),
        ("0.2976661291276024", period["directed_margin_lower"]["T_minus_two_tau0_lower"]),
        ("1.938401848368187", period["directed_margin_lower"]["tau0_plus_tau1_minus_T_upper_end_lower"]),
        ("8.646605780867554", period["directed_margin_lower"]["three_tau0_minus_T_upper_end_lower"]),
    )
    for displayed, certified in advertised_lower_bounds:
        assert gmpy2.mpq(displayed) <= gmpy2.mpq(certified)

    assert grid["returned_output_cell_count"] == 641
    assert grid["input_history_cell_count"] == 640
    displayed_rectangle_count = (
        grid["returned_output_cell_count"] + 1
    ) * grid["input_history_cell_count"]
    assert displayed_rectangle_count == 410_880
    assert (
        center["bernstein_rectangle_count_including_recovery"]
        == displayed_rectangle_count
    )
    assert binary["derived_worst_case_real_operation_count"] == 70_440
    assert binary["maximum_real_operations_per_guarded_kernel"] == 131_072
    assert binary["analytic_binary_kernel_envelope_cap"] == "4096"
    assert binary["local_coefficient_ball_guard_binary64"] == "1e-10"
    assert binary["independent_final_binary_bernstein_guard"] == "0.00001"
    assert gmpy2.mpq("594.72") < gmpy2.mpq(
        grid["true_coordinate_lipschitz_certificate"]["registered_lipschitz_cap"]
    )
    assert gmpy2.mpq(binary["local_coefficient_ball_guard_binary64"]) > gmpy2.mpq(
        binary["gamma_n_upper"]
    )
    assert gmpy2.mpq(binary["independent_final_binary_bernstein_guard"]) > gmpy2.mpq(
        binary["unguarded_reduction_error_upper"]
    )
