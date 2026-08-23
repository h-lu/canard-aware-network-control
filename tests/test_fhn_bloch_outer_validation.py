"""Regression tests for the direct full-complex Bloch validator."""

from __future__ import annotations

from dataclasses import replace
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    pi_interval,
)
from canard_control.fhn_bloch_outer_validation import (
    BlochParameterBoxEvidence,
    DirectedBlochCellCertificate,
    DirectedParameterBoxLocalFloquet,
    _assemble_bloch_arc_certificate,
    _binary_inverse_defect_l1_upper,
    _boxed_left_product_l1_upper,
    _complex_column_weights,
    _finite_center_matrix,
    _finite_phase_derivative_matrix,
    _geometric_phase_cells,
    _realify,
)
from canard_control.fhn_periodic_candidate import solve_fhn_periodic_orbit
from canard_control.fhn_periodic_infinite_validation import _build_base_sequences


_REPOSITORY = Path(__file__).resolve().parents[1]
_RESULT = _REPOSITORY / "experiments/results/fhn_bloch_outer_validation.json"
_EXPECTED_RESULT_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)


def _tracked_payload() -> dict:
    return json.loads(_RESULT.read_text(encoding="utf-8"))


def test_complex_realification_accepts_nonconjugate_coordinates() -> None:
    matrix = np.array(
        [[1.0 + 2.0j, -0.5j], [3.0 - 0.25j, -2.0 + 0.75j]],
        dtype=complex,
    )
    vector = np.array([0.3 - 1.7j, -2.1 + 0.4j], dtype=complex)
    real_vector = np.concatenate((vector.real, vector.imag))
    observed = _realify(matrix) @ real_vector
    expected_complex = matrix @ vector
    expected = np.concatenate((expected_complex.real, expected_complex.imag))
    assert np.allclose(observed, expected, rtol=0.0, atol=2e-15)


def test_bordered_invertibility_does_not_promote_unbordered_kernel() -> None:
    # L=0, b=ell=1 is the one-dimensional counterexample that prevents the
    # outer validator from reusing the bordered periodic inverse.
    operator = np.zeros((1, 1))
    bordered = np.array([[0.0, -1.0], [1.0, 0.0]])
    assert np.linalg.matrix_rank(operator) == 0
    assert abs(np.linalg.det(bordered)) == 1.0


def test_negative_phase_uses_conjugation_and_mode_reversal() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    precision = 100
    cutoff = 16
    base = _build_base_sequences(orbit, precision)
    positive = _finite_center_matrix(
        base, cutoff, DirectedInterval.from_decimal("0.731", precision)
    ).midpoint
    negative = _finite_center_matrix(
        base, cutoff, DirectedInterval.from_decimal("-0.731", precision)
    ).midpoint
    span = 2 * cutoff + 1
    reversal = np.zeros((2 * span, 2 * span), dtype=float)
    for component in (0, 1):
        for mode in range(-cutoff, cutoff + 1):
            row = component * span + (-mode) + cutoff
            column = component * span + mode + cutoff
            reversal[row, column] = 1.0
    rng = np.random.default_rng(1024)
    vector = rng.normal(size=2 * span) + 1.0j * rng.normal(size=2 * span)
    observed = negative @ (reversal @ np.conjugate(vector))
    expected = reversal @ np.conjugate(positive @ vector)
    assert np.max(np.abs(observed - expected)) < 2e-11


def test_geometric_cells_are_exactly_connected_and_cover_directed_pi() -> None:
    precision = 160
    lower = "0.001103718017895787146929057443069462647201200220431078"
    upper = str(
        # A long finite decimal deliberately above the irrational endpoint.
        DirectedInterval.from_bounds(
            pi_interval(precision).upper,
            pi_interval(precision).upper,
            precision,
        ).decimal_bounds(60)[1]
    )
    cells = _geometric_phase_cells(
        lower, upper, "0.006", maximum_cells=1000
    )
    assert 600 < len(cells) < 700
    assert gmpy2.mpq(cells[0][0]) <= gmpy2.mpq(lower)
    for left, center, right, half in cells:
        assert gmpy2.mpq(center) - gmpy2.mpq(half) == gmpy2.mpq(left)
        assert gmpy2.mpq(center) + gmpy2.mpq(half) == gmpy2.mpq(right)
    for previous, following in zip(cells, cells[1:]):
        assert gmpy2.mpq(previous[2]) == gmpy2.mpq(following[0])
    assert DirectedInterval.from_decimal(cells[-1][2], precision).upper >= (
        pi_interval(precision).upper
    )


