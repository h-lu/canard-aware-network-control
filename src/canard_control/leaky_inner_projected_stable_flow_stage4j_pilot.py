"""Source-bound complete-history pilot for the Stage-4J stable flow.

The pilot evaluates the general-start four-word resolvent, transports the
Stage-4D atom--density covector, retains the unadvanced history translation,
and forms the *complete* projected residual before taking an operator norm.
It is deliberately non-directed: binary Hermite guides, trapezoidal density
integrals, and sampled ``(s,t)`` phases are used only to decide whether a
Taylor--Bernstein Stage-4J proof is numerically credible.

No sampled value in this module is a stable-power certificate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import numpy as np

from canard_control.leaky_inner_signed_stable_flow_stage4h import (
    RESULT_RELATIVE_PATH as STAGE4H_RESULT_RELATIVE_PATH,
    _FourWordDiagnostic,
    validate_stage4h_result,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_inner_word_primitive_stage4i import (
    RESULT_RELATIVE_PATH as STAGE4I_RESULT_RELATIVE_PATH,
    _guide_cells,
    validate_stage4i_result,
)
from canard_control.leaky_route_c_adjoint_stage4d import (
    RESULT_RELATIVE_PATH as STAGE4D_RESULT_RELATIVE_PATH,
    validate_stage4d_result,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    _adjoint_mode_rows,
    _model_uncertainty,
)


SCHEMA_ID = "leaky-inner-projected-stable-flow-stage4j-pilot-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_projected_stable_flow_stage4j_pilot.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_projected_stable_flow_stage4j_pilot.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_projected_stable_flow_stage4j_pilot.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-projected-stable-flow-stage4j-pilot.md"
CONTRACT_RELATIVE_PATH = "docs/leaky-inner-projected-stable-flow-stage4j-contract.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_projected_stable_flow_stage4j_pilot.py"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 "
    "experiments/leaky_inner_projected_stable_flow_stage4j_pilot.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source binding; exact general-start four-word "
    "resolvent identity; binary64 cubic-Hermite primitive guides; sampled "
    "complete-history atom+density rows including unadvanced translation; "
    "same-row projected differential residual; sampled history-boundary, "
    "delay-activation and cell-seam diagnostics; endpoint-only event "
    "projection; trapezoidal history integration and finite phase grids; no "
    "outward bivariate integration, continuous (s,t) supremum, directed "
    "Delta/Khat/Kint, stable power, graph, separator, or onset theorem"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    CONTRACT_RELATIVE_PATH,
)
STAGE3_RESULT_SHA256 = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)
STAGE4D_RESULT_SHA256 = (
    "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
)
STAGE4H_RESULT_SHA256 = (
    "6577a7fcba9888b5126adcd894a361c9436b29a6f619b04f3d54ce5c3218fc15"
)
STAGE4I_RESULT_SHA256 = (
    "1248e9d95444f3cc12565c1e11b4bbeab3d4a9a7bb8922893e38b1ffa439f73e"
)
PINNED_OPENBLAS_NUM_THREADS = "8"
FQ_PHASE_COUNT = 9
KHAT_PHASE_COUNT = 17
RESIDUAL_PHASE_COUNT = 5
FLOW_TIME_COUNT = 9
OUTPUT_HISTORY_COUNT = 9
UNADVANCED_COUNT = 65
HISTORY_NODE_COUNT = 49
RESIDUAL_TIME_COUNT = 9

TRUE_FLAGS = (
    "general_start_four_word_formula_implemented",
    "stage4d_covector_transported_in_coherent_gauge",
    "fq_phase_invariance_sampled",
    "complete_history_atoms_and_density_sampled",
    "unadvanced_translation_identity_block_included",
    "same_double_projected_object_used_for_khat_and_residual",
    "projected_initial_defect_sampled",
    "analytic_double_projection_constraints_encoded",
    "common_projected_residual_formed_before_norm",
    "differential_residual_pilot_computed",
    "history_transport_boundary_pilot_computed",
    "delay_activation_seams_pilot_computed",
    "ordinary_cell_seams_imported_from_stage4i",
    "terminal_event_projection_only",
    "stage4j_directed_upgrade_numerically_supported",
)
FALSE_FLAGS = (
    "pilot_history_quadrature_is_outward",
    "continuous_start_phase_supremum_validated",
    "continuous_output_phase_supremum_validated",
    "common_signed_bivariate_density_integral_validated",
    "analytic_stable_residual_constraint_validated",
    "complete_history_khat_upper_validated",
    "projected_residual_delta_upper_validated",
    "kint_upper_validated",
    "preprojection_endpoint_delta_t_upper_validated",
    "terminal_event_row_error_upper_validated",
    "phase_fixed_one_step_stable_map_norm_upper_validated",
    "stable_power_constant_numeric_upper_validated",
    "k_s_equals_one_validated",
    "split_return_tube_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage4JPilotArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    general_start_four_word_identity: dict[str, Any]
    pilot_discretization: dict[str, Any]
    transported_covector_oracles: dict[str, Any]
    complete_history_khat_pilot: dict[str, Any]
    common_projected_residual_pilot: dict[str, Any]
    terminal_event_budget_pilot: dict[str, Any]
    proof_upgrade_contract: dict[str, Any]
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


def _format(value: float | np.floating[Any]) -> str:
    return format(float(value), ".17g")


def _finite_float(value: object, label: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} is not numeric") from error
    if not math.isfinite(parsed):
        raise ValueError(f"{label} is not finite")
    return parsed


def _load_parent(
    repository: Path,
    relative: str,
    expected_sha256: str,
    validator: Any,
) -> Mapping[str, Any]:
    raw = (repository / relative).read_bytes()
    if sha256(raw).hexdigest() != expected_sha256:
        raise ValueError(f"the bound Stage-4J parent changed: {relative}")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the bound Stage-4J parent is malformed: {relative}")
    validator(payload, repository)
    return payload


class _ProjectedFlowPilot:
    def __init__(self, repository: Path):
        self.diagnostic = _FourWordDiagnostic(repository)
        self.cells = _guide_cells(self.diagnostic)
        self.period = self.diagnostic.period
        self.tau0 = self.diagnostic.tau0
        self.tau1 = self.diagnostic.tau1
        self.taus = (self.tau0, self.tau1)
        self.step = self.tau0 / 512
        self.root = float(self.diagnostic.data.root)
        self.adjoint_v, self.adjoint_w = _adjoint_mode_rows(
            self.diagnostic.data,
            self.diagnostic.tail_v,
            self.diagnostic.tail_w,
        )
        self.theta = np.unique(
            np.concatenate(
                (
                    np.linspace(-self.tau1, 0.0, HISTORY_NODE_COUNT),
                    np.asarray([-self.tau0, -self.tau1, 0.0]),
                )
            )
        )

    def adjoint_atom(self, row: Mapping[int, complex], time: float) -> complex:
        return sum(
            coefficient
            * np.exp(
                (-self.root + 2.0j * math.pi * mode)
                * float(time)
                / self.period
            )
            for mode, coefficient in row.items()
        )

    def f_density(self, phase: float, history_time: float) -> complex:
        total = 0.0j
        for delay_index, delay in enumerate(self.taus):
            if history_time >= -delay - 1.0e-12:
                insertion = phase + history_time + delay
                total += self.adjoint_atom(self.adjoint_v, insertion) * (
                    self.diagnostic.delayed_coefficient(
                        delay_index, insertion
                    )
                )
        return total

    def f_action_on_q_quadrature(self, phase: float) -> complex:
        atom = self.adjoint_atom(
            self.adjoint_v, phase
        ) * self.diagnostic.q_flow(phase)[0]
        atom += self.adjoint_atom(
            self.adjoint_w, phase
        ) * self.diagnostic.q_flow(phase)[1]
        density = np.asarray(
            [
                self.f_density(phase, theta)
                * self.diagnostic.q_flow(phase + theta)[0]
                for theta in self.theta
            ],
            dtype=complex,
        )
        return atom + np.trapezoid(density, self.theta)

    def f_action_on_q_high_order(self, phase: float) -> complex:
        """Binary high-order oracle, kept separate from the pilot grid."""

        atom = self.adjoint_atom(
            self.adjoint_v, phase
        ) * self.diagnostic.q_flow(phase)[0]
        atom += self.adjoint_atom(
            self.adjoint_w, phase
        ) * self.diagnostic.q_flow(phase)[1]
        density = self.diagnostic.integrate(
            lambda history_time: self.f_density(phase, history_time)
            * self.diagnostic.q_flow(phase + history_time)[0],
            (-self.tau1, -self.tau0, 0.0),
        )
        return atom + density

    def normalized_f_norm(self, phase: float) -> float:
        density = np.asarray(
            [abs(self.f_density(phase, theta)) for theta in self.theta]
        )
        numerator = (
            abs(self.adjoint_atom(self.adjoint_v, phase))
            + abs(self.adjoint_atom(self.adjoint_w, phase))
            + float(np.trapezoid(density, self.theta))
        )
        return numerator / abs(self.f_action_on_q_quadrature(phase))

    def _field(
        self, name: str, time: float, derivative: bool = False
    ) -> np.ndarray:
        time = min(max(float(time), 0.0), self.period)
        index = min(int(time / self.step), len(self.cells) - 1)
        cell = self.cells[index]
        local_step = cell.right - cell.left
        coordinate = (time - cell.left) / local_step
        coefficients = getattr(cell, name)
        if not derivative:
            return sum(
                coefficients[..., order] * coordinate**order
                for order in range(4)
            )
        return sum(
            order
            * coefficients[..., order]
            * coordinate ** (order - 1)
            / local_step
            for order in range(1, 4)
        )

    def fundamental(self, time: float, derivative: bool = False) -> np.ndarray:
        return self._field("fundamental", time, derivative)

    def inverse(self, time: float) -> np.ndarray:
        return self._field("inverse", time)

    def primitive(
        self, delay_index: int, time: float, derivative: bool = False
    ) -> np.ndarray:
        return self._field(
            "word0" if delay_index == 0 else "word1",
            time,
            derivative,
        )

    def primitive00(
        self, time: float, derivative: bool = False
    ) -> np.ndarray:
        return self._field("word00", time, derivative)

    def _bracket(
        self, time: float, start: float
    ) -> tuple[np.ndarray, np.ndarray]:
        bracket = np.eye(2, dtype=complex)
        derivative = np.zeros((2, 2), dtype=complex)
        for delay_index, delay in enumerate(self.taus):
            if time > start + delay:
                bracket += self.primitive(
                    delay_index, time
                ) - self.primitive(delay_index, start + delay)
                derivative += self.primitive(
                    delay_index, time, derivative=True
                )
        if time > start + 2 * self.tau0:
            constant = self.primitive(0, start + self.tau0)
            bracket += (
                self.primitive00(time)
                - self.primitive00(start + 2 * self.tau0)
                - (
                    self.primitive(0, time)
                    - self.primitive(0, start + 2 * self.tau0)
                )
                @ constant
            )
            derivative += self.primitive00(
                time, derivative=True
            ) - self.primitive(0, time, derivative=True) @ constant
        return bracket, derivative

    @lru_cache(maxsize=None)
    def resolvent(self, time: float, start: float) -> np.ndarray:
        time = float(time)
        start = float(start)
        if time < start - 1.0e-12:
            return np.zeros((2, 2), dtype=complex)
        bracket, _ = self._bracket(time, start)
        return self.fundamental(time) @ bracket @ self.inverse(start)

    @lru_cache(maxsize=None)
    def differential_residual(self, time: float, start: float) -> np.ndarray:
        time = float(time)
        start = float(start)
        if time <= start + 1.0e-11:
            return np.zeros((2, 2), dtype=complex)
        bracket, bracket_derivative = self._bracket(time, start)
        inverse = self.inverse(start)
        resolvent = self.fundamental(time) @ bracket @ inverse
        derivative = (
            self.fundamental(time, derivative=True) @ bracket
            + self.fundamental(time) @ bracket_derivative
        ) @ inverse
        residual = derivative - self.diagnostic.current_matrix(time) @ resolvent
        for delay_index, delay in enumerate(self.taus):
            if time - delay >= start:
                delayed_matrix = np.asarray(
                    [
                        [
                            self.diagnostic.delayed_coefficient(
                                delay_index, time
                            ),
                            0.0,
                        ],
                        [0.0, 0.0],
                    ]
                )
                residual -= delayed_matrix @ self.resolvent(
                    time - delay, start
                )
        return residual

    def resolvent_density(
        self, time: float, start: float, history_time: float
    ) -> np.ndarray:
        result = np.zeros(2, dtype=complex)
        # At ``time=start`` the active density supports have zero measure.
        # Their endpoint values must not be handed a positive trapezoid
        # weight; the complete raw map is the identity (up to the recorded
        # F-guide inverse defect) at this boundary.
        if time <= start + 1.0e-11:
            return result
        for delay_index, delay in enumerate(self.taus):
            insertion = start + history_time + delay
            if start - 1.0e-12 <= insertion <= time + 1.0e-12:
                result += self.resolvent(time, insertion)[:, 0] * (
                    self.diagnostic.delayed_coefficient(
                        delay_index, insertion
                    )
                )
        return result

    @lru_cache(maxsize=None)
    def f_covector(self, phase: float) -> tuple[np.ndarray, np.ndarray]:
        atom = np.asarray(
            [
                self.adjoint_atom(self.adjoint_v, phase),
                self.adjoint_atom(self.adjoint_w, phase),
            ],
            dtype=complex,
        )
        density = np.asarray(
            [self.f_density(phase, theta) for theta in self.theta],
            dtype=complex,
        )
        return atom, density

    def covector_norm(
        self, atom: np.ndarray, density: np.ndarray
    ) -> float:
        return float(
            np.sum(np.abs(atom))
            + np.trapezoid(np.abs(density), self.theta)
        )

    def covector_action_on_q(
        self, atom: np.ndarray, density: np.ndarray, start: float
    ) -> complex:
        current = self.diagnostic.q_flow(start)
        history = np.asarray(
            [self.diagnostic.q_flow(start + theta)[0] for theta in self.theta]
        )
        return atom @ current + np.trapezoid(
            density * history, self.theta
        )

    @lru_cache(maxsize=None)
    def raw_guide_row(
        self, output_time: float, start: float, component: int
    ) -> tuple[np.ndarray, np.ndarray]:
        atom = self.resolvent(output_time, start)[component].astype(
            complex
        )
        density = np.asarray(
            [
                self.resolvent_density(
                    output_time, start, history_time
                )[component]
                for history_time in self.theta
            ],
            dtype=complex,
        )
        return atom, density

    def _composition_grid(self, time: float, start: float) -> np.ndarray:
        lower = max(-self.tau1, start - time)
        candidates = [
            lower,
            0.0,
            -self.tau0,
            start - time,
            start + self.tau0 - time,
            start + self.tau1 - time,
            start + 2.0 * self.tau0 - time,
        ]
        candidates.extend(np.linspace(lower, 0.0, HISTORY_NODE_COUNT))
        return np.unique(
            np.asarray(
                [
                    value
                    for value in candidates
                    if lower - 1.0e-13 <= value <= 1.0e-13
                ],
                dtype=float,
            )
        )

    def _raw_row(
        self,
        output_time: float,
        start: float,
        component: int,
        residual: bool,
    ) -> tuple[np.ndarray, np.ndarray]:
        if residual:
            if output_time <= start + 1.0e-11:
                return (
                    np.zeros(2, dtype=complex),
                    np.zeros(len(self.theta), dtype=complex),
                )
            atom, density = self._raw_residual_rows(output_time, start)
            return atom[component], density[component]
        return self.raw_guide_row(output_time, start, component)

    def _compose_output_covector(
        self, time: float, start: float, residual: bool
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return ``f_t A`` for the same complete-history raw guide ``A``."""

        voltage_atom, voltage_density = self._raw_row(
            time, start, 0, residual
        )
        recovery_atom, recovery_density = self._raw_row(
            time, start, 1, residual
        )
        atom = (
            self.adjoint_atom(self.adjoint_v, time) * voltage_atom
            + self.adjoint_atom(self.adjoint_w, time) * recovery_atom
        )
        density = (
            self.adjoint_atom(self.adjoint_v, time) * voltage_density
            + self.adjoint_atom(self.adjoint_w, time) * recovery_density
        )

        eta = self._composition_grid(time, start)
        if len(eta) >= 2:
            history_atoms = []
            history_densities = []
            weights = []
            for history_time in eta:
                row_atom, row_density = self._raw_row(
                    time + history_time, start, 0, residual
                )
                history_atoms.append(row_atom)
                history_densities.append(row_density)
                weights.append(self.f_density(time, history_time))
            history_atoms_array = np.asarray(history_atoms)
            history_densities_array = np.asarray(history_densities)
            weights_array = np.asarray(weights)
            atom = atom + np.asarray(
                [
                    np.trapezoid(
                        weights_array * history_atoms_array[:, column], eta
                    )
                    for column in range(2)
                ]
            )
            density = density + np.asarray(
                [
                    np.trapezoid(
                        weights_array
                        * history_densities_array[:, history_index],
                        eta,
                    )
                    for history_index in range(len(self.theta))
                ]
            )

        # For the raw evolution guide, output histories before ``start`` are
        # the exact translated input.  Composing that identity block with the
        # output density produces a shifted *input density*.  A residual has
        # no such unadvanced block.
        if not residual and time - start < self.tau1:
            elapsed = time - start
            for history_index, input_history_time in enumerate(self.theta):
                output_history_time = input_history_time - elapsed
                if (
                    -self.tau1 - 1.0e-13
                    <= output_history_time
                    and (
                        output_history_time < start - time - 1.0e-13
                        or (
                            abs(elapsed) <= 1.0e-13
                            and output_history_time <= 1.0e-13
                        )
                    )
                ):
                    density[history_index] += self.f_density(
                        time, output_history_time
                    )
        return atom, density

    @lru_cache(maxsize=None)
    def guide_composition(
        self, time: float, start: float
    ) -> tuple[np.ndarray, np.ndarray]:
        return self._compose_output_covector(time, start, residual=False)

    @lru_cache(maxsize=None)
    def residual_composition(
        self, time: float, start: float
    ) -> tuple[np.ndarray, np.ndarray]:
        return self._compose_output_covector(time, start, residual=True)

    def double_projected_covector(
        self,
        raw_atom: np.ndarray,
        raw_density: np.ndarray,
        output_q_value: complex,
        outer_time: float,
        start: float,
        composition: tuple[np.ndarray, np.ndarray],
        raw_action_on_q: complex | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Form one row of ``P_t A P_s`` before taking absolute values."""

        f_start_atom, f_start_density = self.f_covector(start)
        denominator_start = self.covector_action_on_q(
            f_start_atom, f_start_density, start
        )
        if raw_action_on_q is None:
            raw_action_on_q = self.covector_action_on_q(
                raw_atom, raw_density, start
            )
        composition_atom, composition_density = composition
        composition_action = self.covector_action_on_q(
            composition_atom, composition_density, start
        )
        right_projected_atom = (
            composition_atom
            - composition_action * f_start_atom / denominator_start
        )
        right_projected_density = (
            composition_density
            - composition_action * f_start_density / denominator_start
        )
        # ``output_q_value`` is a component of the complete q history at the
        # outer time, whereas the left denominator is normalized at that
        # outer state time (not at the output-history time).
        f_time_atom, f_time_density = self.f_covector(outer_time)
        denominator_time = self.covector_action_on_q(
            f_time_atom, f_time_density, outer_time
        )
        atom = (
            raw_atom
            - raw_action_on_q * f_start_atom / denominator_start
            - output_q_value * right_projected_atom / denominator_time
        )
        density = (
            raw_density
            - raw_action_on_q * f_start_density / denominator_start
            - output_q_value * right_projected_density / denominator_time
        )
        return atom, density

    def complete_history_norm(
        self, time: float, start: float
    ) -> tuple[float, str]:
        composition = self.guide_composition(time, start)
        recovery_atom, recovery_density = self.raw_guide_row(
            time, start, 1
        )
        projected_atom, projected_density = self.double_projected_covector(
            recovery_atom,
            recovery_density,
            self.diagnostic.q_flow(time)[1],
            time,
            start,
            composition,
        )
        maximum = self.covector_norm(projected_atom, projected_density)
        source = "propagated_recovery"

        propagated_left = max(start, time - self.tau1)
        for output_time in np.linspace(
            propagated_left, time, OUTPUT_HISTORY_COUNT
        ):
            raw_atom, raw_density = self.raw_guide_row(
                float(output_time), start, 0
            )
            projected_atom, projected_density = (
                self.double_projected_covector(
                    raw_atom,
                    raw_density,
                    self.diagnostic.q_flow(float(output_time))[0],
                    time,
                    start,
                    composition,
                )
            )
            value = self.covector_norm(projected_atom, projected_density)
            if value > maximum:
                maximum = value
                source = "propagated_voltage_history"

        unadvanced_left = time - self.tau1
        if unadvanced_left < start:
            for output_time in np.linspace(
                unadvanced_left,
                start,
                UNADVANCED_COUNT,
                endpoint=False,
            ):
                zeros_atom = np.zeros(2, dtype=complex)
                zeros_density = np.zeros(len(self.theta), dtype=complex)
                q_value = self.diagnostic.q_flow(float(output_time))[0]
                projected_atom, projected_density = (
                    self.double_projected_covector(
                        zeros_atom,
                        zeros_density,
                        q_value,
                        time,
                        start,
                        composition,
                        raw_action_on_q=q_value,
                    )
                )
                value = 1.0 + self.covector_norm(
                    projected_atom, projected_density
                )
                if value > maximum:
                    maximum = value
                    source = "unadvanced_translation_identity"
        return maximum, source

    def _raw_residual_rows(
        self, time: float, start: float
    ) -> tuple[np.ndarray, np.ndarray]:
        if time <= start + 1.0e-11:
            return (
                np.zeros((2, 2), dtype=complex),
                np.zeros((2, len(self.theta)), dtype=complex),
            )
        atom = self.differential_residual(time, start)
        density = np.zeros((2, len(self.theta)), dtype=complex)
        for history_index, history_time in enumerate(self.theta):
            for delay_index, delay in enumerate(self.taus):
                insertion = start + history_time + delay
                if start <= insertion < time:
                    density[:, history_index] += self.differential_residual(
                        time, insertion
                    )[:, 0] * self.diagnostic.delayed_coefficient(
                        delay_index, insertion
                    )
        return atom, density

    def common_projected_residual_norm(
        self, time: float, start: float
    ) -> float:
        composition = self.residual_composition(time, start)
        eta = np.unique(
            np.concatenate(
                (
                    np.linspace(-self.tau1, 0.0, HISTORY_NODE_COUNT),
                    np.asarray([-self.tau0, -self.tau1, 0.0, start - time]),
                )
            )
        )
        eta = eta[(eta >= -self.tau1) & (eta <= 0.0)]
        maximum = 0.0
        for history_time in eta:
            output_time = time + history_time
            raw_atom, raw_density = self._raw_row(
                float(output_time), start, 0, residual=True
            )
            atom, density = self.double_projected_covector(
                raw_atom,
                raw_density,
                self.diagnostic.q_flow(float(output_time))[0],
                time,
                start,
                composition,
            )
            maximum = max(
                maximum,
                self.covector_norm(atom, density),
            )
        current_atom, current_density = self._raw_residual_rows(time, start)
        atom, density = self.double_projected_covector(
            current_atom[1],
            current_density[1],
            self.diagnostic.q_flow(time)[1],
            time,
            start,
            composition,
        )
        return max(
            maximum,
            self.covector_norm(atom, density),
        )

    def projected_initial_defect_norm(self, start: float) -> float:
        """Sample ``||P_s-P_s A(s,s)P_s||`` in the complete norm."""

        composition = self.guide_composition(start, start)
        f_atom, f_density = self.f_covector(start)
        denominator = self.covector_action_on_q(f_atom, f_density, start)
        maximum = 0.0
        for output_time in np.linspace(
            start - self.tau1,
            start,
            UNADVANCED_COUNT,
            endpoint=False,
        ):
            q_value = self.diagnostic.q_flow(float(output_time))[0]
            guide_atom, guide_density = self.double_projected_covector(
                np.zeros(2, dtype=complex),
                np.zeros(len(self.theta), dtype=complex),
                q_value,
                start,
                start,
                composition,
                raw_action_on_q=q_value,
            )
            exact_atom = -q_value * f_atom / denominator
            exact_density = -q_value * f_density / denominator
            maximum = max(
                maximum,
                self.covector_norm(
                    exact_atom - guide_atom,
                    exact_density - guide_density,
                ),
            )
        for component in range(2):
            raw_atom, raw_density = self.raw_guide_row(
                start, start, component
            )
            q_value = self.diagnostic.q_flow(start)[component]
            guide_atom, guide_density = self.double_projected_covector(
                raw_atom,
                raw_density,
                q_value,
                start,
                start,
                composition,
            )
            exact_atom = np.eye(2, dtype=complex)[component]
            exact_atom = exact_atom - q_value * f_atom / denominator
            exact_density = -q_value * f_density / denominator
            maximum = max(
                maximum,
                self.covector_norm(
                    exact_atom - guide_atom,
                    exact_density - guide_density,
                ),
            )
        return maximum

    def history_transport_boundary_defect_norm(self, start: float) -> float:
        """Boundary jump between translated and newly propagated history."""

        f_atom, f_density = self.f_covector(start)
        denominator = self.covector_action_on_q(f_atom, f_density, start)
        raw_atom = self.resolvent(start, start)[0] - np.asarray([1.0, 0.0])
        raw_density = np.zeros(len(self.theta), dtype=complex)
        raw_action = self.covector_action_on_q(
            raw_atom, raw_density, start
        )
        atom = raw_atom - raw_action * f_atom / denominator
        density = raw_density - raw_action * f_density / denominator
        return self.covector_norm(atom, density)

    def source_bound_payload(self) -> dict[str, Any]:
        fq_phase_grid = np.linspace(0.0, self.period, FQ_PHASE_COUNT)
        fq_rows = []
        for phase in fq_phase_grid:
            value = self.f_action_on_q_quadrature(float(phase))
            high_order = self.f_action_on_q_high_order(float(phase))
            fq_rows.append(
                {
                    "phase": _format(phase),
                    "pilot_trapezoid_real": _format(value.real),
                    "pilot_trapezoid_imag": _format(value.imag),
                    "pilot_trapezoid_vs_high_order": _format(
                        abs(value - high_order)
                    ),
                    "high_order_real": _format(high_order.real),
                    "high_order_imag": _format(high_order.imag),
                    "high_order_defect_from_phase_zero_direct_action": _format(
                        abs(high_order - self.diagnostic.fq)
                    ),
                    "sampled_normalized_f_norm": _format(
                        self.normalized_f_norm(float(phase))
                    ),
                }
            )

        resolvent_oracle = max(
            np.max(
                abs(
                    self.resolvent(float(time), 0.0)
                    - self.diagnostic.resolvent_atom(float(time))
                )
            )
            for time in np.linspace(0.0, self.period, 17)
        )

        khat_phase_grid = np.linspace(
            0.0, self.period, KHAT_PHASE_COUNT
        )
        khat = 0.0
        khat_argmax = (0.0, 0.0)
        khat_source = ""
        for start in khat_phase_grid:
            times = (
                np.asarray([start])
                if start == self.period
                else np.linspace(start, self.period, FLOW_TIME_COUNT)
            )
            for time in times:
                value, source = self.complete_history_norm(
                    float(time), float(start)
                )
                if value > khat:
                    khat = value
                    khat_argmax = (float(start), float(time))
                    khat_source = source

        residual_rows = []
        differential_integral_sampled = 0.0
        delta_argmax_start = 0.0
        delta_t_sampled = 0.0
        residual_point_maximum = 0.0
        residual_phase_grid = np.linspace(
            0.0, self.period, RESIDUAL_PHASE_COUNT
        )
        residual_phases = residual_phase_grid[:-1]
        initial_defect = 0.0
        initial_defect_argmax = 0.0
        history_boundary_defect = 0.0
        history_boundary_argmax = 0.0
        for start in residual_phase_grid:
            value = self.projected_initial_defect_norm(float(start))
            if value > initial_defect:
                initial_defect = value
                initial_defect_argmax = float(start)
            value = self.history_transport_boundary_defect_norm(float(start))
            if value > history_boundary_defect:
                history_boundary_defect = value
                history_boundary_argmax = float(start)
        for start in residual_phases:
            times = np.linspace(start, self.period, RESIDUAL_TIME_COUNT)
            values = []
            for time in times:
                if time == start:
                    value = 0.0
                else:
                    shifted = float(time)
                    for activation in (
                        start + self.tau0,
                        start + self.tau1,
                        start + 2 * self.tau0,
                    ):
                        if abs(shifted - activation) < 1.0e-8:
                            shifted = min(self.period, shifted + 2.0e-8)
                    value = self.common_projected_residual_norm(
                        shifted, float(start)
                    )
                values.append(value)
                residual_point_maximum = max(
                    residual_point_maximum, value
                )
            integral = float(np.trapezoid(values, times))
            residual_rows.append(
                {
                    "start_phase": _format(start),
                    "sampled_integral": _format(integral),
                    "sampled_point_maximum": _format(max(values)),
                }
            )
            if integral > differential_integral_sampled:
                differential_integral_sampled = integral
                delta_argmax_start = float(start)
            if start == 0.0:
                delta_t_sampled = integral

        stage4i_payload = json.loads(
            (
                self.diagnostic.data.repository
                / STAGE4I_RESULT_RELATIVE_PATH
            ).read_text(encoding="utf-8")
        )["artifact"]
        stage4i_residual = stage4i_payload["directed_residual_certificate"]
        seam_values = [
            float(value)
            for value in stage4i_residual[
                "maximum_intercell_guide_jump_infinity_upper"
            ].values()
        ]
        maximum_cell_seam = max(seam_values)
        cell_count = int(stage4i_residual["cell_count"])
        # This is intentionally only a source-bound conversion.  The proof
        # source must re-form each signed seam before taking its norm.
        ordinary_cell_seam_proxy = (
            cell_count * sum(seam_values) * (1.0 + 2.0 * khat)
        )
        activation_jump_proxy = 0.0
        for start in residual_phases:
            for delay in (self.tau0, self.tau1, 2.0 * self.tau0):
                activation = float(start + delay)
                if activation < self.period:
                    left = np.nextafter(activation, -math.inf)
                    right = np.nextafter(activation, math.inf)
                    raw_jump = self.resolvent(right, float(start)) - self.resolvent(
                        left, float(start)
                    )
                    activation_jump_proxy = max(
                        activation_jump_proxy,
                        float(np.max(np.sum(abs(raw_jump), axis=1)))
                        * (1.0 + 2.0 * khat),
                    )
        delta_sampled = (
            initial_defect
            + differential_integral_sampled
            + history_boundary_defect
            + activation_jump_proxy
            + ordinary_cell_seam_proxy
        )
        delta_t_sampled = (
            delta_t_sampled
            + initial_defect
            + history_boundary_defect
            + activation_jump_proxy
            + ordinary_cell_seam_proxy
        )
        kint_sampled = khat / (1.0 - delta_sampled)
        uncertainty = _model_uncertainty(self.diagnostic.data)
        c_pi = 1.0 + (
            uncertainty["xdot_bound"]
            / uncertainty["event_speed_lower"]
        )
        ratio_error = (
            uncertainty["xdot_error"]
            / uncertainty["event_speed_lower"]
            + uncertainty["xdot_bound"]
            * uncertainty["xdot_error"]
            / uncertainty["event_speed_lower"] ** 2
        )
        epsilon_pi = khat * ratio_error
        stage4h = json.loads(
            (
                self.diagnostic.data.repository
                / STAGE4H_RESULT_RELATIVE_PATH
            ).read_text(encoding="utf-8")
        )["artifact"]
        sampled_terminal_center = float(
            stage4h["phase_fixed_one_step_diagnostic"][
                "sampled_phase_fixed_one_step_stable_map_norm_binary64"
            ]
        )
        terminal_proxy = (
            sampled_terminal_center
            + c_pi * kint_sampled * delta_t_sampled
            + epsilon_pi
        )

        binary_inverse_boundary_defect = max(
            np.max(
                np.sum(
                    abs(
                        self.fundamental(float(phase))
                        @ self.inverse(float(phase))
                        - np.eye(2)
                    ),
                    axis=1,
                )
            )
            for phase in residual_phase_grid
        )
        activation_residual = 0.0
        for start in residual_phases:
            for delay in (self.tau0, self.tau1, 2 * self.tau0):
                time = float(start + delay)
                if time < self.period:
                    activation_residual = max(
                        activation_residual,
                        float(
                            np.max(
                                np.sum(
                                    abs(
                                        self.differential_residual(
                                            time + 2.0e-8,
                                            float(start),
                                        )
                                    ),
                                    axis=1,
                                )
                            )
                        ),
                    )

        return {
            "fq_rows": fq_rows,
            "resolvent_oracle": resolvent_oracle,
            "khat": khat,
            "khat_argmax": khat_argmax,
            "khat_source": khat_source,
            "residual_rows": residual_rows,
            "delta": delta_sampled,
            "differential_integral": differential_integral_sampled,
            "delta_argmax_start": delta_argmax_start,
            "delta_t": delta_t_sampled,
            "residual_point_maximum": residual_point_maximum,
            "kint": kint_sampled,
            "c_pi": c_pi,
            "epsilon_pi": epsilon_pi,
            "terminal_center": sampled_terminal_center,
            "terminal_proxy": terminal_proxy,
            "initial_defect": initial_defect,
            "initial_defect_argmax": initial_defect_argmax,
            "history_boundary_defect": history_boundary_defect,
            "history_boundary_argmax": history_boundary_argmax,
            "binary_inverse_boundary_defect": binary_inverse_boundary_defect,
            "activation_jump_proxy": activation_jump_proxy,
            "ordinary_cell_seam_proxy": ordinary_cell_seam_proxy,
            "maximum_cell_seam": maximum_cell_seam,
            "activation_residual": activation_residual,
        }


def build_stage4j_pilot_artifact(repository: Path) -> Stage4JPilotArtifact:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the Stage-4J pilot requires OPENBLAS_NUM_THREADS="
            + PINNED_OPENBLAS_NUM_THREADS
        )
    repository = repository.resolve()
    parents = {
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
        STAGE4H_RESULT_RELATIVE_PATH: STAGE4H_RESULT_SHA256,
        STAGE4I_RESULT_RELATIVE_PATH: STAGE4I_RESULT_SHA256,
    }
    _load_parent(
        repository,
        STAGE3_RESULT_RELATIVE_PATH,
        STAGE3_RESULT_SHA256,
        validate_stage3_stable_projection_result,
    )
    _load_parent(
        repository,
        STAGE4D_RESULT_RELATIVE_PATH,
        STAGE4D_RESULT_SHA256,
        validate_stage4d_result,
    )
    _load_parent(
        repository,
        STAGE4H_RESULT_RELATIVE_PATH,
        STAGE4H_RESULT_SHA256,
        validate_stage4h_result,
    )
    stage4i = _load_parent(
        repository,
        STAGE4I_RESULT_RELATIVE_PATH,
        STAGE4I_RESULT_SHA256,
        validate_stage4i_result,
    )
    pilot = _ProjectedFlowPilot(repository)
    values = pilot.source_bound_payload()
    stage4i_artifact = _mapping(stage4i.get("artifact"), "Stage-4I artifact")
    stage4i_residual = _mapping(
        stage4i_artifact.get("directed_residual_certificate"),
        "Stage-4I residual",
    )
    seam = _mapping(
        stage4i_residual.get(
            "maximum_intercell_guide_jump_infinity_upper"
        ),
        "Stage-4I seam",
    )
    maximum_seam = max(float(value) for value in seam.values())
    if not (
        values["resolvent_oracle"] < 1.0e-7
        and values["delta"] < 1.0e-3
        and values["terminal_proxy"] < 0.1
        and maximum_seam < 1.0e-12
    ):
        raise ArithmeticError("the Stage-4J source-bound pilot lost feasibility")
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4JPilotArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256=parents,
        general_start_four_word_identity={
            "period": _format(pilot.period),
            "tau0": _format(pilot.tau0),
            "tau1": _format(pilot.tau1),
            "active_words": ["empty", "(0)", "(1)", "(0,0)"],
            "formula": (
                "R(t,s)=F(t)[I+dC0+dC1+dC00-"
                "(C0(t)-C0(s+2*tau0))*C0(s+tau0)]G(s), with each "
                "difference active only after its exact delay threshold"
            ),
            "stage4h_s_zero_resolvent_oracle_binary64": _format(
                values["resolvent_oracle"]
            ),
            "support_status": (
                "analytic finite-word identity on t-s<=T; the oracle checks "
                "only the binary implementation"
            ),
        },
        pilot_discretization={
            "fq_phase_count": FQ_PHASE_COUNT,
            "khat_start_phase_count": KHAT_PHASE_COUNT,
            "residual_start_phase_count": RESIDUAL_PHASE_COUNT,
            "flow_time_count_per_phase": FLOW_TIME_COUNT,
            "output_history_count": OUTPUT_HISTORY_COUNT,
            "unadvanced_time_count": UNADVANCED_COUNT,
            "history_node_count": len(pilot.theta),
            "residual_time_count_per_phase": RESIDUAL_TIME_COUNT,
            "primitive_guide_cells": len(pilot.cells),
            "history_integration": "binary64 trapezoidal pilot",
            "finite_history_nodes_promoted_to_operator_bound": False,
        },
        transported_covector_oracles={
            "rows": values["fq_rows"],
            "phase_zero_density_vs_stage4h_formula": (
                "same p_v(theta+tau_j)b_j(theta+tau_j) formula"
            ),
            "transport_gauge": (
                "p(t)=exp(-s_u*t/T)r(t/T), q(t)=U(t,0)q^Sigma; "
                "f_t(q_t) is invariant"
            ),
        },
        complete_history_khat_pilot={
            "sampled_khat_binary64": _format(values["khat"]),
            "sampled_argmax_start_phase": _format(
                values["khat_argmax"][0]
            ),
            "sampled_argmax_end_time": _format(
                values["khat_argmax"][1]
            ),
            "sampled_argmax_block": values["khat_source"],
            "unadvanced_formula": (
                "1+|q_v(u)|*||f_s/f_s(q_s)|| for u<s, because the "
                "translated point atom is singular to the atom+density row"
            ),
            "current_atoms_included": True,
            "unadvanced_translation_identity_included": True,
            "directed_khat_upper": None,
        },
        common_projected_residual_pilot={
            "construction_order": (
                "assemble the same complete raw operator A; form "
                "P_t A P_s for both Khat and the residual, retaining all "
                "correlated atom+density terms; only then take row norms"
            ),
            "differential_residual_rows": values["residual_rows"],
            "sampled_differential_integral_supremum_binary64": _format(
                values["differential_integral"]
            ),
            "sampled_delta_binary64": _format(values["delta"]),
            "sampled_delta_argmax_start_phase": _format(
                values["delta_argmax_start"]
            ),
            "sampled_point_residual_maximum_binary64": _format(
                values["residual_point_maximum"]
            ),
            "sampled_projected_initial_defect_binary64": _format(
                values["initial_defect"]
            ),
            "sampled_projected_initial_defect_argmax_phase": _format(
                values["initial_defect_argmax"]
            ),
            "sampled_history_transport_boundary_defect_binary64": _format(
                values["history_boundary_defect"]
            ),
            "sampled_history_transport_boundary_argmax_phase": _format(
                values["history_boundary_argmax"]
            ),
            "sampled_binary_inverse_boundary_defect_binary64": _format(
                values["binary_inverse_boundary_defect"]
            ),
            "sampled_delay_activation_jump_proxy_binary64": _format(
                values["activation_jump_proxy"]
            ),
            "sampled_delay_activation_right_residual_binary64": _format(
                values["activation_residual"]
            ),
            "sampled_ordinary_cell_seam_conversion_proxy_binary64": _format(
                values["ordinary_cell_seam_proxy"]
            ),
            "stage4i_maximum_cell_seam_infinity_upper": _format(
                values["maximum_cell_seam"]
            ),
            "sampled_delta_sum_includes_initial_boundary_activation_and_cell_seams": True,
            "history_transport_boundary_included": True,
            "delay_activation_seams_included": True,
            "ordinary_cell_seams_included": True,
            "directed_delta_upper": None,
            "analytic_stable_constraint_validated": False,
            "double_projection_formula": "P_t A P_s",
            "algebraic_constraint_status": (
                "encoded exactly at formula level; a directed enclosure of "
                "the transported rows and normalization is still open"
            ),
        },
        terminal_event_budget_pilot={
            "sampled_kint_binary64": _format(values["kint"]),
            "sampled_preprojection_delta_t_binary64": _format(
                values["delta_t"]
            ),
            "directed_c_pi_t_upper": _format(values["c_pi"]),
            "sampled_event_row_error_proxy_binary64": _format(
                values["epsilon_pi"]
            ),
            "stage4h_sampled_terminal_signed_center_binary64": _format(
                values["terminal_center"]
            ),
            "sampled_terminal_ms_proxy_binary64": _format(
                values["terminal_proxy"]
            ),
            "event_projection_location": "terminal_time_only",
            "moving_pi_t_used": False,
            "directed_kint_upper": None,
            "directed_preprojection_delta_t_upper": None,
            "directed_epsilon_pi_t_upper": None,
            "directed_terminal_ms_upper": None,
        },
        proof_upgrade_contract={
            "numerically_feasible": True,
            "next_object": (
                "192-bit bivariate Taylor--Bernstein cells for the complete "
                "projected guide and residual, including the unadvanced block"
            ),
            "required_directed_fields": [
                "Khat",
                "Delta",
                "Kint=Khat/(1-Delta)",
                "Delta_T",
                "C_Pi,T",
                "epsilon_Pi,T",
                "terminal_Ms_upper",
            ],
            "promotion_rule": (
                "all continuous signed gates must be directed and terminal "
                "Ms_upper<rho_s before stable power or K_s=1 is true"
            ),
        },
        claim_status=claims,
    )


def build_stage4j_pilot_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = asdict(build_stage4j_pilot_artifact(repository))
    parents = {
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
        STAGE4H_RESULT_RELATIVE_PATH: STAGE4H_RESULT_SHA256,
        STAGE4I_RESULT_RELATIVE_PATH: STAGE4I_RESULT_SHA256,
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
                "openblas_num_threads": os.environ.get(
                    "OPENBLAS_NUM_THREADS"
                ),
                "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
            },
        },
    }


def validate_stage4j_pilot_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    artifact = _mapping(payload.get("artifact"), "Stage-4J pilot artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4J pilot manifest")
    if set(artifact) != set(Stage4JPilotArtifact.__dataclass_fields__):
        raise ValueError("the Stage-4J pilot artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4J pilot identity changed")
    identity = _mapping(
        artifact.get("general_start_four_word_identity"),
        "Stage-4J four-word identity",
    )
    if (
        identity.get("active_words")
        != ["empty", "(0)", "(1)", "(0,0)"]
        or _finite_float(
            identity.get("stage4h_s_zero_resolvent_oracle_binary64"),
            "Stage-4J resolvent oracle",
        )
        >= 1.0e-7
    ):
        raise ValueError("the Stage-4J general-start identity changed")
    discretization = _mapping(
        artifact.get("pilot_discretization"), "Stage-4J discretization"
    )
    if (
        discretization.get("fq_phase_count") != FQ_PHASE_COUNT
        or discretization.get("khat_start_phase_count")
        != KHAT_PHASE_COUNT
        or discretization.get("residual_start_phase_count")
        != RESIDUAL_PHASE_COUNT
        or discretization.get("finite_history_nodes_promoted_to_operator_bound")
        is not False
        or discretization.get("history_integration")
        != "binary64 trapezoidal pilot"
    ):
        raise ValueError("the Stage-4J pilot discretization changed")
    covariance = _mapping(
        artifact.get("transported_covector_oracles"),
        "Stage-4J transported covector oracles",
    )
    fq_rows = covariance.get("rows")
    if not isinstance(fq_rows, list) or len(fq_rows) != FQ_PHASE_COUNT:
        raise ValueError("the Stage-4J covariance phase grid changed")
    high_order_defects = [
        _finite_float(
            _mapping(row, "Stage-4J covariance row").get(
                "high_order_defect_from_phase_zero_direct_action"
            ),
            "Stage-4J high-order covariance defect",
        )
        for row in fq_rows
    ]
    trapezoid_defects = [
        _finite_float(
            _mapping(row, "Stage-4J covariance row").get(
                "pilot_trapezoid_vs_high_order"
            ),
            "Stage-4J trapezoid defect",
        )
        for row in fq_rows
    ]
    if max(high_order_defects) >= 2.0e-12 or max(trapezoid_defects) <= 1.0e-9:
        raise ValueError("the Stage-4J covariance diagnostic changed")
    khat = _mapping(
        artifact.get("complete_history_khat_pilot"), "Stage-4J Khat pilot"
    )
    khat_value = _finite_float(
        khat.get("sampled_khat_binary64"), "Stage-4J sampled Khat"
    )
    if (
        khat.get("current_atoms_included") is not True
        or khat.get("unadvanced_translation_identity_included") is not True
        or khat.get("directed_khat_upper") is not None
        or khat.get("sampled_argmax_block")
        != "unadvanced_translation_identity"
        or not 15.0 < khat_value < 20.0
    ):
        raise ValueError("the Stage-4J Khat pilot changed")
    residual = _mapping(
        artifact.get("common_projected_residual_pilot"),
        "Stage-4J residual pilot",
    )
    differential = _finite_float(
        residual.get("sampled_differential_integral_supremum_binary64"),
        "Stage-4J sampled differential integral",
    )
    initial = _finite_float(
        residual.get("sampled_projected_initial_defect_binary64"),
        "Stage-4J sampled initial defect",
    )
    boundary = _finite_float(
        residual.get("sampled_history_transport_boundary_defect_binary64"),
        "Stage-4J sampled history boundary",
    )
    activation = _finite_float(
        residual.get("sampled_delay_activation_jump_proxy_binary64"),
        "Stage-4J sampled activation seam",
    )
    ordinary = _finite_float(
        residual.get(
            "sampled_ordinary_cell_seam_conversion_proxy_binary64"
        ),
        "Stage-4J sampled ordinary seams",
    )
    delta = _finite_float(
        residual.get("sampled_delta_binary64"), "Stage-4J sampled Delta"
    )
    if (
        residual.get("history_transport_boundary_included") is not True
        or residual.get("delay_activation_seams_included") is not True
        or residual.get("ordinary_cell_seams_included") is not True
        or residual.get(
            "sampled_delta_sum_includes_initial_boundary_activation_and_cell_seams"
        )
        is not True
        or residual.get("double_projection_formula") != "P_t A P_s"
        or residual.get("directed_delta_upper") is not None
        or residual.get("analytic_stable_constraint_validated") is not False
        or not 0.0 < delta < 1.0e-3
        or initial <= 0.0
        or boundary < 0.0
        or activation < 0.0
        or ordinary < 0.0
        or abs(delta - (differential + initial + boundary + activation + ordinary))
        > 1.0e-15
    ):
        raise ValueError("the Stage-4J residual pilot changed")
    terminal = _mapping(
        artifact.get("terminal_event_budget_pilot"),
        "Stage-4J terminal pilot",
    )
    kint = _finite_float(
        terminal.get("sampled_kint_binary64"), "Stage-4J sampled Kint"
    )
    delta_t = _finite_float(
        terminal.get("sampled_preprojection_delta_t_binary64"),
        "Stage-4J sampled Delta_T",
    )
    c_pi = _finite_float(
        terminal.get("directed_c_pi_t_upper"), "Stage-4J event factor"
    )
    epsilon_pi = _finite_float(
        terminal.get("sampled_event_row_error_proxy_binary64"),
        "Stage-4J event error proxy",
    )
    center = _finite_float(
        terminal.get("stage4h_sampled_terminal_signed_center_binary64"),
        "Stage-4J terminal center",
    )
    terminal_proxy = _finite_float(
        terminal.get("sampled_terminal_ms_proxy_binary64"),
        "Stage-4J terminal proxy",
    )
    if (
        terminal.get("event_projection_location") != "terminal_time_only"
        or terminal.get("moving_pi_t_used") is not False
        or terminal.get("directed_kint_upper") is not None
        or terminal.get("directed_preprojection_delta_t_upper") is not None
        or terminal.get("directed_epsilon_pi_t_upper") is not None
        or terminal.get("directed_terminal_ms_upper") is not None
        or not 1.0 < c_pi < 3.0
        or not 0.0 < terminal_proxy < 0.1
        or abs(kint - khat_value / (1.0 - delta)) > 1.0e-12
        or abs(terminal_proxy - (center + c_pi * kint * delta_t + epsilon_pi))
        > 1.0e-12
    ):
        raise ValueError("the Stage-4J terminal pilot changed")
    claims = _mapping(artifact.get("claim_status"), "Stage-4J claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4J claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4J pilot fact changed")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4J theorem was promoted")

    parents = {
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
        STAGE4H_RESULT_RELATIVE_PATH: STAGE4H_RESULT_SHA256,
        STAGE4I_RESULT_RELATIVE_PATH: STAGE4I_RESULT_SHA256,
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
        raise ValueError("the Stage-4J pilot manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": parents,
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4J pilot manifest fixed data changed")
    repository = repository.resolve()
    if artifact.get("parent_result_sha256") != parents:
        raise ValueError("the Stage-4J pilot parents changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-4J sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4J pilot source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4J pilot source changed: {relative}")
    for relative, expected in parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"the Stage-4J pilot parent changed: {relative}")


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
    "Stage4JPilotArtifact",
    "TRUE_FLAGS",
    "build_stage4j_pilot_artifact",
    "build_stage4j_pilot_result",
    "canonical_sha256",
    "validate_stage4j_pilot_result",
]
