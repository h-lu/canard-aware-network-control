"""Stage-4T direct-two-period derivative bridge.

The Stage-4S-A event tube constructs a direct selected event near two
periods.  Its physical section map does not have to be the square of a
nonlinear one-period map.  At the exact periodic center, standard RFDE event
calculus and the variational cocycle nevertheless identify its derivative
with the square of the Stage-4L one-period phase-fixed derivative.

The distinction among the compatible full-X map, the physical reduced-Y
section map, and its coordinate representation is mandatory.  If ``J`` is
the affine-section tangent identification used by Stage 4S-A, then

    D Q_Y(Y_*)     = A^2,
    D Q_coord(0)  = J^{-1} A^2 J.

On the compatible lifted histories one instead has the typed intertwining

    D Q_X(Iota(Y_*)) D Iota = D Iota A^2.

No equality ``Q=P^2``, first-return statement, same-scaled-ball self-map,
quantitative Hessian bound, stable graph, or stable-set-germ claim is made.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.finite_delay_eventually_smooth_selected_return_stage4r import (
    validate_stage4r_result,
)
from canard_control.leaky_inner_stage4s_event_tube import (
    validate_stage4s_event_tube_result,
)
from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    validate_stage4l_result,
)
from canard_control.leaky_inner_two_return_stage4s_split_bridge import (
    validate_stage4s_split_bridge_result,
)


SCHEMA_ID = "direct-two-period-derivative-stage4t-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_two_period_event"
STATUS = "PROVED_DIRECT_TWO_PERIOD_DERIVATIVE_BRIDGE"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/direct_two_period_derivative_stage4t.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/direct_two_period_derivative_stage4t.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/direct_two_period_derivative_stage4t.json"
)
NOTE_RELATIVE_PATH = "docs/direct_two_period_derivative_stage4t.md"
TEST_RELATIVE_PATH = "tests/test_direct_two_period_derivative_stage4t.py"

STAGE4SA_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stage4s_event_tube.json"
)
STAGE4SC_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_two_return_stage4s_split_bridge.json"
)
STAGE4L_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_terminal_stable_row_stage4l.json"
)
STAGE4R_RESULT_RELATIVE_PATH = (
    "experiments/results/finite_delay_eventually_smooth_selected_return_stage4r.json"
)

# Final repaired Stage-4S-A v2 result.  Every Stage-4T build verifies these
# exact bytes before consuming its reduced-history/event semantics.
STAGE4SA_RESULT_SHA256 = (
    "b552c5c6fc8afce53ed047ad8264a9d428351d9f031dc566af60969307a1d91f"
)

FROZEN_PARENT_RESULT_SHA256 = {
    STAGE4SC_RESULT_RELATIVE_PATH: (
        "fde3e1d6fc8d55dbaf4f33ef4098e335f3c4febe39c2b9ac78d327ad688fbc70"
    ),
    STAGE4L_RESULT_RELATIVE_PATH: (
        "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
    ),
    STAGE4R_RESULT_RELATIVE_PATH: (
        "4e68835bc3ba5fd44432d98a3b6b1d41506533d66f3353cd500df3e95da76418"
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
    "/usr/bin/python3 experiments/direct_two_period_derivative_stage4t.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and semantic validation; symbolic RFDE selected-event "
    "first-derivative formula; periodic variational cocycle and phase-tangent "
    "annihilation identity; exact physical-versus-coordinate chart conjugacy; "
    "no new floating-point or interval arithmetic"
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

STABLE_RATE_TWO = "0.01"
UNSTABLE_BACKWARD_RATE_TWO = (
    "0.302183501335053468766049321268313699617093109911449469063818668425"
    "607982682870864983343314167041012216402531488839876224555070910009"
    "877958313689944253533344086871769103550439695624961741628356"
)

TRUE_FLAGS = (
    "stage4sa_stage4sc_stage4l_stage4r_parents_validated",
    "full_x_reduced_y_and_coordinate_selected_maps_distinguished",
    "direct_selected_center_event_time_equals_two_periods_proved",
    "direct_selected_reduced_physical_map_fixes_exact_center_proved",
    "direct_selected_compatible_full_map_fixes_lifted_center_proved",
    "direct_selected_coordinate_map_fixes_zero_proved",
    "event_derivative_projection_formula_proved",
    "periodic_variational_cocycle_identity_registered",
    "phase_tangent_monodromy_identity_registered",
    "periodic_event_projection_identity_registered",
    "projected_cocycle_square_identity_proved",
    "reduced_physical_direct_two_period_derivative_equals_a_squared_proved",
    "compatible_full_lift_derivative_intertwining_proved",
    "coordinate_derivative_is_conjugate_to_a_squared_proved",
    "nonlinear_one_period_map_not_needed_for_derivative_identity",
    "stage4sc_fixed_splitting_transfers_to_reduced_physical_derivative",
    "stage4sc_stable_rate_transfers_in_physical_y_norm",
    "stage4sc_unstable_backward_rate_transfers_in_physical_y_norm",
    "pullback_j_norm_preserves_the_transferred_rates",
    "selected_branch_and_first_return_remain_separated",
    "q_equals_p_squared_kept_false",
    "semantic_type_audit_fail_closed",
)

FALSE_FLAGS = (
    "direct_selected_map_equals_square_of_nonlinear_one_period_map_validated",
    "nonlinear_one_period_selected_map_validated",
    "coordinate_derivative_literally_equals_a_squared_without_identification",
    "full_x_derivative_literally_equals_reduced_a_squared",
    "arbitrary_coordinate_product_norm_preserves_stage4sc_numeric_rates",
    "same_scaled_anisotropic_ball_self_map_validated",
    "preferred_lambda_one_ball_validated",
    "numerical_lambda_star_lower_bound_validated",
    "first_positive_return_validated",
    "second_positive_oriented_hit_ordinal_validated",
    "no_earlier_section_hit_validated",
    "uniform_two_period_hessian_blocks_validated",
    "quantitative_stable_graph_validated",
    "periodic_orbit_stable_set_germ_identification_validated",
    "pulse_crossing_onset_routing_or_safety_validated",
)


@dataclass(frozen=True)
class DirectTwoPeriodDerivativeCertificate:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    map_type_audit: dict[str, Any]
    direct_two_period_center: dict[str, Any]
    selected_event_derivative_theorem: dict[str, Any]
    periodic_cocycle_projection_identity: dict[str, Any]
    reduced_physical_derivative_identification: dict[str, Any]
    coordinate_conjugacy: dict[str, Any]
    linear_split_and_rate_transfer: dict[str, Any]
    semantic_binding_ledger: dict[str, Any]
    proved_conditional_open_ledger: dict[str, Any]
    scope_boundary: dict[str, bool]
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


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def parent_result_sha256() -> dict[str, str]:
    if not _is_sha256(STAGE4SA_RESULT_SHA256):
        raise RuntimeError(
            "Stage-4T is fail closed pending the repaired Stage-4S-A result SHA-256"
        )
    return {
        STAGE4SA_RESULT_RELATIVE_PATH: STAGE4SA_RESULT_SHA256,
        **FROZEN_PARENT_RESULT_SHA256,
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS", ""),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS", ""),
        "arithmetic": (
            "formal operator identities and exact JSON/SHA-256 binding; no "
            "new floating-point arithmetic"
        ),
    }


def _parent_payloads(repository: Path) -> dict[str, Mapping[str, Any]]:
    repository = repository.resolve()
    expected = parent_result_sha256()
    payloads: dict[str, Mapping[str, Any]] = {}
    for relative, digest in expected.items():
        path = repository / relative
        if _sha256_path(path) != digest:
            raise ValueError(f"the Stage-4T parent changed: {relative}")
        payloads[relative] = json.loads(path.read_text(encoding="utf-8"))

    validate_stage4s_event_tube_result(
        payloads[STAGE4SA_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    validate_stage4s_split_bridge_result(
        payloads[STAGE4SC_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    validate_stage4l_result(
        payloads[STAGE4L_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    validate_stage4r_result(
        payloads[STAGE4R_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    return payloads


def _validate_parent_semantics(
    parents: Mapping[str, Mapping[str, Any]],
) -> None:
    stage4sa = _mapping(
        parents[STAGE4SA_RESULT_RELATIVE_PATH].get("certificate"),
        "Stage-4S-A certificate",
    )
    if (
        stage4sa.get("model_id") != MODEL_ID
        or stage4sa.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4S-A model identity changed")
    inputs = _mapping(stage4sa.get("exact_inputs"), "Stage-4S-A exact inputs")
    if (
        inputs.get("reduced_event_functional")
        != "g_Y(y)=y_v(0)-Y_{*,v}(0)"
        or inputs.get("exact_affine_section_in_Y")
        != "Sigma=Y_*+Sigma_0, Sigma_0={h in Y:h_v(0)=0}"
        or inputs.get("reduced_history_space")
        != (
            "Y=C([-tau_max,0],R)_v x R_w with "
            "||(phi,w)||_Y=max(||phi||_infinity,|w|)"
        )
        or inputs.get("initial_coordinate_injection")
        != (
            "j(x_s,x_u)=Y_*+x_s+q_hat*x_u, with x_s in "
            "ker(f_hat), ||q_hat||_Y=1, and the fixed Stage-3/4N "
            "Route-C splitting"
        )
        or inputs.get("validated_periodic_center")
        != (
            "the exact phase-fixed full RFDE orbit X_*^X and its reduced "
            "projection Y_*=pi(X_*^X)"
        )
    ):
        raise ValueError("the Stage-4S-A event section changed")
    center = _mapping(
        stage4sa.get("exact_center_event_window"),
        "Stage-4S-A center event",
    )
    if (
        center.get("center_selected_time") != "T(Y_*)=2P exactly"
        or center.get("center_returned_history")
        != (
            "Psi_{2P}(Y_*)=Y_* and "
            "Phi_{2P}(Iota(Y_*))=Iota(Y_*) exactly"
        )
    ):
        raise ValueError("the Stage-4S-A center fixed-return data changed")
    reduced = _mapping(
        stage4sa.get("reduced_history_bridge"),
        "Stage-4S-A reduced-history bridge",
    )
    if (
        reduced.get("status")
        != "PROVED_EXACT_REDUCED_HISTORY_FACTORISATION"
        or reduced.get("reduced_semiflow")
        != "Psi_t=pi o Phi_t o Iota for every t>=0"
        or "g_X(Phi_t(Iota(y)))=g_Y(Psi_t(y))"
        not in str(reduced.get("event_intertwining"))
        or "Phi_{T(y)}(Iota(y))=Iota(R_Y(y))"
        not in str(reduced.get("compatible_full_hit"))
        or reduced.get("full_X_identified_with_Y_without_bridge") is not False
    ):
        raise ValueError("the Stage-4S-A full-X/reduced-Y bridge changed")
    claims4sa = _mapping(
        stage4sa.get("claim_status"), "Stage-4S-A claims"
    )
    for name in (
        "C2_selected_event_hit_on_open_neighborhood_of_scaled_ball_proved",
        "exact_periodic_RFDE_center_validated",
        "exact_reduced_history_lift_projection_bridge_validated",
        "full_X_and_reduced_Y_event_functions_intertwined",
        "reduced_Y_joint_C2_smoothing_corollary_proved",
    ):
        if claims4sa.get(name) is not True:
            raise ValueError(f"a required Stage-4S-A claim changed: {name}")
    for name in (
        "Q_equals_P2_validated",
        "full_X_and_reduced_Y_phase_spaces_identified_without_bridge",
        "return_is_self_map_of_same_scaled_anisotropic_ball_validated",
    ):
        if claims4sa.get(name) is not False:
            raise ValueError(f"a Stage-4S-A boundary was promoted: {name}")
    stage4sa_parents = _mapping(
        stage4sa.get("parent_result_sha256"), "Stage-4S-A parents"
    )
    if (
        stage4sa_parents.get(STAGE4L_RESULT_RELATIVE_PATH)
        != FROZEN_PARENT_RESULT_SHA256[STAGE4L_RESULT_RELATIVE_PATH]
        or stage4sa_parents.get(STAGE4R_RESULT_RELATIVE_PATH)
        != FROZEN_PARENT_RESULT_SHA256[STAGE4R_RESULT_RELATIVE_PATH]
    ):
        raise ValueError("the Stage-4S-A analytic parents changed")
    returned = _mapping(
        stage4sa.get("return_domain_containment"),
        "Stage-4S-A return containment",
    )
    if (
        returned.get("same_scaled_ball_self_map") is not False
        or "P_sel=chi o R_j" not in str(returned.get("induced_return"))
        or "has inverse j" not in str(returned.get("terminal_chart"))
        or returned.get("reduced_coordinate_hit") != "R_j=R_Y o j on D_in"
    ):
        raise ValueError("the Stage-4S-A chart or self-map boundary changed")

    stage4sc = _mapping(
        parents[STAGE4SC_RESULT_RELATIVE_PATH].get("certificate"),
        "Stage-4S-C certificate",
    )
    if stage4sc.get("model_id") != MODEL_ID:
        raise ValueError("the Stage-4S-C model identity changed")
    split = _mapping(
        stage4sc.get("model_linear_instance"),
        "Stage-4S-C linear instance",
    )
    if (
        split.get("two_return_registered_stable_rate_upper")
        != STABLE_RATE_TWO
        or split.get("two_return_unstable_backward_rate_upper")
        != UNSTABLE_BACKWARD_RATE_TWO
        or split.get("nonlinear_claim") is not False
    ):
        raise ValueError("the Stage-4S-C linear rate boundary changed")
    claims4sc = _mapping(
        stage4sc.get("claim_status"), "Stage-4S-C claims"
    )
    for name in (
        "b_equals_a_squared_preserves_same_fixed_splitting_proved",
        "b_stable_power_bound_is_squared_proved",
        "b_unstable_inverse_power_formula_proved",
        "model_two_step_stable_rate_0p01_with_k_one_proved",
        "model_two_step_unstable_backward_rate_squared_proved",
    ):
        if claims4sc.get(name) is not True:
            raise ValueError(f"a required Stage-4S-C claim changed: {name}")
    if (
        claims4sc.get("model_q_equals_p_squared_identity_validated")
        is not False
    ):
        raise ValueError("Stage-4S-C promoted Q=P^2")

    stage4l = _mapping(
        parents[STAGE4L_RESULT_RELATIVE_PATH].get("artifact"),
        "Stage-4L artifact",
    )
    if stage4l.get("model_id") != MODEL_ID:
        raise ValueError("the Stage-4L model identity changed")
    lemma = _mapping(
        stage4l.get("analytic_discrete_lemma"),
        "Stage-4L analytic discrete lemma",
    )
    if (
        lemma.get("section") != "Sigma_0={h in Y:h_v(0)=0}"
        or lemma.get("selected_linear_map")
        != "A=Pi_T U(T,0)|_{Sigma_0}"
        or lemma.get("event_operator")
        != "Pi_T y=y-Xdot_T*ell_0(y)/Xdot_v(T)"
    ):
        raise ValueError("the Stage-4L phase/event projection changed")
    stage4sa_period = _mapping(
        stage4sa.get("physical_normalization"), "Stage-4S-A period"
    )
    stage4l_period = _mapping(
        stage4l.get("true_period_and_word_support"), "Stage-4L period"
    )
    if (
        stage4l.get("branch") != "inner_saddle_candidate"
        or stage4sa_period.get("period_lower")
        != stage4l_period.get("true_period_lower")
        or stage4sa_period.get("period_upper")
        != stage4l_period.get("true_period_upper")
    ):
        raise ValueError("the Stage-4S-A/Stage-4L period binding changed")

    stage4r = _mapping(
        parents[STAGE4R_RESULT_RELATIVE_PATH].get("theorem"),
        "Stage-4R theorem",
    )
    formulas = _mapping(
        stage4r.get("event_and_return_derivative_formulas"),
        "Stage-4R derivative formulas",
    )
    if (
        formulas.get("first_event_derivative") != "T_h=-H_u[h]/H_t"
        or formulas.get("first_hit_derivative")
        != "DR[h]=S_u[h]+S_t*T_h"
    ):
        raise ValueError("the Stage-4R event derivative formula changed")


def _formal_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "map_type_audit": certificate["map_type_audit"],
        "selected_event_derivative_theorem": certificate[
            "selected_event_derivative_theorem"
        ],
        "periodic_cocycle_projection_identity": certificate[
            "periodic_cocycle_projection_identity"
        ],
        "reduced_physical_derivative_identification": certificate[
            "reduced_physical_derivative_identification"
        ],
        "coordinate_conjugacy": certificate["coordinate_conjugacy"],
        "claim_status": certificate["claim_status"],
    }


def build_direct_two_period_derivative_certificate(
    repository: Path,
) -> DirectTwoPeriodDerivativeCertificate:
    parents = _parent_payloads(repository)
    _validate_parent_semantics(parents)
    parent_hashes = parent_result_sha256()
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    scope = {
        "direct_selected_C2_map_on_qualitative_scaled_ball": True,
        "center_fixed_point_and_two_period_time": True,
        "reduced_Y_derivative_equals_A_squared": True,
        "compatible_full_X_derivative_intertwining": True,
        "coordinate_derivative_conjugate_to_A_squared": True,
        "fixed_linear_split_and_rates_at_center": True,
        "Q_equals_nonlinear_P_squared": False,
        "same_scaled_ball_self_map": False,
        "first_return_or_event_ordinal": False,
        "uniform_Hessian_blocks_or_quantitative_stable_graph": False,
        "periodic_orbit_stable_set_germ": False,
        "pulse_onset_routing_or_safety": False,
    }
    return DirectTwoPeriodDerivativeCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=parent_hashes,
        map_type_audit={
            "stage4sa_reduced_hit": (
                "R_Y(y)=Psi_{T(y)}(y) maps the ambient reduced event "
                "neighborhood W into Y"
            ),
            "tangent_identification": (
                "J=D j(0):E_s x R->Sigma_0, "
                "J(x_s,x_u)=x_s+q_hat*x_u"
            ),
            "reduced_physical_section_map": (
                "Q_Y=R_Y|_{j(D)}:j(D)->Sigma_loc"
            ),
            "coordinate_section_map": (
                "Q_coord=chi o R_Y o j:D->D_out, with "
                "D chi(Y_*)=J^{-1}"
            ),
            "compatible_full_section_map": (
                "Q_X(Iota(y))=Iota(Q_Y(y)) on Iota(j(D))"
            ),
            "reduced_fixed_point_notation": "Q_Y(Y_*)=Y_*",
            "full_fixed_point_notation": (
                "Q_X(Iota(Y_*))=Iota(Y_*)"
            ),
            "coordinate_fixed_point_notation": "Q_coord(0)=0",
            "ill_typed_notation_rejected": (
                "D Q_X=A^2 and D Q_coord=A^2 are not literal typed "
                "statements because A acts on reduced Sigma_0"
            ),
        },
        direct_two_period_center={
            "full_periodic_center": (
                "Phi_{P_orb}(Iota(Y_*))=Iota(Y_*)"
            ),
            "reduced_periodic_center": "Psi_{P_orb}(Y_*)=Y_*",
            "selected_center_time": "T(Y_*)=2*P_orb exactly",
            "returned_history": (
                "Psi_{2*P_orb}(Y_*)=Y_* and "
                "Phi_{2*P_orb}(Iota(Y_*))=Iota(Y_*) exactly"
            ),
            "reduced_fixed_point": "Q_Y(Y_*)=Y_*",
            "full_fixed_point": "Q_X(Iota(Y_*))=Iota(Y_*)",
            "coordinate_fixed_point": "Q_coord(0)=0",
            "first_return_used": False,
            "nonlinear_one_period_map_used": False,
        },
        selected_event_derivative_theorem={
            "setting": (
                "Psi is the C1 reduced semiflow induced from the full RFDE, "
                "Y_* lies on its smooth P_orb-periodic orbit, g_Y is the fixed "
                "affine phase-zero event, ell=Dg_Y=ell_0, and a=ell(v)!=0 "
                "for v=dot Y_*(0)"
            ),
            "variational_operator": (
                "U_Y(t,s)=D_y Psi_{t-s}(Y_*(s)) on the reduced physical "
                "history space Y"
            ),
            "direct_event_time_derivative": (
                "D T(Y_*)[h]=-ell(U_Y(2P_orb,0)h)/a"
            ),
            "event_projection": "Pi=I-v*ell/a",
            "direct_reduced_derivative": (
                "D Q_Y(Y_*)=Pi U_Y(2P_orb,0)|_{Sigma_0}"
            ),
            "proof": (
                "apply the scalar implicit-function derivative to "
                "g_Y(Psi_T(y))=0 and substitute it into the first reduced-"
                "history hit derivative"
            ),
            "first_or_ordinal_return_needed": False,
        },
        periodic_cocycle_projection_identity={
            "one_period_monodromy": "M=U_Y(P_orb,0)",
            "periodic_cocycle": (
                "U_Y(2P_orb,P_orb)=U_Y(P_orb,0)=M and "
                "U_Y(2P_orb,0)=M^2"
            ),
            "phase_tangent": "M v=v",
            "periodic_projection": (
                "Pi_{P_orb}=Pi_{2P_orb}=Pi because the orbit point, tangent, "
                "event differential, and event speed repeat"
            ),
            "projection_kernel": (
                "(I-Pi)y=v*ell(y)/a, Pi v=0, and Pi M v=0"
            ),
            "square_calculation": (
                "for h in Sigma_0, (Pi M|Sigma_0)^2 h="
                "Pi M Pi M h=Pi M^2 h because Pi M(I-Pi)M h=0"
            ),
            "invertibility_of_semiflow_used": False,
            "nonlinear_one_period_return_used": False,
        },
        reduced_physical_derivative_identification={
            "stage4l_operator": "A=Pi M|_{Sigma_0}",
            "direct_two_period_operator": (
                "D Q_Y(Y_*)=Pi M^2|_{Sigma_0}"
            ),
            "exact_identity": "D Q_Y(Y_*)=A^2",
            "compatible_full_lift_intertwining": (
                "D Q_X(Iota(Y_*)) o D Iota(Y_*)="
                "D Iota(Y_*) o A^2"
            ),
            "full_X_literal_A_squared": False,
            "identity_is_linearization_not_map_equality": True,
            "Q_equals_P_squared": False,
            "nonlinear_one_period_P_required": False,
        },
        coordinate_conjugacy={
            "chart_differentials": (
                "D j(0)=J and D chi(Y_*)=J^{-1}"
            ),
            "exact_identity": "D Q_coord(0)=J^{-1} A^2 J",
            "literal_A_squared_only_after_identification": (
                "after identifying E_s x R with Sigma_0 through J, the "
                "coordinate derivative represents A^2"
            ),
            "arbitrary_product_norm_isometry_claimed": False,
            "pullback_norm": "||z||_J:=||Jz||_Y",
        },
        linear_split_and_rate_transfer={
            "physical_fixed_splitting": (
                "Sigma_0=E_s direct_sum E_u is invariant under "
                "D Q_Y(Y_*)=A^2"
            ),
            "stable_power_bound": (
                "||(D Q_Y|E_s)^n||_Y<=0.01^n with K_s=1"
            ),
            "stable_rate_upper": STABLE_RATE_TWO,
            "unstable_backward_power_bound": (
                "||((D Q_Y)|E_u)^(-n)||_Y<=rho_u,2^n with K_u=1"
            ),
            "unstable_backward_rate_upper": UNSTABLE_BACKWARD_RATE_TWO,
            "coordinate_spaces": "J^{-1}E_s direct_sum J^{-1}E_u",
            "coordinate_rate_norm": (
                "the same numeric rates hold in the pullback norm ||.||_J"
            ),
            "arbitrary_coordinate_product_norm_rate": None,
        },
        semantic_binding_ledger={
            "same_exact_center": (
                "Stage-4S-A Y_*=pi(X_*^X) and Stage-4L's phase-zero reduced "
                "center are the same source-bound periodic orbit in Y"
            ),
            "same_period": (
                "Stage-4L T is the same exact period P_orb used by the "
                "Stage-4S-A center event"
            ),
            "same_semiflow_and_variational_cocycle": (
                "Stage-4L U is U_Y=D_y Psi along that same exact reduced "
                "orbit, while Phi and Psi are connected only through the "
                "proved pi/Iota factorisation"
            ),
            "same_event_and_section": (
                "Stage-4S-A Dg=ell_0, Sigma_0=ker(ell_0), and Stage-4L's "
                "Pi_T use the identical physical phase-zero voltage event"
            ),
            "periodic_standard_identities": (
                "U(2P,P)=U(P,0), U(P,0)v=v, and Pi_P=Pi_2P"
            ),
            "chart_type_binding": (
                "the reduced map uses Y_* and A^2; the compatible full map "
                "uses Iota(Y_*) and derivative intertwining; the coordinate "
                "map uses 0 and J^{-1}A^2J"
            ),
            "all_bindings_required": True,
        },
        proved_conditional_open_ledger={
            "proved": [
                "the direct selected center time is 2P_orb",
                "the direct reduced return fixes Y_* and its full lift fixes Iota(Y_*)",
                "D Q_Y(Y_*)=A^2 without a nonlinear one-period P",
                "D Q_X(Iota(Y_*)) D Iota=D Iota A^2",
                "D Q_coord(0)=J^{-1}A^2J",
                "the Stage-4S-C fixed splitting and rates transfer at the center",
            ],
            "conditional": [
                "literal coordinate A^2 notation only under the J identification",
                "unchanged numeric coordinate rates only in the pullback J norm",
            ],
            "open": [
                "Q=P^2 as a nonlinear identity",
                "a same-scaled-ball self-map and numerical lambda_* lower bound",
                "first/second-return ordinal or no-earlier-hit statement",
                "uniform Hessian blocks, quantitative stable graph, and "
                "stable-set germ",
                "pulse crossing, biological onset/control, routing, capture, or safety",
            ],
        },
        scope_boundary=scope,
        claim_status=claims,
    )


def build_direct_two_period_derivative_result(
    repository: Path,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_direct_two_period_derivative_certificate(repository))
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
            "parent_result_sha256": parent_result_sha256(),
            "runtime": _runtime_record(),
        },
    }


def validate_direct_two_period_derivative_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4T result has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "Stage-4T certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-4T manifest")
    if set(certificate) != {
        field.name for field in fields(DirectTwoPeriodDerivativeCertificate)
    }:
        raise ValueError("the Stage-4T certificate schema changed")
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4T manifest schema changed")

    expected_certificate = asdict(
        build_direct_two_period_derivative_certificate(repository)
    )
    if dict(certificate) != expected_certificate:
        raise ValueError("the Stage-4T theorem or semantic audit changed")

    claims = _mapping(certificate.get("claim_status"), "Stage-4T claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4T claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4T claim was demoted")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an excluded Stage-4T claim was promoted")

    expected_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(certificate),
        "formal_core_sha256": canonical_sha256(_formal_core(certificate)),
        "source_sha256": {
            relative: _sha256_path(repository.resolve() / relative)
            for relative in SOURCE_MANIFEST
        },
        "parent_result_sha256": parent_result_sha256(),
        "runtime": _runtime_record(),
    }
    if dict(manifest) != expected_manifest:
        raise ValueError("the Stage-4T manifest or source binding changed")
    if recompute and dict(payload) != build_direct_two_period_derivative_result(
        repository
    ):
        raise ValueError("the Stage-4T fresh replay changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "FROZEN_PARENT_RESULT_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_KEYS",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STABLE_RATE_TWO",
    "STAGE4SA_RESULT_SHA256",
    "STATUS",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "UNSTABLE_BACKWARD_RATE_TWO",
    "DirectTwoPeriodDerivativeCertificate",
    "_formal_core",
    "build_direct_two_period_derivative_certificate",
    "build_direct_two_period_derivative_result",
    "canonical_sha256",
    "parent_result_sha256",
    "validate_direct_two_period_derivative_result",
]
