from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "transverse_lin_sweep.py"
)
SPEC = importlib.util.spec_from_file_location("transverse_lin_sweep", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
SWEEP = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SWEEP
SPEC.loader.exec_module(SWEEP)


def test_singular_limit_tangent_is_an_exact_discrete_null_vector() -> None:
    matrix, nodes = SWEEP.assemble_diagnostic_lin_matrix(
        delta=0.0,
        left=-2.5,
        right=2.5,
        intervals=40,
        scaffold=0.0,
    )
    tangent = np.concatenate((-np.ones_like(nodes), nodes))

    assert np.linalg.norm(matrix @ tangent, ord=np.inf) < 1.0e-12


def test_symmetric_weak_only_diagnostic_has_quadratic_tail() -> None:
    case = SWEEP.DiagnosticCase("symmetric", -2.5, 2.5, 0.0)
    deltas = tuple(2.0 ** (-power) for power in range(4, 10))
    result = SWEEP.sweep_case(
        case,
        deltas,
        intervals=80,
        tail_count=4,
    )

    assert 1.85 < result.tail_slope < 2.15


def test_asymmetric_weak_only_diagnostic_has_linear_tail() -> None:
    case = SWEEP.DiagnosticCase("asymmetric", -1.5, 2.5, 0.0)
    deltas = tuple(2.0 ** (-power) for power in range(5, 12))
    result = SWEEP.sweep_case(
        case,
        deltas,
        intervals=80,
        tail_count=4,
    )

    assert 0.9 < result.tail_slope < 1.1


def test_fixed_scaffold_produces_a_nonzero_small_delta_plateau() -> None:
    case = SWEEP.DiagnosticCase("chart_scaffold", -2.5, 2.5, 0.5, "chart")
    deltas = tuple(2.0 ** (-power) for power in range(5, 12))
    result = SWEEP.sweep_case(
        case,
        deltas,
        intervals=80,
        tail_count=4,
    )
    sigma_at_zero = SWEEP.smallest_singular_value(
        delta=0.0,
        left=case.left,
        right=case.right,
        intervals=80,
        scaffold=case.scaffold,
        scaffold_scaling=case.scaffold_scaling,
    )

    assert abs(result.tail_slope) < 0.1
    assert sigma_at_zero > 1.0e-5
    assert abs(result.sigma_min[-1] / sigma_at_zero - 1.0) < 0.05


def test_fixed_physical_scaffold_has_a_discrete_small_delta_plateau() -> None:
    case = SWEEP.DiagnosticCase(
        "physical_scaffold",
        -2.5,
        2.5,
        0.5,
        "physical",
    )
    deltas = tuple(2.0 ** (-power) for power in range(5, 12))
    result = SWEEP.sweep_case(
        case,
        deltas,
        intervals=80,
        tail_count=4,
    )

    # This is a plateau of the chosen Euclidean finite matrix.  Its value is
    # not invariant under grid, interval, norm, or residual-row rescaling.
    assert abs(result.tail_slope) < 0.1
    assert result.sigma_min[-1] > 1.0e-3


def test_physical_scaffold_is_not_evaluated_at_delta_zero() -> None:
    try:
        SWEEP.assemble_diagnostic_lin_matrix(
            delta=0.0,
            left=-2.5,
            right=2.5,
            scaffold=0.5,
            scaffold_scaling="physical",
        )
    except ValueError as error:
        assert "singular at delta=0" in str(error)
    else:
        raise AssertionError("physical scaffold must reject delta=0")