def test_geometric_grid_refuses_an_unbounded_cell_request() -> None:
    try:
        _geometric_phase_cells(
            "0.001", "3.2", "0.000001", maximum_cells=10
        )
    except RuntimeError as error:
        assert "maximum_cells" in str(error)
    else:
        raise AssertionError("an undersized maximum_cells guard was ignored")


def test_phase_derivative_matches_the_full_complex_symbol() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    precision = 120
    cutoff = 16
    base = _build_base_sequences(orbit, precision)
    center = Decimal("0.731")
    step = Decimal("1e-6")
    phase = DirectedInterval.from_decimal(str(center), precision)
    plus = DirectedInterval.from_decimal(str(center + step), precision)
    minus = DirectedInterval.from_decimal(str(center - step), precision)
    derivative = _finite_phase_derivative_matrix(
        base, cutoff, phase
    ).midpoint
    difference = (
        _finite_center_matrix(base, cutoff, plus).midpoint
        - _finite_center_matrix(base, cutoff, minus).midpoint
    ) / (2.0 * float(step))
    assert np.max(np.abs(derivative - difference)) < 2e-7


def test_binary_products_are_covered_by_directed_interval_remainders() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    precision = 100
    cutoff = 16
    base = _build_base_sequences(orbit, precision)
    phase = DirectedInterval.from_decimal("0.731", precision)
    operator = _finite_center_matrix(base, cutoff, phase)
    inverse = np.linalg.inv(operator.midpoint)
    weights = _complex_column_weights(inverse, precision)
    defect_upper = _binary_inverse_defect_l1_upper(
        inverse, operator, precision, weights
    )
    midpoint_defect = np.linalg.norm(
        np.eye(2 * len(inverse)) - _realify(inverse) @ _realify(operator.midpoint),
        1,
    )
    assert float(defect_upper) >= midpoint_defect

    derivative = _finite_phase_derivative_matrix(base, cutoff, phase)
    product_upper = _boxed_left_product_l1_upper(
        inverse, derivative, precision, weights
    )
    midpoint_product = np.linalg.norm(
        _realify(inverse) @ _realify(derivative.midpoint), 1
    )
    assert float(product_upper) >= midpoint_product


