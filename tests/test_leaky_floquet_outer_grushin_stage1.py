from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_floquet_outer_grushin_stage1 import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    canonical_sha256,
    validate_leaky_outer_grushin_stage1_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_stage1_failure_contract_replays(payload):
    validate_leaky_outer_grushin_stage1_result(payload, REPOSITORY)


def test_complete_grushin_inverse_closes_but_scalar_rouche_does_not(payload):
    certificate = payload["certificate"]
    for name in TRUE_FLAGS:
        assert certificate[name] is True
    for name in FALSE_FLAGS:
        assert certificate[name] is False
    assert float(certificate["closed_disk_full_grushin_contraction_upper"]) < 0.487
    assert float(certificate["closed_disk_full_grushin_margin_lower"]) > 0.513
    assert float(certificate["closed_disk_bloch_amplitude_upper"]) > 1
    assert float(certificate["rouche_margin_lower"]) < 0
    assert float(certificate["rouche_deficit_upper"]) > 1.94e-5
    assert float(certificate["maximum_boundary_comparison_error_upper"]) > 26 * float(
        certificate["affine_boundary_modulus_lower"]
    )
    assert float(certificate["parent_punctured_right_half_disk_radius_lower"]) > 0.0028635


def test_neumann_back_substitution_is_the_dominant_failed_term(payload):
    certificate = payload["certificate"]
    total = float(certificate["maximum_boundary_comparison_error_upper"])
    neumann = float(certificate["worst_neumann_remainder_upper"])
    assert neumann / total > 0.995
    assert float(certificate["worst_reference_affine_difference_upper"]) < 1e-10
    assert float(certificate["worst_center_inverse_first_error_upper"]) < 8.2e-8
    assert float(certificate["worst_local_taylor_error_upper"]) < 1.8e-10


def test_outer_support_tail_and_physical_delay_convention_are_fixed(payload):
    certificate = payload["certificate"]
    assert certificate["fourier_cutoff"] == 64
    assert certificate["coefficient_support_half_bandwidth"] == 256
    assert certificate["explicit_coupling_tail_minimum_mode"] == 65
    assert certificate["explicit_coupling_tail_maximum_mode"] == 320
    assert "output row" in certificate["delay_operator_representation"]
    assert certificate["nested_correction_radius"] == "1e-8"
    assert certificate["binary_blas_thread_count"] == 8


def _refresh(value):
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"closed_disk_full_grushin_contraction_upper": "1.01"}
        ),
        lambda value: value["certificate"].update(
            {"closed_disk_bloch_amplitude_upper": "1"}
        ),
        lambda value: value["certificate"].update(
            {"rouche_margin_lower": "1e-9"}
        ),
        lambda value: value["certificate"].update(
            {"scalar_effective_hamiltonian_rouche_count_validated": True}
        ),
        lambda value: value["certificate"].update(
            {"outer_attracting_floquet_index_validated": True}
        ),
        lambda value: value["certificate"].update(
            {"explicit_coupling_tail_maximum_mode": 319}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_mutations_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_leaky_outer_grushin_stage1_result(changed, REPOSITORY)


def test_note_states_failure_and_global_claim_boundary():
    text = (
        REPOSITORY / "docs/leaky-floquet-outer-grushin-stage1.md"
    ).read_text()
    normalized = " ".join(text.split())
    assert "Stage-1 failure contract" in normalized
    assert "does not close" in normalized
    assert "output row" in normalized
    assert "mode 320" in normalized
    assert "outer attracting Floquet index" in normalized
    assert "physical pulse onset" in normalized
