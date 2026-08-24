"""A theorem-native univalence gate for the target causal chart.

This module replaces the sampled-boundary route by a lower-dimensional
P-matrix route.  On the physical strip the fixed output frame

    L_P = ((-7, 2), (3, 1))

turns three scalar inequalities into the hypotheses of the Gale--Nikaido
global-univalence theorem.  On the prepared-history strip a different fixed
frame gives an analytic P-matrix estimate.  A scalar X-separation then glues
the two injective pieces.

The elementary history estimate retained below is exact only for the legacy
first-order preparation and is not applied to the combined chart.  The C4
preparation seam and its incoming label derivative are obtained from exact
frozen-anchor endpoint polynomials.  All C4-history and physical inequalities
are then sampled from a binary64 method-of-steps solution and its *actual
variational DDE*, rather than transverse finite differences.  They are
feasibility diagnostics, not interval bounds.  The module also supplies a
strict interval-cell acceptance schema for a future outward-rounded
Taylor-model computation; the committed result contains no accepted interval
cells and proves no target embedding.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp

from canard_control.fixed_epsilon_target_c4_preparation_seam import (
    PATCH_WIDTH,
    c4_prepared_history_jet,
    c4_prepared_history_state,
    c4_prepared_history_transverse_derivative,
)
from canard_control.fixed_epsilon_target_causal_tube_candidate import (
    SOLVER_ATOL,
    SOLVER_RTOL,
    TargetTubeConfiguration,
    TargetTubeNumericalSolution,
    _physical_fields,
)


MODEL_ID = "fixed-epsilon-target-chart-p-matrix-univalence-gate"
AUDIT_ID = "fixed-epsilon-target-chart-p-matrix-univalence-gate-v1"

PHYSICAL_TIME_FRAME = ((-7, 2), (3, 1))
PHYSICAL_FRAME_DETERMINANT = -13
HISTORY_FRAME = ((-1, 0), (0, 1))
HISTORY_FRAME_DETERMINANT = -1

PHYSICAL_TIME_SAMPLE_COUNT = 1201
C4_HISTORY_TIME_SAMPLE_COUNT = 1201
CROSS_EARLY_TIME_SAMPLE_COUNT = 401
CROSS_LATE_TIME_SAMPLE_COUNT = 1001
CROSS_SPLIT_TIME = -2.0
VARIATIONAL_MAXIMUM_STEPS = (0.02, 0.01)

PARENT_RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_causal_tube_candidate.json"
)
PARENT_RESULT_SHA256 = (
    "fb61c0576afb9a401f16947d47917fa03b4461a8889fbb04f3d450411c448ffd"
)
C4_SEAM_RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_c4_preparation_seam.json"
)
C4_SEAM_RESULT_SHA256 = (
    "5cc678e56a2d1c203d174a27617c28963082ba8e7cf9c6dc48f3f6de8bff840b"
)
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_chart_univalence_gate.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_target_chart_univalence_gate.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_chart_univalence_gate.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-chart-univalence-gate.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_chart_univalence_gate.py"
)
MANIFEST_ARITHMETIC = (
    "exact frozen-anchor C4 preparation and analytic lambda-history "
    "derivative plus conditional univalence algebra; binary64 SciPy DOP853 "
    "C4-state and true variational DDE sampling; strict future interval-cell "
    "schema, but no outward-rounded history or physical cells, Taylor-model "
    "flow proof, global target embedding, or target graph"
)


def _finite(value: object, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _format(value: float) -> str:
    return format(float(value), ".17g")


def _decimal(value: object, name: str) -> Decimal:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise ValueError(f"{name} must be an exact decimal string or integer")
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True)
class ExactHistoryGate:
    """Exact constants for the legacy first-order-history P-matrix proof."""

    transverse_radius_upper: str
    smooth_step_derivative_upper: str
    preparation_bump_derivative_absolute_upper: str
    negative_x_time_derivative_lower: str
    negative_y_time_derivative_lower: str
    history_frame: tuple[tuple[int, int], tuple[int, int]]
    history_frame_determinant: int
    first_principal_minor_lower: str
    second_principal_minor: str
    determinant_lower: str


def exact_history_gate() -> ExactHistoryGate:
    """Return the exact rational estimate for the legacy first-order strip.

    For the flat step ``S``, direct differentiation gives

        S' = L/(4 cosh(h/2)^2),
        h=1/z-1/(1-z),  L=z^-2+(1-z)^-2.

    Writing ``s=sqrt(4+h^2)`` gives ``L=h^2+4+2s``.  Concavity of
    ``sqrt`` yields ``L<=8+3h^2/2``, whereas
    ``4 cosh(h/2)^2=2(1+cosh h)>=4+h^2``.  In the equivalent comparison
    ``L<=4(1+cosh h)``, this proves ``0<=S'<=2``.  Hence for
    ``b(r)=r S(r+1)``, ``|b'|<=3``.

    With ``|lambda|<=1/20``, ``q<=0`` and ``rho*nu<=1/8``, one has
    ``-X_t>=7/20`` and ``Y_t<=-11/8`` on ``t<=-3``.  Since ``b<=0``, the
    two-dimensional P-matrix determinant in the frame ``(-X,Y)`` is at
    least ``7/20``.  The degree-nine C4 correction has different derivatives,
    so this exact estimate is retained only as a benchmark and is not applied
    to the combined C4 chart.
    """

    radius = Fraction(1, 20)
    step_derivative = Fraction(2)
    bump_derivative = Fraction(1) + step_derivative
    negative_x_time = Fraction(1, 2) - radius * bump_derivative
    negative_y_time = Fraction(3, 2) - Fraction(1, 8)
    if negative_x_time != Fraction(7, 20):
        raise AssertionError("history X derivative arithmetic changed")
    if negative_y_time != Fraction(11, 8):
        raise AssertionError("history Y derivative arithmetic changed")
    return ExactHistoryGate(
        transverse_radius_upper="1/20",
        smooth_step_derivative_upper="2",
        preparation_bump_derivative_absolute_upper="3",
        negative_x_time_derivative_lower="7/20",
        negative_y_time_derivative_lower="11/8",
        history_frame=HISTORY_FRAME,
        history_frame_determinant=HISTORY_FRAME_DETERMINANT,
        first_principal_minor_lower="7/20",
        second_principal_minor="1",
        determinant_lower="7/20",
    )


@dataclass(frozen=True)
class PMatrixIntervalCell:
    """One future outward-rounded physical P-matrix cell.

    The three margin fields must be certified lower endpoints for
    ``(-7,2).u_t``, ``(3,1).u_lambda``, and
    ``det D(L_P Psi)=-13 det D(Psi)``, respectively.
    """

    time_left: str
    time_right: str
    lambda_left: str
    lambda_right: str
    time_minor_lower: str
    lambda_minor_lower: str
    oriented_determinant_lower: str


def validate_p_matrix_interval_cover(
    cells: Sequence[PMatrixIntervalCell],
    *,
    time_nodes: Sequence[str | int],
    lambda_nodes: Sequence[str | int],
) -> tuple[Decimal, Decimal, Decimal]:
    """Validate a rectangular strict P-matrix cell cover.

    This checks exact decimal coverage and strict stored margins.  It does
    not certify that an external solver produced valid enclosures; that
    provenance and outward-rounding check remains part of the future
    Taylor-model backend.
    """

    times = tuple(_decimal(value, "time node") for value in time_nodes)
    labels = tuple(_decimal(value, "lambda node") for value in lambda_nodes)
    if len(times) < 2 or len(labels) < 2:
        raise ValueError("each interval grid needs at least two nodes")
    if any(left >= right for left, right in zip(times[:-1], times[1:])):
        raise ValueError("time nodes must be strictly increasing")
    if any(left >= right for left, right in zip(labels[:-1], labels[1:])):
        raise ValueError("lambda nodes must be strictly increasing")

    expected = {
        (times[i], times[i + 1], labels[j], labels[j + 1])
        for i in range(len(times) - 1)
        for j in range(len(labels) - 1)
    }
    actual: dict[tuple[Decimal, Decimal, Decimal, Decimal], tuple[Decimal, ...]] = {}
    for cell in cells:
        if not isinstance(cell, PMatrixIntervalCell):
            raise ValueError("every P-matrix cell must have the frozen schema")
        rectangle = (
            _decimal(cell.time_left, "cell time_left"),
            _decimal(cell.time_right, "cell time_right"),
            _decimal(cell.lambda_left, "cell lambda_left"),
            _decimal(cell.lambda_right, "cell lambda_right"),
        )
        margins = (
            _decimal(cell.time_minor_lower, "time minor"),
            _decimal(cell.lambda_minor_lower, "lambda minor"),
            _decimal(cell.oriented_determinant_lower, "oriented determinant"),
        )
        if rectangle in actual:
            raise ValueError("the interval cover contains a duplicate cell")
        if any(margin <= 0 for margin in margins):
            raise ValueError("every P-matrix interval margin must be strict")
        actual[rectangle] = margins
    if set(actual) != expected:
        raise ValueError("P-matrix interval cells do not cover the exact grid")
    all_margins = tuple(actual.values())
    return tuple(min(row[index] for row in all_margins) for index in range(3))  # type: ignore[return-value]


class C4TargetTubeNumericalSolution(TargetTubeNumericalSolution):
    """Target-tube solution whose entire incoming branch is the C4 seam."""

    def states(self, time: float) -> NDArray[np.float64]:
        time_value = _finite(time, "time")
        config = self.configuration
        tolerance = 2.0e-11 * max(1.0, abs(time_value))
        if time_value <= config.incoming_time:
            return np.asarray(
                [
                    c4_prepared_history_state(time_value, value, config)
                    for value in self.transverse_values
                ],
                dtype=float,
            )
        for left, right, interpolant in reversed(self.segments):
            if left - tolerance <= time_value <= right + tolerance:
                clipped = min(max(time_value, left), right)
                return np.asarray(interpolant(clipped), dtype=float).reshape(
                    len(self.transverse_values), 2
                )
        if time_value <= config.incoming_time + tolerance:
            return np.asarray(
                [
                    c4_prepared_history_state(
                        config.incoming_time, value, config
                    )
                    for value in self.transverse_values
                ],
                dtype=float,
            )
        raise ValueError("time lies outside the computed C4 causal tube")

    def fields(self, time: float) -> NDArray[np.float64]:
        time_value = _finite(time, "time")
        config = self.configuration
        if time_value < config.incoming_time:
            return np.asarray(
                [
                    c4_prepared_history_jet(time_value, value, 1, config)
                    for value in self.transverse_values
                ],
                dtype=float,
            )
        current, delayed_4, delayed_5, delayed_theta = self.slot_states(
            time_value
        )
        return _physical_fields(
            current,
            delayed_4,
            delayed_5,
            delayed_theta,
            config,
        )


def solve_target_c4_causal_tube(
    maximum_step: float = VARIATIONAL_MAXIMUM_STEPS[-1],
    configuration: TargetTubeConfiguration | None = None,
) -> C4TargetTubeNumericalSolution:
    """Integrate the target family from the exact C4 prepared history."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    step = _finite(maximum_step, "maximum_step")
    if step <= 0.0 or step > 4.0:
        raise ValueError("maximum_step must lie in (0,4]")
    transverse_values = np.linspace(
        -config.transverse_radius,
        config.transverse_radius,
        config.transverse_sample_count,
        dtype=float,
    )
    count = len(transverse_values)
    segments: list[tuple[float, float, Any]] = []

    def prepared_states(time: float) -> NDArray[np.float64]:
        return np.asarray(
            [
                c4_prepared_history_state(time, value, config)
                for value in transverse_values
            ],
            dtype=float,
        )

    def known_states(time: float) -> NDArray[np.float64]:
        tolerance = 2.0e-11 * max(1.0, abs(time))
        if time <= config.incoming_time:
            return prepared_states(time)
        for left, right, interpolant in reversed(segments):
            if left - tolerance <= time <= right + tolerance:
                clipped = min(max(time, left), right)
                return np.asarray(interpolant(clipped), dtype=float).reshape(
                    count, 2
                )
        if time <= config.incoming_time + tolerance:
            return prepared_states(config.incoming_time)
        raise RuntimeError("C4 method of steps queried unfinished history")

    def right_hand_side(
        time: float, flattened_state: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        current = np.asarray(flattened_state, dtype=float).reshape(count, 2)
        return _physical_fields(
            current,
            known_states(time - 4.0),
            known_states(time - 5.0),
            known_states(time - config.theta),
            config,
        ).ravel()

    left = config.incoming_time
    state = prepared_states(left).ravel()
    function_evaluations = 0
    while left < config.outgoing_time - 1.0e-14:
        right = min(left + 4.0, config.outgoing_time)
        integration = solve_ivp(
            right_hand_side,
            (left, right),
            state,
            method="DOP853",
            rtol=SOLVER_RTOL,
            atol=SOLVER_ATOL,
            max_step=step,
            dense_output=True,
        )
        if not integration.success or integration.sol is None:
            raise RuntimeError(
                f"target C4 tube integration failed: {integration.message}"
            )
        segments.append((left, right, integration.sol))
        state = np.asarray(integration.y[:, -1], dtype=float)
        function_evaluations += int(integration.nfev)
        left = right
    return C4TargetTubeNumericalSolution(
        configuration=config,
        transverse_values=transverse_values,
        segments=segments,
        function_evaluations=function_evaluations,
        maximum_step=step,
    )


@dataclass
class TargetVariationalSolution:
    """Dense binary64 solution of the lambda-variational DDE."""

    base: C4TargetTubeNumericalSolution
    segments: list[tuple[float, float, Any]]
    function_evaluations: int
    maximum_step: float

    def variations(self, time: float) -> NDArray[np.float64]:
        value = _finite(time, "time")
        config = self.base.configuration
        if value <= config.incoming_time:
            return np.asarray(
                [
                    c4_prepared_history_transverse_derivative(
                        value, label, config
                    )
                    for label in self.base.transverse_values
                ],
                dtype=float,
            )
        tolerance = 2.0e-11 * max(1.0, abs(value))
        for left, right, interpolant in reversed(self.segments):
            if left - tolerance <= value <= right + tolerance:
                clipped = min(max(value, left), right)
                return np.asarray(interpolant(clipped), dtype=float).reshape(
                    len(self.base.transverse_values), 2
                )
        if value <= config.incoming_time + tolerance:
            return np.asarray(
                [
                    c4_prepared_history_transverse_derivative(
                        config.incoming_time, label, config
                    )
                    for label in self.base.transverse_values
                ],
                dtype=float,
            )
        raise ValueError("time lies outside the variational solution")


def _linearized_physical_fields(
    current_variation: NDArray[np.float64],
    delayed_4_variation: NDArray[np.float64],
    delayed_5_variation: NDArray[np.float64],
    delayed_theta_variation: NDArray[np.float64],
    current_state: NDArray[np.float64],
    delayed_4_state: NDArray[np.float64],
    delayed_5_state: NDArray[np.float64],
    delayed_theta_state: NDArray[np.float64],
    configuration: TargetTubeConfiguration,
) -> NDArray[np.float64]:
    """Evaluate the exact lambda-variational slot algebra in binary64."""

    rho = configuration.rho
    eta = configuration.eta
    x = current_state[:, 0]
    x4 = delayed_4_state[:, 0]
    x5 = delayed_5_state[:, 0]
    xtheta = delayed_theta_state[:, 0]
    local_x = (
        -2.0 * x
        + rho * (-x * x - 0.2)
        + 2.0 * rho**2 * eta * x
        - 0.75 * rho**3 * x * x
    )
    delay_4_x = rho / 10.0 + 3.0 * rho**3 * x4 * x4 / 8.0
    delay_5_x = rho / 10.0 + 3.0 * rho**3 * x5 * x5 / 8.0
    delay_theta_x = -2.0 * rho**2 * eta * xtheta

    output = np.empty_like(current_variation)
    output[:, 0] = (
        local_x * current_variation[:, 0]
        + current_variation[:, 1]
        + delay_4_x * delayed_4_variation[:, 0]
        + delay_5_x * delayed_5_variation[:, 0]
        + delay_theta_x * delayed_theta_variation[:, 0]
    )
    output[:, 1] = -current_variation[:, 0]
    return output


def solve_target_variational_dde(
    base: C4TargetTubeNumericalSolution,
    maximum_step: float = VARIATIONAL_MAXIMUM_STEPS[-1],
) -> TargetVariationalSolution:
    """Integrate the true lambda-variational DDE by method of steps."""

    step = _finite(maximum_step, "maximum_step")
    if step <= 0.0 or step > 4.0:
        raise ValueError("maximum_step must lie in (0,4]")
    config = base.configuration
    count = len(base.transverse_values)
    segments: list[tuple[float, float, Any]] = []

    def known_variations(time: float) -> NDArray[np.float64]:
        if time <= config.incoming_time:
            return np.asarray(
                [
                    c4_prepared_history_transverse_derivative(
                        time, label, config
                    )
                    for label in base.transverse_values
                ],
                dtype=float,
            )
        tolerance = 2.0e-11 * max(1.0, abs(time))
        for left, right, interpolant in reversed(segments):
            if left - tolerance <= time <= right + tolerance:
                clipped = min(max(time, left), right)
                return np.asarray(interpolant(clipped), dtype=float).reshape(
                    count, 2
                )
        if time <= config.incoming_time + tolerance:
            return np.asarray(
                [
                    c4_prepared_history_transverse_derivative(
                        config.incoming_time, label, config
                    )
                    for label in base.transverse_values
                ],
                dtype=float,
            )
        raise RuntimeError("variational method of steps queried future data")

    def right_hand_side(
        time: float, flattened_variation: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        current_variation = np.asarray(
            flattened_variation, dtype=float
        ).reshape(count, 2)
        current, delayed_4, delayed_5, delayed_theta = base.slot_states(time)
        output = _linearized_physical_fields(
            current_variation,
            known_variations(time - 4.0),
            known_variations(time - 5.0),
            known_variations(time - config.theta),
            current,
            delayed_4,
            delayed_5,
            delayed_theta,
            config,
        )
        return output.ravel()

    left = config.incoming_time
    state = np.asarray(
        [
            c4_prepared_history_transverse_derivative(
                config.incoming_time, label, config
            )
            for label in base.transverse_values
        ],
        dtype=float,
    ).ravel()
    function_evaluations = 0
    while left < config.outgoing_time - 1.0e-14:
        right = min(left + 4.0, config.outgoing_time)
        integration = solve_ivp(
            right_hand_side,
            (left, right),
            state,
            method="DOP853",
            rtol=SOLVER_RTOL,
            atol=SOLVER_ATOL,
            max_step=step,
            dense_output=True,
        )
        if not integration.success or integration.sol is None:
            raise RuntimeError(
                f"target variational integration failed: {integration.message}"
            )
        segments.append((left, right, integration.sol))
        state = np.asarray(integration.y[:, -1], dtype=float)
        function_evaluations += int(integration.nfev)
        left = right
    return TargetVariationalSolution(
        base=base,
        segments=segments,
        function_evaluations=function_evaluations,
        maximum_step=step,
    )


@dataclass(frozen=True)
class Binary64C4HistoryGate:
    """Sampled C4-history P-matrix margins for the combined candidate."""

    history_frame: tuple[tuple[int, int], tuple[int, int]]
    history_frame_determinant: int
    patch_width: str
    history_time_sample_count: int
    transverse_sample_count: int
    minimum_time_principal_minor: str
    minimum_lambda_principal_minor: str
    minimum_oriented_determinant: str
    minimum_raw_chart_determinant: str
    maximum_raw_chart_determinant: str


def _build_binary64_c4_history_gate() -> Binary64C4HistoryGate:
    config = TargetTubeConfiguration()
    times = np.linspace(
        config.oldest_retained_time,
        config.incoming_time,
        C4_HISTORY_TIME_SAMPLE_COUNT,
    )
    labels = np.linspace(
        -config.transverse_radius,
        config.transverse_radius,
        config.transverse_sample_count,
    )
    time_jets = np.asarray(
        [
            [
                c4_prepared_history_jet(float(time), float(label), 1, config)
                for label in labels
            ]
            for time in times
        ]
    )
    label_jets = np.asarray(
        [
            [
                c4_prepared_history_transverse_derivative(
                    float(time), float(label), config
                )
                for label in labels
            ]
            for time in times
        ]
    )
    raw_determinant = (
        time_jets[:, :, 0] * label_jets[:, :, 1]
        - time_jets[:, :, 1] * label_jets[:, :, 0]
    )
    return Binary64C4HistoryGate(
        history_frame=HISTORY_FRAME,
        history_frame_determinant=HISTORY_FRAME_DETERMINANT,
        patch_width=_format(PATCH_WIDTH),
        history_time_sample_count=C4_HISTORY_TIME_SAMPLE_COUNT,
        transverse_sample_count=len(labels),
        minimum_time_principal_minor=_format(np.min(-time_jets[:, :, 0])),
        minimum_lambda_principal_minor=_format(np.min(label_jets[:, :, 1])),
        minimum_oriented_determinant=_format(np.min(-raw_determinant)),
        minimum_raw_chart_determinant=_format(np.min(raw_determinant)),
        maximum_raw_chart_determinant=_format(np.max(raw_determinant)),
    )


@dataclass(frozen=True)
class Binary64PhysicalGate:
    """Sampled physical-strip P-matrix and cross-separation margins."""

    physical_time_frame: tuple[tuple[int, int], tuple[int, int]]
    physical_frame_determinant: int
    physical_time_sample_count: int
    transverse_sample_count: int
    minimum_time_principal_minor: str
    minimum_lambda_principal_minor: str
    minimum_oriented_determinant: str
    minimum_raw_chart_determinant: str
    maximum_raw_chart_determinant: str
    maximum_variational_refinement_change: str
    maximum_variational_to_centered_difference_change: str
    cross_split_time: str
    maximum_early_x_time_derivative: str
    entry_x: str
    maximum_late_physical_x: str
    minimum_late_entry_x_gap: str


def _build_binary64_physical_gate() -> Binary64PhysicalGate:
    base = solve_target_c4_causal_tube(VARIATIONAL_MAXIMUM_STEPS[-1])
    variational = [
        solve_target_variational_dde(base, step)
        for step in VARIATIONAL_MAXIMUM_STEPS
    ]
    finest = variational[-1]
    config = base.configuration
    times = np.linspace(
        config.incoming_time,
        config.outgoing_time,
        PHYSICAL_TIME_SAMPLE_COUNT,
    )
    fields_at_times = np.asarray([base.fields(float(time)) for time in times])
    variations_at_times = np.asarray(
        [finest.variations(float(time)) for time in times]
    )
    time_minor = (
        -7.0 * fields_at_times[:, :, 0]
        + 2.0 * fields_at_times[:, :, 1]
    )
    lambda_minor = (
        3.0 * variations_at_times[:, :, 0]
        + variations_at_times[:, :, 1]
    )
    raw_determinant = (
        fields_at_times[:, :, 0] * variations_at_times[:, :, 1]
        - fields_at_times[:, :, 1] * variations_at_times[:, :, 0]
    )
    oriented_determinant = PHYSICAL_FRAME_DETERMINANT * raw_determinant

    refinement_times = np.linspace(
        config.incoming_time, config.outgoing_time, 301
    )
    refinement_change = max(
        float(
            np.max(
                np.abs(
                    variational[0].variations(float(time))
                    - variational[1].variations(float(time))
                )
            )
        )
        for time in refinement_times
    )
    states_at_times = np.asarray([base.states(float(time)) for time in times])
    denominator = (
        base.transverse_values[2:] - base.transverse_values[:-2]
    )[None, :, None]
    centered = (
        states_at_times[:, 2:, :] - states_at_times[:, :-2, :]
    ) / denominator
    variational_difference = float(
        np.max(np.abs(variations_at_times[:, 1:-1, :] - centered))
    )

    early_times = np.linspace(
        config.incoming_time,
        CROSS_SPLIT_TIME,
        CROSS_EARLY_TIME_SAMPLE_COUNT,
    )
    early_x_time = np.asarray(
        [base.fields(float(time))[:, 0] for time in early_times]
    )
    late_times = np.linspace(
        CROSS_SPLIT_TIME,
        config.outgoing_time,
        CROSS_LATE_TIME_SAMPLE_COUNT,
    )
    late_x = np.asarray(
        [base.states(float(time))[:, 0] for time in late_times]
    )
    entry_x_values = base.states(config.incoming_time)[:, 0]
    entry_x = float(entry_x_values[0])
    if np.max(np.abs(entry_x_values - entry_x)) > 1.0e-14:
        raise AssertionError("the prepared entry X is not label independent")
    maximum_late_x = float(np.max(late_x))

    return Binary64PhysicalGate(
        physical_time_frame=PHYSICAL_TIME_FRAME,
        physical_frame_determinant=PHYSICAL_FRAME_DETERMINANT,
        physical_time_sample_count=PHYSICAL_TIME_SAMPLE_COUNT,
        transverse_sample_count=len(base.transverse_values),
        minimum_time_principal_minor=_format(np.min(time_minor)),
        minimum_lambda_principal_minor=_format(np.min(lambda_minor)),
        minimum_oriented_determinant=_format(np.min(oriented_determinant)),
        minimum_raw_chart_determinant=_format(np.min(raw_determinant)),
        maximum_raw_chart_determinant=_format(np.max(raw_determinant)),
        maximum_variational_refinement_change=_format(refinement_change),
        maximum_variational_to_centered_difference_change=_format(
            variational_difference
        ),
        cross_split_time=_format(CROSS_SPLIT_TIME),
        maximum_early_x_time_derivative=_format(np.max(early_x_time)),
        entry_x=_format(entry_x),
        maximum_late_physical_x=_format(maximum_late_x),
        minimum_late_entry_x_gap=_format(entry_x - maximum_late_x),
    )


@dataclass(frozen=True)
class TargetChartUnivalenceGateCertificate:
    model_id: str
    audit_id: str
    arithmetic: str
    legacy_first_order_exact_history_gate: ExactHistoryGate
    binary64_c4_history_gate: Binary64C4HistoryGate
    binary64_physical_gate: Binary64PhysicalGate
    c4_history_p_matrix_interval_gate: tuple[str, str, str]
    physical_p_matrix_interval_gate: tuple[str, str, str]
    cross_interval_gate: tuple[str, str]
    collar_interval_gate: str
    degree_conclusion_if_gates_close: str
    c4_history_interval_cell_count: int
    interval_cell_count: int
    smooth_step_derivative_bound_proved_exactly: bool
    legacy_first_order_history_p_matrix_proved_exactly: bool
    c4_prepared_history_lambda_derivative_derived_exactly: bool
    p_matrix_global_univalence_reduction_proved_conditionally: bool
    piecewise_cross_separation_reduction_proved_conditionally: bool
    oriented_degree_one_conclusion_proved_conditionally: bool
    expanded_strict_gate_implies_open_collar_proved_conditionally: bool
    strict_interval_cell_schema_implemented: bool
    c4_state_dde_sampled_binary64: bool
    true_lambda_variational_dde_sampled_binary64: bool
    sampled_c4_history_p_matrix_margins_positive: bool
    sampled_physical_p_matrix_margins_positive: bool
    sampled_cross_separation_margins_positive: bool
    c4_history_p_matrix_interval_cover_validated: bool
    physical_p_matrix_interval_cover_validated: bool
    physical_cross_separation_interval_validated: bool
    expanded_open_collar_interval_validated: bool
    target_chart_global_injectivity_proved: bool
    target_chart_embedding_on_open_collar_proved: bool
    target_boundary_degree_validated: bool
    target_c4_chart_and_seam_compatibility_validated: bool
    target_global_graph_fixed_point_validated: bool
    exact_acceptance_contract: str


EXACT_TRUE_FLAGS = (
    "smooth_step_derivative_bound_proved_exactly",
    "legacy_first_order_history_p_matrix_proved_exactly",
    "c4_prepared_history_lambda_derivative_derived_exactly",
    "p_matrix_global_univalence_reduction_proved_conditionally",
    "piecewise_cross_separation_reduction_proved_conditionally",
    "oriented_degree_one_conclusion_proved_conditionally",
    "expanded_strict_gate_implies_open_collar_proved_conditionally",
    "strict_interval_cell_schema_implemented",
)
NUMERICAL_TRUE_FLAGS = (
    "c4_state_dde_sampled_binary64",
    "true_lambda_variational_dde_sampled_binary64",
    "sampled_c4_history_p_matrix_margins_positive",
    "sampled_physical_p_matrix_margins_positive",
    "sampled_cross_separation_margins_positive",
)
OPEN_FLAGS = (
    "c4_history_p_matrix_interval_cover_validated",
    "physical_p_matrix_interval_cover_validated",
    "physical_cross_separation_interval_validated",
    "expanded_open_collar_interval_validated",
    "target_chart_global_injectivity_proved",
    "target_chart_embedding_on_open_collar_proved",
    "target_boundary_degree_validated",
    "target_c4_chart_and_seam_compatibility_validated",
    "target_global_graph_fixed_point_validated",
)


def build_target_chart_univalence_gate() -> TargetChartUnivalenceGateCertificate:
    """Build the exact reduction plus binary64 feasibility record."""

    legacy_history = exact_history_gate()
    c4_history = _build_binary64_c4_history_gate()
    physical = _build_binary64_physical_gate()
    sampled_c4_history = (
        float(c4_history.minimum_time_principal_minor) > 0.0
        and float(c4_history.minimum_lambda_principal_minor) > 0.0
        and float(c4_history.minimum_oriented_determinant) > 0.0
        and float(c4_history.maximum_raw_chart_determinant) < 0.0
    )
    sampled_p_matrix = (
        float(physical.minimum_time_principal_minor) > 0.0
        and float(physical.minimum_lambda_principal_minor) > 0.0
        and float(physical.minimum_oriented_determinant) > 0.0
        and float(physical.maximum_raw_chart_determinant) < 0.0
    )
    sampled_cross = (
        float(physical.maximum_early_x_time_derivative) < 0.0
        and float(physical.minimum_late_entry_x_gap) > 0.0
    )
    return TargetChartUnivalenceGateCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        arithmetic=MANIFEST_ARITHMETIC,
        legacy_first_order_exact_history_gate=legacy_history,
        binary64_c4_history_gate=c4_history,
        binary64_physical_gate=physical,
        c4_history_p_matrix_interval_gate=(
            "inf_cell -partial_t Psi_X > 0",
            "inf_cell partial_lambda Psi_Y > 0",
            "inf_cell -det D(Psi) > 0",
        ),
        physical_p_matrix_interval_gate=(
            "inf_cell (-7,2).partial_t Psi > 0",
            "inf_cell (3,1).partial_lambda Psi > 0",
            "inf_cell det D(L_P Psi)=-13 det D(Psi) > 0",
        ),
        cross_interval_gate=(
            "sup partial_t Psi_X < 0 on [-3,-2]xLambda",
            "sup Psi_X < X_entry on [-2,3]xLambda",
        ),
        collar_interval_gate=(
            "repeat every strict C4-history, physical and cross inequality "
            "on an enlarged closed time-label rectangle with a strictly "
            "larger label radius; its interior is the open embedding domain "
            "containing the retained target rectangle compactly"
        ),
        degree_conclusion_if_gates_close=(
            "Psi has local degree -1; for y in L_P Psi(int P), "
            "deg(L_P Psi,int P,y)=+1, and the glued chart is a one-to-one "
            "local diffeomorphism on the retained rectangle"
        ),
        c4_history_interval_cell_count=0,
        interval_cell_count=0,
        smooth_step_derivative_bound_proved_exactly=True,
        legacy_first_order_history_p_matrix_proved_exactly=True,
        c4_prepared_history_lambda_derivative_derived_exactly=True,
        p_matrix_global_univalence_reduction_proved_conditionally=True,
        piecewise_cross_separation_reduction_proved_conditionally=True,
        oriented_degree_one_conclusion_proved_conditionally=True,
        expanded_strict_gate_implies_open_collar_proved_conditionally=True,
        strict_interval_cell_schema_implemented=True,
        c4_state_dde_sampled_binary64=True,
        true_lambda_variational_dde_sampled_binary64=True,
        sampled_c4_history_p_matrix_margins_positive=bool(sampled_c4_history),
        sampled_physical_p_matrix_margins_positive=bool(sampled_p_matrix),
        sampled_cross_separation_margins_positive=bool(sampled_cross),
        c4_history_p_matrix_interval_cover_validated=False,
        physical_p_matrix_interval_cover_validated=False,
        physical_cross_separation_interval_validated=False,
        expanded_open_collar_interval_validated=False,
        target_chart_global_injectivity_proved=False,
        target_chart_embedding_on_open_collar_proved=False,
        target_boundary_degree_validated=False,
        target_c4_chart_and_seam_compatibility_validated=False,
        target_global_graph_fixed_point_validated=False,
        exact_acceptance_contract=(
            "accept the target embedding only after outward-rounded C4-history "
            "cells and a state-plus-variational method-of-steps cover verify "
            "both sets of three strict P-matrix margins and the two strict "
            "X-separation margins on an enlarged collar; binary64 samples and "
            "schema-valid decimal cells without solver provenance are "
            "insufficient"
        ),
    )


def json_ready_target_chart_univalence_gate() -> dict[str, Any]:
    """Return the deterministic JSON-ready gate record."""

    return json.loads(
        json.dumps({"certificate": asdict(build_target_chart_univalence_gate())})
    )


def validate_target_chart_univalence_gate_audit(
    payload: Mapping[str, Any],
) -> None:
    """Reject claim promotion, numerical weakening, and scalar tampering."""

    if not isinstance(payload, Mapping):
        raise ValueError("target univalence audit must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("target univalence certificate must be a mapping")
    if any(certificate.get(key) is not True for key in EXACT_TRUE_FLAGS):
        raise ValueError("an exact or conditional univalence flag was weakened")
    if any(certificate.get(key) is not True for key in NUMERICAL_TRUE_FLAGS):
        raise ValueError("a binary64 feasibility flag was weakened")
    if any(certificate.get(key) is not False for key in OPEN_FLAGS):
        raise ValueError("an open interval or embedding gate was promoted")
    for count_name in ("c4_history_interval_cell_count", "interval_cell_count"):
        if type(certificate.get(count_name)) is not int:
            raise ValueError(f"{count_name} has the wrong type")
        if certificate.get(count_name) != 0:
            raise ValueError(f"{count_name} must remain zero in this candidate")
    boolean_fields = {
        field.name
        for field in fields(TargetChartUnivalenceGateCertificate)
        if field.type in (bool, "bool")
    }
    expected = set(EXACT_TRUE_FLAGS) | set(NUMERICAL_TRUE_FLAGS) | set(OPEN_FLAGS)
    if boolean_fields != expected:
        raise AssertionError("the univalence claim ledger is incomplete")
    if dict(payload) != json_ready_target_chart_univalence_gate():
        raise ValueError("target univalence audit differs from reference")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_target_chart_univalence_gate_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate a generated result and its frozen parent."""

    if not isinstance(payload, Mapping):
        raise ValueError("target univalence result must be a mapping")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("target univalence result requires audit and manifest")
    validate_target_chart_univalence_gate_audit(audit)
    parent = repository / PARENT_RESULT_RELATIVE_PATH
    if _sha256(parent) != PARENT_RESULT_SHA256:
        raise ValueError("the target causal-chart parent hash changed")
    c4_seam = repository / C4_SEAM_RESULT_RELATIVE_PATH
    if _sha256(c4_seam) != C4_SEAM_RESULT_SHA256:
        raise ValueError("the exact C4 seam parent hash changed")
    expected_paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
    }
    for key, relative in expected_paths.items():
        if manifest.get(key) != relative:
            raise ValueError(f"manifest {key} path changed")
        if manifest.get(f"{key}_sha256") != _sha256(repository / relative):
            raise ValueError(f"manifest {key} hash changed")
    if manifest.get("parent") != PARENT_RESULT_RELATIVE_PATH:
        raise ValueError("manifest parent path changed")
    if manifest.get("parent_sha256") != PARENT_RESULT_SHA256:
        raise ValueError("manifest parent digest changed")
    if manifest.get("c4_seam_parent") != C4_SEAM_RESULT_RELATIVE_PATH:
        raise ValueError("manifest C4 seam parent path changed")
    if manifest.get("c4_seam_parent_sha256") != C4_SEAM_RESULT_SHA256:
        raise ValueError("manifest C4 seam parent digest changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("manifest command changed")
    if manifest.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("manifest arithmetic changed")
    if manifest.get("python") != platform.python_version():
        raise ValueError("manifest Python version changed")
    if manifest.get("platform") != platform.platform():
        raise ValueError("manifest platform changed")


__all__ = [
    "AUDIT_ID",
    "Binary64C4HistoryGate",
    "C4_SEAM_RESULT_RELATIVE_PATH",
    "C4_SEAM_RESULT_SHA256",
    "C4TargetTubeNumericalSolution",
    "CROSS_SPLIT_TIME",
    "DEFAULT_COMMAND",
    "EXACT_TRUE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "HISTORY_FRAME",
    "MANIFEST_ARITHMETIC",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "NUMERICAL_TRUE_FLAGS",
    "OPEN_FLAGS",
    "PARENT_RESULT_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "PHYSICAL_TIME_FRAME",
    "PMatrixIntervalCell",
    "PROOF_SOURCE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "TargetVariationalSolution",
    "build_target_chart_univalence_gate",
    "exact_history_gate",
    "json_ready_target_chart_univalence_gate",
    "solve_target_c4_causal_tube",
    "solve_target_variational_dde",
    "validate_p_matrix_interval_cover",
    "validate_target_chart_univalence_gate_audit",
    "validate_target_chart_univalence_gate_result",
]
