"""Fixed-epsilon quadratic-root BVP contract and shooting diagnostic.

The required theorem is a phase-fixed, two-sided, complete-history Lin/trace
BVP.  The repository has no interval solver for that object.  This module
keeps an exact validation contract separate from a binary64 forward-shooting
diagnostic with a prescribed singular-canard older history.  The diagnostic
has no selected repelling trace, full-history jump, dynamic adjoint, or
interval inverse; its section drift is reported to prevent false promotion.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
import math
from typing import Any, Mapping

import numpy as np
from numpy.typing import NDArray
import sympy as sp


MODEL_ID = "synchronous-dual-scaffold-fhn-quadratic-period-lock"
PERIOD_DIAGNOSTIC = 16.54038779818094
DELTA = 1.0 / math.sqrt(5.0)
THETA_PERIOD_DIAGNOSTIC = DELTA * PERIOD_DIAGNOSTIC


@dataclass(frozen=True)
class FixedEpsilonBVPAlgebra:
    """Exact chart and adjoint-column identities at eta=0."""

    delta: sp.Expr
    epsilon: sp.Expr
    physical_delay_0: sp.Expr
    physical_delay_1: sp.Expr
    scaled_delay_0: sp.Expr
    scaled_delay_1: sp.Expr
    scaled_period_delay: sp.Expr
    chart_fast_field: sp.Expr
    chart_slow_field: sp.Expr
    current_linearization: sp.Matrix
    delay_4_linearization: sp.Matrix
    delay_5_linearization: sp.Matrix
    period_delay_linearization_at_eta_zero: sp.Matrix
    eta_vector_field_column: sp.Matrix
    nu_vector_field_column: sp.Matrix
    a_residual_column: sp.Matrix
    eta_residual_column: sp.Matrix
    normalized_energy_gap: sp.Expr
    normalized_energy_gradient: sp.Matrix
    root_response_from_gap: sp.Expr


@dataclass(frozen=True)
class FixedEpsilonBVPContract:
    """Minimum analytic and interval data for a rigorous selected root."""

    model_id: str
    physical_epsilon: str
    physical_horizon: str
    scaled_horizon: str
    state_space: str
    strong_left_domain: str
    strong_right_domain: str
    left_flow_equation: str
    right_flow_equation: str
    entry_trace_equation: str
    exit_trace_equation: str
    phase_equation: str
    complete_history_jump: str
    jump_complement: str
    augmented_operator: str
    dynamic_adjoint: str
    adjoint_normalization: str
    eta_pairing: str
    a_pairing: str
    root_response: str
    collocation_representation: str
    interval_newton_contract: str
    required_validation_gates: tuple[str, ...]


@dataclass(frozen=True)
class ShootingRow:
    """One finite-section forward shooting result."""

    section_half_width: float
    root_bracket: tuple[float, float]
    bracket_sign_margin: float
    nu_root: float
    a_root: float
    gap_residual: float
    gap_nu_derivative: float
    gap_eta_derivative: float
    scalar_gap_inverse_norm: float
    forward_rho: float
    finite_difference_rho: float
    forward_finite_difference_disagreement: float
    eta_difference_step: float
    function_evaluations: int


@dataclass(frozen=True)
class FixedEpsilonQuadraticRootCertificate:
    """Numerical diagnostics and strict claim refusals."""

    model_id: str
    arithmetic: str
    period_input: str
    delta: str
    epsilon: str
    scaled_period_delay: str
    asymptotic_leading_rho_candidate: str
    central_section_half_width: str
    central_nu_candidate: str
    central_a_candidate: str
    central_rho_candidate: str
    section_rho_min: str
    section_rho_max: str
    section_rho_spread: str
    section_a_spread: str
    maximum_gap_residual: str
    minimum_bracket_sign_margin: str
    maximum_forward_finite_difference_disagreement: str
    exact_full_history_bvp_contract_specified: bool
    finite_section_shooting_diagnostic_computed: bool
    prescribed_older_history_is_selected_attracting_trace: bool
    selected_repelling_trace_constructed: bool
    complete_history_jump_solved: bool
    phase_fixed_augmented_inverse_validated: bool
    dynamic_adjoint_validated: bool
    interval_newton_or_radii_polynomial_validated: bool
    endpoint_zero_fiber_implication_validated: bool
    fixed_epsilon_selected_root_validated: bool
    fixed_epsilon_nonzero_rho_validated: bool
    physical_onset_identification_validated: bool


def fixed_epsilon_bvp_algebra() -> FixedEpsilonBVPAlgebra:
    """Return exact synchronous chart, linearization, and response columns."""

    delta = sp.sqrt(5) / 5
    epsilon = sp.Rational(1, 5)
    kappa_1 = sp.Rational(1, 5)
    kappa_3 = sp.Rational(1, 4)
    X, Y, X4, X5, XT, eta, nu = sp.symbols(
        "X Y X4 X5 XT eta nu", real=True
    )
    period = sp.Symbol("T_*", positive=True)
    theta_period = sp.simplify(delta * period)
    fast = (
        Y
        - X**2
        + delta * (-X**3 / 3 + kappa_1 * ((X4 + X5) / 2 - X))
        + delta**2 * eta * (X**2 - XT**2)
        + delta**3 * kappa_3 * ((X4**3 + X5**3) / 2 - X**3)
    )
    slow = -X + delta * nu
    current = sp.Matrix(
        [[sp.diff(fast, X).subs(eta, 0), sp.diff(fast, Y)], [-1, 0]]
    )
    delayed_4 = sp.Matrix(
        [[sp.diff(fast, X4).subs(eta, 0), 0], [0, 0]]
    )
    delayed_5 = sp.Matrix(
        [[sp.diff(fast, X5).subs(eta, 0), 0], [0, 0]]
    )
    delayed_period = sp.Matrix(
        [[sp.diff(fast, XT).subs(eta, 0), 0], [0, 0]]
    )
    eta_column = sp.Matrix([sp.diff(fast, eta).subs(eta, 0), 0])
    nu_column = sp.Matrix([0, sp.diff(slow, nu)])
    V, VT = sp.symbols("V VT", real=True)
    a_residual = sp.Matrix([0, epsilon])
    eta_residual = sp.Matrix(
        [-epsilon * ((V - 1) ** 2 - (VT - 1) ** 2), 0]
    )
    gap = X**2 / 2 - Y / 2 - sp.Rational(1, 4)
    gap_gradient = sp.Matrix([sp.diff(gap, X), sp.diff(gap, Y)])
    g_eta, g_nu = sp.symbols("g_eta g_nu", real=True, nonzero=True)
    response = sp.simplify(delta**2 * (-g_eta / g_nu))
    return FixedEpsilonBVPAlgebra(
        delta=delta,
        epsilon=epsilon,
        physical_delay_0=4 / delta,
        physical_delay_1=5 / delta,
        scaled_delay_0=sp.Integer(4),
        scaled_delay_1=sp.Integer(5),
        scaled_period_delay=theta_period,
        chart_fast_field=sp.expand(fast),
        chart_slow_field=slow,
        current_linearization=sp.simplify(current),
        delay_4_linearization=sp.simplify(delayed_4),
        delay_5_linearization=sp.simplify(delayed_5),
        period_delay_linearization_at_eta_zero=sp.simplify(delayed_period),
        eta_vector_field_column=sp.simplify(eta_column),
        nu_vector_field_column=nu_column,
        a_residual_column=a_residual,
        eta_residual_column=eta_residual,
        normalized_energy_gap=gap,
        normalized_energy_gradient=gap_gradient,
        root_response_from_gap=response,
    )


def fixed_epsilon_bvp_algebra_is_exact(
    algebra: FixedEpsilonBVPAlgebra | None = None,
) -> bool:
    """Check the exact identities used by the validation contract."""

    if algebra is None:
        algebra = fixed_epsilon_bvp_algebra()
    X, XT = sp.symbols("X XT", real=True)
    expected_eta = sp.Matrix(
        [sp.Rational(1, 5) * (X**2 - XT**2), 0]
    )
    g_eta, g_nu = sp.symbols("g_eta g_nu", real=True, nonzero=True)
    return bool(
        algebra.delta == sp.sqrt(5) / 5
        and algebra.epsilon == sp.Rational(1, 5)
        and algebra.physical_delay_0 == 4 * sp.sqrt(5)
        and algebra.physical_delay_1 == 5 * sp.sqrt(5)
        and algebra.period_delay_linearization_at_eta_zero == sp.zeros(2)
        and algebra.eta_vector_field_column == expected_eta
        and algebra.nu_vector_field_column == sp.Matrix([0, sp.sqrt(5) / 5])
        and algebra.root_response_from_gap
        == -sp.Rational(1, 5) * g_eta / g_nu
    )


def reference_fixed_epsilon_bvp_contract() -> FixedEpsilonBVPContract:
    """Return the exact two-sided complete-history validation contract."""

    return FixedEpsilonBVPContract(
        model_id=MODEL_ID,
        physical_epsilon="1/5",
        physical_horizon="h=max{4*sqrt(5),5*sqrt(5),T_*}=T_*",
        scaled_horizon="Theta_h=max{4,5,T_*/sqrt(5)}=T_*/sqrt(5)",
        state_space="C([-h,0],R^2) on the RFDE solution manifold",
        strong_left_domain="W^{2,p}([-L_- - h,0],R^2) plus entry coordinates",
        strong_right_domain="W^{2,p}([-h,L_+],R^2) plus exit coordinates",
        left_flow_equation="x_-'(t)-F(x^-_t;a,eta)=0, -L_-<t<0",
        right_flow_equation="x_+'(t)-F(x^+_t;a,eta)=0, 0<t<L_+",
        entry_trace_equation=(
            "B_-(x^-_{-L_-},xi_-;a,eta)=0 from one fixed "
            "enlarged-horizon attracting selection"
        ),
        exit_trace_equation=(
            "B_+(x^+_{L_+},xi_+;a,eta)=0 from one fixed "
            "backward-extendible repelling selection"
        ),
        phase_equation="c(x^-_0)=V^-(0)-1=0",
        complete_history_jump=(
            "J(theta)=x^-(theta)-x^+(theta), -h<=theta<=0"
        ),
        jump_complement="solve F_BVP(z,a,eta)=d*e with e in the full jump slot",
        augmented_operator="(z_dot,d_dot)->D_z F_BVP z_dot-d_dot*e is an isomorphism",
        dynamic_adjoint=(
            "-p'(t)=A_0(t)^T p(t)+sum_j "
            "1_{t+tau_j in I} A_j(t+tau_j)^T p(t+tau_j), "
            "with entry, exit, phase, seam, and jump multipliers"
        ),
        adjoint_normalization="<Psi,e>=1 and Psi D_z F_BVP=0",
        eta_pairing="m_eta=<Psi,partial_eta F_BVP>, including every endpoint block",
        a_pairing="m_a=<Psi,partial_a F_BVP>, including every endpoint block",
        root_response="rho_*=-m_eta/m_a",
        collocation_representation=(
            "piecewise Chebyshev coefficients on a mesh closed under shifts "
            "by 4*sqrt(5), 5*sqrt(5), and T_*; weighted l1 tails"
        ),
        interval_newton_contract=(
            "Y=||A F(x_bar)||, Z1=||I-A D F(x_bar)||, "
            "Z2(r)>=sup||A(D F(x)-D F(x_bar))||/r, "
            "and Y+(Z1-1)r+Z2(r)r^2<0"
        ),
        required_validation_gates=(
            "construct parameter-coherent entry and exit trace bundles on the enlarged horizon",
            "validate a zero of the full nonlinear BVP",
            "validate the phase-fixed augmented inverse with a tail bound",
            "validate the advanced adjoint and all boundary multipliers",
            "exclude zero from directed enclosures of m_a and m_eta",
            "prove the zero-fiber implication and complete-history injectivity",
            "bound second parameter derivatives on a nonempty eta neighborhood",
            "compare the selected root with an input-independent onset event",
        ),
    )


def _leading_canard(time: float) -> NDArray[np.float64]:
    return np.asarray([-time / 2.0, (time * time - 2.0) / 4.0], dtype=float)


def _shooting_integration(
    nu: float,
    eta: float,
    section_half_width: float,
    *,
    include_sensitivities: bool,
    rtol: float = 2.0e-10,
    atol: float = 2.0e-12,
    max_step: float = 0.04,
) -> tuple[float, float | None, float | None, int]:
    """Integrate the prescribed-history shooting diagnostic.

    Sensitivities use an older history independent of nu and eta.  This is
    intentional and is one reason the result is not a selected-root theorem.
    """

    from scipy.integrate import solve_ivp

    if not section_half_width > 0.0:
        raise ValueError("section_half_width must be positive")
    if not max_step > 0.0 or rtol <= 0.0 or atol <= 0.0:
        raise ValueError("integration tolerances must be positive")
    start = -float(section_half_width)
    stop = float(section_half_width)
    if include_sensitivities:
        initial = np.concatenate((_leading_canard(start), np.zeros(4)))
    else:
        initial = _leading_canard(start)
    completed: list[tuple[float, float, Any]] = []
    evaluations = 0
    left = start

    def prescribed(time: float) -> NDArray[np.float64]:
        base = _leading_canard(time)
        if include_sensitivities:
            return np.concatenate((base, np.zeros(4)))
        return base

    def known(time: float) -> NDArray[np.float64]:
        tolerance = 2.0e-10 * max(1.0, abs(time), abs(left))
        if time <= start + tolerance:
            return prescribed(min(time, start))
        for lower, upper, interpolant in reversed(completed):
            if lower - tolerance <= time <= upper + tolerance:
                clipped = min(max(time, lower), upper)
                return np.asarray(interpolant(clipped), dtype=float)
        raise RuntimeError("shooting method queried an unfinished history")

    while left < stop - 1.0e-14:
        right = min(stop, left + 4.0)

        def rhs(time: float, state: NDArray[np.float64]) -> NDArray[np.float64]:
            delayed_4 = known(time - 4.0)
            delayed_5 = known(time - 5.0)
            delayed_period = known(time - THETA_PERIOD_DIAGNOSTIC)
            x, y = state[:2]
            x4 = delayed_4[0]
            x5 = delayed_5[0]
            xt = delayed_period[0]
            fast = (
                y
                - x * x
                + DELTA
                * (-x**3 / 3.0 + 0.2 * ((x4 + x5) / 2.0 - x))
                + DELTA**2 * eta * (x * x - xt * xt)
                + DELTA**3
                * 0.25
                * ((x4**3 + x5**3) / 2.0 - x**3)
            )
            output = [fast, -x + DELTA * nu]
            if include_sensitivities:
                current_fast = (
                    -2.0 * x
                    + DELTA * (-x * x - 0.2)
                    + DELTA**2 * eta * 2.0 * x
                    + DELTA**3 * 0.25 * (-3.0 * x * x)
                )
                delay_4_fast = (
                    DELTA * 0.1
                    + DELTA**3 * 0.25 * 1.5 * x4 * x4
                )
                delay_5_fast = (
                    DELTA * 0.1
                    + DELTA**3 * 0.25 * 1.5 * x5 * x5
                )
                delay_period_fast = -DELTA**2 * eta * 2.0 * xt
                columns = (
                    (2, 0.0, DELTA),
                    (4, DELTA**2 * (x * x - xt * xt), 0.0),
                )
                for offset, forcing_fast, forcing_slow in columns:
                    sx, sy = state[offset : offset + 2]
                    sx4 = delayed_4[offset]
                    sx5 = delayed_5[offset]
                    sxt = delayed_period[offset]
                    output.extend(
                        (
                            current_fast * sx
                            + sy
                            + delay_4_fast * sx4
                            + delay_5_fast * sx5
                            + delay_period_fast * sxt
                            + forcing_fast,
                            -sx + forcing_slow,
                        )
                    )
            return np.asarray(output, dtype=float)

        solution = solve_ivp(
            rhs,
            (left, right),
            initial,
            method="DOP853",
            dense_output=True,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        )
        if not solution.success or solution.sol is None:
            raise RuntimeError(f"shooting integration failed: {solution.message}")
        evaluations += int(solution.nfev)
        completed.append((left, right, solution.sol))
        initial = np.asarray(solution.y[:, -1], dtype=float)
        if not np.all(np.isfinite(initial)):
            raise RuntimeError("shooting integration produced a nonfinite state")
        left = right

    x, y = initial[:2]
    gap = x * x / 2.0 - y / 2.0 - 0.25
    if not include_sensitivities:
        return float(gap), None, None, evaluations
    gap_nu = x * initial[2] - initial[3] / 2.0
    gap_eta = x * initial[4] - initial[5] / 2.0
    return float(gap), float(gap_nu), float(gap_eta), evaluations


_SECTION_BRACKETS = {
    2.5: (0.125, 0.25),
    3.0: (0.125, 0.25),
    3.5: (0.0, 0.125),
}


def shooting_row(
    section_half_width: float,
    *,
    eta_difference_step: float = 0.001,
) -> ShootingRow:
    """Compute one finite-section root and two sensitivity estimates."""

    from scipy.optimize import brentq

    section = float(section_half_width)
    if section not in _SECTION_BRACKETS:
        raise ValueError("the diagnostic section is not in the pinned table")
    bracket = _SECTION_BRACKETS[section]
    evaluations = 0

    def gap(candidate: float, eta: float = 0.0) -> float:
        nonlocal evaluations
        value, _, _, count = _shooting_integration(
            candidate,
            eta,
            section,
            include_sensitivities=False,
        )
        evaluations += count
        return value

    left_value = gap(bracket[0])
    right_value = gap(bracket[1])
    if left_value * right_value >= 0.0:
        raise RuntimeError("the pinned diagnostic bracket lost its sign change")
    root = brentq(
        lambda candidate: gap(candidate),
        bracket[0],
        bracket[1],
        xtol=2.0e-12,
        rtol=2.0e-12,
    )
    residual, gap_nu, gap_eta, count = _shooting_integration(
        root,
        0.0,
        section,
        include_sensitivities=True,
    )
    evaluations += count
    if gap_nu is None or gap_eta is None or gap_nu == 0.0:
        raise RuntimeError("the shooting gap is not numerically simple")
    forward_rho = DELTA**2 * (-gap_eta / gap_nu)
    step = float(eta_difference_step)
    if not step > 0.0:
        raise ValueError("eta_difference_step must be positive")

    def eta_root(eta: float) -> float:
        return brentq(
            lambda candidate: gap(candidate, eta),
            bracket[0],
            bracket[1],
            xtol=2.0e-12,
            rtol=2.0e-12,
        )

    plus = eta_root(step)
    minus = eta_root(-step)
    finite_difference = DELTA**2 * (plus - minus) / (2.0 * step)
    return ShootingRow(
        section_half_width=section,
        root_bracket=bracket,
        bracket_sign_margin=float(min(abs(left_value), abs(right_value))),
        nu_root=float(root),
        a_root=float(1.0 + DELTA**2 * root),
        gap_residual=float(residual),
        gap_nu_derivative=float(gap_nu),
        gap_eta_derivative=float(gap_eta),
        scalar_gap_inverse_norm=float(1.0 / abs(gap_nu)),
        forward_rho=float(forward_rho),
        finite_difference_rho=float(finite_difference),
        forward_finite_difference_disagreement=float(
            abs(forward_rho - finite_difference)
        ),
        eta_difference_step=step,
        function_evaluations=evaluations,
    )


@lru_cache(maxsize=1)
def reference_shooting_rows() -> tuple[ShootingRow, ...]:
    """Return the pinned section-drift diagnostic."""

    return tuple(shooting_row(section) for section in sorted(_SECTION_BRACKETS))


def _format(value: float) -> str:
    return format(float(value), ".17g")


def reference_fixed_epsilon_quadratic_root_certificate(
) -> FixedEpsilonQuadraticRootCertificate:
    """Build the strict diagnostic/proof-status certificate."""

    if not fixed_epsilon_bvp_algebra_is_exact():
        raise RuntimeError("the exact fixed-epsilon BVP algebra did not close")
    rows = reference_shooting_rows()
    central = next(row for row in rows if row.section_half_width == 3.0)
    rho_values = [row.forward_rho for row in rows]
    a_values = [row.a_root for row in rows]
    return FixedEpsilonQuadraticRootCertificate(
        model_id=MODEL_ID,
        arithmetic="binary64 SciPy DOP853 shooting diagnostic; no intervals",
        period_input=_format(PERIOD_DIAGNOSTIC),
        delta=_format(DELTA),
        epsilon="0.2",
        scaled_period_delay=_format(THETA_PERIOD_DIAGNOSTIC),
        asymptotic_leading_rho_candidate=_format(-PERIOD_DIAGNOSTIC / 50.0),
        central_section_half_width="3",
        central_nu_candidate=_format(central.nu_root),
        central_a_candidate=_format(central.a_root),
        central_rho_candidate=_format(central.forward_rho),
        section_rho_min=_format(min(rho_values)),
        section_rho_max=_format(max(rho_values)),
        section_rho_spread=_format(max(rho_values) - min(rho_values)),
        section_a_spread=_format(max(a_values) - min(a_values)),
        maximum_gap_residual=_format(max(abs(row.gap_residual) for row in rows)),
        minimum_bracket_sign_margin=_format(
            min(row.bracket_sign_margin for row in rows)
        ),
        maximum_forward_finite_difference_disagreement=_format(
            max(row.forward_finite_difference_disagreement for row in rows)
        ),
        exact_full_history_bvp_contract_specified=True,
        finite_section_shooting_diagnostic_computed=True,
        prescribed_older_history_is_selected_attracting_trace=False,
        selected_repelling_trace_constructed=False,
        complete_history_jump_solved=False,
        phase_fixed_augmented_inverse_validated=False,
        dynamic_adjoint_validated=False,
        interval_newton_or_radii_polynomial_validated=False,
        endpoint_zero_fiber_implication_validated=False,
        fixed_epsilon_selected_root_validated=False,
        fixed_epsilon_nonzero_rho_validated=False,
        physical_onset_identification_validated=False,
    )


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [
            [str(sp.simplify(value[i, j])) for j in range(value.cols)]
            for i in range(value.rows)
        ]
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return value


def reference_fixed_epsilon_quadratic_root_payload() -> dict[str, Any]:
    """Return the deterministic exact-contract plus diagnostic record."""

    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "exact_algebra": _json_value(asdict(fixed_epsilon_bvp_algebra())),
        "bvp_contract": _json_value(asdict(reference_fixed_epsilon_bvp_contract())),
        "shooting_rows": _json_value(
            [asdict(row) for row in reference_shooting_rows()]
        ),
        "certificate": _json_value(
            asdict(reference_fixed_epsilon_quadratic_root_certificate())
        ),
        "scope": {
            "exact_validation_contract": True,
            "shooting_diagnostic": True,
            "complete_history_bvp_solution": False,
            "validated_dynamic_adjoint": False,
            "interval_inverse": False,
            "fixed_epsilon_selected_root": False,
            "nonzero_rho_star": False,
            "physical_onset": False,
        },
    }


def validate_fixed_epsilon_quadratic_root_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject mutation or promotion of the diagnostic record."""

    expected = reference_fixed_epsilon_quadratic_root_payload()
    if dict(payload) != expected:
        raise ValueError(
            "fixed-epsilon quadratic-root payload does not match "
            "the exact contract and pinned diagnostic"
        )


__all__ = [
    "DELTA",
    "MODEL_ID",
    "PERIOD_DIAGNOSTIC",
    "THETA_PERIOD_DIAGNOSTIC",
    "FixedEpsilonBVPAlgebra",
    "FixedEpsilonBVPContract",
    "FixedEpsilonQuadraticRootCertificate",
    "ShootingRow",
    "fixed_epsilon_bvp_algebra",
    "fixed_epsilon_bvp_algebra_is_exact",
    "reference_fixed_epsilon_bvp_contract",
    "reference_fixed_epsilon_quadratic_root_certificate",
    "reference_fixed_epsilon_quadratic_root_payload",
    "reference_shooting_rows",
    "shooting_row",
    "validate_fixed_epsilon_quadratic_root_payload",
]
