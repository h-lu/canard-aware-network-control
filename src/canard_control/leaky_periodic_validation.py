"""Directed finite/tail validation contract for the leaky FHN slice.

The fast equation is identical to the synchronous two-delay FHN equation
treated in :mod:`canard_control.fhn_periodic_infinite_validation`.  The slow
equation is instead

    w' = epsilon * (v - a - w).

This module reuses the real-conjugate Wiener coefficient space, the exact
delay rotations, the de-aliased finite/tail splitting, and the directed
binary64 error model from that validator.  It replaces every slow-row formula
whose value changes when ``-epsilon*w`` is added.  In particular, it does not
silently feed a leaky orbit to the non-leaky validator.

The returned Floquet fields are a validation *contract*.  A successful
radii inequality is recorded only as a directed candidate until the changed
majorants receive an independent mathematical audit and a replay artifact is
committed.  Even after that promotion, a phase-bordered periodic BVP does not
by itself prove algebraic simplicity of the neutral multiplier or count
multipliers inside/outside the unit circle; those flags remain false until
the registered spectral gates are supplied.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_periodic_candidate import PeriodicOrbitCandidate
from canard_control.fhn_periodic_directed_validation import (
    _binary_product_defect_upper,
    _complex_zero,
    _sequence_add,
    _sequence_scale,
)
from canard_control.fhn_periodic_infinite_validation import (
    DealiasedFiniteCoefficientCertificate,
    DirectedCorrectionRadiiBound,
    DirectedFiniteTailBlocks,
    _BaseSequences,
    _RealConjugateLayout,
    _binary_matvec_l1_upper,
    _build_base_sequences,
    _coefficient_column_outputs,
    _embedded_mode_factors,
    _float_matrix_l1_upper,
    _nonlinear_coefficients,
    _residual_vector,
    _scaled_real_coordinate_intervals,
    _sequence_box_norm_upper,
    _state_voltage_entry,
    _tail_from_finite_upper,
    _tail_residual_upper,
)


@dataclass(frozen=True)
class LeakyMachineryReuseAudit:
    """Executable claim boundary for adapting the old periodic machinery."""

    old_nonleaky_validator_directly_applies: bool
    exact_reusable_components: tuple[str, ...]
    model_dependent_replacements: tuple[str, ...]
    parameter_box_coordinates_match: bool
    branch_specific_replay_artifacts_available: bool
    old_floquet_artifacts_transfer_to_leaky_orbits: bool
    directed_outer_periodic_orbit_validated: bool
    directed_inner_periodic_orbit_validated: bool
    directed_outer_floquet_index_validated: bool
    directed_inner_floquet_index_validated: bool


@dataclass(frozen=True)
class LeakyFloquetValidationContract:
    """Truth-valued gates from a periodic BVP to a Floquet index theorem."""

    translation_identity_exact_for_validated_orbit: bool
    phase_bordered_rfde_inverse_validated: bool
    geometric_translation_kernel_conditional_on_standard_bvp_identification: bool
    fredholm_to_monodromy_multiplicity_transfer_registered: bool
    neutral_multiplier_algebraically_simple_validated: bool
    nontranslation_unit_circle_exclusion_validated: bool
    unstable_multiplier_count_validated: bool
    attracting_or_saddle_index_validated: bool
    required_next_certificates: tuple[str, ...]


@dataclass(frozen=True)
class DirectedLeakyPeriodicValidation:
    """One branch's directed prototype and unpromoted proof contract."""

    branch: str
    recovery_leak: str
    finite: DealiasedFiniteCoefficientCertificate
    blocks: DirectedFiniteTailBlocks
    correction: DirectedCorrectionRadiiBound
    directed_radii_inequality_candidate_closed: bool
    formula_adaptation_independently_audited: bool
    periodic_rfde_orbit_validated: bool
    phase_bordered_rfde_inverse_validated: bool
    floquet: LeakyFloquetValidationContract
    arithmetic_scope: str


