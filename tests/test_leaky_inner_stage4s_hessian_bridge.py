from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, getcontext, setcontext
from fractions import Fraction
import json
from pathlib import Path
import subprocess

import pytest

import canard_control.leaky_inner_stage4s_hessian_bridge as stage4s
from canard_control.leaky_inner_stage4s_hessian_bridge import (
    BLOCK_NAMES,
    CORE_TARGETS,
    ERROR_FRACTIONS,
    FALSE_FLAGS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STATUS,
    TRUE_FLAGS,
    _arithmetic_core,
    build_stage4s_hessian_bridge_result,
    canonical_sha256,
    validate_stage4s_hessian_bridge_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _isolated_high_precision_decimal_context() -> object:
    previous = getcontext().copy()
    getcontext().prec = 110
    try:
        yield
    finally:
        setcontext(previous)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_digests(payload: dict[str, object]) -> None:
    bridge = payload["bridge"]
    payload["manifest"]["bridge_sha256"] = canonical_sha256(bridge)
    payload["manifest"]["arithmetic_core_sha256"] = canonical_sha256(
        _arithmetic_core(bridge)
    )


def _all_none(value: object) -> bool:
    if isinstance(value, dict):
        return all(_all_none(item) for item in value.values())
    return value is None


def _lagrange_weights(nodes: tuple[Fraction, ...], x: Fraction) -> list[Fraction]:
    return [
        product(
            (x - other) / (node - other)
            for other in nodes
            if other != node
        )
        for node in nodes
    ]


def product(values: object) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def test_registered_result_validates_and_rebuilds_deterministically() -> None:
    payload = _payload()
    validate_stage4s_hessian_bridge_result(payload, REPOSITORY, recompute=True)
    assert payload == build_stage4s_hessian_bridge_result(REPOSITORY)


def test_all_five_parent_results_and_their_source_manifests_are_bound() -> None:
    payload = _payload()
    assert len(PARENT_RESULT_SHA256) == 5
    assert payload["bridge"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    for relative, digest in PARENT_RESULT_SHA256.items():
        assert stage4s._sha256_path(REPOSITORY / relative) == digest
        parent = json.loads((REPOSITORY / relative).read_text(encoding="utf-8"))
        for source_relative, source_digest in parent["manifest"][
            "source_sha256"
        ].items():
            assert stage4s._sha256_path(REPOSITORY / source_relative) == source_digest


def test_stage4q_remains_a_nineteen_flag_diagnostic_only() -> None:
    audit = _payload()["bridge"]["finite_section_audit"]
    assert audit["stage4q_mesh_counts"] == [120, 180, 240]
    assert audit["stage4q_evidence_status"] == (
        "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND"
    )
    assert audit["stage4q_all_nineteen_theorem_flags_false"] is True
    assert audit["stage4q_binary_rows_are_outward_rounded"] is False
    assert audit["stage4q_direct_vs_composition_oracle_is_an_error_bound"] is False
    assert audit["stage4q_mesh_envelope_is_an_error_bound"] is False


def test_finite_sampling_no_go_has_the_exact_norm_one_witness() -> None:
    row = _payload()["bridge"]["finite_sampling_no_go"]
    assert row["operator_norm_lower"] == "1"
    assert row["identity"] == "S_N h=0, hence (I-R_N S_N)h=h"
    assert "t_* outside the nodes" in row["witness"]
    assert "B_*(h,k)" in row["bilinear_invisibility_witness"]
    assert row["mesh_refinement_alone_controls_arbitrary_C_ball"] is False
    assert row["proved"] is True


def test_atomic_bimeasure_lift_is_real_but_has_no_directed_stage4q_ingress() -> None:
    row = _payload()["bridge"]["atomic_bimeasure_lift"]
    assert row["input_sampler_norm"] == "1"
    assert row["piecewise_linear_output_reconstruction_norm"] == "1"
    assert row["operator_bound"] == "||B_N|| <= max_o sum_ij |a_oij|"
    assert "Delta*L_theta/2" in row["continuous_output_completion"]
    assert row["directed_coefficients_required"] is True
    assert row["stage4q_coefficients_directed_here"] is False
    assert row["difference_to_true_RFDE_Hessian_bounded_here"] is False


def test_interior_cubic_constants_replay_exactly() -> None:
    nodes = tuple(Fraction(node) for node in (-1, 0, 1, 2))
    x = Fraction(1, 2)
    weights = _lagrange_weights(nodes, x)
    lebesgue = sum(abs(weight) for weight in weights)
    lipschitz = sum(
        abs(weight) * abs(x - node) for weight, node in zip(weights, nodes)
    )
    assert lebesgue == Fraction(5, 4)
    assert lipschitz == Fraction(3, 4)
    row = _payload()["bridge"]["cubic_stencil_certificates"][
        "interior_four_node"
    ]
    assert row["weight_signs_on_open_cell"] == ["-", "+", "+", "-"]
    assert row["lebesgue_polynomial_on_cell"] == "1+x-x^2"
    assert row["exact_lebesgue_constant"] == "5/4"
    assert row["lebesgue_maximizer"] == "x=1/2"
    assert row["exact_common_Lipschitz_error_constant_times_Delta"] == "3/4"
    assert row["common_Lipschitz_error_maximizer"] == "x=1/2"
    assert row["stability_proved"] is True
    assert row["uniform_C_ball_convergence_proved"] is False


def test_one_sided_endpoint_stencil_constants_are_directed() -> None:
    row = _payload()["bridge"]["cubic_stencil_certificates"][
        "one_sided_right_endpoint"
    ]
    expected = (Decimal(7) + Decimal(14) * Decimal(7).sqrt()) / Decimal(27)
    bracket = row["lebesgue_constant_directed_decimal"]
    assert Decimal(bracket["lower"]) < expected < Decimal(bracket["upper"])
    assert Decimal(bracket["upper"]) - Decimal(bracket["lower"]) <= Decimal(
        "2e-70"
    )
    assert row["exact_lebesgue_constant"] == "(7+14*sqrt(7))/27"
    assert row["lebesgue_polynomial_on_cell"] == "1-3*x-4*x^2-x^3"
    assert row["lebesgue_maximizer"] == "x=(-4+sqrt(7))/3"
    assert row["exact_common_Lipschitz_error_constant_times_Delta"] == "4/3"
    assert row["common_Lipschitz_error_maximizer"] == "x=(-3+sqrt(5))/2"
    assert row["positive_time_nodes_used"] is False
    assert row["uniform_C_ball_convergence_proved"] is False


def test_stencil_modulus_formulas_are_not_promoted_to_the_arbitrary_C_ball() -> None:
    certificate = _payload()["bridge"]["cubic_stencil_certificates"]
    assert "omega_h(2*Delta)" in certificate["interior_four_node"][
        "modulus_bound"
    ]
    assert "omega_h(3*Delta)" in certificate["one_sided_right_endpoint"][
        "modulus_bound"
    ]
    assert "supplies no such common modulus" in certificate["application_boundary"]


def test_continuous_projection_factors_recompute_from_stage4l_norm() -> None:
    row = _payload()["bridge"]["continuous_projection_stability"]
    f_norm = Decimal(row["stage4l_exact_restricted_fhat_norm_upper"])
    p_norm = Decimal(row["P_s_norm_upper"])
    assert p_norm == Decimal(1) + f_norm
    expected = {
        "stable_output_ss_upper": p_norm**3,
        "stable_output_su_upper": p_norm**2,
        "stable_output_uu_upper": p_norm,
        "unstable_output_ss_upper": f_norm * p_norm**2,
        "unstable_output_su_upper": f_norm * p_norm,
        "unstable_output_uu_upper": f_norm,
    }
    assert {
        name: Decimal(value)
        for name, value in row["block_amplification_factors"].items()
    } == expected
    assert row["stage4d_continuous_atom_density_measure_enclosed"] is True
    assert row["direct_projected_residual_avoids_raw_factor_loss"] is True


def test_each_wide_box_budget_is_exact_and_has_ten_percent_reserve() -> None:
    budget = _payload()["bridge"]["wide_box_error_budget"]
    rows = budget["blocks"]
    assert set(rows) == set(BLOCK_NAMES)
    raw_ceilings = []
    for name in BLOCK_NAMES:
        row = rows[name]
        cap = Decimal(row["stage4p_wide_cap"])
        pilot = Decimal(row["stage4q_heuristic_envelope_diagnostic_only"])
        core = Decimal(row["independent_directed_banach_core_target"])
        residual = Decimal(row["residual_after_core_target"])
        reserve = Decimal(row["strict_unused_reserve"])
        assert core == CORE_TARGETS[name]
        assert Decimal(0) <= pilot < core < cap
        assert residual == cap - core
        assert reserve == residual * Decimal("0.10")
        allocations = {
            category: Decimal(value)
            for category, value in row["projected_error_allowances"].items()
        }
        assert allocations == {
            category: residual * fraction
            for category, fraction in ERROR_FRACTIONS.items()
        }
        assert core + sum(allocations.values(), Decimal(0)) + reserve == cap
        factor = Decimal(row["raw_hessian_remainder_amplification_factor"])
        raw = sum(allocations.values(), Decimal(0)) / factor
        assert Decimal(
            row[
                "raw_hessian_only_error_ceiling_if_it_consumes_all_six_allowances"
            ]
        ) == raw
        raw_ceilings.append(raw)
        assert row["actual_directed_core_bound"] is None
        assert row["strict_block_acceptance_validated"] is False
    assert Decimal(budget["error_allowance_fraction_sum"]) == Decimal("0.90")
    assert Decimal(budget["reserve_fraction"]) == Decimal("0.10")
    assert Decimal(budget["simultaneous_raw_hessian_only_error_ceiling"]) == min(
        raw_ceilings
    )
    assert budget["all_six_strict_acceptance_tests_validated"] is False


def test_all_A_through_G_interval_ingress_values_remain_null() -> None:
    groups = _payload()["bridge"]["required_interval_quantities"]
    assert [name[0] for name in groups] == list("ABCDEFG")
    for row in groups.values():
        assert row["purpose"] == "required outward interval ingress"
        assert row["values"]
        assert _all_none(row["values"])
        assert row["validated"] is False


def test_strict_numeric_ingress_is_empty_and_fail_closed() -> None:
    ingress = _payload()["bridge"]["strict_numeric_ingress"]
    assert ingress["evidence_status"] == "OPEN_FAIL_CLOSED_AFTER_EXACT_BRIDGE_AUDIT"
    for key in (
        "directed_finite_atomic_tensor_coefficients",
        "continuous_signed_kernel_residual_norms",
        "directed_banach_core_blocks",
        "projected_error_contributions",
        "uniform_full_ball_hessian_blocks",
    ):
        assert _all_none(ingress[key])
    for key in (
        "all_source_time_cells_and_delay_seams_covered",
        "all_output_phase_cells_and_endpoints_covered",
        "all_six_blocks_from_one_correlated_run",
        "all_six_strict_budget_tests_pass",
    ):
        assert ingress[key] is False


def test_failure_gates_record_seven_current_failures_and_correct_order() -> None:
    gates = _payload()["bridge"]["failure_gates"]
    rows = gates["gates"]
    assert [row["id"].split("_")[0] for row in rows] == [
        f"S{index}" for index in range(1, 9)
    ]
    assert [row["triggered_by_current_stage4q"] for row in rows] == [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        False,
    ]
    assert gates["all_release_gates_pass"] is False


def test_claim_ledger_separates_proved_design_from_open_hessian_claims() -> None:
    payload = _payload()["bridge"]
    claims = payload["claim_status"]
    assert payload["status"] == STATUS
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert len(TRUE_FLAGS) == 12
    assert len(FALSE_FLAGS) == 20


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (("bridge", "claim_status", "stage4q_binary_tensor_outward_rounded"), True),
        (("bridge", "claim_status", "all_six_complete_history_hessian_blocks_validated"), True),
        (("bridge", "finite_section_audit", "stage4q_mesh_envelope_is_an_error_bound"), True),
        (("bridge", "finite_sampling_no_go", "mesh_refinement_alone_controls_arbitrary_C_ball"), True),
        (("bridge", "atomic_bimeasure_lift", "stage4q_coefficients_directed_here"), True),
        (("bridge", "wide_box_error_budget", "all_six_strict_acceptance_tests_validated"), True),
        (("bridge", "strict_numeric_ingress", "all_six_strict_budget_tests_pass"), True),
        (("bridge", "failure_gates", "all_release_gates_pass"), True),
    ),
)
def test_hostile_promotions_are_rejected(
    path: tuple[object, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_hessian_bridge_result(payload, REPOSITORY)


def test_filled_numeric_ingress_is_rejected_even_with_refreshed_hashes() -> None:
    payload = deepcopy(_payload())
    payload["bridge"]["strict_numeric_ingress"][
        "directed_banach_core_blocks"
    ]["stable_output_ss_upper"] = "0.00009"
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_hessian_bridge_result(payload, REPOSITORY)


def test_parent_hash_mutation_is_rejected_even_with_refreshed_hashes() -> None:
    payload = deepcopy(_payload())
    first = next(iter(PARENT_RESULT_SHA256))
    payload["bridge"]["parent_result_sha256"][first] = "0" * 64
    payload["manifest"]["parent_result_sha256"][first] = "0" * 64
    _refresh_digests(payload)
    with pytest.raises(ValueError, match="identity"):
        validate_stage4s_hessian_bridge_result(payload, REPOSITORY)


def test_source_manifest_binds_exactly_the_four_stage4s_files() -> None:
    payload = _payload()
    hashes = payload["manifest"]["source_sha256"]
    assert tuple(hashes) == tuple(sorted(SOURCE_MANIFEST))
    assert set(hashes) == set(SOURCE_MANIFEST)
    assert len(hashes) == 4
    assert all("stage4s_hessian_bridge" in relative for relative in hashes)
    for relative, digest in hashes.items():
        assert stage4s._sha256_path(REPOSITORY / relative) == digest


def test_generator_uses_validate_then_fsync_and_atomic_replace() -> None:
    source = (REPOSITORY / stage4s.GENERATOR_RELATIVE_PATH).read_text(
        encoding="utf-8"
    )
    validate_position = source.index("validate_stage4s_hessian_bridge_result")
    replace_position = source.index("os.replace(temporary, destination)")
    assert validate_position < replace_position
    assert "os.fsync(handle.fileno())" in source
    assert "os.fsync(directory_descriptor)" in source


def test_fresh_interpreter_validates_registered_result() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_stage4s_hessian_bridge import "
        "RESULT_RELATIVE_PATH, validate_stage4s_hessian_bridge_result; "
        "r=Path('.').resolve(); "
        "p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4s_hessian_bridge_result(p,r,recompute=True)"
    )
    completed = subprocess.run(
        ["/usr/bin/python3", "-c", code],
        cwd=REPOSITORY,
        env={"PYTHONPATH": "src"},
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout == ""


def test_note_keeps_theorem_boundary_and_has_no_tab_corruption() -> None:
    note = (REPOSITORY / stage4s.NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    compact = " ".join(note.split())
    assert "no Banach Hessian block is validated" in compact
    assert "cannot converge" in compact
    assert "atom--density-bimeasure residual" in compact
    assert "Every numerical field corresponding to A--G is `null`" in compact
    assert "\t" not in note
