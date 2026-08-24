"""Fredholm-to-monodromy transfer for the validated periodic FHN orbit.

This module deliberately separates two gates.

* A phase-bordered periodic derivative with the *moving-delay* period
  column proves that the autonomous unit multiplier is algebraically simple.
* Excluding every other unit-circle multiplier requires invertibility of a
  complex Bloch family on the remaining compact phase arc.

The first gate is a theorem-level transfer from the existing infinite
Fourier validation.  The second is reduced to a strict directed-cover
specification.  The helper below checks only bare-number bookkeeping and
never promotes those declarations to validated exclusion evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct
from typing import Iterable

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_periodic_candidate import PeriodicOrbitCandidate
from canard_control.fhn_periodic_infinite_validation import (
    _build_base_sequences,
    _sequence_box_norm_upper,
)


# The transfer is bound to a stored binary64 Fourier polynomial and to the
# tracked directed validation that places the exact center orbit in its
# correction ball.  In particular, none of these identifiers is computed
# by rerunning the floating Newton solver: its last bits depend on the BLAS
# reduction tree and are not theorem-bearing data.
_TRACKED_CENTER_CANDIDATE_RESULT_SHA256 = (
    "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
)
_TRACKED_CENTER_VALIDATION_RESULT_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
_TRACKED_CENTER_REPLAY_RESULT_SHA256 = (
    "28e74d2316f7e9324f03874c3294d27d83708c9dbb3f4eefaf04925f55bbba60"
)
_TRACKED_CENTER_CANDIDATE_FINGERPRINT = (
    "2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169"
)
_TRACKED_CENTER_CORRECTION_RADIUS = "5e-9"
_TRACKED_CENTER_INVERSE_NORM_UPPER = (
    "23.3856903454031599021282567540224673284586776860761524"
)


@dataclass(frozen=True)
class PhaseBorderedOrbitEvidence:
    """Validated inputs needed by the structural transfer theorem.

    The booleans are evidence hand-offs, not numerical heuristics.  For the
    tracked center orbit they come from the parameter-box radii proof and
    the exact differentiation of ``tau_j / T`` in its period column.  The
    three result digests bind the stored polynomial, its directed
    validation, and the exact-candidate replay that connects those two.
    """

    correction_radius: str
    bordered_inverse_norm_upper: str
    periodic_rfde_orbit_validated: bool
    bordered_rfde_inverse_validated: bool
    moving_delay_period_column_validated: bool
    candidate_fingerprint: str
    candidate_result_sha256: str
    validation_result_sha256: str
    candidate_validation_replay_sha256: str


@dataclass(frozen=True)
class CenterFloquetTransferCertificate:
    """Proof ledger for the center unit multiplier and its local arc."""

    precision_bits: int
    correction_radius: str
    bordered_inverse_norm_upper: str
    nonconstant_fourier_mode_lower: str
    minimum_period_lower: str
    maximum_delay_upper: str
    monodromy_compact: bool
    regularity_bridge_to_validated_fourier_domain: bool
    period_column_jordan_identity: str
    unit_multiplier_geometrically_simple_validated: bool
    unit_multiplier_algebraically_simple_validated: bool
    delayed_variational_coefficient_norm_upper: str
    orbit_tangent_norm_upper: str
    bloch_first_order_coefficient_upper: str
    bloch_second_order_coefficient_upper: str
    local_phase_radius_lower: str
    local_unit_circle_exclusion_validated: bool
    outer_arc_lower_endpoint: str
    outer_arc_upper_endpoint: str
    outer_arc_directed_exclusion_validated: bool
    full_unit_circle_exclusion_validated: bool
    full_floquet_hyperbolicity_validated: bool
    remaining_gate: str


@dataclass(frozen=True)
class DirectedBlochCell:
    """Bare declaration of four bounds on one positive Bloch-phase cell.

    To become proof evidence, every bound would have to include the
    exact-orbit correction ball and complete phase interval.  This data class
    cannot establish that provenance; midpoint numbers fit its schema but
    remain inadmissible as validated cells.
    """

    phase_lower: str
    phase_upper: str
    finite_to_finite_upper: str
    tail_from_finite_upper: str
    finite_from_tail_upper: str
    tail_to_tail_upper: str


@dataclass(frozen=True)
class DirectedBlochArcContract:
    """Conditional bookkeeping result for a compact Bloch-phase arc."""

    required_lower: str
    required_upper: str
    cell_count: int
    maximum_contraction_upper: str | None
    connected_cover: bool
    strict_block_contract: bool
    bookkeeping_contract_satisfied: bool
    outer_arc_exclusion_validated: bool
    conditional_conclusion: str


def _up(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value)


def _down(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return gmpy2.mpfr(value)


def _upper_add(
    values: Iterable[gmpy2.mpfr], precision: int
) -> gmpy2.mpfr:
    return upward_sum(list(values), precision)


def _positive_lower_quotient(
    numerator: gmpy2.mpfr,
    denominator: gmpy2.mpfr,
    precision: int,
) -> gmpy2.mpfr:
    if numerator <= 0 or denominator <= 0:
        raise ValueError("directed quotient requires positive bounds")
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return numerator / denominator


def _state_sequence_norm_upper(base, precision: int) -> gmpy2.mpfr:
    return _upper_add(
        (
            _sequence_box_norm_upper(base.phase_voltage, precision),
            _sequence_box_norm_upper(base.phase_recovery, precision),
        ),
        precision,
    )


def _residual_sequence_norm_upper(base, precision: int) -> gmpy2.mpfr:
    return _upper_add(
        (
            _sequence_box_norm_upper(base.residual_voltage, precision),
            _sequence_box_norm_upper(base.residual_recovery, precision),
        ),
        precision,
    )


def _nonconstant_mode_lower(base, radius: gmpy2.mpfr) -> gmpy2.mpfr:
    """Use a nonzero candidate coefficient minus the whole correction ball."""

    precision = base.period.precision
    candidate_distances = []
    for sequence in (base.voltage, base.recovery):
        for mode, coefficient in sequence.items():
            if mode:
                candidate_distances.append(coefficient.lower_abs())
    if not candidate_distances:
        return _down(0, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return max(gmpy2.mpfr(0), max(candidate_distances) - radius)


def periodic_orbit_candidate_fingerprint(
    orbit: PeriodicOrbitCandidate,
) -> str:
    """Bind transferred proof data to one exact stored binary candidate."""

    digest = hashlib.sha256()
    digest.update(struct.pack("<d", float(orbit.period)))
    for value in vars(orbit.parameters).values():
        digest.update(struct.pack("<d", float(value)))
    digest.update(np.asarray(orbit.state, dtype="<f8").tobytes(order="C"))
    return digest.hexdigest()


def validate_fhn_center_floquet_transfer(
    orbit: PeriodicOrbitCandidate,
    evidence: PhaseBorderedOrbitEvidence,
    *,
    precision: int = 160,
) -> CenterFloquetTransferCertificate:
    """Transfer the validated FHN bordered inverse to the monodromy gate.

    Besides algebraic simplicity, the function proves a quantitative local
    exclusion for Bloch phases ``0 < |phi| <= delta``.  It does not claim
    invertibility on the remaining arc ``delta <= |phi| <= pi``.
    """

    if not evidence.periodic_rfde_orbit_validated:
        raise ValueError("a validated periodic RFDE orbit is required")
    if not evidence.bordered_rfde_inverse_validated:
        raise ValueError("a validated phase-bordered RFDE inverse is required")
    if not evidence.moving_delay_period_column_validated:
        raise ValueError("the exact moving-delay period column is required")
    if evidence.candidate_fingerprint != periodic_orbit_candidate_fingerprint(
        orbit
    ):
        raise ValueError("the bordered evidence belongs to a different candidate")
    if (
        evidence.candidate_result_sha256
        != _TRACKED_CENTER_CANDIDATE_RESULT_SHA256
    ):
        raise ValueError("the candidate is not the tracked theorem artifact")
    if (
        evidence.validation_result_sha256
        != _TRACKED_CENTER_VALIDATION_RESULT_SHA256
    ):
        raise ValueError("the validation is not the tracked theorem artifact")
    if (
        evidence.candidate_validation_replay_sha256
        != _TRACKED_CENTER_REPLAY_RESULT_SHA256
    ):
        raise ValueError("the candidate-validation replay is not tracked")
    if evidence.candidate_fingerprint != _TRACKED_CENTER_CANDIDATE_FINGERPRINT:
        raise ValueError("the candidate is not the tracked center polynomial")
    if (
        evidence.correction_radius != _TRACKED_CENTER_CORRECTION_RADIUS
        or evidence.bordered_inverse_norm_upper
        != _TRACKED_CENTER_INVERSE_NORM_UPPER
    ):
        raise ValueError("the evidence does not match the tracked center theorem")
    if orbit.parameters.kappa_1 < 0 or orbit.parameters.kappa_3 < 0:
        raise ValueError("the local coefficient majorant assumes nonnegative gains")

    radius_interval = DirectedInterval.from_decimal(
        evidence.correction_radius, precision
    )
    inverse_interval = DirectedInterval.from_decimal(
        evidence.bordered_inverse_norm_upper, precision
    )
    radius = radius_interval.upper
    inverse_norm = inverse_interval.upper
    if radius <= 0:
        raise ValueError("the correction radius must be positive")
    if inverse_norm <= 0:
        raise ValueError("the inverse-norm upper bound must be positive")

    base = _build_base_sequences(orbit, precision)
    parameters = base.parameters
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        minimum_period = base.period.lower - radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_period = base.period.upper + radius
    if minimum_period <= 0:
        raise ValueError("the correction ball crosses a nonpositive period")

    maximum_delay = max(
        parameters["tau_0"].upper,
        parameters["tau_1"].upper,
    )
    monodromy_compact = minimum_period > maximum_delay
    nonconstant_lower = _nonconstant_mode_lower(base, radius)
    if nonconstant_lower <= 0:
        raise ValueError("the correction ball does not prove a nonconstant orbit")
    if not monodromy_compact:
        raise ValueError(
            "this application requires one-period RFDE smoothing (T > max tau)"
        )

    voltage_bar = _sequence_box_norm_upper(base.voltage, precision)
    centered_bar = _sequence_box_norm_upper(
        base.centered_voltage, precision
    )
    delayed_field_derivative_bar = _sequence_box_norm_upper(
        base.delayed_field_derivative, precision
    )
    tangent_bar = _state_sequence_norm_upper(base, precision)
    residual_bar = _residual_sequence_norm_upper(base, precision)

    epsilon = parameters["epsilon"].upper
    kappa_1 = parameters["kappa_1"].upper
    kappa_3 = parameters["kappa_3"].upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    one = _up(1, precision)
    two = _up(2, precision)
    three = _up(3, precision)

    voltage = _upper_add((voltage_bar, radius), precision)
    centered = _upper_add((centered_bar, radius), precision)

    # H_v(v) = eps*kappa_1/2 + 3*eps*kappa_3*(v-1)^2/2.
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        delayed_variational = (
            epsilon * kappa_1 / two
            + three * epsilon * kappa_3 * centered * centered / two
        )

        voltage_cubic_slope = (
            voltage * voltage
            + voltage * voltage_bar
            + voltage_bar * voltage_bar
        ) / three
        centered_cubic_slope = (
            centered * centered
            + centered * centered_bar
            + centered_bar * centered_bar
        )
        fast_voltage_lipschitz = (
            one
            + epsilon * kappa_1
            + voltage_cubic_slope
            + epsilon * kappa_3 * centered_cubic_slope
        )
        state_field_lipschitz = max(
            fast_voltage_lipschitz + epsilon,
            one,
        )
        delayed_field_lipschitz = (
            epsilon * kappa_1 / two
            + epsilon * kappa_3 * centered_cubic_slope / two
        )

    delay_field_changes: list[gmpy2.mpfr] = []
    for key in ("tau_0", "tau_1"):
        tau = parameters[key].upper
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            alpha_change = (
                tau * radius / (minimum_period * base.period.lower)
            )
            delay_field_changes.append(
                sqrt_two * delayed_field_lipschitz * radius
                + sqrt_two * alpha_change * delayed_field_derivative_bar
            )

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        field_change = (
            state_field_lipschitz * radius
            + sum(delay_field_changes, gmpy2.mpfr(0))
        )
        candidate_field = (
            tangent_bar + residual_bar
        ) / base.period.lower
        tangent_change = (
            maximum_period * field_change
            + radius * candidate_field
            + residual_bar
        )
        tangent_upper = tangent_bar + tangent_change

        delay_sum = (
            parameters["tau_0"].upper
            + parameters["tau_1"].upper
        )
        first_order = one + two * delay_sum * delayed_variational

        alpha_square_sum = (
            (parameters["tau_0"].upper / minimum_period) ** 2
            + (parameters["tau_1"].upper / minimum_period) ** 2
        )
        second_order = (
            maximum_period
            * delayed_variational
            * alpha_square_sum
            * tangent_upper
        )

        first_denominator = inverse_norm * first_order
        second_denominator = inverse_norm * second_order

    first_radius = _positive_lower_quotient(
        one, first_denominator, precision
    )
    second_radius = _positive_lower_quotient(
        minimum_period, second_denominator, precision
    )
    # The factor 1/2 makes both strict inequalities have a directed margin.
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        local_radius = min(first_radius, second_radius) / two
    if local_radius <= 0:
        raise ArithmeticError("the directed local Floquet radius vanished")

    unit_simple = True
    local_exclusion = True
    upper_phase = pi_interval(precision).upper
    return CenterFloquetTransferCertificate(
        precision_bits=precision,
        correction_radius=evidence.correction_radius,
        bordered_inverse_norm_upper=evidence.bordered_inverse_norm_upper,
        nonconstant_fourier_mode_lower=decimal_lower(nonconstant_lower),
        minimum_period_lower=decimal_lower(minimum_period),
        maximum_delay_upper=decimal_upper(maximum_delay),
        monodromy_compact=monodromy_compact,
        regularity_bridge_to_validated_fourier_domain=True,
        period_column_jordan_identity=(
            "L(theta*X') = T*b, with b = f + "
            "sum_j (tau_j/T) A_j S_j X'"
        ),
        unit_multiplier_geometrically_simple_validated=unit_simple,
        unit_multiplier_algebraically_simple_validated=unit_simple,
        delayed_variational_coefficient_norm_upper=decimal_upper(
            delayed_variational
        ),
        orbit_tangent_norm_upper=decimal_upper(tangent_upper),
        bloch_first_order_coefficient_upper=decimal_upper(first_order),
        bloch_second_order_coefficient_upper=decimal_upper(second_order),
        local_phase_radius_lower=decimal_lower(local_radius),
        local_unit_circle_exclusion_validated=local_exclusion,
        outer_arc_lower_endpoint=decimal_lower(local_radius),
        outer_arc_upper_endpoint=decimal_upper(upper_phase),
        outer_arc_directed_exclusion_validated=False,
        full_unit_circle_exclusion_validated=False,
        full_floquet_hyperbolicity_validated=False,
        remaining_gate=(
            "Validate the complex Bloch operator on the compact positive "
            "phase arc [delta, pi] with connected directed finite/tail "
            "cells; conjugation then covers the negative arc."
        ),
    )


def check_directed_bloch_arc_contract(
    cells: Iterable[DirectedBlochCell],
    *,
    required_lower: str,
    required_upper: str,
    precision: int = 160,
) -> DirectedBlochArcContract:
    """Check the bookkeeping contract for a future directed phase cover.

    Bare decimal cells carry no arithmetic provenance.  Consequently this
    function can establish only that the declared cells are gap-free and
    satisfy the formal four-block inequality.  It always leaves the actual
    outer-arc exclusion flag false.  A future validator must manufacture the
    cells by outward-rounded evaluation of the exact-orbit ball over every
    complete phase interval before promoting the conditional conclusion.
    """

    lower_required_exact = gmpy2.mpq(required_lower)
    upper_required_exact = gmpy2.mpq(required_upper)
    if lower_required_exact <= 0:
        raise ValueError("the outer Bloch arc must start at positive phase")
    if upper_required_exact < lower_required_exact:
        raise ValueError("the required Bloch arc is reversed")

    parsed = []
    contractions: list[gmpy2.mpfr] = []
    for cell in cells:
        phase_lower_exact = gmpy2.mpq(cell.phase_lower)
        phase_upper_exact = gmpy2.mpq(cell.phase_upper)
        phase_lower = DirectedInterval.from_decimal(
            cell.phase_lower, precision
        )
        phase_upper = DirectedInterval.from_decimal(
            cell.phase_upper, precision
        )
        if phase_lower_exact <= 0 or phase_upper_exact < phase_lower_exact:
            raise ValueError("a Bloch cell has an invalid phase interval")
        bounds = [
            DirectedInterval.from_decimal(value, precision)
            for value in (
                cell.finite_to_finite_upper,
                cell.tail_from_finite_upper,
                cell.finite_from_tail_upper,
                cell.tail_to_tail_upper,
            )
        ]
        if any(item.lower < 0 for item in bounds):
            raise ValueError("Bloch block bounds must be nonnegative")
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            contraction = max(
                bounds[0].upper + bounds[1].upper,
                bounds[2].upper + bounds[3].upper,
            )
        parsed.append(
            (
                phase_lower_exact,
                phase_upper_exact,
                contraction,
            )
        )
        contractions.append(contraction)

    parsed.sort(key=lambda item: item[0])
    connected = bool(parsed)
    if parsed:
        connected = parsed[0][0] <= lower_required_exact
        right = parsed[0][1]
        for phase_lower, phase_upper, _ in parsed[1:]:
            if phase_lower > right:
                connected = False
            right = max(right, phase_upper)
        connected = connected and right >= upper_required_exact

    strict_blocks = bool(contractions) and all(
        bound < 1 for bound in contractions
    )
    maximum = max(contractions) if contractions else None
    contract = connected and strict_blocks
    return DirectedBlochArcContract(
        required_lower=required_lower,
        required_upper=required_upper,
        cell_count=len(parsed),
        maximum_contraction_upper=(
            decimal_upper(maximum) if maximum is not None else None
        ),
        connected_cover=connected,
        strict_block_contract=strict_blocks,
        bookkeeping_contract_satisfied=contract,
        outer_arc_exclusion_validated=False,
        conditional_conclusion=(
            "If every supplied block bound is independently proved outward "
            "for the exact orbit ball over its whole phase cell, this "
            "gap-free strict contract excludes the declared outer arc."
        ),
    )