def test_tracked_outer_arc_is_exactly_replayable_and_source_bound() -> None:
    raw = _RESULT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == _EXPECTED_RESULT_SHA256
    payload = json.loads(raw)
    provenance = payload["provenance"]
    generator = _REPOSITORY / provenance["generator"]
    proof_source = _REPOSITORY / provenance["proof_source"]
    assert hashlib.sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    assert hashlib.sha256(proof_source.read_bytes()).hexdigest() == provenance[
        "proof_source_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert hashlib.sha256((_REPOSITORY / relative).read_bytes()).hexdigest() == digest
    blas = provenance["blas_thread_control"]
    assert blas["controlled"] and blas["after"] == 1
    assert len(blas["library_sha256"]) == 64

    local = payload["local_transfer"]
    arc = payload["outer_arc"]
    cells = arc["cells"]
    assert len(cells) == arc["cell_count"] == 319
    assert Decimal(cells[0]["phase_lower"]) == Decimal(
        local["local_phase_radius_lower"]
    )
    for previous, following in zip(cells, cells[1:]):
        assert previous["phase_upper"] == following["phase_lower"]
    precision = arc["precision_bits"]
    assert DirectedInterval.from_decimal(
        cells[-1]["phase_upper"], precision
    ).upper >= pi_interval(precision).upper

    with localcontext() as context:
        context.prec = 160
        contractions = []
        margins = []
        for cell in cells:
            finite_column = Decimal(cell["finite_to_finite_upper"]) + Decimal(
                cell["tail_from_finite_upper"]
            )
            tail_column = Decimal(cell["finite_from_tail_upper"]) + Decimal(
                cell["tail_to_tail_upper"]
            )
            contraction = max(finite_column, tail_column)
            margin = Decimal(1) - contraction
            assert Decimal(cell["finite_input_column_sum_upper"]) == finite_column
            assert Decimal(cell["tail_input_column_sum_upper"]) == tail_column
            assert Decimal(cell["contraction_upper"]) == contraction
            assert Decimal(cell["contraction_margin_lower"]) == margin
            assert contraction < 1 and margin > 0
            assert cell["cell_validated"] and cell["failure_reason"] is None
            assert cell["direct_unbordered_operator"]
            assert cell["arbitrary_complex_modes"]
            assert cell["moving_delay_output_rotation_validated"]
            assert cell["exact_parameter_box_orbit_ball_included"]
            contractions.append(contraction)
            margins.append(margin)
        assert Decimal(arc["maximum_contraction_upper"]) == max(contractions)
        assert Decimal(arc["minimum_contraction_margin_lower"]) == min(margins)
        worst = max(range(len(cells)), key=contractions.__getitem__)
        assert worst == 317

    assert cells[317]["complex_finite_dimension"] == 258
    assert cells[317]["realified_finite_dimension"] == 516
    assert Decimal(cells[317]["finite_from_tail_upper"]) > 0
    assert Decimal(cells[317]["tail_from_finite_upper"]) > 0
    assert local["regularity_bridge_to_history_monodromy"]
    assert payload["scope"]["uniform_history_fourier_regularity_bridge"]
    for field in (
        "uniform_simple_unit_multiplier",
        "uniform_local_punctured_arc_exclusion",
        "uniform_positive_outer_arc_exclusion",
        "all_nontrivial_unit_multipliers_excluded",
        "synchronous_orbital_hyperbolicity",
    ):
        assert payload["scope"][field]
    assert not payload["scope"]["attraction"]
    assert not payload["scope"]["full_network_transverse_stability"]
    assert arc["failure_reason"] is None


def test_tail_gap_uses_the_exact_negative_tail_extremizer() -> None:
    payload = _tracked_payload()
    cell = payload["outer_arc"]["cells"][317]
    precision = cell["precision_bits"]
    cutoff = cell["cutoff"]
    phase = DirectedInterval.from_decimal(cell["phase_center"], precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        expected = pi_interval(precision).lower * (2 * (cutoff + 1)) - phase.upper
    assert decimal_lower(expected) == cell["tail_diagonal_gap_lower"]

    center = gmpy2.mpfr(cell["phase_center"], precision)
    pi = gmpy2.const_pi(precision)
    tail_modes = tuple(range(-cutoff - 5, -cutoff)) + tuple(
        range(cutoff + 1, cutoff + 6)
    )
    extremizer = min(tail_modes, key=lambda mode: abs(2 * pi * mode + center))
    assert extremizer == -(cutoff + 1)


def test_arc_assembly_refuses_a_manufactured_phase_gap() -> None:
    payload = _tracked_payload()
    local = DirectedParameterBoxLocalFloquet(**payload["local_transfer"])
    evidence = BlochParameterBoxEvidence(**payload["source_evidence"])
    cells = tuple(
        DirectedBlochCellCertificate(**cell)
        for cell in payload["outer_arc"]["cells"]
    )
    declarations = tuple(
        (
            cell.phase_lower,
            cell.phase_center,
            cell.phase_upper,
            cell.phase_half_width,
        )
        for cell in cells
    )
    forged = list(cells)
    forged[1] = replace(forged[1], phase_lower="0.00114")
    certificate = _assemble_bloch_arc_certificate(
        local,
        evidence,
        tuple(forged),
        declarations,
        cutoff=payload["outer_arc"]["cutoff"],
        precision=payload["outer_arc"]["precision_bits"],
        relative_half_width=payload["outer_arc"]["relative_half_width_seed"],
    )
    assert not certificate.connected_positive_arc_cover
    assert not certificate.every_cell_validated
    assert not certificate.all_nontrivial_unit_multipliers_excluded
    assert not certificate.synchronous_orbital_hyperbolicity_validated
    assert certificate.failure_reason is not None
