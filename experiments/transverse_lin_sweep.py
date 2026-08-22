#!/usr/bin/env python3
"""Finite-interval transverse Lin diagnostic near the right fold.

This script is deliberately a *diagnostic*, not an RFDE Fredholm theorem or a
certified bound for ``G_perp(epsilon)``.  It discretizes one modal inner
equation,

    U' = a_delta(s) U + V
         + delta K [U - lambda U(s - theta)] - D U,
    V' = -U - delta b V,

where

    a_delta(s) = s - delta (1 + 2 b) s**2 / 8.

Here ``lambda`` is a transverse block eigenvalue.  The scaffold has three
declared scalings:

``none``
    no instantaneous transverse scaffold;
``chart``
    a coefficient ``D`` fixed in the blown-up equation, corresponding to a
    physical zero-row-sum coupling of strength ``sqrt(epsilon) D``;
``physical``
    a physical coefficient ``D`` fixed before blow-up, which appears as
    ``D / delta`` in the chart equation.

Thus the chart and physical scaffold cases answer different modelling
questions and are never silently identified.  The discretization uses
implicit midpoint equations and the two fixed singular-limit endpoint
conditions

    V(s_minus) + s_minus U(s_minus) = 0,
    V(s_plus)  + s_plus  U(s_plus)  = 0.

For delayed arguments before ``s_minus``, the incoming history is closed by
constant continuation from ``U(s_minus)``.  That closure, the fixed endpoint
lines, the finite interval, and the reduction to one scalar mode are modelling
choices made only for this sweep.  In particular, this script does not:

* construct the RFDE solution manifold or its adjoint bilinear form;
* derive Lin boundary bundles from attracting and repelling slow manifolds;
* impose the phase condition of the eventual network Lin problem;
* control discretization error or prove an inverse estimate uniform in
  ``epsilon`` or network size.

The useful output is therefore the observed *finite-matrix* scaling of its
smallest Euclidean singular value.  Its numerical plateau depends on the
interval, grid, unknown norm, and residual-row scaling.  It is evidence for
choosing and falsifying a Lin-BVP formulation, not evidence that the same
exponent or constant holds for the final RFDE.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable, Literal

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]
ScaffoldScaling = Literal["none", "chart", "physical"]


@dataclass(frozen=True)
class DiagnosticCase:
    """One finite-interval/scaffold choice in the diagnostic sweep."""

    name: str
    left: float
    right: float
    scaffold: float
    scaffold_scaling: ScaffoldScaling = "chart"


@dataclass(frozen=True)
class SweepResult:
    """Machine-readable result for one diagnostic case."""

    case: DiagnosticCase
    deltas: tuple[float, ...]
    sigma_min: tuple[float, ...]
    tail_slope: float

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["interpretation"] = (
            "finite-interval midpoint diagnostic; not an RFDE inverse bound"
        )
        return result


def default_cases() -> tuple[DiagnosticCase, ...]:
    """Return cases exposing endpoint symmetry and scaffold effects."""

    return (
        DiagnosticCase("symmetric_weak_only", -2.5, 2.5, 0.0, "none"),
        DiagnosticCase("asymmetric_weak_only", -1.5, 2.5, 0.0, "none"),
        DiagnosticCase("symmetric_chart_scaffold", -2.5, 2.5, 0.5, "chart"),
        DiagnosticCase("asymmetric_chart_scaffold", -1.5, 2.5, 0.5, "chart"),
        DiagnosticCase(
            "symmetric_physical_scaffold",
            -2.5,
            2.5,
            0.5,
            "physical",
        ),
    )


def _delay_interpolation_matrix(
    nodes: FloatArray,
    midpoints: FloatArray,
    theta: float,
) -> FloatArray:
    """Map nodal U values to U(midpoint - theta).

    Values before the left endpoint use constant incoming-history
    continuation.  This is the principal non-RFDE closure in the diagnostic.
    """

    if theta < 0.0:
        raise ValueError("theta must be nonnegative")

    intervals = midpoints.size
    node_count = nodes.size
    step = nodes[1] - nodes[0]
    left = nodes[0]
    interpolation = np.zeros((intervals, node_count), dtype=float)

    for row, delayed_point in enumerate(midpoints - theta):
        if delayed_point <= left:
            interpolation[row, 0] = 1.0
            continue

        column = min(
            int(np.floor((delayed_point - left) / step)),
            node_count - 2,
        )
        fraction = (delayed_point - nodes[column]) / step
        interpolation[row, column] = 1.0 - fraction
        interpolation[row, column + 1] = fraction

    return interpolation


def assemble_diagnostic_lin_matrix(
    *,
    delta: float,
    left: float,
    right: float,
    intervals: int = 120,
    weak_k: float = 1.0,
    mode_lambda: float = 0.4,
    theta: float = 0.5,
    slow_b: float = 0.0,
    scaffold: float = 0.0,
    scaffold_scaling: ScaffoldScaling = "chart",
) -> tuple[FloatArray, FloatArray]:
    """Assemble the square implicit-midpoint diagnostic matrix.

    Unknowns are ordered as all nodal ``U`` values followed by all nodal
    ``V`` values.  Evolution residuals are written in integrated midpoint
    form, followed by one scalar condition at each endpoint.
    """

    if delta < 0.0:
        raise ValueError("delta must be nonnegative")
    if right <= left:
        raise ValueError("right must be greater than left")
    if intervals < 4:
        raise ValueError("at least four intervals are required")
    if scaffold < 0.0:
        raise ValueError("scaffold must be nonnegative")
    if scaffold_scaling not in {"none", "chart", "physical"}:
        raise ValueError("scaffold_scaling must be none, chart, or physical")
    if scaffold_scaling == "none" and scaffold != 0.0:
        raise ValueError("a none-scaled scaffold must have zero strength")
    if scaffold_scaling == "physical" and delta == 0.0:
        raise ValueError(
            "the physical scaffold chart coefficient is singular at delta=0"
        )

    if scaffold_scaling == "none":
        chart_scaffold = 0.0
    elif scaffold_scaling == "chart":
        chart_scaffold = scaffold
    else:
        chart_scaffold = scaffold / delta

    nodes = np.linspace(left, right, intervals + 1, dtype=float)
    step = nodes[1] - nodes[0]
    midpoints = 0.5 * (nodes[:-1] + nodes[1:])
    delayed = _delay_interpolation_matrix(nodes, midpoints, theta)

    node_count = nodes.size
    matrix = np.zeros((2 * node_count, 2 * node_count), dtype=float)
    row = 0

    for interval, midpoint in enumerate(midpoints):
        average = np.zeros(node_count, dtype=float)
        average[interval : interval + 2] = 0.5
        difference = np.zeros(node_count, dtype=float)
        difference[interval] = -1.0
        difference[interval + 1] = 1.0

        fold_coefficient = (
            midpoint
            - delta * (1.0 + 2.0 * slow_b) * midpoint**2 / 8.0
        )

        # U_{j+1} - U_j - h * RHS_U(midpoint) = 0.
        matrix[row, :node_count] = (
            difference
            - step
            * (fold_coefficient + delta * weak_k - chart_scaffold)
            * average
            + step * delta * weak_k * mode_lambda * delayed[interval]
        )
        matrix[row, node_count:] = -step * average
        row += 1

        # V_{j+1} - V_j + h * (U_mid + delta b V_mid) = 0.
        matrix[row, :node_count] = step * average
        matrix[row, node_count:] = difference + step * delta * slow_b * average
        row += 1

    # Fixed singular-limit endpoint lines.  They make phi_0=(-1,s) an exact
    # null vector when delta=D=0, but they are not transported Lin bundles.
    matrix[row, 0] = left
    matrix[row, node_count] = 1.0
    row += 1
    matrix[row, node_count - 1] = right
    matrix[row, 2 * node_count - 1] = 1.0
    row += 1

    if row != 2 * node_count:  # defensive check against assembly changes
        raise RuntimeError("diagnostic matrix assembly produced wrong row count")

    return matrix, nodes


def smallest_singular_value(**matrix_parameters: float | int) -> float:
    """Return the Euclidean smallest singular value of the diagnostic matrix."""

    matrix, _ = assemble_diagnostic_lin_matrix(**matrix_parameters)
    return float(np.linalg.svd(matrix, compute_uv=False)[-1])


def estimate_loglog_slope(
    deltas: Iterable[float],
    sigma_min: Iterable[float],
    *,
    tail_count: int = 5,
) -> float:
    """Fit log(sigma_min) against log(delta) on the smallest deltas."""

    delta_array = np.asarray(tuple(deltas), dtype=float)
    sigma_array = np.asarray(tuple(sigma_min), dtype=float)
    if delta_array.shape != sigma_array.shape:
        raise ValueError("deltas and sigma_min must have the same shape")
    if delta_array.ndim != 1 or delta_array.size < 2:
        raise ValueError("at least two one-dimensional samples are required")
    if np.any(delta_array <= 0.0) or np.any(sigma_array <= 0.0):
        raise ValueError("log-log samples must be strictly positive")
    if not 2 <= tail_count <= delta_array.size:
        raise ValueError("tail_count must lie between 2 and the sample count")

    order = np.argsort(delta_array)
    chosen = order[:tail_count]
    slope, _ = np.polyfit(
        np.log(delta_array[chosen]),
        np.log(sigma_array[chosen]),
        deg=1,
    )
    return float(slope)


def sweep_case(
    case: DiagnosticCase,
    deltas: Iterable[float],
    *,
    intervals: int = 120,
    weak_k: float = 1.0,
    mode_lambda: float = 0.4,
    theta: float = 0.5,
    slow_b: float = 0.0,
    tail_count: int = 5,
) -> SweepResult:
    """Run one diagnostic case and fit its small-delta exponent."""

    delta_tuple = tuple(float(value) for value in deltas)
    singular_values = tuple(
        smallest_singular_value(
            delta=delta,
            left=case.left,
            right=case.right,
            intervals=intervals,
            weak_k=weak_k,
            mode_lambda=mode_lambda,
            theta=theta,
            slow_b=slow_b,
            scaffold=case.scaffold,
            scaffold_scaling=case.scaffold_scaling,
        )
        for delta in delta_tuple
    )
    slope = estimate_loglog_slope(
        delta_tuple,
        singular_values,
        tail_count=tail_count,
    )
    return SweepResult(case, delta_tuple, singular_values, slope)


def run_default_sweep(
    *,
    intervals: int = 120,
    first_power: int = 3,
    last_power: int = 12,
    tail_count: int = 5,
) -> tuple[SweepResult, ...]:
    """Run the five default section/scaffold comparisons."""

    if last_power < first_power:
        raise ValueError("last_power must be at least first_power")
    deltas = tuple(2.0 ** (-power) for power in range(first_power, last_power + 1))
    return tuple(
        sweep_case(
            case,
            deltas,
            intervals=intervals,
            tail_count=tail_count,
        )
        for case in default_cases()
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intervals", type=int, default=120)
    parser.add_argument("--first-power", type=int, default=3)
    parser.add_argument("--last-power", type=int, default=12)
    parser.add_argument("--tail-count", type=int, default=5)
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit JSON rather than a compact text table",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    results = run_default_sweep(
        intervals=args.intervals,
        first_power=args.first_power,
        last_power=args.last_power,
        tail_count=args.tail_count,
    )
    if args.json:
        print(json.dumps([result.to_dict() for result in results], indent=2))
        return

    print("FINITE-INTERVAL DIAGNOSTIC ONLY -- NOT AN RFDE INVERSE BOUND")
    print("case                         tail slope    final sigma_min")
    for result in results:
        print(
            f"{result.case.name:28s} "
            f"{result.tail_slope:10.4f}    "
            f"{result.sigma_min[-1]:.8e}"
        )


if __name__ == "__main__":
    main()