def build_leaky_machinery_reuse_audit() -> LeakyMachineryReuseAudit:
    """Record what transfers structurally and what must be recomputed."""

    return LeakyMachineryReuseAudit(
        old_nonleaky_validator_directly_applies=False,
        exact_reusable_components=(
            "real-conjugate Wiener coefficient space and weights",
            "de-aliased cubic support and finite/tail projections",
            "exact Fourier delay rotations and moving-delay tail cancellation",
            "binary64 midpoint inverse with directed Higham error bounds",
            "analytic Fourier-derivative inverse on the tail",
        ),
        model_dependent_replacements=(
            "slow residual: Dw-T*epsilon*(v-a-w)",
            "slow w-column: D+T*epsilon*I",
            "slow period column: -epsilon*(v-a-w)",
            "tail recovery-column majorant: 1+epsilon",
            "parameter box and sensitivities: (a,kappa_3), not (kappa_1,kappa_3)",
            "both orbit-dependent Floquet operators, covers, and index counts",
        ),
        parameter_box_coordinates_match=False,
        branch_specific_replay_artifacts_available=False,
        old_floquet_artifacts_transfer_to_leaky_orbits=False,
        directed_outer_periodic_orbit_validated=False,
        directed_inner_periodic_orbit_validated=False,
        directed_outer_floquet_index_validated=False,
        directed_inner_floquet_index_validated=False,
    )


def _build_leaky_base_sequences(
    orbit: PeriodicOrbitCandidate,
    precision: int,
) -> _BaseSequences:
    """Return exact interval Fourier data for ``w'=eps*(v-a-w)``.

    The non-leaky builder already constructs every fast-row sequence.  The
    leaky recovery field differs by ``-eps*w``.  Therefore its residual and
    period column change by ``+T*eps*w`` and ``+eps*w``, respectively.  This
    algebraic replacement avoids duplicating the delicate moving-delay
    formulas in the fast row.
    """

    base = _build_base_sequences(orbit, precision)
    leak_field = _sequence_scale(
        base.recovery, base.parameters["epsilon"]
    )
    return replace(
        base,
        residual_recovery=_sequence_add(
            base.residual_recovery,
            _sequence_scale(leak_field, base.period),
        ),
        period_recovery=_sequence_add(
            base.period_recovery,
            leak_field,
        ),
    )


def _leaky_coefficient_column_outputs(
    base: _BaseSequences,
    output_modes: list[int],
    *,
    input_component: int | None,
    input_mode: int = 0,
    input_part: str = "real",
) -> tuple[
    dict[int, DirectedComplexInterval],
    dict[int, DirectedComplexInterval],
    DirectedComplexInterval,
]:
    """Apply the leaky coefficient Jacobian to one real-conjugate column."""

    if input_component is None:
        return _coefficient_column_outputs(
            base,
            output_modes,
            input_component=None,
            input_mode=input_mode,
            input_part=input_part,
        )

    precision = base.period.precision
    zero = _complex_zero(precision)
    fast = {mode: zero for mode in output_modes}
    slow = {mode: zero for mode in output_modes}
    phase = zero
    epsilon = base.parameters["epsilon"]
    factors = _embedded_mode_factors(input_mode, input_part, precision)
    for embedded_mode, factor in factors:
        for output_mode in output_modes:
            if input_component == 0:
                fast[output_mode] += (
                    _state_voltage_entry(base, output_mode, embedded_mode)
                    * factor
                )
                if output_mode == embedded_mode:
                    slow[output_mode] += (
                        DirectedComplexInterval.from_real(
                            -(base.period * epsilon)
                        )
                        * factor
                    )
            elif input_component == 1:
                if output_mode == embedded_mode:
                    fast[output_mode] += (
                        DirectedComplexInterval.from_real(base.period)
                        * factor
                    )
                    slow[output_mode] += (
                        DirectedComplexInterval(
                            DirectedInterval.from_decimal(0, precision),
                            pi_interval(precision) * (2 * output_mode),
                        )
                        + DirectedComplexInterval.from_real(
                            base.period * epsilon
                        )
                    ) * factor
            else:
                raise ValueError(
                    "input_component must be zero, one, or None"
                )
        phase_sequence = (
            base.phase_voltage
            if input_component == 0
            else base.phase_recovery
        )
        phase += phase_sequence.get(-embedded_mode, zero) * factor
    return fast, slow, phase


