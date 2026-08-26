from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import gmpy2
import numpy as np
import pytest

from canard_control.leaky_route_c_adjoint_stage4c import (
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    PILOT_STEP_COUNTS,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    apply_discrete_normalized_deflation,
    validate_stage4c_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "5ddd440449e0405bab4ca33818174a8e214d85fa695f603ea45ddef051ceaa29"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4c_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4c_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_nonzero_pairing_is_a_theorem_but_numeric_normalization_is_open() -> None:
    theorem = _payload()["artifact"]["simple_multiplier_and_pairing_theorem"]
    assert theorem["unstable_restriction_dimension"] == 1
    assert theorem["characteristic_root_algebraic_multiplicity"] == 1
    assert theorem["f_of_q_nonzero_validated"]
    assert theorem["qualitative_rescaling_f_of_q_equals_one_allowed"]
    assert not theorem["directed_numeric_rescaling_available"]
    assert theorem["slope_is_not_identified_with_f_of_q"]


def test_rfde_measure_formula_and_section_invariance_are_explicit() -> None:
    identity = _payload()["artifact"]["rfde_adjoint_history_measure_identity"]
    assert "A_j(t+tau_j)^T" in identity["advanced_adjoint_equation"]
    assert "integral_{-tau_j}^0" in identity["history_functional"]
    assert identity["pairing_invariance"] == "d/dt f_t(x_t)=0"
    assert "f(Qy)=f(y)" in identity["route_c_section_consequence"]
    assert identity["analytic_identity_proved"]
    assert not identity["atoms_and_density_numerically_enclosed"]


def test_directed_fourier_row_has_large_nonzero_margin() -> None:
    row = _payload()["artifact"]["directed_fourier_grushin_left_row"]
    assert row["full_infinite_fourier_cokernel_row_enclosed"]
    assert row["fourier_cokernel_row_nonzero"]
    assert not row["history_adjoint_measure_identification_validated"]
    assert gmpy2.mpq(row["full_grushin_contraction_upper"]) < gmpy2.mpq("0.095")
    assert gmpy2.mpq(row["exact_bottom_row_distance_dual_upper"]) < gmpy2.mpq(
        "1.18e-9"
    )
    assert gmpy2.mpq(row["largest_component"]["exact_modulus_lower"]) > gmpy2.mpq(
        "0.0296"
    )
    assert len(row["finite_row_coefficients"]) == 258


def test_discrete_action_is_reproducible_and_deflates_q() -> None:
    pilot = _payload()["artifact"]["finite_section_history_action_pilot"]
    rows = pilot["mesh_rows"]
    assert [row["step_count"] for row in rows] == list(PILOT_STEP_COUNTS)
    finest = pilot["finest_discrete_action_operator"]
    left = np.asarray(
        finest["left_voltage_history_weights"]
        + [finest["left_current_recovery_atom"]],
        dtype=np.longdouble,
    )
    right = np.asarray(
        finest["right_voltage_history_values"]
        + [finest["right_current_recovery_value"]],
        dtype=np.longdouble,
    )
    residual, coordinate = apply_discrete_normalized_deflation(
        right, right, left
    )
    assert abs(coordinate - 1) < np.longdouble("1e-18")
    assert np.max(np.abs(residual)) < np.longdouble("1e-18")
    trial = np.linspace(-1, 1, len(right), dtype=np.longdouble)
    stable, _ = apply_discrete_normalized_deflation(trial, right, left)
    assert abs(left @ stable) < np.longdouble("1e-17")


def test_pilot_mesh_changes_are_not_interval_errors() -> None:
    pilot = _payload()["artifact"]["finite_section_history_action_pilot"]
    assert not pilot["mesh_changes_are_interval_errors"]
    assert not pilot["pilot_promoted_to_history_measure"]
    final = pilot["mesh_rows"][-1]
    assert gmpy2.mpq(final["recovery_atom_weight"]) > gmpy2.mpq("1.37")
    assert gmpy2.mpq(final["history_voltage_total_variation_discrete"]) < (
        gmpy2.mpq("0.024")
    )


def test_stage4b_update_keeps_actual_yqq_and_csuu_open() -> None:
    update = _payload()["artifact"]["stage4b_ingress_update"]
    assert update["qualitative_f_of_q_nonzero_gate_closed"]
    assert update["fourier_pencil_left_row_gate_closed"]
    assert not update["continuous_history_measure_action_gate_closed"]
    assert not update["action_on_actual_y_qq_gate_closed"]
    assert update["stable_output_uu_directed_upper"] is None
    assert not update["structural_obstruction_found"]


def test_claim_ledger_separates_proof_from_pilot() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_note_does_not_promote_the_pilot() -> None:
    text = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    prose = " ".join(text.split())
    assert "These changes are diagnostics, not interval errors" in prose
    assert "is not yet a certified history measure" in text
    assert "it is not silently relabeled" in text


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (("artifact", "claim_status", "adjoint_history_measure_numeric_enclosed"), True),
        (
            (
                "artifact",
                "directed_fourier_grushin_left_row",
                "history_adjoint_measure_identification_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "simple_multiplier_and_pairing_theorem",
                "directed_numeric_rescaling_available",
            ),
            True,
        ),
        (
            (
                "artifact",
                "stage4b_ingress_update",
                "action_on_actual_y_qq_gate_closed",
            ),
            True,
        ),
        (
            (
                "artifact",
                "stage4b_ingress_update",
                "stable_output_uu_directed_upper",
            ),
            "12",
        ),
    ),
)
def test_hostile_promotions_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        validate_stage4c_result(payload, REPOSITORY)
