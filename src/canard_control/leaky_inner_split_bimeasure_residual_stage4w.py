"""Stage-4W split-aware bimeasure residual theorem.

This module closes an analytic, not numerical, gap in the selected near-two-
period return argument.  It proves the correct quotient norm for stable
section inputs, gives a projective atom--density/bimeasure norm that retains
the fixed ``q_hat/f_hat`` cancellations, and states a fail-closed residual
criterion for all six Hessian blocks.

The theorem also records a qualitative consequence of the Stage-4T parent
that was not available in the earlier Stage-4O contract.  Since the direct
selected return is C2 on an open coordinate neighbourhood, its complete-
history Hessian exists, is operator-norm continuous at the periodic center,
and is therefore uniformly finite on an unknown small ball having the
preferred anisotropic shape. Neither that scale nor any Hessian bound is
numerical here; in particular this is not the preferred scale lambda=1.

No finite sampling or mesh refinement is used as an operator-norm error
bound.  Every strict numerical ingress needed by the six-block test remains
null, and all graph, crossing, onset, routing, capture, and safety claims are
false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping


SCHEMA_ID = "leaky-inner-split-bimeasure-residual-stage4w-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_two_period_event"
STATUS = (
    "PROVED_SPLIT_QUOTIENT_AND_RESIDUAL_THEOREM; "
    "QUALITATIVE_LOCAL_HESSIAN_AND_SELECTED_MAP_STABLE_GRAPH; "
    "NUMERICAL_INGRESS_OPEN"
)

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_split_bimeasure_residual_stage4w.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_split_bimeasure_residual_stage4w.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_split_bimeasure_residual_stage4w.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-split-bimeasure-residual-stage4w.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_split_bimeasure_residual_stage4w.py"
)

STAGE4O_RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_event_aligned_return_hessian_stage4o_contract.json"
)
STAGE4P_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_graph_closure_arithmetic_stage4p.json"
)
STAGE4Q_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_signed_second_variation_stage4q_pilot.json"
)
STAGE4SB_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stage4s_hessian_bridge.json"
)
STAGE4T_RESULT_RELATIVE_PATH = (
    "experiments/results/direct_two_period_derivative_stage4t.json"
)

PARENT_RESULT_SHA256 = {
    STAGE4O_RESULT_RELATIVE_PATH: (
        "dc0e3951cb529dbdca384ff548ab0d7cd7786fe02573741e80e9c945452b2a23"
    ),
    STAGE4P_RESULT_RELATIVE_PATH: (
        "860a51d51648919f74bd7bd4e8230a629f7864b2bdcccf490aab5ff9e8e6b542"
    ),
    STAGE4Q_RESULT_RELATIVE_PATH: (
        "e4481bca2d021517073216dab15ee91c43cf301822b15e337c1b5061e9aaf49a"
    ),
    STAGE4SB_RESULT_RELATIVE_PATH: (
        "28e7116d855ec1a7e2b169356dce4d4dfb130069b35616a5ed6416f6634522e5"
    ),
    STAGE4T_RESULT_RELATIVE_PATH: (
        "6998c1ac89440f180ebe753d1aa41c36c8a849183794fdc38c52f2d8d54e94e1"
    ),
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 "
    "experiments/leaky_inner_split_bimeasure_residual_stage4w.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source-manifest validation; Banach-dual quotient "
    "identity for the fixed phase/stable section; projective signed "
    "atom-density/bimeasure inequalities; exact complete-history event "
    "Hessian algebra and fixed q_hat/f_hat output action; qualitative C2 "
    "center-to-ball localization; exact replay of the Stage-4S-B six-block "
    "budgets; no numerical kernel, interval, mesh, graph, or onset claim"
)

TOP_KEYS = {"certificate", "manifest"}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "artifact_sha256",
    "formal_core_sha256",
    "source_sha256",
    "parent_result_sha256",
    "runtime",
}

BLOCK_NAMES = (
    "stable_output_ss_upper",
    "stable_output_su_upper",
    "stable_output_uu_upper",
    "unstable_output_ss_upper",
    "unstable_output_su_upper",
    "unstable_output_uu_upper",
)

ERROR_CATEGORIES = (
    "base_orbit_and_coefficient_error",
    "first_variation_kernel_residual",
    "second_variation_kernel_residual",
    "event_quotient_and_history_translation",
    "continuous_qf_and_output_phase_completion",
    "full_ball_inflation_and_return_domain",
)

TRUE_FLAGS = (
    "all_five_parent_results_byte_and_source_manifest_validated",
    "direct_selected_map_C2_on_qualitative_coordinate_neighborhood_imported",
    "complete_history_hessian_exists_and_is_continuous_locally_proved",
    "some_unknown_small_preferred_shape_ball_has_finite_uniform_hessian_proved",
    "qualitative_local_selected_map_C2_stable_graph_proved",
    "global_same_ball_self_map_not_needed_for_local_graph_proved",
    "phase_section_stable_annihilator_quotient_identity_proved",
    "unstable_input_exact_qhat_action_identity_proved",
    "split_projective_bimeasure_upper_bound_proved",
    "exact_event_quotient_assembly_registered",
    "complete_history_translation_before_projection_registered",
    "moving_event_projection_applied_exactly_once_registered",
    "fixed_qhat_fhat_output_action_before_norm_proved",
    "six_block_center_plus_residual_implication_proved",
    "strict_center_caps_imply_some_qualitative_full_ball_caps_proved",
    "directed_interval_residual_algorithm_registered",
    "finite_sampling_operator_norm_shortcut_rejected",
    "current_zero_of_six_numeric_block_ingress_audited",
    "stage4q_diagnostic_values_excluded_from_strict_ingress",
)

FALSE_FLAGS = (
    "preferred_lambda_one_ball_validated",
    "numerical_preferred_lambda_lower_bound_imported",
    "same_preferred_scaled_ball_self_map_validated",
    "directed_base_orbit_and_field_jet_cover_validated",
    "directed_first_variation_measure_residual_validated",
    "directed_second_variation_bimeasure_residual_validated",
    "event_quotient_interval_residual_validated",
    "complete_output_phase_interval_cover_validated",
    "exact_qhat_fhat_six_kernel_action_numerically_validated",
    "full_ball_hessian_inflation_numerically_validated",
    "any_one_continuous_history_hessian_block_numeric_bound_validated",
    "all_six_continuous_history_hessian_block_numeric_bounds_validated",
    "stage4p_wide_box_entered_into_strict_numeric_ingress",
    "quantitative_inner_stable_graph_validated",
    "selected_map_graph_identified_with_periodic_orbit_stable_set_germ",
    "preferred_scale_stable_graph_domain_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "biological_capture_validated",
    "asynchronous_network_safety_validated",
)


@dataclass(frozen=True)
class Stage4WSplitBimeasureResidualCertificate:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    parent_theorem_audit: dict[str, Any]
    qualitative_hessian_localization: dict[str, Any]
    qualitative_local_stable_graph: dict[str, Any]
    phase_section_dual: dict[str, Any]
    stable_quotient_norm_theorem: dict[str, Any]
    split_projective_bimeasure_theorem: dict[str, Any]
    complete_history_event_hessian: dict[str, Any]
    exact_output_split_action: dict[str, Any]
    six_block_residual_acceptance: dict[str, Any]
    full_ball_inflation_theorem: dict[str, Any]
    rigorous_interval_algorithm: dict[str, Any]
    current_numeric_ingress: dict[str, Any]
    minimal_missing_ingress: dict[str, Any]
    theorem_boundary: dict[str, Any]
    claim_status: dict[str, bool]


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is missing")
    return value


def _load_parent(
    repository: Path, relative: str, expected_digest: str
) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected_digest:
        raise ValueError(f"the Stage-4W parent changed: {relative}")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the Stage-4W parent is malformed: {relative}")
    manifest = _mapping(
        payload.get("manifest"), f"manifest of the Stage-4W parent {relative}"
    )
    for manifest_name in ("source_sha256", "dependency_source_sha256"):
        source_hashes = manifest.get(manifest_name, {})
        if source_hashes is None:
            source_hashes = {}
        source_hashes = _mapping(
            source_hashes,
            f"{manifest_name} of the Stage-4W parent {relative}",
        )
        for source_relative, source_digest in source_hashes.items():
            if _sha256_path(repository / str(source_relative)) != source_digest:
                raise ValueError(
                    "a source bound by a Stage-4W parent changed: "
                    f"{source_relative}"
                )
    parent_hashes = manifest.get("parent_result_sha256", {})
    if parent_hashes is None:
        parent_hashes = {}
    parent_hashes = _mapping(
        parent_hashes,
        f"parent bytes of the Stage-4W parent {relative}",
    )
    for parent_relative, parent_digest in parent_hashes.items():
        if _sha256_path(repository / str(parent_relative)) != parent_digest:
            raise ValueError(
                "a result bound by a Stage-4W parent changed: "
                f"{parent_relative}"
            )
    return payload


def _load_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    parents = {
        relative: _load_parent(repository, relative, digest)
        for relative, digest in PARENT_RESULT_SHA256.items()
    }

    contract_o = _mapping(
        parents[STAGE4O_RESULT_RELATIVE_PATH].get("contract"),
        "Stage-4O contract",
    )
    claims_o = _mapping(contract_o.get("claim_status"), "Stage-4O claims")
    if (
        claims_o.get("exact_implicit_event_Tx_Txx_registered") is not True
        or claims_o.get(
            "moving_event_phase_projection_applied_exactly_once_registered"
        )
        is not True
        or claims_o.get("all_six_projected_return_hessian_blocks_validated")
        is not False
    ):
        raise ValueError("the Stage-4O analytic Hessian boundary changed")

    design_p = _mapping(
        parents[STAGE4P_RESULT_RELATIVE_PATH].get("design"),
        "Stage-4P design",
    )
    claims_p = _mapping(design_p.get("claim_status"), "Stage-4P claims")
    if (
        claims_p.get("wide_box_conditional_unique_crossing_arithmetic_closes")
        is not True
        or claims_p.get("two_return_six_projected_hessian_blocks_validated")
        is not False
    ):
        raise ValueError("the Stage-4P target-box boundary changed")

    pilot_q = _mapping(
        parents[STAGE4Q_RESULT_RELATIVE_PATH].get("pilot"),
        "Stage-4Q pilot",
    )
    claims_q = _mapping(pilot_q.get("claim_status"), "Stage-4Q claims")
    if (
        pilot_q.get("status") != "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND"
        or len(claims_q) != 19
        or any(value is not False for value in claims_q.values())
    ):
        raise ValueError("a Stage-4Q diagnostic was promoted")

    bridge_sb = _mapping(
        parents[STAGE4SB_RESULT_RELATIVE_PATH].get("bridge"),
        "Stage-4S-B bridge",
    )
    claims_sb = _mapping(
        bridge_sb.get("claim_status"), "Stage-4S-B claims"
    )
    strict_sb = _mapping(
        bridge_sb.get("strict_numeric_ingress"),
        "Stage-4S-B strict ingress",
    )
    if (
        claims_sb.get("finite_sampling_operator_norm_no_go_proved") is not True
        or claims_sb.get("all_six_complete_history_hessian_blocks_validated")
        is not False
        or strict_sb.get("all_six_strict_budget_tests_pass") is not False
    ):
        raise ValueError("the Stage-4S-B residual boundary changed")

    certificate_t = _mapping(
        parents[STAGE4T_RESULT_RELATIVE_PATH].get("certificate"),
        "Stage-4T certificate",
    )
    scope_t = _mapping(
        certificate_t.get("scope_boundary"), "Stage-4T scope"
    )
    claims_t = _mapping(
        certificate_t.get("claim_status"), "Stage-4T claims"
    )
    if (
        scope_t.get("direct_selected_C2_map_on_qualitative_scaled_ball")
        is not True
        or scope_t.get("fixed_linear_split_and_rates_at_center") is not True
        or scope_t.get("uniform_Hessian_blocks_or_quantitative_stable_graph")
        is not False
        or claims_t.get(
            "reduced_physical_direct_two_period_derivative_equals_a_squared_proved"
        )
        is not True
    ):
        raise ValueError("the Stage-4T C2/splitting boundary changed")
    return parents


def _stage4sb_bridge(
    parents: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any]:
    return _mapping(
        parents[STAGE4SB_RESULT_RELATIVE_PATH].get("bridge"),
        "Stage-4S-B bridge",
    )


def _stage4q_diagnostic_envelope(
    parents: Mapping[str, Mapping[str, Any]],
) -> dict[str, str]:
    pilot = _mapping(
        parents[STAGE4Q_RESULT_RELATIVE_PATH].get("pilot"),
        "Stage-4Q pilot",
    )
    refinement = _mapping(
        pilot.get("refinement_and_acceptance"), "Stage-4Q refinement"
    )
    envelope = _mapping(
        refinement.get("two_period_projected_block_heuristic_envelope"),
        "Stage-4Q heuristic envelope",
    )
    if set(envelope) != set(BLOCK_NAMES):
        raise ValueError("the Stage-4Q heuristic block set changed")
    return {name: str(envelope[name]) for name in BLOCK_NAMES}


def _budget_copy(
    parents: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    bridge = _stage4sb_bridge(parents)
    budget = _mapping(
        bridge.get("wide_box_error_budget"), "Stage-4S-B budget"
    )
    blocks = _mapping(budget.get("blocks"), "Stage-4S-B budget blocks")
    if set(blocks) != set(BLOCK_NAMES):
        raise ValueError("the Stage-4S-B block budget changed")
    result: dict[str, Any] = {}
    for name in BLOCK_NAMES:
        row = _mapping(blocks[name], f"Stage-4S-B budget row {name}")
        allocations = _mapping(
            row.get("projected_error_allowances"),
            f"Stage-4S-B allowances {name}",
        )
        if set(allocations) != set(ERROR_CATEGORIES):
            raise ValueError("the Stage-4S-B error categories changed")
        result[name] = {
            "stage4p_wide_cap": str(row["stage4p_wide_cap"]),
            "directed_center_core_target": str(
                row["independent_directed_banach_core_target"]
            ),
            "projected_error_allowances": {
                category: str(allocations[category])
                for category in ERROR_CATEGORIES
            },
            "strict_unused_reserve": str(row["strict_unused_reserve"]),
            "actual_directed_center_core_bound": None,
            "actual_projected_residuals": {
                category: None for category in ERROR_CATEGORIES
            },
            "strict_acceptance_validated": False,
        }
    return result


def _interval_coverage_count(
    parents: Mapping[str, Mapping[str, Any]],
) -> tuple[int, int]:
    required = _mapping(
        _stage4sb_bridge(parents).get("required_interval_quantities"),
        "Stage-4S-B interval ledger",
    )
    total = 0
    filled = 0
    for group in required.values():
        values = _mapping(
            _mapping(group, "Stage-4S-B interval group").get("values"),
            "Stage-4S-B interval values",
        )
        total += len(values)
        filled += sum(value is not None for value in values.values())
    return filled, total


def _formal_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qualitative_hessian_localization": certificate[
            "qualitative_hessian_localization"
        ],
        "qualitative_local_stable_graph": certificate[
            "qualitative_local_stable_graph"
        ],
        "phase_section_dual": certificate["phase_section_dual"],
        "stable_quotient_norm_theorem": certificate[
            "stable_quotient_norm_theorem"
        ],
        "split_projective_bimeasure_theorem": certificate[
            "split_projective_bimeasure_theorem"
        ],
        "complete_history_event_hessian": certificate[
            "complete_history_event_hessian"
        ],
        "exact_output_split_action": certificate["exact_output_split_action"],
        "six_block_residual_acceptance": certificate[
            "six_block_residual_acceptance"
        ],
        "full_ball_inflation_theorem": certificate[
            "full_ball_inflation_theorem"
        ],
        "rigorous_interval_algorithm": certificate[
            "rigorous_interval_algorithm"
        ],
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
    }


def build_stage4w_certificate(
    repository: Path,
) -> Stage4WSplitBimeasureResidualCertificate:
    repository = repository.resolve()
    parents = _load_parents(repository)
    budgets = _budget_copy(parents)
    diagnostic = _stage4q_diagnostic_envelope(parents)
    filled, total = _interval_coverage_count(parents)
    bridge_sb = _stage4sb_bridge(parents)
    projection = _mapping(
        bridge_sb.get("continuous_projection_stability"),
        "Stage-4S-B projection stability",
    )
    raw_ceiling = str(
        _mapping(
            bridge_sb.get("wide_box_error_budget"),
            "Stage-4S-B budget",
        )["simultaneous_raw_hessian_only_error_ceiling"]
    )

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})

    return Stage4WSplitBimeasureResidualCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        parent_theorem_audit={
            "stage4o": (
                "exact fixed-time, event-time, complete-history, and one-phase-"
                "projection D2 formulas; every numerical Hessian ingress null"
            ),
            "stage4p": (
                "six-block graph arithmetic and wide target box only; no "
                "continuous-history block supplied"
            ),
            "stage4q": (
                "signed finite-section diagnostic with all nineteen theorem "
                "flags false"
            ),
            "stage4s_b": (
                "finite-sampling no-go, atomic lift, projection factors, and "
                "six-block budgets; strict numerical ingress null"
            ),
            "stage4t": (
                "binds and types the Stage-4S-A/4R direct selected C2 map, "
                "then proves D Q_Y(Y_*)=A^2 and transfers the fixed center "
                "splitting/rates"
            ),
            "all_parent_bytes_and_source_manifests_validated": True,
        },
        qualitative_hessian_localization={
            "existence_source": (
                "the Stage-4S-A/4R direct selected map bound and typed by "
                "Stage-4T"
            ),
            "imported_map": (
                "Q_coord:D->E_s x R is C2 on an open neighborhood D of 0, "
                "Q_coord(0)=0"
            ),
            "hessian": "H(z)=D2 Q_coord(z) in Bil(E_s x R,E_s x R;E_s x R)",
            "operator_norm_continuity": (
                "for every epsilon>0 there is delta>0 such that ||z||<delta "
                "implies ||H(z)-H(0)||_bilinear<epsilon"
            ),
            "preferred_shape_ball": (
                "B_lambda={||x_s||_Y<=0.0097*lambda, "
                "|x_u|<=0.00025*lambda}"
            ),
            "local_boundedness_conclusion": (
                "there exist lambda_H>0 and K_H<infinity with B_lambda_H "
                "subset D and sup_{z in B_lambda_H}||H(z)||<=K_H"
            ),
            "reason": (
                "operator-norm continuity at 0, not compactness of an "
                "infinite-dimensional closed ball"
            ),
            "lambda_H_numeric_lower": None,
            "K_H_numeric_upper": None,
            "lambda_H_equals_preferred_scale_one": False,
            "same_ball_self_map_claimed": False,
            "proved": True,
        },
        qualitative_local_stable_graph={
            "coordinate_space": (
                "Z=E_s x R with the pullback J norm and splitting "
                "Z=Z_s direct_sum Z_u"
            ),
            "local_map": (
                "Q_coord:D->D_out, where D and D_out are open neighborhoods "
                "of 0 in the same Banach coordinate space and Q_coord(0)=0"
            ),
            "linearization": (
                "L=DQ_coord(0)=J^(-1)A^2J preserves Z_s and Z_u"
            ),
            "stable_power_bound": "||(L|Z_s)^n||<=0.01^n",
            "unstable_inverse_power_bound": (
                "||((L|Z_u)^(-1))^n||<=rho_u,2^n with "
                "rho_u,2<=0.3021835013350534687660493212683136997<1"
            ),
            "nonlinear_remainder": (
                "Q_coord(z)=Lz+N(z), N(0)=0 and DN(0)=0; C2 regularity "
                "makes sup_{||z||<r}||DN(z)|| arbitrarily small as r decreases"
            ),
            "theorem_invoked": (
                "the local stable-manifold theorem for a C2 Banach-space map "
                "with a hyperbolic fixed point and invertible unstable block"
            ),
            "conclusion": (
                "there are neighborhoods U_s of 0 in Z_s and U of 0 in Z "
                "and a C2 map psi:U_s->Z_u with psi(0)=0 and Dpsi(0)=0 such "
                "that W_sel^s,loc={x_s+psi(x_s)} is the local stable manifold "
                "of the selected coordinate map"
            ),
            "local_characterization": (
                "after shrinking U inside D intersect D_out, W_sel^s,loc "
                "consists of the points whose Q_coord iterates remain in U "
                "and converge to 0"
            ),
            "global_self_map_needed": False,
            "reason_global_self_map_not_needed": (
                "the local theorem uses Q_coord only while iterates remain in "
                "one smaller open neighborhood; it does not require Q_coord "
                "to map the entire anisotropic ball into itself"
            ),
            "effective_domain_radius": None,
            "effective_graph_height_or_slope": None,
            "periodic_orbit_stable_set_germ_identified": False,
            "why_periodic_germ_still_open": (
                "identifying selected-map iterates with convergence to the "
                "periodic orbit along all intervening flow arcs still needs "
                "the Stage-4R recurrence/phase-isolation hypotheses"
            ),
            "physical_first_return_or_event_ordinal_used": False,
            "pulse_sheet_crossing_implied": False,
            "proved": True,
        },
        phase_section_dual={
            "history_space": (
                "Y=C(K,R) x R, K=[-tau_max,0], with "
                "||(phi,w)||_Y=max(||phi||_infinity,|w|)"
            ),
            "dual": (
                "Y*=M(K) x R with ||(mu,c)||=||mu||_TV+|c|"
            ),
            "phase_section": "Sigma_0=ker(ell_0), ell_0(phi,w)=phi(0)",
            "fixed_pair": (
                "q_hat in Sigma_0, f_hat in Sigma_0*, ||q_hat||_Y=1, "
                "f_hat(q_hat)=1"
            ),
            "stable_and_unstable": (
                "E_s=ker(f_hat) inside Sigma_0 and E_u=span{q_hat}"
            ),
            "extension_convention": (
                "tilde_f is any Hahn-Banach extension of f_hat from Sigma_0 "
                "to Y; the quotient value below is extension independent"
            ),
        },
        stable_quotient_norm_theorem={
            "statement": (
                "for every mu in Y*, ||mu|_{E_s}|| = "
                "inf_{alpha,beta in R} ||mu-alpha*ell_0-beta*tilde_f||_{Y*}"
            ),
            "annihilator_identity": (
                "E_s^perp=span{ell_0,tilde_f} because "
                "E_s=ker(ell_0) intersect ker(tilde_f)"
            ),
            "proof": (
                "the restriction Y*->E_s* is a metric quotient with kernel "
                "E_s^perp; Hahn-Banach gives the reverse inequality and hence "
                "the exact distance formula"
            ),
            "stable_row_cost": (
                "d_s(mu):=inf_{alpha,beta}"
                "||mu-alpha*ell_0-beta*tilde_f||_{Y*}"
            ),
            "unstable_row_cost": "d_u(mu):=|mu(q_hat)|",
            "unstable_identity": (
                "sup_{|c|<=1}|mu(c*q_hat)|=|mu(q_hat)|"
            ),
            "coarse_projection_factor_necessary": False,
            "gain": (
                "current-phase atoms and f_hat multiples may be removed before "
                "total variation, while q_hat inputs are evaluated with sign"
            ),
            "proved": True,
        },
        split_projective_bimeasure_theorem={
            "admissible_representation": (
                "B=sum_or_Bochner_integral y_r tensor mu_r tensor nu_r with "
                "y_r in Sigma_0 and "
                "sum/integral ||y_r||||mu_r||||nu_r|| finite; mu_r,nu_r are "
                "signed atom-density measures including the recovery atom"
            ),
            "output_costs": {
                "stable": "omega_s(y)=||y-q_hat*f_hat(y)||_Y",
                "unstable": "omega_u(y)=|f_hat(y)|",
            },
            "input_costs": {
                "stable": "d_s(mu)=dist(mu,span{ell_0,tilde_f}) in Y*",
                "unstable": "d_u(mu)=|mu(q_hat)|",
            },
            "split_projective_cost": (
                "N_ab^o(B)=inf_rep sum/integral "
                "omega_o(y_r)*d_a(mu_r)*d_b(nu_r)"
            ),
            "operator_inequality": (
                "||O_o B[I_a .,I_b .]||_bilinear <= N_ab^o(B) for "
                "a,b,o in {s,u}"
            ),
            "proof": (
                "apply the exact restriction/evaluation bounds to each signed "
                "rank-one term, apply P_s or f_hat to its output coefficient, "
                "sum, and take the infimum over projective representations"
            ),
            "symmetry": (
                "the su block may use a symmetric representation, but no "
                "factor of two is inserted unless it is present in that "
                "representation"
            ),
            "scope": (
                "a validated projective atom-density representation or a "
                "residual in this norm is required; finite nodal values alone "
                "do not establish membership or an error bound"
            ),
            "proved": True,
        },
        complete_history_event_hessian={
            "terminal_objects": (
                "U^T,dot_U^T in L(Y,Y), V^T in Bil(Y,Y;Y), "
                "n=ell_0 o U^T, d=dot_X_T in Y, e=ddot_X_T in Y, "
                "a=ell_0(d)>0"
            ),
            "complete_history_meaning": (
                "every voltage output phase theta in [-tau_max,0] is evaluated "
                "at T(x)+theta and the recovery output is evaluated at T(x)"
            ),
            "event_time_first_derivative": "T_h=-n(h)/a",
            "preprojection_bimeasure": (
                "Z=V^T-a^(-1)*(dot_U^T tensor n+n tensor dot_U^T)"
                "+a^(-2)*e tensor n tensor n"
            ),
            "event_phase_projection": (
                "D2 Q_Y=H=Z-a^(-1)*d tensor (ell_0 o Z)"
            ),
            "equivalent_second_event_derivative": "T_hk=-ell_0(Z[h,k])/a",
            "inverse_denominator_order": "powers through a^(-3) after expansion",
            "correlation_rule": (
                "assemble every term with one common outward enclosure of a "
                "and its inverse powers before any norm"
            ),
            "translation_order": (
                "form U^T,dot_U^T,V^T,d,e on the complete translated history "
                "first, then apply the event projection exactly once"
            ),
            "moving_event_projection_count": 1,
            "proved_identity_source": "Stage-4O, now typed for the Stage-4T direct Q_Y",
        },
        exact_output_split_action={
            "elementary_tensor": "y tensor mu tensor nu",
            "stable_output": (
                "P_s(y tensor mu tensor nu)="
                "(y-q_hat*f_hat(y)) tensor mu tensor nu"
            ),
            "unstable_output": (
                "f_hat(y tensor mu tensor nu)=f_hat(y)*mu tensor nu"
            ),
            "stable_input": (
                "replace each input measure norm by its exact quotient cost d_s"
            ),
            "unstable_input": (
                "evaluate each input measure on q_hat before absolute values"
            ),
            "output_phase_action": (
                "evaluate the continuous atom-density f_hat on the entire "
                "completed output history, including its recovery atom and "
                "certified density/tail, before subtracting q_hat*f_hat"
            ),
            "affine_chart_identity": (
                "because j and chi are affine, D2Q_coord is obtained from "
                "D2Q_Y by the fixed input injection J and the displayed "
                "P_s/f_hat output actions, with no chart Hessian remainder"
            ),
            "raw_projection_factors_avoided": True,
            "raw_f_norm_upper_for_comparison_only": str(
                projection["stage4l_exact_restricted_fhat_norm_upper"]
            ),
            "raw_Ps_norm_upper_for_comparison_only": str(
                projection["P_s_norm_upper"]
            ),
            "same_finite_adapter_may_replace_continuous_pair": False,
            "proved": True,
        },
        six_block_residual_acceptance={
            "blocks": budgets,
            "acceptance_inequality": (
                "C_i + sum_{r in six residual categories} delta_{i,r} "
                "< cap_i for every one of the six blocks"
            ),
            "C_i_definition": (
                "one outward split-projective bound for the signed center "
                "event Hessian after exact input and output actions"
            ),
            "delta_definition": (
                "one outward split-projective norm of the corresponding true "
                "minus represented object, uniformly over the declared ball"
            ),
            "implication": (
                "the triangle inequality and the split-projective operator "
                "inequality imply all six continuous-history block bounds"
            ),
            "all_six_one_correlated_run_required": True,
            "simultaneous_raw_ambient_route_ceiling_for_comparison_only": raw_ceiling,
            "direct_split_route_uses_raw_ambient_ceiling": False,
            "strict_acceptance_currently_validated": False,
            "proved_implication": True,
        },
        full_ball_inflation_theorem={
            "block_map": (
                "B_i(z)=O_o D2Q_coord(z)[I_a .,I_b .] for the fixed split"
            ),
            "continuity": (
                "each B_i is operator-norm continuous at 0 because Q_coord is "
                "C2 and every I_a,O_o is fixed and bounded"
            ),
            "qualitative_target_transfer": (
                "if ||B_i(0)||<target_i for all six strict targets, then there "
                "exists lambda>0 such that sup_{z in B_lambda}||B_i(z)||"
                "<target_i simultaneously"
            ),
            "proof": (
                "take the minimum of the six positive center headrooms and use "
                "continuity at 0; no compactness and no mesh argument is used"
            ),
            "quantitative_inflation": (
                "Delta_i(lambda)=sup_{z in B_lambda}"
                "N_i(D2Q_coord(z)-D2Q_coord(0))"
            ),
            "quantitative_acceptance": (
                "C_i+Delta_i(lambda)<cap_i, with both terms outward and "
                "source-bound"
            ),
            "center_strict_caps_currently_validated": False,
            "lambda_numeric_lower_currently_validated": False,
            "inflation_numeric_upper_currently_validated": False,
            "proved_qualitative_implication": True,
        },
        rigorous_interval_algorithm={
            "representation": (
                "signed atoms plus interval polynomial/L1 densities for first "
                "variation rows, and projective signed bimeasures for second "
                "variation rows"
            ),
            "steps": [
                (
                    "fix one selected-event domain and partition physical source "
                    "time and output phase at every delay activation, method-of-"
                    "steps seam, event-window endpoint, and theta endpoint"
                ),
                (
                    "enclose the nonlinear base tube and D1F,D2F,D3F on the "
                    "whole anisotropic ball with outward interval Taylor/Picard "
                    "remainders"
                ),
                (
                    "propagate the current/delayed first-variation Riesz rows as "
                    "signed atom-density measures for arbitrary stable inputs and "
                    "for q_hat; bound the signed defect and initial trace in TV"
                ),
                (
                    "assemble the ss,su,uu D2F sources before modulus and solve "
                    "the Volterra second-variation equation in projective "
                    "bimeasure norm; bound its signed differential/integral defect"
                ),
                (
                    "form Z and H with the same positive event-speed enclosure, "
                    "retaining n,dot_U,d,e and inverse powers of a in one "
                    "correlated interval object"
                ),
                (
                    "complete every theta output and the recovery coordinate, "
                    "including left/right endpoints, short cells, and all seams; "
                    "use interval polynomial remainders, not nodal interpolation"
                ),
                (
                    "apply the continuous q_hat/f_hat pair to the correlated "
                    "object, including normalization, atom, density, and tail "
                    "errors; use the phase/stable quotient before absolute values"
                ),
                (
                    "separate a directed center core from a uniform ball residual "
                    "using D3F and the validated base/first/second-kernel defects"
                ),
                (
                    "take the six split-projective norms once, allocate every "
                    "residual to the frozen Stage-4S-B budget, and require six "
                    "strict inequalities in one source-bound run"
                ),
            ],
            "first_variation_defect": (
                "R_U=dot(U_tilde)-DF(X_tilde)U_tilde with every delayed row and "
                "the affine initial trace included; propagate its signed measure "
                "TV bound by a validated retarded resolvent"
            ),
            "second_variation_defect": (
                "R_V=dot(V_tilde)-DF(X_tilde)V_tilde-"
                "D2F(X_tilde)[U_tilde,U_tilde]; propagate in projective "
                "bimeasure norm with zero affine initial second jet"
            ),
            "forbidden": [
                "mesh convergence as an error bound on an arbitrary C ball",
                "binary64 Stage-4Q rows as outward intervals",
                "separate absolute values before the event/output correlations",
                "a finite q/f adapter in place of the continuous Grushin pair",
                "a center calculation promoted to a full-ball bound",
            ],
            "minimally_sufficient": True,
        },
        current_numeric_ingress={
            "qualitative_C2_map_and_local_hessian": True,
            "explicit_preferred_shape_lambda_from_bound_parents": None,
            "directed_center_core_blocks": {name: None for name in BLOCK_NAMES},
            "directed_full_ball_block_residuals": {
                name: {category: None for category in ERROR_CATEGORIES}
                for name in BLOCK_NAMES
            },
            "continuous_history_numeric_blocks_validated": 0,
            "continuous_history_numeric_blocks_required": 6,
            "required_interval_fields_filled": filled,
            "required_interval_fields_total": total,
            "stage4q_heuristic_envelope_diagnostic_only": diagnostic,
            "stage4q_values_enter_strict_ingress": False,
            "all_six_strict_acceptance_tests_pass": False,
        },
        minimal_missing_ingress={
            "decisive_missing_object": (
                "one source-bound directed atom-density/projective-bimeasure "
                "enclosure of the center D2Q and its uniform residual on a "
                "numerically declared preferred-shape ball after the exact "
                "event and q/f actions"
            ),
            "not_missing_anymore": [
                "a qualitative C2 selected near-two-period return",
                "existence and local boundedness of its Banach Hessian",
                "a qualitative C2 local stable graph for the selected map",
                "the center derivative DQ_Y(Y_*)=A^2",
                "the fixed center splitting and two-step rates",
                "the correct analytic event-Hessian formula",
                "the correct split-aware residual norm and acceptance implication",
            ],
            "still_missing": [
                "outward center first-variation atom-density rows on every source cell",
                "outward center ss,su,uu projective bimeasure rows on every output cell",
                "correlated event quotient and full output phase completion",
                "continuous q_hat/f_hat action with all tails on those six rows",
                "uniform base-ball inflation with a numerical lambda and strict caps",
            ],
            "finite_mesh_refinement_would_close": False,
        },
        theorem_boundary={
            "proved": (
                "qualitative existence/local boundedness of the complete-history "
                "Hessian, a qualitative local C2 stable graph for the selected "
                "map, the exact stable quotient and split-projective bounds, "
                "the exact event/output assembly order, the six-block residual "
                "implication, and the center-to-small-ball continuity implication"
            ),
            "conditional": (
                "strict continuous-history six-block bounds follow if the listed "
                "directed center cores and residuals satisfy the frozen budgets"
            ),
            "open": (
                "every numerical center/block/residual value, an explicit useful "
                "ball, a quantitative graph, identification with the periodic-"
                "orbit stable-set germ, pulse crossing/onset, routing, capture, "
                "biological control, and network safety"
            ),
            "graph_or_onset_promoted": False,
        },
        claim_status=claims,
    )


def build_stage4w_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_stage4w_certificate(repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "artifact_sha256": canonical_sha256(certificate),
            "formal_core_sha256": canonical_sha256(_formal_core(certificate)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": _runtime_record(),
        },
    }


def validate_stage4w_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4W result has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "Stage-4W certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-4W manifest")
    if set(certificate) != {
        field.name for field in fields(Stage4WSplitBimeasureResidualCertificate)
    }:
        raise ValueError("the Stage-4W certificate schema changed")
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4W manifest schema changed")

    repository = repository.resolve()
    expected = asdict(build_stage4w_certificate(repository))
    if dict(certificate) != expected:
        raise ValueError("the Stage-4W theorem or null ingress changed")

    claims = _mapping(certificate.get("claim_status"), "Stage-4W claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4W claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4W claim was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4W gate was promoted")

    ingress = _mapping(
        certificate.get("current_numeric_ingress"),
        "Stage-4W numeric ingress",
    )
    if (
        ingress.get("continuous_history_numeric_blocks_validated") != 0
        or ingress.get("continuous_history_numeric_blocks_required") != 6
        or ingress.get("required_interval_fields_filled") != 0
        or ingress.get("all_six_strict_acceptance_tests_pass") is not False
        or ingress.get("stage4q_values_enter_strict_ingress") is not False
    ):
        raise ValueError("a Stage-4W numerical Hessian gate was promoted")
    if any(
        value is not None
        for value in _mapping(
            ingress.get("directed_center_core_blocks"),
            "Stage-4W center blocks",
        ).values()
    ):
        raise ValueError("a Stage-4W center block was filled")
    for row in _mapping(
        ingress.get("directed_full_ball_block_residuals"),
        "Stage-4W ball residuals",
    ).values():
        if any(
            value is not None
            for value in _mapping(row, "Stage-4W residual row").values()
        ):
            raise ValueError("a Stage-4W residual was filled")

    expected_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(certificate),
        "formal_core_sha256": canonical_sha256(_formal_core(certificate)),
        "source_sha256": {
            relative: _sha256_path(repository / relative)
            for relative in SOURCE_MANIFEST
        },
        "parent_result_sha256": dict(PARENT_RESULT_SHA256),
        "runtime": _runtime_record(),
    }
    if dict(manifest) != expected_manifest:
        raise ValueError("the Stage-4W manifest or source binding changed")
    if recompute and dict(payload) != build_stage4w_result(repository):
        raise ValueError("the Stage-4W fresh replay changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BLOCK_NAMES",
    "BRANCH",
    "DEFAULT_COMMAND",
    "ERROR_CATEGORIES",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_KEYS",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATUS",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "Stage4WSplitBimeasureResidualCertificate",
    "_formal_core",
    "build_stage4w_certificate",
    "build_stage4w_result",
    "canonical_sha256",
    "validate_stage4w_result",
]
