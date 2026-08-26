from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.leaky_route_c_adjoint_stage4d import (
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    PILOT_STEP_COUNTS,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    fourier_reversal_oracle,
    validate_stage4d_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4d_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4d_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_bilinear_reversal_matches_advanced_shift() -> None:
    oracle = fourier_reversal_oracle()
    assert float(oracle["fourier_vs_physical_bilinear_error_binary64"]) < 1e-14
    assert float(
        oracle["forward_vs_advanced_change_of_variables_error_binary64"]
    ) < 1e-14
    assert float(oracle["hermitian_mutation_separation_binary64"]) > 1e-4
    bridge = _payload()["artifact"]["fourier_reversal_and_advanced_adjoint"]
    assert bridge["row_to_adjoint_coefficients"] == (
        "r_hat[n]=E_minus_state[-n]"
    )
    assert not bridge["complex_conjugation_used"]


def test_exact_adjoint_tail_is_wiener_summable() -> None:
    tail = _payload()["artifact"]["summable_adjoint_tail_certificate"]
    assert tail["tail_summability_validated"]
    assert gmpy2.mpq(tail["tail_row_contraction_upper"]) < gmpy2.mpq("0.105")
    assert gmpy2.mpq(tail["full_tail_split_l1_upper"]) < gmpy2.mpq("0.012")
    assert gmpy2.mpq(tail["recovery_tail_split_l1_upper"]) < gmpy2.mpq(
        tail["full_tail_split_l1_upper"]
    )


def test_grushin_derivative_gives_directed_history_normalization() -> None:
    norm = _payload()["artifact"]["grushin_border_normalization"]
    assert "E_minus L'(s_star) E_plus" in norm[
        "averaged_history_pairing_identity"
    ]
    assert norm["directed_numeric_normalization_available"]
    assert gmpy2.mpq(norm["f_of_q_modulus_lower"]) > gmpy2.mpq("0.0003")
    assert gmpy2.mpq(norm["f_of_q_modulus_upper"]) < gmpy2.mpq("0.00055")


def test_recovery_only_history_is_a_nonzero_continuous_shard() -> None:
    measure = _payload()["artifact"]["continuous_history_measure_enclosure"]
    assert measure["continuous_atom_density_measure_numeric_enclosed"]
    assert gmpy2.mpq(measure["current_recovery_atom_modulus_lower"]) > 0
    assert gmpy2.mpq(
        measure["normalized_recovery_only_history_action_modulus_lower"]
    ) > 0
    assert "phi_v(theta)=0" in measure["recovery_only_history_shard"]


def test_shared_yqq_pilot_subtracts_before_norm() -> None:
    pilot = _payload()["artifact"]["shared_y_qq_deflation_pilot"]
    rows = pilot["mesh_rows"]
    assert [row["step_count"] for row in rows] == list(PILOT_STEP_COUNTS)
    final = rows[-1]
    assert final["evaluation_order"].startswith("form y_qq-right")
    assert gmpy2.mpq(final["correlated_stable_output_linf"]) < gmpy2.mpq("7.27")
    assert gmpy2.mpq(final["triangle_to_correlated_ratio"]) > gmpy2.mpq("7")
    assert not pilot["mesh_change_is_interval_error"]
    assert not pilot["pilot_promoted_to_directed_y_qq_action"]


def test_directed_shared_yqq_ingress_remains_null() -> None:
    artifact = _payload()["artifact"]
    contract = artifact["directed_shared_y_qq_contract"]
    assert contract["physical_return_y_qq_directed_enclosure"] is None
    assert contract["normalized_adjoint_action_on_y_qq_directed_enclosure"] is None
    assert contract["correlated_stable_output_uu_upper"] is None
    assert not contract["contract_closes"]
    assert not contract["global_projection_norm_transfer_allowed"]
    update = artifact["stage4b_ingress_update"]
    assert update["continuous_history_measure_action_gate_closed"]
    assert update["directed_normalization_gate_closed"]
    assert not update["action_on_actual_shared_y_qq_gate_closed"]
    assert update["stable_output_uu_directed_upper"] is None


def test_claim_ledger_separates_bridge_from_yqq_theorem() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_note_keeps_mesh_and_csuu_claims_open() -> None:
    prose = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "These three meshes are not interval evidence" in prose
    assert "applying its global norm would discard the needed cancellation" in prose
    assert "the correlated bound" in prose
    assert "remains open" in prose


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            (
                "artifact",
                "summable_adjoint_tail_certificate",
                "tail_summability_validated",
            ),
            False,
        ),
        (
            (
                "artifact",
                "grushin_border_normalization",
                "directed_numeric_normalization_available",
            ),
            False,
        ),
        (
            (
                "artifact",
                "shared_y_qq_deflation_pilot",
                "pilot_promoted_to_directed_y_qq_action",
            ),
            True,
        ),
        (
            (
                "artifact",
                "directed_shared_y_qq_contract",
                "correlated_stable_output_uu_upper",
            ),
            "12",
        ),
        (
            (
                "artifact",
                "stage4b_ingress_update",
                "action_on_actual_shared_y_qq_gate_closed",
            ),
            True,
        ),
    ),
)
def test_hostile_bridge_or_yqq_mutations_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        validate_stage4d_result(payload, REPOSITORY)
