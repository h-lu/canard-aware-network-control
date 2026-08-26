"""Stage-4H signed stable-flow diagnostic for the inner Route-C return.

This module uses the exact finite Volterra-word identity available on one
inner period.  Since ``T < tau_0 + tau_1`` and ``T < 3*tau_0``, the current
resolvent contains only the words ``empty, (0), (1), (0,0)``.  The history
density contains the corresponding input words ``(0), (1), (0,0)``.

The Stage-3 Route-C unstable history and the Stage-4D atom-plus-density row
are combined *before* total variation through

    U(t) P_s = U(t) - U(t) q f / f(q).

The present artifact is intentionally source-bound, not directed.  DOP853,
Gauss--Legendre quadrature and sampled output phases expose the size and the
location of the signed cancellation, but they do not enclose the continuous
two-variable density or its time supremum.  Consequently no stable power,
stable graph, split tube, separator or onset theorem is promoted here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Callable, Mapping

import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp

from canard_control.leaky_floquet_inner_strong_stable_gap import (
    RESULT_RELATIVE_PATH as STRONG_GAP_RESULT_RELATIVE_PATH,
    validate_inner_strong_stable_gap_result,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_route_c_adjoint_stage4d import (
    RESULT_RELATIVE_PATH as STAGE4D_RESULT_RELATIVE_PATH,
    validate_stage4d_result,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    _adjoint_mode_rows,
    _centre_data,
    _evaluate,
    _guide_density_dictionary,
    _history_action,
    _row_tail_neumann,
)


SCHEMA_ID = "leaky-inner-signed-stable-flow-stage4h-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_signed_stable_flow_stage4h.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_signed_stable_flow_stage4h.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_signed_stable_flow_stage4h.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-signed-stable-flow-stage4h.md"
TEST_RELATIVE_PATH = "tests/test_leaky_inner_signed_stable_flow_stage4h.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_inner_signed_stable_flow_stage4h.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source binding; exact finite Volterra-word support "
    "on the one-period horizon; source-bound binary64 DOP853 fundamental "
    "matrix and word primitives; direct Stage-4D atom-plus-density action; "
    "same-row rank-one deflation before Gauss--Legendre total variation; "
    "nested sampled time meshes only, with no outward ODE residual, bivariate "
    "density enclosure, continuous-time supremum, stable power, graph, split "
    "tube, separator, or onset theorem"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

STAGE3_RESULT_SHA256 = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)
STAGE4D_RESULT_SHA256 = (
    "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
)
STRONG_GAP_RESULT_SHA256 = (
    "e61792cd946103b33da8209cae1c3123baa07b14aa6ccef4ae63b1c9a14848cc"
)
PINNED_OPENBLAS_NUM_THREADS = "8"
QUADRATURE_ORDER = 8
QUADRATURE_MAX_PANEL = 0.08
FUNDAMENTAL_MAX_STEP = 0.03
WORD_MAX_STEP = 0.02
OUTPUT_TIME_COUNT = 129
CURRENT_TIME_COUNT = 65
NESTED_TIME_COUNTS = (17, 33, 65, 129)
DECLARED_STRONG_RATE = float(
    "0.995024916874584026786952988590018278886039540627453615"
)

TRUE_FLAGS = (
    "one_return_volterra_word_support_proved",
    "stage3_route_c_unstable_history_used",
    "stage4d_continuous_atom_density_row_used",
    "rank_one_deflation_formed_before_total_variation",
    "phase_fixed_event_row_formed_before_total_variation",
    "source_bound_signed_stable_flow_diagnostic_computed",
    "unstable_q_flow_diagnostic_computed_separately",
    "split_tube_linear_budget_diagnostic_computed",
    "finite_node_pilot_not_promoted",
)
FALSE_FLAGS = (
    "dop853_roundoff_and_truncation_outward_enclosed",
    "gauss_legendre_total_variation_is_directed_upper",
    "continuous_output_phase_supremum_validated",
    "fourier_orbit_q_and_adjoint_errors_propagated_through_all_words",
    "intermediate_stable_flow_norm_upper_validated",
    "phase_fixed_one_step_stable_map_norm_upper_validated",
    "stable_power_constant_numeric_upper_validated",
    "k_s_equals_one_validated",
    "uniform_split_ball_statement",
    "inner_local_stable_graph_quantitatively_validated",
    "split_return_tube_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage4HArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    exact_four_word_reduction: dict[str, Any]
    continuous_history_split: dict[str, Any]
    source_bound_numerics: dict[str, Any]
    rank_one_identity_oracles: dict[str, Any]
    intermediate_signed_flow_diagnostic: dict[str, Any]
    phase_fixed_one_step_diagnostic: dict[str, Any]
    unstable_q_flow_diagnostic: dict[str, Any]
    split_tube_linear_budget_diagnostic: dict[str, Any]
    directed_ingress_obstruction: dict[str, Any]
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


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} is missing")
    return value


def _load_parent(
    repository: Path, relative: str, expected_hash: str, label: str
) -> Mapping[str, Any]:
    raw = (repository / relative).read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise ValueError(f"the bound {label} result changed")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the bound {label} result is malformed")
    return payload


def _format(value: float | np.floating[Any]) -> str:
    return format(float(value), ".17g")


class _FourWordDiagnostic:
    """Binary centre calculation for the exact four-word formula."""

    def __init__(self, repository: Path):
        self.data = _centre_data(repository)
        self.tail_v, self.tail_w, _ = _row_tail_neumann(self.data)
        self.period = float(self.data.period)
        self.tau0 = float(self.data.tau0)
        self.tau1 = float(self.data.tau1)
        self.epsilon = float(self.data.epsilon)
        self.nodes, self.weights = leggauss(QUADRATURE_ORDER)
        self._compiled: dict[int, tuple[np.ndarray, np.ndarray]] = {}

        adjoint_v, adjoint_w = _adjoint_mode_rows(
            self.data, self.tail_v, self.tail_w
        )
        self.f_voltage_atom = sum(adjoint_v.values())
        self.f_recovery_atom = sum(adjoint_w.values())
        self.fq = _history_action(
            self.data,
            self.tail_v,
            self.tail_w,
            self.data.qsection_v,
            self.data.qsection_w,
        )
        self.f_densities: list[tuple[float, Mapping[Any, complex]]] = []
        for delay, coefficient in (
            (self.tau0, self.data.delayed0),
            (self.tau1, self.data.delayed1),
        ):
            retained, omitted = _guide_density_dictionary(
                self.data,
                self.tail_v,
                self.tail_w,
                delay,
                coefficient,
            )
            complete = dict(retained)
            complete.update(omitted)
            self.f_densities.append((delay, complete))
        for value in (
            self.data.current,
            self.data.delayed0,
            self.data.delayed1,
            self.data.qsection_v,
            self.data.qsection_w,
            self.data.xdot_v,
            self.data.xdot_w,
            *(value for _, value in self.f_densities),
        ):
            self._compile(value)

        self._build_word_primitives()

    def _compile(
        self, value: Mapping[Any, complex]
    ) -> tuple[np.ndarray, np.ndarray]:
        key = id(value)
        if key not in self._compiled:
            exponents = np.asarray(
                [
                    growth * float(self.data.root)
                    + 2.0j * math.pi * mode
                    for growth, mode in value
                ],
                dtype=complex,
            )
            coefficients = np.asarray(tuple(value.values()), dtype=complex)
            self._compiled[key] = (exponents, coefficients)
        return self._compiled[key]

    def evaluate(self, value: Mapping[Any, complex], time: float) -> complex:
        exponents, coefficients = self._compile(value)
        return complex(
            np.sum(coefficients * np.exp(exponents * float(time) / self.period))
        )

    def current_matrix(self, time: float) -> np.ndarray:
        coefficient = self.evaluate(self.data.current, time).real
        return np.asarray(
            [[coefficient, -1.0], [self.epsilon, -self.epsilon]],
            dtype=float,
        )

    def delayed_coefficient(self, delay_index: int, time: float) -> float:
        dictionary = (
            self.data.delayed0
            if delay_index == 0
            else self.data.delayed1
        )
        return float(self.evaluate(dictionary, time).real)

    def _build_word_primitives(self) -> None:
        fundamental = solve_ivp(
            lambda time, value: (
                self.current_matrix(time) @ value.reshape(2, 2)
            ).ravel(),
            (0.0, self.period),
            np.eye(2).ravel(),
            method="DOP853",
            rtol=5.0e-13,
            atol=2.0e-15,
            max_step=FUNDAMENTAL_MAX_STEP,
            dense_output=True,
        )
        if not fundamental.success:
            raise ArithmeticError("the fundamental-matrix pilot failed")
        self.fundamental_solution = fundamental
        self.word_solutions = []
        for delay_index, delay in enumerate((self.tau0, self.tau1)):
            solution = solve_ivp(
                lambda time, _value, j=delay_index, tau=delay: np.outer(
                    self.insertion_column(j, time),
                    self.fundamental(time - tau)[0, :],
                ).ravel(),
                (delay, self.period),
                np.zeros(4),
                method="DOP853",
                rtol=5.0e-13,
                atol=2.0e-15,
                max_step=WORD_MAX_STEP,
                dense_output=True,
            )
            if not solution.success:
                raise ArithmeticError("a one-delay word pilot failed")
            self.word_solutions.append(solution)

        two_delay_start = 2.0 * self.tau0
        double_solution = solve_ivp(
            lambda time, _value: np.outer(
                self.insertion_column(0, time),
                self.fundamental(time - self.tau0)[0, :]
                @ self.word_primitive(0, time - self.tau0),
            ).ravel(),
            (two_delay_start, self.period),
            np.zeros(4),
            method="DOP853",
            rtol=5.0e-13,
            atol=2.0e-15,
            max_step=0.01,
            dense_output=True,
        )
        if not double_solution.success:
            raise ArithmeticError("the double-delay word pilot failed")
        self.double_word_solution = double_solution
        self.nfev = {
            "fundamental": int(fundamental.nfev),
            "word_0": int(self.word_solutions[0].nfev),
            "word_1": int(self.word_solutions[1].nfev),
            "word_00": int(double_solution.nfev),
        }

    def fundamental(self, time: float) -> np.ndarray:
        time = min(max(float(time), 0.0), self.period)
        return self.fundamental_solution.sol(time).reshape(2, 2)

    def insertion_column(self, delay_index: int, time: float) -> np.ndarray:
        forcing = np.asarray(
            [self.delayed_coefficient(delay_index, time), 0.0]
        )
        return np.linalg.solve(self.fundamental(time), forcing)

    def word_primitive(self, delay_index: int, time: float) -> np.ndarray:
        delay = self.tau0 if delay_index == 0 else self.tau1
        if time <= delay:
            return np.zeros((2, 2))
        time = min(float(time), self.period)
        return self.word_solutions[delay_index].sol(time).reshape(2, 2)

    def double_word_primitive(self, time: float) -> np.ndarray:
        if time <= 2.0 * self.tau0:
            return np.zeros((2, 2))
        time = min(float(time), self.period)
        return self.double_word_solution.sol(time).reshape(2, 2)

    def resolvent_atom(self, time: float) -> np.ndarray:
        bracket = (
            np.eye(2)
            + self.word_primitive(0, time)
            + self.word_primitive(1, time)
            + self.double_word_primitive(time)
        )
        return self.fundamental(time) @ bracket

    def resolvent_density(self, time: float, history_time: float) -> np.ndarray:
        """Voltage-history density of the two-coordinate current state."""

        output = np.zeros(2)
        fundamental_at_time = self.fundamental(time)
        for delay_index, delay in enumerate((self.tau0, self.tau1)):
            insertion_time = history_time + delay
            if -1.0e-13 <= insertion_time <= time + 1.0e-13:
                insertion_time = max(0.0, insertion_time)
                column = self.insertion_column(delay_index, insertion_time)
                output += fundamental_at_time @ column
                if (
                    delay_index == 0
                    and insertion_time + self.tau0 <= time + 1.0e-13
                ):
                    output += fundamental_at_time @ (
                        self.word_primitive(0, time)
                        - self.word_primitive(
                            0, insertion_time + self.tau0
                        )
                    ) @ column
        return output

    def f_density(self, history_time: float) -> complex:
        total = 0.0j
        for delay, density in self.f_densities:
            if -delay - 1.0e-13 <= history_time <= 1.0e-13:
                total += self.evaluate(density, history_time)
        return total

    def q_flow(self, time: float) -> np.ndarray:
        return np.asarray(
            [
                self.evaluate(self.data.qsection_v, time),
                self.evaluate(self.data.qsection_w, time),
            ]
        )

    def xdot(self, time: float) -> np.ndarray:
        return np.asarray(
            [
                self.evaluate(self.data.xdot_v, time).real,
                self.evaluate(self.data.xdot_w, time).real,
            ]
        )

    def integration_breaks(self, time: float | None = None) -> tuple[float, ...]:
        values = {-self.tau1, -self.tau0, 0.0}
        if time is not None:
            values.update(
                {
                    min(0.0, time - self.tau1),
                    min(0.0, time - self.tau0),
                    min(0.0, time - 2.0 * self.tau0),
                }
            )
        return tuple(
            sorted(
                value
                for value in values
                if -self.tau1 - 1.0e-13 <= value <= 1.0e-13
            )
        )

    def integrate(
        self,
        function: Callable[[float], Any],
        breaks: tuple[float, ...],
    ) -> Any:
        total: Any = None
        for left, right in zip(breaks[:-1], breaks[1:], strict=True):
            if right - left <= 1.0e-15:
                continue
            panel_count = max(
                1, int(math.ceil((right - left) / QUADRATURE_MAX_PANEL))
            )
            edges = np.linspace(left, right, panel_count + 1)
            for panel_left, panel_right in zip(
                edges[:-1], edges[1:], strict=True
            ):
                points = (
                    0.5 * (panel_left + panel_right)
                    + 0.5 * (panel_right - panel_left) * self.nodes
                )
                local: Any = None
                for weight, point in zip(self.weights, points, strict=True):
                    term = weight * np.asarray(function(float(point)))
                    local = term if local is None else local + term
                local = 0.5 * (panel_right - panel_left) * local
                total = local if total is None else total + local
        if total is None:
            return 0.0
        return total

    def restricted_f_norm(self) -> float:
        density_tv = float(
            self.integrate(
                lambda history_time: abs(self.f_density(history_time)),
                self.integration_breaks(),
            )
        )
        return (abs(self.f_recovery_atom) + density_tv) / abs(self.fq)

    def stable_current_row_norms(self, time: float) -> np.ndarray:
        q_value = self.q_flow(time)
        atom = (
            self.resolvent_atom(time)[:, 1]
            - q_value * self.f_recovery_atom / self.fq
        )
        fundamental_at_time = self.fundamental(time)
        primitive_at_time = self.word_primitive(0, time)

        def density(history_time: float) -> np.ndarray:
            # Keep the common signed row until the final absolute value.
            raw = self.resolvent_density_with_cache(
                time,
                history_time,
                fundamental_at_time,
                primitive_at_time,
            )
            return np.abs(
                raw - q_value * self.f_density(history_time) / self.fq
            )

        density_tv = np.asarray(
            self.integrate(density, self.integration_breaks(time)),
            dtype=float,
        )
        return np.abs(atom) + density_tv

    def resolvent_density_with_cache(
        self,
        time: float,
        history_time: float,
        fundamental_at_time: np.ndarray,
        primitive_at_time: np.ndarray,
    ) -> np.ndarray:
        output = np.zeros(2)
        for delay_index, delay in enumerate((self.tau0, self.tau1)):
            insertion_time = history_time + delay
            if -1.0e-13 <= insertion_time <= time + 1.0e-13:
                insertion_time = max(0.0, insertion_time)
                column = self.insertion_column(delay_index, insertion_time)
                output += fundamental_at_time @ column
                if (
                    delay_index == 0
                    and insertion_time + self.tau0 <= time + 1.0e-13
                ):
                    output += fundamental_at_time @ (
                        primitive_at_time
                        - self.word_primitive(
                            0, insertion_time + self.tau0
                        )
                    ) @ column
        return output

    def event_rows(self, output_time: float) -> dict[str, float]:
        final_time = self.period
        final_speed = self.xdot(final_time)[0]
        phase_ratio = self.xdot(output_time)[0] / final_speed
        raw_atom = (
            self.resolvent_atom(output_time)[0, 1]
            - phase_ratio * self.resolvent_atom(final_time)[0, 1]
        )
        q_event = (
            self.q_flow(output_time)[0]
            - phase_ratio * self.q_flow(final_time)[0]
        )
        stable_atom = raw_atom - q_event * self.f_recovery_atom / self.fq
        output_fundamental = self.fundamental(output_time)
        output_primitive = self.word_primitive(0, output_time)
        final_fundamental = self.fundamental(final_time)
        final_primitive = self.word_primitive(0, final_time)

        def rows(history_time: float) -> np.ndarray:
            raw = self.resolvent_density_with_cache(
                output_time,
                history_time,
                output_fundamental,
                output_primitive,
            )[0] - phase_ratio * self.resolvent_density_with_cache(
                final_time,
                history_time,
                final_fundamental,
                final_primitive,
            )[0]
            rank_one = q_event * self.f_density(history_time) / self.fq
            return np.asarray([abs(raw), abs(rank_one), abs(raw - rank_one)])

        breaks = tuple(
            sorted(
                set(self.integration_breaks(output_time))
                | set(self.integration_breaks(final_time))
            )
        )
        density_tvs = np.asarray(self.integrate(rows, breaks), dtype=float)
        raw_norm = abs(raw_atom) + density_tvs[0]
        rank_one_norm = (
            abs(q_event * self.f_recovery_atom / self.fq)
            + density_tvs[1]
        )
        signed_norm = abs(stable_atom) + density_tvs[2]
        return {
            "raw_norm": raw_norm,
            "rank_one_norm": rank_one_norm,
            "separate_triangle_norm": raw_norm + rank_one_norm,
            "signed_norm": signed_norm,
            "q_event_abs": abs(q_event),
        }

    def recovery_event_rows(self) -> dict[str, float]:
        final_time = self.period
        final_speed = self.xdot(final_time)[0]
        phase_ratio = self.xdot(final_time)[1] / final_speed
        raw_atom = (
            self.resolvent_atom(final_time)[1, 1]
            - phase_ratio * self.resolvent_atom(final_time)[0, 1]
        )
        q_event = (
            self.q_flow(final_time)[1]
            - phase_ratio * self.q_flow(final_time)[0]
        )
        stable_atom = raw_atom - q_event * self.f_recovery_atom / self.fq
        final_fundamental = self.fundamental(final_time)
        final_primitive = self.word_primitive(0, final_time)

        def rows(history_time: float) -> np.ndarray:
            vector = self.resolvent_density_with_cache(
                final_time,
                history_time,
                final_fundamental,
                final_primitive,
            )
            raw = vector[1] - phase_ratio * vector[0]
            rank_one = q_event * self.f_density(history_time) / self.fq
            return np.asarray([abs(raw), abs(rank_one), abs(raw - rank_one)])

        density_tvs = np.asarray(
            self.integrate(rows, self.integration_breaks(final_time)),
            dtype=float,
        )
        raw_norm = abs(raw_atom) + density_tvs[0]
        rank_one_norm = (
            abs(q_event * self.f_recovery_atom / self.fq)
            + density_tvs[1]
        )
        signed_norm = abs(stable_atom) + density_tvs[2]
        return {
            "raw_norm": raw_norm,
            "rank_one_norm": rank_one_norm,
            "separate_triangle_norm": raw_norm + rank_one_norm,
            "signed_norm": signed_norm,
            "q_event_abs": abs(q_event),
        }

    def q_action_oracle(self, time: float) -> tuple[np.ndarray, np.ndarray]:
        q_initial = np.asarray(
            [
                self.evaluate(self.data.qsection_v, 0.0),
                self.evaluate(self.data.qsection_w, 0.0),
            ]
        )
        atom = self.resolvent_atom(time) @ q_initial
        density = self.integrate(
            lambda history_time: self.resolvent_density(
                time, history_time
            )
            * self.evaluate(self.data.qsection_v, history_time),
            self.integration_breaks(time),
        )
        return np.asarray(atom + density, dtype=complex), self.q_flow(time)


def _nested_rows(times: np.ndarray, values: np.ndarray) -> list[dict[str, Any]]:
    rows = []
    finest = len(times)
    for count in (
        count
        for count in NESTED_TIME_COUNTS
        if count <= finest and (finest - 1) % (count - 1) == 0
    ):
        stride = (finest - 1) // (count - 1)
        indices = np.arange(0, finest, stride, dtype=int)
        sampled = values[indices]
        maximum_index = int(indices[int(np.argmax(sampled))])
        rows.append(
            {
                "time_count": count,
                "sampled_maximum": _format(values[maximum_index]),
                "sampled_argmax_time": _format(times[maximum_index]),
            }
        )
    return rows


def _diagnostic_payload(repository: Path) -> dict[str, Any]:
    diagnostic = _FourWordDiagnostic(repository)
    period = diagnostic.period
    tau0 = diagnostic.tau0
    tau1 = diagnostic.tau1
    rho_s = DECLARED_STRONG_RATE

    f_quad = (
        diagnostic.f_voltage_atom
        * diagnostic.evaluate(diagnostic.data.qsection_v, 0.0)
        + diagnostic.f_recovery_atom
        * diagnostic.evaluate(diagnostic.data.qsection_w, 0.0)
        + diagnostic.integrate(
            lambda history_time: diagnostic.f_density(history_time)
            * diagnostic.evaluate(
                diagnostic.data.qsection_v, history_time
            ),
            diagnostic.integration_breaks(),
        )
    )
    oracle_times = (
        0.0,
        period - tau1,
        tau0,
        tau1,
        2.0 * tau0,
        period,
    )
    q_oracles = []
    for time in oracle_times:
        reconstructed, direct = diagnostic.q_action_oracle(time)
        q_oracles.append(
            {
                "time": _format(time),
                "word_reconstruction_vs_direct_q_inf_error": _format(
                    np.max(np.abs(reconstructed - direct))
                ),
            }
        )

    current_times = np.linspace(0.0, period, CURRENT_TIME_COUNT)
    current_row_norms = np.asarray(
        [diagnostic.stable_current_row_norms(time) for time in current_times]
    )
    voltage_current_norms = current_row_norms[:, 0]
    recovery_current_norms = current_row_norms[:, 1]
    current_norms = np.maximum(voltage_current_norms, recovery_current_norms)

    initial_times = np.linspace(-tau1, 0.0, OUTPUT_TIME_COUNT)
    restricted_f_norm = diagnostic.restricted_f_norm()
    initial_voltage_norms = np.asarray(
        [
            0.0
            if abs(time) < 1.0e-15
            else 1.0
            + abs(
                diagnostic.evaluate(
                    diagnostic.data.qsection_v, time
                )
            )
            * restricted_f_norm
            for time in initial_times
        ]
    )
    initial_recovery_norm = diagnostic.stable_current_row_norms(0.0)[1]
    full_history_candidates = np.concatenate(
        (
            initial_voltage_norms,
            voltage_current_norms,
            recovery_current_norms,
            np.asarray([initial_recovery_norm]),
        )
    )
    full_history_maximum = float(np.max(full_history_candidates))

    output_times = np.linspace(period - tau1, period, OUTPUT_TIME_COUNT)
    event_rows = [diagnostic.event_rows(time) for time in output_times]
    signed_values = np.asarray([row["signed_norm"] for row in event_rows])
    triangle_values = np.asarray(
        [row["separate_triangle_norm"] for row in event_rows]
    )
    raw_values = np.asarray([row["raw_norm"] for row in event_rows])
    recovery_event = diagnostic.recovery_event_rows()
    phase_fixed_one_step = max(
        float(np.max(signed_values)), recovery_event["signed_norm"]
    )
    triangle_one_step = max(
        float(np.max(triangle_values)),
        recovery_event["separate_triangle_norm"],
    )
    signed_argmax_index = int(np.argmax(signed_values))

    q_input_times = np.linspace(-tau1, 0.0, 2049)
    q_input_norm = max(
        float(
            np.max(
                np.abs(
                    [
                        diagnostic.evaluate(
                            diagnostic.data.qsection_v, time
                        )
                        for time in q_input_times
                    ]
                )
            )
        ),
        abs(
            diagnostic.evaluate(diagnostic.data.qsection_w, 0.0)
        ),
    )
    q_event_voltage = np.asarray(
        [row["q_event_abs"] for row in event_rows]
    )
    q_event_norm = max(
        float(np.max(q_event_voltage)), recovery_event["q_event_abs"]
    )
    q_current_values = np.asarray(
        [np.max(np.abs(diagnostic.q_flow(time))) for time in current_times]
    )
    stable_radius = 0.001
    unstable_radius = 0.0007
    stable_linear_contribution = full_history_maximum * stable_radius
    unstable_flow_ratio = float(np.max(q_current_values)) / q_input_norm
    unstable_linear_contribution = unstable_flow_ratio * unstable_radius
    linear_tube_total = (
        stable_linear_contribution + unstable_linear_contribution
    )

    return {
        "word": {
            "period": period,
            "tau0": tau0,
            "tau1": tau1,
            "period_minus_two_tau0": period - 2.0 * tau0,
            "period_less_than_tau0_plus_tau1": period < tau0 + tau1,
            "period_less_than_three_tau0": period < 3.0 * tau0,
        },
        "numerics": {
            "quadrature_order_per_smooth_piece": QUADRATURE_ORDER,
            "quadrature_max_panel_width": QUADRATURE_MAX_PANEL,
            "output_time_count": OUTPUT_TIME_COUNT,
            "current_time_count": CURRENT_TIME_COUNT,
            "fundamental_max_step": FUNDAMENTAL_MAX_STEP,
            "word_max_step": WORD_MAX_STEP,
            "rtol": 5.0e-13,
            "atol": 2.0e-15,
            "ode_function_evaluations": diagnostic.nfev,
        },
        "pairing": {
            "f_q_direct_action_real": float(diagnostic.fq.real),
            "f_q_direct_action_imag": float(diagnostic.fq.imag),
            "f_q_quadrature_action_real": float(f_quad.real),
            "f_q_quadrature_action_imag": float(f_quad.imag),
            "direct_vs_quadrature_abs_defect": abs(f_quad - diagnostic.fq),
            "restricted_normalized_f_measure_norm": restricted_f_norm,
        },
        "oracles": q_oracles,
        "intermediate": {
            "nested_current_state_rows": _nested_rows(
                current_times, current_norms
            ),
            "sampled_current_state_maximum": float(np.max(current_norms)),
            "sampled_current_state_argmax_time": float(
                current_times[int(np.argmax(current_norms))]
            ),
            "sampled_initial_projection_voltage_maximum": float(
                np.max(initial_voltage_norms)
            ),
            "sampled_initial_projection_voltage_argmax_history_time": float(
                initial_times[int(np.argmax(initial_voltage_norms))]
            ),
            "sampled_full_history_flow_maximum_on_one_return": (
                full_history_maximum
            ),
        },
        "event": {
            "nested_signed_voltage_rows": _nested_rows(
                output_times, signed_values
            ),
            "sampled_signed_voltage_maximum": float(np.max(signed_values)),
            "sampled_signed_voltage_argmax_time": float(
                output_times[signed_argmax_index]
            ),
            "sampled_raw_voltage_maximum": float(np.max(raw_values)),
            "sampled_separate_triangle_voltage_maximum": float(
                np.max(triangle_values)
            ),
            "recovery_event_row": recovery_event,
            "sampled_phase_fixed_one_step_stable_map_norm": (
                phase_fixed_one_step
            ),
            "sampled_phase_fixed_separate_triangle_norm": triangle_one_step,
            "cancellation_factor_triangle_over_signed": (
                triangle_one_step / phase_fixed_one_step
            ),
            "declared_strong_rate_rho_s": rho_s,
            "sampled_margin_to_declared_rho_s": (
                rho_s - phase_fixed_one_step
            ),
        },
        "unstable": {
            "sampled_input_q_section_norm": q_input_norm,
            "sampled_event_q_norm": q_event_norm,
            "sampled_event_expansion_ratio": q_event_norm / q_input_norm,
            "exact_center_multiplier_exp_root": math.exp(
                float(diagnostic.data.root)
            ),
            "sampled_raw_current_q_maximum": float(
                np.max(q_current_values)
            ),
            "sampled_raw_current_q_argmax_time": float(
                current_times[int(np.argmax(q_current_values))]
            ),
        },
        "split_tube": {
            "stable_radius": stable_radius,
            "unstable_radius": unstable_radius,
            "section_radius": 0.01,
            "stable_linear_contribution": stable_linear_contribution,
            "unstable_normalized_flow_ratio": unstable_flow_ratio,
            "unstable_linear_contribution": unstable_linear_contribution,
            "linear_tube_total": linear_tube_total,
            "remaining_nonlinear_and_directed_error_margin": (
                0.01 - linear_tube_total
            ),
        },
    }


def build_stage4h_artifact(repository: Path) -> Stage4HArtifact:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the Stage-4H source replay requires OPENBLAS_NUM_THREADS="
            + PINNED_OPENBLAS_NUM_THREADS
        )
    repository = repository.resolve()
    stage3 = _load_parent(
        repository,
        STAGE3_RESULT_RELATIVE_PATH,
        STAGE3_RESULT_SHA256,
        "Stage-3 projection",
    )
    stage4d = _load_parent(
        repository,
        STAGE4D_RESULT_RELATIVE_PATH,
        STAGE4D_RESULT_SHA256,
        "Stage-4D adjoint",
    )
    strong_gap = _load_parent(
        repository,
        STRONG_GAP_RESULT_RELATIVE_PATH,
        STRONG_GAP_RESULT_SHA256,
        "strong stable gap",
    )
    validate_stage3_stable_projection_result(stage3, repository)
    validate_stage4d_result(stage4d, repository)
    validate_inner_strong_stable_gap_result(strong_gap, repository)
    payload = _diagnostic_payload(repository)
    word = payload["word"]
    pairing = payload["pairing"]
    intermediate = payload["intermediate"]
    event = payload["event"]
    unstable = payload["unstable"]
    split_tube = payload["split_tube"]
    if not (
        word["period_less_than_tau0_plus_tau1"]
        and word["period_less_than_three_tau0"]
        and word["period_minus_two_tau0"] > 0
    ):
        raise ArithmeticError("the exact four-word horizon changed")
    if pairing["direct_vs_quadrature_abs_defect"] >= 1.0e-10:
        raise ArithmeticError("the Stage-4D density action oracle failed")
    if max(
        float(row["word_reconstruction_vs_direct_q_inf_error"])
        for row in payload["oracles"]
    ) >= 1.0e-4:
        raise ArithmeticError("the exact word reconstruction oracle failed")
    if not event["sampled_phase_fixed_one_step_stable_map_norm"] < 0.02:
        raise ArithmeticError("the signed one-step diagnostic changed")
    if not event["sampled_phase_fixed_separate_triangle_norm"] > 1.0:
        raise ArithmeticError("the cancellation diagnostic disappeared")

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4HArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
            STRONG_GAP_RESULT_RELATIVE_PATH: STRONG_GAP_RESULT_SHA256,
        },
        exact_four_word_reduction={
            "time_horizon": "0<=t<=T",
            "period": _format(word["period"]),
            "tau0": _format(word["tau0"]),
            "tau1": _format(word["tau1"]),
            "period_minus_two_tau0": _format(
                word["period_minus_two_tau0"]
            ),
            "period_less_than_tau0_plus_tau1": True,
            "period_less_than_three_tau0": True,
            "current_resolvent_words": ["empty", "(0)", "(1)", "(0,0)"],
            "initial_voltage_density_words": ["(0)", "(1)", "(0,0)"],
            "word_support_status": (
                "exact consequence of positive delays and the one-period "
                "horizon; not a numerical truncation"
            ),
            "resolvent_formula": (
                "R(t,0)=F(t)[I+C_0(t)+C_1(t)+C_00(t)]"
            ),
            "density_formula": (
                "K(t,theta)=sum_j F(t)a_j(theta+tau_j) plus "
                "F(t)[C_0(t)-C_0(theta+2*tau_0)]a_0(theta+tau_0) "
                "on the active (0,0) triangle"
            ),
        },
        continuous_history_split={
            "history_space": (
                "Sigma subset C([-tau1,0],R) x R with phi_v(0)=0 and "
                "max norm"
            ),
            "restricted_row_norm": (
                "absolute current-recovery atom plus voltage-density total "
                "variation; the current-voltage atom vanishes on Sigma"
            ),
            "stable_projection_identity": (
                "U(t)P_s=U(t)-U(t)q*f/f(q), with the common atom-density "
                "row subtracted before total variation"
            ),
            "phase_fixed_voltage_row": (
                "S_v(t)-dot(v)(t)S_v(T)/dot(v)(T), "
                "T-tau1<=t<=T"
            ),
            "phase_fixed_recovery_row": (
                "S_w(T)-dot(w)(T)S_v(T)/dot(v)(T)"
            ),
            "stage4d_restricted_normalized_measure_norm_binary64": _format(
                pairing["restricted_normalized_f_measure_norm"]
            ),
        },
        source_bound_numerics={
            **payload["numerics"],
            "evidence_status": (
                "source-bound binary64 diagnostic; neither DOP853 nor "
                "Gauss--Legendre values are outward enclosures"
            ),
            "nested_mesh_spread_is_interval_error": False,
            "finite_history_nodes_used_as_operator_bound": False,
        },
        rank_one_identity_oracles={
            "f_q_direct_action_real_binary64": _format(
                pairing["f_q_direct_action_real"]
            ),
            "f_q_direct_action_imag_binary64": _format(
                pairing["f_q_direct_action_imag"]
            ),
            "f_q_quadrature_action_real_binary64": _format(
                pairing["f_q_quadrature_action_real"]
            ),
            "f_q_quadrature_action_imag_binary64": _format(
                pairing["f_q_quadrature_action_imag"]
            ),
            "f_q_direct_vs_quadrature_abs_defect_binary64": _format(
                pairing["direct_vs_quadrature_abs_defect"]
            ),
            "word_reconstruction_rows": payload["oracles"],
            "oracle_status": (
                "binary implementation oracles only; the exact finite-word "
                "and rank-one identities are analytic"
            ),
        },
        intermediate_signed_flow_diagnostic={
            "nested_current_state_rows": intermediate[
                "nested_current_state_rows"
            ],
            "sampled_current_state_maximum_binary64": _format(
                intermediate["sampled_current_state_maximum"]
            ),
            "sampled_current_state_argmax_time_binary64": _format(
                intermediate["sampled_current_state_argmax_time"]
            ),
            "sampled_initial_projection_voltage_maximum_binary64": _format(
                intermediate[
                    "sampled_initial_projection_voltage_maximum"
                ]
            ),
            "sampled_initial_projection_voltage_argmax_history_time_binary64": _format(
                intermediate[
                    "sampled_initial_projection_voltage_argmax_history_time"
                ]
            ),
            "sampled_full_history_flow_maximum_on_one_return_binary64": _format(
                intermediate[
                    "sampled_full_history_flow_maximum_on_one_return"
                ]
            ),
            "directed_upper": None,
            "intermediate_stable_flow_norm_upper_validated": False,
        },
        phase_fixed_one_step_diagnostic={
            "nested_signed_voltage_rows": event[
                "nested_signed_voltage_rows"
            ],
            "sampled_signed_voltage_maximum_binary64": _format(
                event["sampled_signed_voltage_maximum"]
            ),
            "sampled_signed_voltage_argmax_time_binary64": _format(
                event["sampled_signed_voltage_argmax_time"]
            ),
            "sampled_raw_voltage_maximum_binary64": _format(
                event["sampled_raw_voltage_maximum"]
            ),
            "sampled_separate_triangle_voltage_maximum_binary64": _format(
                event["sampled_separate_triangle_voltage_maximum"]
            ),
            "recovery_event_row": {
                name: _format(value)
                for name, value in event["recovery_event_row"].items()
            },
            "sampled_phase_fixed_one_step_stable_map_norm_binary64": _format(
                event["sampled_phase_fixed_one_step_stable_map_norm"]
            ),
            "sampled_phase_fixed_separate_triangle_norm_binary64": _format(
                event["sampled_phase_fixed_separate_triangle_norm"]
            ),
            "cancellation_factor_triangle_over_signed_binary64": _format(
                event["cancellation_factor_triangle_over_signed"]
            ),
            "declared_strong_rate_rho_s": _format(
                event["declared_strong_rate_rho_s"]
            ),
            "sampled_margin_to_declared_rho_s_binary64": _format(
                event["sampled_margin_to_declared_rho_s"]
            ),
            "directed_upper": None,
            "phase_fixed_one_step_stable_map_norm_upper_validated": False,
            "k_s_equals_one_validated": False,
        },
        unstable_q_flow_diagnostic={
            "sampled_input_q_section_norm_binary64": _format(
                unstable["sampled_input_q_section_norm"]
            ),
            "sampled_event_q_norm_binary64": _format(
                unstable["sampled_event_q_norm"]
            ),
            "sampled_event_expansion_ratio_binary64": _format(
                unstable["sampled_event_expansion_ratio"]
            ),
            "exact_center_multiplier_exp_root_binary64": _format(
                unstable["exact_center_multiplier_exp_root"]
            ),
            "sampled_raw_current_q_maximum_binary64": _format(
                unstable["sampled_raw_current_q_maximum"]
            ),
            "sampled_raw_current_q_argmax_time_binary64": _format(
                unstable["sampled_raw_current_q_argmax_time"]
            ),
            "status": (
                "separate source-bound scale diagnostic; not used as a "
                "stable-row triangle bound"
            ),
        },
        split_tube_linear_budget_diagnostic={
            "stable_split_radius": _format(split_tube["stable_radius"]),
            "unstable_split_radius": _format(
                split_tube["unstable_radius"]
            ),
            "validated_section_radius": _format(
                split_tube["section_radius"]
            ),
            "coordinate_normalization": (
                "Stage-4E divides the q-q output by ||q^Sigma||_Y^2; "
                "therefore the Stage-4B unstable coordinate is represented "
                "by q^Sigma/||q^Sigma||_Y.  This row uses the sampled q norm "
                "only and remains diagnostic."
            ),
            "stable_formula": "M_s*R_s",
            "sampled_stable_contribution_binary64": _format(
                split_tube["stable_linear_contribution"]
            ),
            "unstable_formula": (
                "(max_[0,T]||U(t)q^Sigma||_Y/||q^Sigma||_Y)*R_u"
            ),
            "sampled_unstable_normalized_flow_ratio_binary64": _format(
                split_tube["unstable_normalized_flow_ratio"]
            ),
            "sampled_unstable_contribution_binary64": _format(
                split_tube["unstable_linear_contribution"]
            ),
            "sampled_linear_tube_total_binary64": _format(
                split_tube["linear_tube_total"]
            ),
            "sampled_remaining_nonlinear_and_directed_error_margin_binary64": _format(
                split_tube[
                    "remaining_nonlinear_and_directed_error_margin"
                ]
            ),
            "sampled_linear_tube_inside_section_radius": (
                split_tube["linear_tube_total"]
                < split_tube["section_radius"]
            ),
            "diagnostic_promoted_to_split_return_tube": False,
        },
        directed_ingress_obstruction={
            "smallest_missing_object": (
                "one common outward piecewise-polynomial enclosure of the "
                "signed two-variable density S(t,theta), including the four "
                "word primitives, Stage-3 q error and Stage-4D measure error"
            ),
            "required_continuous_operations": [
                "Bernstein or monotonic enclosure of the density absolute integral on every support triangle",
                "continuous output-phase supremum on [T-tau1,T]",
                "outward residual bounds for F,C_0,C_1,C_00",
                "parent orbit, q, adjoint-row and normalization uncertainty propagated in the same signed row",
            ],
            "sampled_center_plus_total_directed_error_required_below": _format(
                event["declared_strong_rate_rho_s"]
            ),
            "sampled_center_margin_available_binary64": _format(
                event["sampled_margin_to_declared_rho_s"]
            ),
            "structural_obstruction_found": False,
            "numerical_margin_is_large": True,
            "directed_error_budget_available": False,
            "stable_power_ingress_closed": False,
        },
        claim_status=claims,
    )


def build_stage4h_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = asdict(build_stage4h_artifact(repository))
    parents = {
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
        STRONG_GAP_RESULT_RELATIVE_PATH: STRONG_GAP_RESULT_SHA256,
    }
    return {
        "artifact": artifact,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "artifact_sha256": canonical_sha256(artifact),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": parents,
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "openblas_num_threads": os.environ.get(
                    "OPENBLAS_NUM_THREADS"
                ),
                "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
            },
        },
    }


def validate_stage4h_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    artifact = _mapping(payload.get("artifact"), "Stage-4H artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4H manifest")
    if set(artifact) != {field.name for field in Stage4HArtifact.__dataclass_fields__.values()}:
        raise ValueError("the Stage-4H artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4H identity changed")
    words = _mapping(
        artifact.get("exact_four_word_reduction"), "four-word reduction"
    )
    if (
        words.get("current_resolvent_words")
        != ["empty", "(0)", "(1)", "(0,0)"]
        or words.get("initial_voltage_density_words")
        != ["(0)", "(1)", "(0,0)"]
        or words.get("period_less_than_tau0_plus_tau1") is not True
        or words.get("period_less_than_three_tau0") is not True
    ):
        raise ValueError("the exact four-word support changed")
    split = _mapping(
        artifact.get("continuous_history_split"), "history split"
    )
    if "before total variation" not in str(split.get("stable_projection_identity")):
        raise ValueError("the signed stable projection order changed")
    numerics = _mapping(
        artifact.get("source_bound_numerics"), "source-bound numerics"
    )
    if (
        numerics.get("nested_mesh_spread_is_interval_error") is not False
        or numerics.get("finite_history_nodes_used_as_operator_bound") is not False
    ):
        raise ValueError("a Stage-4H pilot was promoted")
    identity = _mapping(
        artifact.get("rank_one_identity_oracles"), "identity oracles"
    )
    if float(identity["f_q_direct_vs_quadrature_abs_defect_binary64"]) >= 1.0e-10:
        raise ValueError("the Stage-4H pairing oracle changed")
    event = _mapping(
        artifact.get("phase_fixed_one_step_diagnostic"), "one-step row"
    )
    if (
        float(event["sampled_phase_fixed_one_step_stable_map_norm_binary64"])
        >= 0.02
        or float(event["sampled_phase_fixed_separate_triangle_norm_binary64"])
        <= 1.0
        or event.get("directed_upper") is not None
        or event.get("phase_fixed_one_step_stable_map_norm_upper_validated")
        is not False
        or event.get("k_s_equals_one_validated") is not False
    ):
        raise ValueError("the Stage-4H one-step status changed")
    intermediate = _mapping(
        artifact.get("intermediate_signed_flow_diagnostic"),
        "intermediate flow",
    )
    if (
        intermediate.get("directed_upper") is not None
        or intermediate.get("intermediate_stable_flow_norm_upper_validated")
        is not False
    ):
        raise ValueError("the Stage-4H intermediate flow was promoted")
    tube = _mapping(
        artifact.get("split_tube_linear_budget_diagnostic"),
        "split-tube linear diagnostic",
    )
    if (
        float(tube["sampled_linear_tube_total_binary64"]) >= 0.01
        or float(
            tube[
                "sampled_remaining_nonlinear_and_directed_error_margin_binary64"
            ]
        )
        <= 0
        or tube.get("sampled_linear_tube_inside_section_radius") is not True
        or tube.get("diagnostic_promoted_to_split_return_tube") is not False
    ):
        raise ValueError("the Stage-4H split-tube diagnostic changed")
    obstruction = _mapping(
        artifact.get("directed_ingress_obstruction"), "directed obstruction"
    )
    if (
        obstruction.get("directed_error_budget_available") is not False
        or obstruction.get("stable_power_ingress_closed") is not False
        or obstruction.get("structural_obstruction_found") is not False
    ):
        raise ValueError("the Stage-4H open ingress changed")
    claims = _mapping(artifact.get("claim_status"), "Stage-4H claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4H claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4H flag changed")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4H flag was promoted")

    parents = {
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
        STRONG_GAP_RESULT_RELATIVE_PATH: STRONG_GAP_RESULT_SHA256,
    }
    expected_manifest = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest:
        raise ValueError("the Stage-4H manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": parents,
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4H manifest fixed data changed")
    repository = repository.resolve()
    if artifact.get("parent_result_sha256") != parents:
        raise ValueError("the Stage-4H artifact parents changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-4H sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4H source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4H source changed: {relative}")
    for relative, digest in parents.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4H parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "Stage4HArtifact",
    "TRUE_FLAGS",
    "build_stage4h_artifact",
    "build_stage4h_result",
    "canonical_sha256",
    "validate_stage4h_result",
]