def _leaky_finite_coefficient_matrix(
    base: _BaseSequences,
    cutoff: int,
) -> tuple[np.ndarray, gmpy2.mpfr, _RealConjugateLayout]:
    """Enclose the leaky ``W R J E W^-1`` finite block."""

    precision = base.period.precision
    layout = _RealConjugateLayout(cutoff)
    output_modes = list(range(cutoff + 1))
    matrix = np.zeros((layout.dimension, layout.dimension), dtype=float)
    column_distances: list[list[gmpy2.mpfr]] = [
        [] for _ in range(layout.dimension)
    ]

    specifications: list[tuple[int | None, int, str, int, int]] = []
    for component in (0, 1):
        specifications.append(
            (
                component,
                0,
                "real",
                layout.state_index(component, 0, "real"),
                1,
            )
        )
        for mode in range(1, cutoff + 1):
            for part in ("real", "imag"):
                specifications.append(
                    (
                        component,
                        mode,
                        part,
                        layout.state_index(component, mode, part),
                        2,
                    )
                )
    specifications.append((None, 0, "real", layout.period_index, 1))

    for component, mode, part, column, input_weight in specifications:
        fast, slow, phase = _leaky_coefficient_column_outputs(
            base,
            output_modes,
            input_component=component,
            input_mode=mode,
            input_part=part,
        )
        intervals = _scaled_real_coordinate_intervals(
            layout,
            fast,
            slow,
            phase,
            input_weight=input_weight,
        )
        for row, enclosure in enumerate(intervals):
            center = float(enclosure.midpoint_nearest())
            matrix[row, column] = center
            center_interval = DirectedInterval.from_float(center, precision)
            column_distances[column].append(
                (enclosure - center_interval).upper_abs()
            )
    distance = max(
        upward_sum(terms, precision) for terms in column_distances
    )
    return matrix, distance, layout


