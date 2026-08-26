from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.directed_interval import DirectedInterval, pi_interval
from canard_control.leaky_floquet_inner_unstable_root import (
    FALSE_FLAGS,
    FOURIER_CUTOFF,
    PINNED_OPENBLAS_NUM_THREADS,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    _coupling_variation,
    _dependency_fingerprint,
    _preconditioned_tail_coupling_variation,
    _prepare_cached,
    _tail_inverse_upper,
    canonical_sha256,
    physical_delay_convolution_oracle_error,
    validate_leaky_inner_unstable_root_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_tracked_inner_root_result_validates(payload):
    validate_leaky_inner_unstable_root_result(payload, REPOSITORY)


def test_claim_boundary_is_local_and_strict(payload):
    certificate = payload["certificate"]
    for name in TRUE_FLAGS:
        assert certificate[name] is True
    for name in FALSE_FLAGS:
        assert certificate[name] is False
    assert certificate["fourier_cutoff"] == FOURIER_CUTOFF
    assert certificate["binary_blas_thread_count"] == int(
        PINNED_OPENBLAS_NUM_THREADS
    )
    assert certificate["finite_block_maximum_delay_output_mode"] == 64
    assert certificate["finite_tail_maximum_delay_output_mode"] == 64
    assert certificate["tail_finite_maximum_delay_output_mode"] == 192
    assert float(certificate["root_disk_real_part_lower"]) > 0
    assert float(certificate["multiplier_modulus_lower"]) > 1
    assert float(certificate["closed_disk_full_grushin_contraction_upper"]) < 1
    assert float(certificate["rouche_margin_lower"]) > 0
    assert float(certificate["center_finite_second_smallest_singular_value_binary64"]) > 0.9
    assert certificate["inner_no_other_right_half_roots_validated"] is False
    assert certificate["inner_total_unstable_multiplier_count_validated"] is False
    assert certificate["common_parameter_box_root_validated"] is False


def test_physical_delay_dual_representation_oracle_rejects_both_mixes():
    assert physical_delay_convolution_oracle_error(
        representation="unshifted_row"
    ) < 5e-15
    assert physical_delay_convolution_oracle_error(
        representation="shifted_column"
    ) < 5e-15
    assert physical_delay_convolution_oracle_error(
        representation="unshifted_column"
    ) > 1e-3
    assert physical_delay_convolution_oracle_error(
        representation="shifted_row"
    ) > 1e-3


def _independent_coupling_variation(
    prepared,
    *,
    maximum_output_mode: int,
    s_modulus_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    """Reassociate the displayed input-frequency majorant independently."""

    base = prepared.base
    radius = prepared.period_radius
    period_lower = base.period.lower - radius
    tau_upper = max(
        base.parameters["tau_0"].upper,
        base.parameters["tau_1"].upper,
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        coefficient_part = (
            (base.period.upper + radius)
            * (
                prepared.current_total_variation
                + prepared.delayed_total_variation
            )
            + radius
            * (
                prepared.current_binary_norm
                + 2 * prepared.delayed_binary_norm
            )
        )
        input_frequency = (
            s_modulus_upper
            + 2
            * pi_interval(PRECISION_BITS).upper
            * maximum_output_mode
        )
        phase_part = (
            base.period.upper
            * 2
            * prepared.delayed_binary_norm
            * tau_upper
            * radius
            * input_frequency
            / (period_lower * base.period.lower)
        )
        return coefficient_part + phase_part


def _relative_mpfr_error(left: gmpy2.mpfr, right: gmpy2.mpfr) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        return abs(left - right) / max(abs(left), abs(right), gmpy2.mpfr(1))


def test_coupling_variation_formula_oracle_uses_physical_output_modes():
    prepared, _ = _prepare_cached(
        str(REPOSITORY), _dependency_fingerprint(REPOSITORY)
    )
    s_upper = DirectedInterval.from_decimal("0.8", PRECISION_BITS).upper
    finite = _coupling_variation(
        prepared,
        maximum_output_mode=64,
        s_modulus_upper=s_upper,
    )
    finite_from_tail = _coupling_variation(
        prepared,
        maximum_output_mode=64,
        s_modulus_upper=s_upper,
    )
    for actual, maximum_output_mode in (
        (finite, 64),
        (finite_from_tail, 64),
    ):
        expected = _independent_coupling_variation(
            prepared,
            maximum_output_mode=maximum_output_mode,
            s_modulus_upper=s_upper,
        )
        assert _relative_mpfr_error(actual, expected) < gmpy2.mpfr("1e-40")
    assert finite == finite_from_tail

    neighborhood = DirectedInterval.from_decimal("0.1", PRECISION_BITS).upper
    fast_inverse, _ = _tail_inverse_upper(
        prepared,
        real_center=0.7,
        imag_center=0.0,
        neighborhood=neighborhood,
    )
    tail_from_finite = _preconditioned_tail_coupling_variation(
        prepared,
        fast_tail_inverse=fast_inverse,
        spectral_neighborhood=neighborhood,
    )
    base = prepared.base
    radius = prepared.period_radius
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        period_lower = base.period.lower - radius
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        common = (
            (base.period.upper + radius)
            * (
                prepared.current_total_variation
                + prepared.delayed_total_variation
            )
            + radius
            * (
                prepared.current_binary_norm
                + 2 * prepared.delayed_binary_norm
            )
        )
        tau_sum = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        )
        expected_tail = fast_inverse * common + (
            prepared.delayed_binary_norm
            * tau_sum
            * radius
            / period_lower
            * (1 + fast_inverse * neighborhood)
        )
    assert _relative_mpfr_error(
        tail_from_finite, expected_tail
    ) < gmpy2.mpfr("1e-40")
    assert tail_from_finite != fast_inverse * finite


def test_nested_radii_ball_is_strict(payload):
    certificate = payload["certificate"]
    assert certificate["source_correction_radius"] == "1e-5"
    assert certificate["nested_correction_radius"] == "1e-12"
    assert float(certificate["nested_radii_contraction_upper"]) < 1
    assert float(certificate["nested_radii_margin_lower"]) > 0


def test_full_replay_and_parent_source_binding(payload):
    # ``test_tracked_inner_root_result_validates`` already performs the full
    # numerical replay.  This test isolates the resulting provenance ledger.
    manifest = payload["manifest"]
    assert set(manifest["source_sha256"]) == set(SOURCE_MANIFEST)
    assert manifest["riesz_parent_result"].endswith(
        "leaky_floquet_riesz_reduction.json"
    )
    assert manifest["inner_orbit_result"] == payload["certificate"][
        "inner_orbit_result"
    ]


def _promote_total_count_and_refresh(value):
    value["certificate"]["inner_total_unstable_multiplier_count_validated"] = True
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"exactly_one_characteristic_value_in_root_disk": False}
        ),
        lambda value: value["certificate"].update(
            {"root_disk_real_part_lower": "-0.1"}
        ),
        lambda value: value["certificate"].update(
            {"closed_disk_full_grushin_contraction_upper": "1.01"}
        ),
        lambda value: value["certificate"].update(
            {"rouche_margin_lower": "-1e-8"}
        ),
        lambda value: value["certificate"].update(
            {"unshifted_column_mutation_separation_binary64": "0"}
        ),
        lambda value: value["certificate"].update(
            {"tail_output_frequency_cancellation_validated": False}
        ),
        lambda value: value["certificate"].update(
            {"finite_tail_maximum_delay_output_mode": 192}
        ),
        lambda value: value["certificate"].update(
            {"binary_blas_thread_count": 1}
        ),
        lambda value: value["manifest"].update(
            {"riesz_parent_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"].update(
            {"inner_orbit_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"].update({"extra": "forbidden"}),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
        _promote_total_count_and_refresh,
    ],
)
def test_hostile_tampering_is_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises(ValueError):
        validate_leaky_inner_unstable_root_result(changed, REPOSITORY)


def test_note_states_the_local_scope_and_phase_rule():
    text = (REPOSITORY / "docs/leaky-floquet-inner-unstable-root.md").read_text()
    normalized = " ".join(text.split())
    assert "unshifted coefficient plus output row phase" in normalized
    assert "shifted coefficient plus input column phase" in normalized
    assert "Both illegal mixtures" in normalized
    assert "OPENBLAS_NUM_THREADS=8" in normalized
    assert "fresh subprocess" in normalized
    assert "exactly one" in normalized
    assert "does not yet prove the total inner unstable index" in normalized
    assert "does not by itself validate any" in normalized
    assert "physical onset all remain" in normalized