def _leaky_finite_from_tail_upper(
    base: _BaseSequences,
    layout: _RealConjugateLayout,
    approximate_inverse: np.ndarray,
    inverse_l1_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    """Bound tail-to-finite coupling using the leaky finite rows.

    Only a voltage tail can create a different Fourier mode: the added leak
    and the existing recovery coupling are diagonal in Fourier index.  The
    support search is therefore identical to the non-leaky implementation,
    while the finite columns use the corrected slow row.
    """

    precision = base.period.precision
    support = set(base.current_coefficient)
    for coefficient in base.delayed_coefficients:
        support.update(coefficient)
    support_radius = max(abs(mode) for mode in support)
    bounds: list[gmpy2.mpfr] = [gmpy2.mpfr(0, precision)]
    output_modes = list(range(layout.cutoff + 1))
    tail_modes = range(
        layout.cutoff + 1,
        layout.cutoff + support_radius + 1,
    )
    for input_mode in tail_modes:
        for input_part in ("real", "imag"):
            fast, slow, phase = _leaky_coefficient_column_outputs(
                base,
                output_modes,
                input_component=0,
                input_mode=input_mode,
                input_part=input_part,
            )
            intervals = _scaled_real_coordinate_intervals(
                layout,
                fast,
                slow,
                phase,
                input_weight=2,
            )
            centers = np.asarray(
                [float(value.midpoint_nearest()) for value in intervals],
                dtype=float,
            )
            distance_terms = []
            for value, center in zip(intervals, centers, strict=True):
                center_interval = DirectedInterval.from_float(
                    float(center), precision
                )
                distance_terms.append(
                    (value - center_interval).upper_abs()
                )
            distance = upward_sum(distance_terms, precision)
            midpoint_bound = _binary_matvec_l1_upper(
                approximate_inverse,
                centers,
                precision,
                inverse_l1_upper,
            )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                bounds.append(
                    midpoint_bound + inverse_l1_upper * distance
                )
    return max(bounds)


def _leaky_tail_to_tail_upper(
    base: _BaseSequences,
    cutoff: int,
) -> gmpy2.mpfr:
    """Bound the analytic tail block, including the diagonal recovery leak."""

    precision = base.period.precision
    current_norm = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_norms = [
        _sequence_box_norm_upper(coefficient, precision)
        for coefficient in base.delayed_coefficients
    ]
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    denominator = (
        pi_interval(precision) * (2 * (cutoff + 1))
    ).lower
    epsilon = base.parameters["epsilon"].upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage_column = (
            current_norm
            + sqrt_two * sum(
                delayed_norms, gmpy2.mpfr(0, precision)
            )
            + epsilon
        )
        recovery_column = 1 + epsilon
        lower_order_norm = max(voltage_column, recovery_column)
        return base.period.upper * lower_order_norm / denominator


def _leaky_nonlinear_coefficients(
    base: _BaseSequences,
    cutoff: int,
    approximate_inverse_l1: gmpy2.mpfr,
    maximum_radius: str,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    """Use the existing majorant plus the sole changed state-column term.

    The nonlinear and moving-delay variations are identical to the
    non-leaky model.  The only larger zeroth-order state column is the
    recovery column, whose lower-order l1 norm changes from ``1`` to
    ``1+epsilon``.  The existing general bound can therefore be enlarged by
    ``||A_P||*epsilon`` in its linear coefficient.  This is conservative:
    it leaves every other directed term unchanged.
    """

    z1, z2, z3 = _nonlinear_coefficients(
        base,
        cutoff,
        approximate_inverse_l1,
        maximum_radius,
    )
    epsilon = base.parameters["epsilon"].upper
    with gmpy2.context(precision=base.period.precision, round=gmpy2.RoundUp):
        return z1 + approximate_inverse_l1 * epsilon, z2, z3


def _floquet_contract(
    orbit_validated: bool,
    bordered_inverse_validated: bool,
) -> LeakyFloquetValidationContract:
    if bordered_inverse_validated and not orbit_validated:
        raise ValueError(
            "a bordered inverse cannot be registered without its orbit"
        )
    return LeakyFloquetValidationContract(
        translation_identity_exact_for_validated_orbit=orbit_validated,
        phase_bordered_rfde_inverse_validated=bordered_inverse_validated,
        geometric_translation_kernel_conditional_on_standard_bvp_identification=(
            orbit_validated and bordered_inverse_validated
        ),
        fredholm_to_monodromy_multiplicity_transfer_registered=False,
        neutral_multiplier_algebraically_simple_validated=False,
        nontranslation_unit_circle_exclusion_validated=False,
        unstable_multiplier_count_validated=False,
        attracting_or_saddle_index_validated=False,
        required_next_certificates=(
            "Fredholm-to-history-monodromy algebraic-multiplicity transfer",
            "directed unit-circle resolvent cover away from multiplier one",
            "directed Riesz/winding count at one center orbit per branch",
        ),
    )


def evaluate_leaky_periodic_radii_candidate(
    orbit: PeriodicOrbitCandidate,
    *,
    branch: str,
    cutoff: int = 192,
    precision: int = 160,
    maximum_radius: str = "1e-5",
    chosen_radius: str = "1e-5",
) -> DirectedLeakyPeriodicValidation:
    """Evaluate a directed radii *candidate* for one leaky branch.

    The endpoint arithmetic is directed.  Until the leaky majorant
    adaptation receives an independent mathematical audit and a committed
    replay artifact, even a negative radii polynomial is not promoted to the
    repository's periodic-orbit proof ledger.
    """

    if branch not in {"outer_pulse", "inner_saddle_candidate"}:
        raise ValueError("branch must identify the outer or inner candidate")
    if cutoff < 3 * ((len(orbit.state) - 1) // 2):
        raise ValueError("cutoff must contain the cubic residual support")
    if orbit.parameters.kappa_1 < 0 or orbit.parameters.kappa_3 < 0:
        raise ValueError("the majorant requires nonnegative delayed gains")

    base = _build_leaky_base_sequences(orbit, precision)
    real_matrix, matrix_distance, layout = (
        _leaky_finite_coefficient_matrix(base, cutoff)
    )
    approximate_inverse = np.linalg.inv(real_matrix)
    inverse_norm = _float_matrix_l1_upper(
        approximate_inverse, precision
    )
    base_defect, product_roundoff, _, ieee_checked = (
        _binary_product_defect_upper(
            real_matrix.T,
            approximate_inverse.T,
            precision,
        )
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_defect = base_defect + inverse_norm * matrix_distance
    finite_inverse_norm: gmpy2.mpfr | None = None
    if finite_defect < 1:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            finite_inverse_norm = inverse_norm / (1 - finite_defect)

    residual_midpoint, residual_distance = _residual_vector(base, layout)
    finite_y = _binary_matvec_l1_upper(
        approximate_inverse,
        residual_midpoint,
        precision,
        inverse_norm,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_y += inverse_norm * residual_distance
        total_y = finite_y + _tail_residual_upper(base, cutoff)

    tail_from_finite = _tail_from_finite_upper(base, layout)
    finite_from_tail = _leaky_finite_from_tail_upper(
        base,
        layout,
        approximate_inverse,
        inverse_norm,
    )
    tail_to_tail = _leaky_tail_to_tail_upper(base, cutoff)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_input = finite_defect + tail_from_finite
        tail_input = finite_from_tail + tail_to_tail
        full_defect = max(finite_input, tail_input)

    z1, z2, z3 = _leaky_nonlinear_coefficients(
        base,
        cutoff,
        inverse_norm,
        maximum_radius,
    )
    radius = DirectedInterval.from_decimal(chosen_radius, precision)
    maximum = DirectedInterval.from_decimal(maximum_radius, precision)
    if radius.upper > maximum.upper:
        raise ValueError("chosen radius exceeds the coefficient-bound radius")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        variation = (
            z1 * radius.upper
            + z2 * radius.upper * radius.upper
            + z3 * radius.upper * radius.upper * radius.upper
        )
        contraction = full_defect + variation
        radii_left = total_y + contraction * radius.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin = radius.lower - radii_left
    radii_negative = contraction < 1 and margin > 0
    bordered_inverse_norm: gmpy2.mpfr | None = None
    if radii_negative:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            bordered_inverse_norm = inverse_norm / (1 - contraction)

    residual_support = max(
        max(abs(mode) for mode in base.residual_voltage),
        max(abs(mode) for mode in base.residual_recovery),
    )
    finite = DealiasedFiniteCoefficientCertificate(
        cutoff=cutoff,
        ambient_complex_dimension=2 * (2 * cutoff + 1) + 1,
        real_conjugate_dimension=layout.dimension,
        ambient_complexification_used=False,
        precision_bits=precision,
        norm="unweighted component Wiener l1 plus the period scalar",
        independent_coordinate_weights=(
            "mode zero and period weight 1; each positive-mode real and "
            "imaginary coordinate weight 2"
        ),
        residual_support_half_bandwidth=residual_support,
        approximate_inverse_l1_upper=decimal_upper(inverse_norm),
        finite_jacobian_distance_l1_upper=decimal_upper(matrix_distance),
        floating_product_roundoff_upper=decimal_upper(product_roundoff),
        finite_inverse_defect_upper=decimal_upper(finite_defect),
        finite_inverse_norm_upper=(
            decimal_upper(finite_inverse_norm)
            if finite_inverse_norm is not None
            else None
        ),
        preconditioned_residual_l1_upper=decimal_upper(total_y),
        finite_inverse_validated=finite_inverse_norm is not None,
        ieee_binary64_product_model_checked=ieee_checked,
    )
    blocks = DirectedFiniteTailBlocks(
        finite_to_finite_upper=decimal_upper(finite_defect),
        tail_from_finite_upper=decimal_upper(tail_from_finite),
        finite_from_tail_upper=decimal_upper(finite_from_tail),
        tail_to_tail_upper=decimal_upper(tail_to_tail),
        finite_input_column_upper=decimal_upper(finite_input),
        tail_input_column_upper=decimal_upper(tail_input),
        full_point_defect_upper=decimal_upper(full_defect),
        full_point_inverse_gate=full_defect < 1,
    )
    correction = DirectedCorrectionRadiiBound(
        maximum_radius=maximum_radius,
        coefficient_z1_upper=decimal_upper(z1),
        coefficient_z2_upper=decimal_upper(z2),
        coefficient_z3_upper=decimal_upper(z3),
        chosen_radius=chosen_radius,
        derivative_variation_upper=decimal_upper(variation),
        contraction_upper=decimal_upper(contraction),
        radii_left_upper=decimal_upper(radii_left),
        radii_margin_lower=decimal_lower(margin),
        bordered_inverse_norm_upper=(
            decimal_upper(bordered_inverse_norm)
            if bordered_inverse_norm is not None
            else None
        ),
        radii_polynomial_evaluated=True,
        radii_polynomial_negative=radii_negative,
    )
    formula_audited = False
    orbit_validated = radii_negative and formula_audited
    floquet = _floquet_contract(orbit_validated, orbit_validated)
    return DirectedLeakyPeriodicValidation(
        branch=branch,
        recovery_leak="1",
        finite=finite,
        blocks=blocks,
        correction=correction,
        directed_radii_inequality_candidate_closed=radii_negative,
        formula_adaptation_independently_audited=formula_audited,
        periodic_rfde_orbit_validated=False,
        phase_bordered_rfde_inverse_validated=False,
        floquet=floquet,
        arithmetic_scope=(
            "MPFR-directed interval endpoints and directed bounds for the "
            "exact Fourier polynomial represented by the supplied binary64 "
            "coefficients; NumPy supplies only midpoint inverses. The "
            "leaky majorant is an auditable prototype and is not yet a "
            "registered proof artifact"
        ),
    )


__all__ = [
    "DirectedLeakyPeriodicValidation",
    "LeakyMachineryReuseAudit",
    "LeakyFloquetValidationContract",
    "build_leaky_machinery_reuse_audit",
    "evaluate_leaky_periodic_radii_candidate",
]
