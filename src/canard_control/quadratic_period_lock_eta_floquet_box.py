"""Explicit nonzero-eta Floquet box for the quadratic period lock.

At the validated centre the carrier delay equals the exact period, so the
periodic orbit is unchanged for every real eta.  In logarithmic Floquet
coordinates its additional synchronous pencil column is

    -2*epsilon*T*eta*M_(V-1)*(1-exp(-s))

on the voltage component.  This module combines a new leafwise bound for
that column with the frozen directed right-half cover.  It also treats the
translation neighbourhood, the Fourier tail and the outer half-plane.

The expensive function :func:`build_eta_floquet_certificate` reruns the
parent's complete directed four-block base contraction at all 32,046 stored
cover leaves, then adds the eta channel to the freshly matched
preconditioner.  It does not rebuild or adapt the right-half partition.
Normal tests validate the source-bound result artifact; the full leaf replay
is the generator's separate proof command.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Callable, Mapping

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    upward_sum,
)
from canard_control.fhn_dobrushin_periodic_attraction import (
    validate_dobrushin_periodic_payload,
)
from canard_control.fhn_periodic_infinite_validation import (
    _build_base_sequences,
)
from canard_control.fhn_synchronous_floquet_right_half_cover import (
    _binary_environment_checked,
    _build_parameter_box_sequences,
    _orbit_from_payload,
    _prepare_binary_candidate,
    _rectangle_from_path,
    _root_rectangles,
    _validate_cell,
    validate_right_half_cover_payload,
)
from canard_control.fhn_synchronous_floquet_riesz_reduction import (
    validate_synchronous_floquet_riesz_result_payload,
)
from canard_control.quadratic_period_locked_root_carrier import (
    validate_quadratic_period_lock_payload,
)


MODEL_ID = "quadratic-period-lock-explicit-eta-floquet-stability-box"
ETA_RADIUS = "0.000003"
PRECISION_BITS = 160

TRACKED_RIGHT_HALF_SHA256 = (
    "6795e6f19f31ffb6bfcf9abd24efb1c5dde4dccf54d896d01298b3e8f9a0d1c3"
)
TRACKED_RIESZ_SHA256 = (
    "b68483ae12421195a485e6c9af950d8d101cf04497565cf079fcf57ba57793f6"
)
TRACKED_BLOCH_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)
TRACKED_CANDIDATE_SHA256 = (
    "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
)
TRACKED_QUADRATIC_CARRIER_SHA256 = (
    "4f80cd8ef53161e16886c06fdc52d99be774a9b1cf15d3e7ba534fe37925f7f8"
)
TRACKED_DOBRUSHIN_ATTRACTION_SHA256 = (
    "20fb3f0259f7d2bf8d5ccd24303250661a405418ea733e5419de5f2f07ddea72"
)
TRACKED_PARENT_LEAF_DIGEST = (
    "9ee81b724449c8ef8b465d332b2fb9a78843870dca59e77b440aa459203ea7b2"
)
TRACKED_PARENT_LEAF_COUNT = 32046

REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_PATHS = {
    "right_half": REPOSITORY
    / "experiments/results/fhn_synchronous_floquet_right_half_cover.json",
    "riesz": REPOSITORY
    / "experiments/results/fhn_synchronous_floquet_riesz_reduction.json",
    "bloch": REPOSITORY / "experiments/results/fhn_bloch_outer_validation.json",
    "candidate": REPOSITORY / "experiments/results/fhn_periodic_box_candidate.json",
    "carrier": REPOSITORY
    / "experiments/results/quadratic_period_locked_root_carrier.json",
    "dobrushin": REPOSITORY
    / "experiments/results/fhn_dobrushin_periodic_attraction.json",
}


@dataclass(frozen=True)
class EtaWorstLeaf:
    """The leaf attaining the smallest directed eta budget."""

    root_id: str
    path: str
    sigma_lower: str
    sigma_upper: str
    phase_lower: str
    phase_upper: str
    parent_contraction_upper: str
    replayed_base_contraction_upper: str
    replayed_margin_lower: str
    finite_preconditioner_norm_upper: str
    tail_preconditioner_norm_upper: str
    period_lock_factor_split_upper: str
    eta_slope_upper: str
    eta_radius_lower: str
    selected_eta_contraction_upper: str


@dataclass(frozen=True)
class EtaFloquetCertificate:
    """Numerical theorem record and strict scope ledger."""

    model_id: str
    precision_bits: int
    epsilon: str
    eta_radius: str
    gain_pair: tuple[str, str]
    right_half_result_sha256: str
    riesz_result_sha256: str
    bloch_result_sha256: str
    candidate_result_sha256: str
    quadratic_carrier_result_sha256: str
    dobrushin_attraction_result_sha256: str
    carrier_pencil: str
    carrier_coefficient_wiener_upper: str
    centered_voltage_wiener_upper: str
    orbit_tangent_wiener_upper: str
    exact_period_upper: str
    parent_leaf_count: int
    parent_leaf_digest: str
    eta_budget_digest: str
    minimum_leaf_eta_radius_lower: str
    maximum_finite_preconditioner_norm_upper: str
    maximum_finite_preconditioner_leaf: str
    worst_leaf: EtaWorstLeaf
    bordered_inverse_norm_upper: str
    bordered_period_column_eta_slope_upper: str
    bordered_neumann_contraction_upper: str
    perturbed_bordered_inverse_norm_upper: str
    parent_local_first_order_coefficient_upper: str
    parent_local_second_order_coefficient_upper: str
    minimum_period_lower: str
    local_radius: str
    local_first_contraction_upper: str
    local_second_contraction_upper: str
    parent_tail_contraction_upper: str
    tail_diagonal_gap_lower: str
    tail_contraction_at_eta_upper: str
    parent_outer_contraction_upper: str
    outer_real_part_lower: str
    outer_contraction_at_eta_upper: str
    exact_periodic_orbit_unchanged_for_every_eta: bool
    carrier_pencil_vanishes_at_translation: bool
    translation_multiplier_preserved: bool
    translation_multiplier_algebraically_simple_on_eta_box: bool
    every_parent_leaf_base_contraction_recomputed: bool
    every_replayed_base_contraction_strict: bool
    every_right_half_leaf_revalidated_with_eta_channel: bool
    tail_and_outer_eta_perturbations_strict: bool
    synchronous_nontranslation_right_half_zero_free_on_eta_box: bool
    active_horizon_equals_period: bool
    monodromy_square_compact: bool
    monodromy_power_compact: bool
    translation_generalized_history_bootstrap: bool
    nonzero_multiplier_characteristic_correspondence_validated: bool
    translation_bridge_instantiated: bool
    bordered_inverse_excludes_translation_jordan_chain: bool
    quadratic_carrier_pure_transverse_derivative_zero: bool
    dobrushin_transverse_rate_unchanged_on_eta_box: bool
    full_network_local_orbital_attraction_on_eta_box: bool
    arbitrary_finite_admitted_dobrushin_topology_covered: bool
    eta_parameter_box_for_gain_pair_only: bool
    joint_gain_eta_box_validated: bool
    fixed_epsilon_root_response_nonzero_validated: bool
    uniform_nonlinear_basin_validated: bool
    biological_pulse_capture_validated: bool


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound(path: str | Path, expected: str, name: str) -> Mapping[str, Any]:
    raw = Path(path).read_bytes()
    actual = sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError(f"{name} SHA-256 mismatch: expected {expected}, got {actual}")
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{name} is not valid UTF-8 JSON") from error
    return _mapping(payload, name)


def _decimal_precision(*values: str) -> int:
    return max(220, sum(len(str(value)) for value in values) + 80)


def _decimal_upper_sum(*values: str) -> str:
    with localcontext() as context:
        context.prec = _decimal_precision(*values)
        context.rounding = ROUND_CEILING
        return format(sum((Decimal(value) for value in values), Decimal(0)), "f")


def _decimal_upper_product(*values: str) -> str:
    with localcontext() as context:
        context.prec = _decimal_precision(*values)
        context.rounding = ROUND_CEILING
        product = Decimal(1)
        for value in values:
            product *= Decimal(value)
        return format(product, "f")


def _decimal_upper_quotient(numerator: str, denominator: str) -> str:
    with localcontext() as context:
        context.prec = _decimal_precision(numerator, denominator)
        context.rounding = ROUND_CEILING
        return format(Decimal(numerator) / Decimal(denominator), "f")


def _decimal_lower_one_minus(upper: str) -> str:
    with localcontext() as context:
        context.prec = _decimal_precision(upper)
        context.rounding = ROUND_FLOOR
        return format(Decimal(1) - Decimal(upper), "f")


def _validate_parents(payloads: Mapping[str, Mapping[str, Any]]) -> None:
    validate_right_half_cover_payload(payloads["right_half"])
    validate_synchronous_floquet_riesz_result_payload(payloads["riesz"])
    validate_quadratic_period_lock_payload(
        _mapping(payloads["carrier"].get("audit"), "quadratic carrier audit")
    )
    validate_dobrushin_periodic_payload(payloads["dobrushin"])
    right = _mapping(payloads["right_half"].get("certificate"), "right-half certificate")
    if (
        right.get("accepted_leaf_count") != TRACKED_PARENT_LEAF_COUNT
        or right.get("leaf_partition_sha256") != TRACKED_PARENT_LEAF_DIGEST
        or right.get("entire_keyhole_region_zero_free_validated") is not True
        or right.get("synchronous_nontranslation_unstable_index_zero_validated")
        is not True
    ):
        raise ValueError("the frozen right-half parent has changed scope")
    carrier = _mapping(
        _mapping(payloads["carrier"].get("audit"), "carrier audit").get(
            "certificate"
        ),
        "carrier certificate",
    )
    if (
        carrier.get("distinguished_periodic_orbit_preserved_for_every_eta")
        is not True
        or carrier.get("pure_transverse_first_variation_zero") is not True
    ):
        raise ValueError("the exact quadratic carrier identities are absent")
    dobrushin = _mapping(
        payloads["dobrushin"].get("certificate"), "Dobrushin certificate"
    )
    if (
        dobrushin.get("uniform_transverse_exponential_rate_validated") is not True
        or dobrushin.get("arbitrary_admitted_balanced_topology_covered") is not True
    ):
        raise ValueError("the Dobrushin transverse theorem is absent")


def _parent_payloads(paths: Mapping[str, str | Path]) -> dict[str, Mapping[str, Any]]:
    expected = {
        "right_half": TRACKED_RIGHT_HALF_SHA256,
        "riesz": TRACKED_RIESZ_SHA256,
        "bloch": TRACKED_BLOCH_SHA256,
        "candidate": TRACKED_CANDIDATE_SHA256,
        "carrier": TRACKED_QUADRATIC_CARRIER_SHA256,
        "dobrushin": TRACKED_DOBRUSHIN_ATTRACTION_SHA256,
    }
    return {
        name: _load_bound(paths[name], expected[name], name)
        for name in expected
    }


def build_eta_floquet_certificate(
    paths: Mapping[str, str | Path] = DEFAULT_PATHS,
    *,
    precision: int = PRECISION_BITS,
    progress: Callable[[int, int], None] | None = None,
) -> EtaFloquetCertificate:
    """Replay every base leaf and certify ``|eta|<=3e-6``."""

    if isinstance(precision, bool) or int(precision) != precision or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)
    payloads = _parent_payloads(paths)
    _validate_parents(payloads)
    _binary_environment_checked()

    right = _mapping(payloads["right_half"]["certificate"], "right certificate")
    riesz = _mapping(payloads["riesz"]["certificate"], "Riesz certificate")
    bloch = _mapping(payloads["bloch"]["local_transfer"], "Bloch local transfer")
    bloch_evidence = _mapping(
        payloads["bloch"]["source_evidence"], "Bloch source evidence"
    )
    orbit = _orbit_from_payload(payloads["candidate"])
    base = _build_base_sequences(orbit, precision)
    box = _build_parameter_box_sequences(
        orbit,
        precision,
        str(bloch_evidence["gain_half_width"]),
    )
    candidate = _prepare_binary_candidate(orbit, base, precision)
    correction = DirectedInterval.from_decimal(str(bloch["correction_radius"]), precision)
    centered = upward_sum(
        tuple(
            upward_sum(
                (value.real.upper_abs(), value.imag.upper_abs()), precision
            )
            for value in base.centered_voltage.values()
        ),
        precision,
    )
    eta_box = DirectedInterval.from_decimal(ETA_RADIUS, precision)
    two = DirectedInterval.from_decimal(2, precision)
    one = DirectedInterval.from_decimal(1, precision)
    sqrt_two = two.sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        centered_exact = centered + correction.upper
        period_exact = (base.period + correction).upper
        global_split_factor = 1 + sqrt_two
    centered_text = decimal_upper(centered_exact)
    period_text = decimal_upper(period_exact)
    carrier_text = _decimal_upper_product(
        "2", "0.2", period_text, centered_text
    )
    carrier_coefficient = DirectedInterval.from_decimal(
        carrier_text, precision
    ).upper

    rho = Decimal(str(riesz["local_complex_keyhole_radius"]))
    phase_outer = Decimal(str(riesz["logarithmic_strip_imaginary_upper"]))
    roots = {
        rectangle.root_id: rectangle
        for rectangle in _root_rectangles(rho, phase_outer)
    }
    leaves = tuple(right["leaves"])
    if len(leaves) != TRACKED_PARENT_LEAF_COUNT:
        raise ValueError("the frozen leaf count changed")

    minimum: tuple[gmpy2.mpfr, EtaWorstLeaf] | None = None
    maximum_inverse = gmpy2.mpfr(0)
    maximum_inverse_leaf = ""
    digest_lines: list[str] = []
    for index, raw_leaf in enumerate(leaves, 1):
        leaf = _mapping(raw_leaf, "cover leaf")
        root_id = str(leaf["root_id"])
        path = str(leaf["path"])
        rectangle = _rectangle_from_path(roots[root_id], path)
        replay = _validate_cell(
            rectangle,
            candidate,
            base,
            box,
            correction,
            precision,
            Decimal(1),
        )
        if not replay.validated:
            raise ArithmeticError(
                "one frozen leaf failed the full base-contraction replay"
            )
        replayed_q_text = replay.leaf.contraction_upper
        inverse_text = replay.worst.finite_inverse_l1_upper
        tail_text = replay.worst.tail_diagonal_inverse_split_upper
        inverse_norm = DirectedInterval.from_decimal(
            inverse_text, precision
        ).upper
        tail_inverse = DirectedInterval.from_decimal(
            tail_text, precision
        ).upper
        sigma_max = DirectedInterval.from_decimal(
            format(rectangle.sigma_upper, "f"), precision
        )
        phase_max = DirectedInterval.from_decimal(
            format(max(abs(rectangle.phase_lower), abs(rectangle.phase_upper)), "f"),
            precision,
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            factor = min(
                global_split_factor,
                sqrt_two * (sigma_max.upper + phase_max.upper),
            )
        factor_text = decimal_upper(factor)
        inverse_sum_text = _decimal_upper_sum(inverse_text, tail_text)
        slope_text = _decimal_upper_product(
            carrier_text, factor_text, inverse_sum_text
        )
        slope = DirectedInterval.from_decimal(slope_text, precision).upper
        contraction = DirectedInterval.from_decimal(
            replayed_q_text, precision
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            margin = one.lower - contraction.upper
            eta_radius = margin / slope
        if margin <= 0 or eta_radius <= 0:
            raise ArithmeticError("one replayed right-half leaf lost its margin")
        eta_text = decimal_lower(eta_radius)
        margin_text = decimal_lower(margin)
        selected_text = _decimal_upper_sum(
            replayed_q_text,
            _decimal_upper_product(ETA_RADIUS, slope_text),
        )
        detail = EtaWorstLeaf(
            root_id=root_id,
            path=path,
            sigma_lower=format(rectangle.sigma_lower, "f"),
            sigma_upper=format(rectangle.sigma_upper, "f"),
            phase_lower=format(rectangle.phase_lower, "f"),
            phase_upper=format(rectangle.phase_upper, "f"),
            parent_contraction_upper=str(leaf["contraction_upper"]),
            replayed_base_contraction_upper=replayed_q_text,
            replayed_margin_lower=margin_text,
            finite_preconditioner_norm_upper=inverse_text,
            tail_preconditioner_norm_upper=tail_text,
            period_lock_factor_split_upper=factor_text,
            eta_slope_upper=slope_text,
            eta_radius_lower=eta_text,
            selected_eta_contraction_upper=selected_text,
        )
        if minimum is None or eta_radius < minimum[0]:
            minimum = (eta_radius, detail)
        if inverse_norm > maximum_inverse:
            maximum_inverse = inverse_norm
            maximum_inverse_leaf = f"{root_id}:{path}"
        digest_lines.append(
            "|".join(
                (
                    root_id,
                    path,
                    str(leaf["contraction_upper"]),
                    replayed_q_text,
                    inverse_text,
                    tail_text,
                    factor_text,
                    slope_text,
                    eta_text,
                )
            )
        )
        if progress is not None and index % 1000 == 0:
            progress(index, len(leaves))
    if minimum is None:
        raise ArithmeticError("the frozen right-half cover has no leaves")
    minimum_radius, worst = minimum
    if not eta_box.upper < minimum_radius:
        raise ArithmeticError("the selected eta radius exceeds a leaf budget")
    parent_worst = _mapping(right["worst_cell"], "parent worst cell")
    if (
        worst.root_id != parent_worst.get("root_id")
        or worst.path != parent_worst.get("path")
    ):
        raise ArithmeticError("the new tight leaf moved away from its parent")
    budget_digest = sha256(
        ("\n".join(digest_lines) + "\n").encode("ascii")
    ).hexdigest()

    # Translation neighbourhood.  At s=0 the carrier state column vanishes.
    # Only the bordered period column changes, by
    # 2*epsilon*M_(V-1)*p.  Neumann inversion gives the perturbed bordered
    # inverse used in the two standard local estimates.
    bordered_text = str(riesz["bordered_inverse_norm_upper"])
    tangent_text = str(bloch["orbit_tangent_norm_upper"])
    first_text = str(riesz["local_complex_first_order_coefficient_upper"])
    second_text = str(riesz["local_complex_second_order_coefficient_upper"])
    period_lower_text = str(riesz["minimum_period_lower"])
    local_radius_text = str(riesz["local_complex_exclusion_radius_lower"])
    # In b=f+(tau/T)BSp, the carrier contribution at tau=T is
    # -2*epsilon*eta*M_(V-1)p.  Hence this slope has no factor T.
    period_column_slope_text = _decimal_upper_product(
        "2", "0.2", centered_text, tangent_text
    )
    bordered_contraction_text = _decimal_upper_product(
        bordered_text, ETA_RADIUS, period_column_slope_text
    )
    if Decimal(bordered_contraction_text) >= 1:
        raise ArithmeticError("the eta-bordered inverse lost its Neumann margin")
    perturbed_bordered_text = _decimal_upper_quotient(
        bordered_text,
        _decimal_lower_one_minus(bordered_contraction_text),
    )
    first_eta_text = _decimal_upper_sum(
        first_text,
        _decimal_upper_product(ETA_RADIUS, carrier_text),
    )
    # The second Taylor remainder of 1-exp(-s) contributes the exact 1/2.
    second_eta_text = _decimal_upper_sum(
        second_text,
        _decimal_upper_quotient(
            _decimal_upper_product(
                ETA_RADIUS, carrier_text, tangent_text
            ),
            "2",
        ),
    )
    local_first_text = _decimal_upper_product(
        perturbed_bordered_text, first_eta_text, local_radius_text
    )
    local_second_text = _decimal_upper_quotient(
        _decimal_upper_product(
            perturbed_bordered_text, second_eta_text, local_radius_text
        ),
        period_lower_text,
    )
    if Decimal(local_first_text) >= 1 or Decimal(local_second_text) >= 1:
        raise ArithmeticError("the eta translation neighbourhood did not close")

    # The tail and outer estimates use the complex-modulus Wiener norm, so
    # |1-exp(-s)|<=2 throughout the closed right half-plane.
    tail_parent_text = str(riesz["uniform_tail_contraction_upper"])
    tail_gap_text = str(riesz["uniform_tail_diagonal_gap_lower"])
    outer_parent_text = str(riesz["outer_half_plane_contraction_upper"])
    outer_real_text = str(riesz["outer_real_part"])
    tail_eta_text = _decimal_upper_sum(
        tail_parent_text,
        _decimal_upper_quotient(
            _decimal_upper_product("2", ETA_RADIUS, carrier_text),
            tail_gap_text,
        ),
    )
    outer_eta_text = _decimal_upper_sum(
        outer_parent_text,
        _decimal_upper_quotient(
            _decimal_upper_product("2", ETA_RADIUS, carrier_text),
            outer_real_text,
        ),
    )
    if Decimal(tail_eta_text) >= 1 or Decimal(outer_eta_text) >= 1:
        raise ArithmeticError("the eta tail or outer half-plane margin closed")

    return EtaFloquetCertificate(
        model_id=MODEL_ID,
        precision_bits=precision,
        epsilon="0.2",
        eta_radius=ETA_RADIUS,
        gain_pair=("1/5", "1/4"),
        right_half_result_sha256=TRACKED_RIGHT_HALF_SHA256,
        riesz_result_sha256=TRACKED_RIESZ_SHA256,
        bloch_result_sha256=TRACKED_BLOCH_SHA256,
        candidate_result_sha256=TRACKED_CANDIDATE_SHA256,
        quadratic_carrier_result_sha256=TRACKED_QUADRATIC_CARRIER_SHA256,
        dobrushin_attraction_result_sha256=TRACKED_DOBRUSHIN_ATTRACTION_SHA256,
        carrier_pencil=(
            "Delta_eta L_s=-2*epsilon*T_*eta*M_(V_*-1)*(1-exp(-s)) "
            "on voltage; zero on recovery"
        ),
        carrier_coefficient_wiener_upper=carrier_text,
        centered_voltage_wiener_upper=centered_text,
        orbit_tangent_wiener_upper=tangent_text,
        exact_period_upper=period_text,
        parent_leaf_count=len(leaves),
        parent_leaf_digest=TRACKED_PARENT_LEAF_DIGEST,
        eta_budget_digest=budget_digest,
        minimum_leaf_eta_radius_lower=decimal_lower(minimum_radius),
        maximum_finite_preconditioner_norm_upper=decimal_upper(maximum_inverse),
        maximum_finite_preconditioner_leaf=maximum_inverse_leaf,
        worst_leaf=worst,
        bordered_inverse_norm_upper=bordered_text,
        bordered_period_column_eta_slope_upper=period_column_slope_text,
        bordered_neumann_contraction_upper=bordered_contraction_text,
        perturbed_bordered_inverse_norm_upper=perturbed_bordered_text,
        parent_local_first_order_coefficient_upper=first_text,
        parent_local_second_order_coefficient_upper=second_text,
        minimum_period_lower=period_lower_text,
        local_radius=local_radius_text,
        local_first_contraction_upper=local_first_text,
        local_second_contraction_upper=local_second_text,
        parent_tail_contraction_upper=tail_parent_text,
        tail_diagonal_gap_lower=tail_gap_text,
        tail_contraction_at_eta_upper=tail_eta_text,
        parent_outer_contraction_upper=outer_parent_text,
        outer_real_part_lower=outer_real_text,
        outer_contraction_at_eta_upper=outer_eta_text,
        exact_periodic_orbit_unchanged_for_every_eta=True,
        carrier_pencil_vanishes_at_translation=True,
        translation_multiplier_preserved=True,
        translation_multiplier_algebraically_simple_on_eta_box=True,
        every_parent_leaf_base_contraction_recomputed=True,
        every_replayed_base_contraction_strict=True,
        every_right_half_leaf_revalidated_with_eta_channel=True,
        tail_and_outer_eta_perturbations_strict=True,
        synchronous_nontranslation_right_half_zero_free_on_eta_box=True,
        active_horizon_equals_period=True,
        monodromy_square_compact=True,
        monodromy_power_compact=True,
        translation_generalized_history_bootstrap=True,
        nonzero_multiplier_characteristic_correspondence_validated=True,
        translation_bridge_instantiated=True,
        bordered_inverse_excludes_translation_jordan_chain=True,
        quadratic_carrier_pure_transverse_derivative_zero=True,
        dobrushin_transverse_rate_unchanged_on_eta_box=True,
        full_network_local_orbital_attraction_on_eta_box=True,
        arbitrary_finite_admitted_dobrushin_topology_covered=True,
        eta_parameter_box_for_gain_pair_only=True,
        joint_gain_eta_box_validated=False,
        fixed_epsilon_root_response_nonzero_validated=False,
        uniform_nonlinear_basin_validated=False,
        biological_pulse_capture_validated=False,
    )


def eta_floquet_payload(certificate: EtaFloquetCertificate) -> dict[str, Any]:
    """Serialize a freshly replayed certificate."""

    return {
        "certificate": asdict(certificate),
        "scope": {
            "explicit_eta_interval": True,
            "eta_radius": ETA_RADIUS,
            "central_gain_pair_only": True,
            "synchronous_floquet_stability": True,
            "dobrushin_full_network_local_attraction": True,
            "joint_gain_eta_box": False,
            "fixed_epsilon_root_response_nonzero": False,
            "uniform_nonlinear_basin": False,
            "biological_pulse_capture": False,
        },
        "source_evidence": {
            "right_half_result_sha256": TRACKED_RIGHT_HALF_SHA256,
            "riesz_result_sha256": TRACKED_RIESZ_SHA256,
            "bloch_result_sha256": TRACKED_BLOCH_SHA256,
            "candidate_result_sha256": TRACKED_CANDIDATE_SHA256,
            "quadratic_carrier_result_sha256": TRACKED_QUADRATIC_CARRIER_SHA256,
            "dobrushin_attraction_result_sha256": (
                TRACKED_DOBRUSHIN_ATTRACTION_SHA256
            ),
        },
    }


def validate_eta_floquet_payload(payload: Mapping[str, Any]) -> None:
    """Structural and arithmetic validation without the full leaf replay."""

    certificate = _mapping(payload.get("certificate"), "eta certificate")
    scope = _mapping(payload.get("scope"), "eta scope")
    evidence = _mapping(payload.get("source_evidence"), "eta evidence")
    expected_evidence = {
        "right_half_result_sha256": TRACKED_RIGHT_HALF_SHA256,
        "riesz_result_sha256": TRACKED_RIESZ_SHA256,
        "bloch_result_sha256": TRACKED_BLOCH_SHA256,
        "candidate_result_sha256": TRACKED_CANDIDATE_SHA256,
        "quadratic_carrier_result_sha256": TRACKED_QUADRATIC_CARRIER_SHA256,
        "dobrushin_attraction_result_sha256": TRACKED_DOBRUSHIN_ATTRACTION_SHA256,
    }
    if dict(evidence) != expected_evidence:
        raise ValueError("the eta Floquet source evidence changed")
    expected_scope = {
        "explicit_eta_interval": True,
        "eta_radius": ETA_RADIUS,
        "central_gain_pair_only": True,
        "synchronous_floquet_stability": True,
        "dobrushin_full_network_local_attraction": True,
        "joint_gain_eta_box": False,
        "fixed_epsilon_root_response_nonzero": False,
        "uniform_nonlinear_basin": False,
        "biological_pulse_capture": False,
    }
    if dict(scope) != expected_scope:
        raise ValueError("the eta Floquet scope changed")
    for field, expected in expected_evidence.items():
        if certificate.get(field) != expected:
            raise ValueError(f"the certificate parent hash changed: {field}")
    if (
        certificate.get("model_id") != MODEL_ID
        or certificate.get("precision_bits") != PRECISION_BITS
        or certificate.get("epsilon") != "0.2"
        or certificate.get("eta_radius") != ETA_RADIUS
        or (
            certificate.get("gain_pair") != ["1/5", "1/4"]
            and certificate.get("gain_pair") != ("1/5", "1/4")
        )
        or certificate.get("parent_leaf_count") != TRACKED_PARENT_LEAF_COUNT
        or certificate.get("parent_leaf_digest") != TRACKED_PARENT_LEAF_DIGEST
    ):
        raise ValueError("the eta Floquet fixed theorem data changed")
    for name in (
        "exact_periodic_orbit_unchanged_for_every_eta",
        "carrier_pencil_vanishes_at_translation",
        "translation_multiplier_preserved",
        "translation_multiplier_algebraically_simple_on_eta_box",
        "every_parent_leaf_base_contraction_recomputed",
        "every_replayed_base_contraction_strict",
        "every_right_half_leaf_revalidated_with_eta_channel",
        "tail_and_outer_eta_perturbations_strict",
        "synchronous_nontranslation_right_half_zero_free_on_eta_box",
        "active_horizon_equals_period",
        "monodromy_square_compact",
        "monodromy_power_compact",
        "translation_generalized_history_bootstrap",
        "nonzero_multiplier_characteristic_correspondence_validated",
        "translation_bridge_instantiated",
        "bordered_inverse_excludes_translation_jordan_chain",
        "quadratic_carrier_pure_transverse_derivative_zero",
        "dobrushin_transverse_rate_unchanged_on_eta_box",
        "full_network_local_orbital_attraction_on_eta_box",
        "arbitrary_finite_admitted_dobrushin_topology_covered",
        "eta_parameter_box_for_gain_pair_only",
    ):
        if certificate.get(name) is not True:
            raise ValueError(f"required eta theorem flag is absent: {name}")
    for name in (
        "joint_gain_eta_box_validated",
        "fixed_epsilon_root_response_nonzero_validated",
        "uniform_nonlinear_basin_validated",
        "biological_pulse_capture_validated",
    ):
        if certificate.get(name) is not False:
            raise ValueError(f"unsupported eta scope was promoted: {name}")
    digest = certificate.get("eta_budget_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValueError("the eta leaf-budget digest is malformed")
    try:
        int(digest, 16)
    except ValueError as error:
        raise ValueError("the eta leaf-budget digest is not hexadecimal") from error
    fixed_parent_numbers = {
        "centered_voltage_wiener_upper": (
            "2.92712337524556553483716133719149384707213412688446588"
        ),
        "orbit_tangent_wiener_upper": (
            "41.1189992295311925794707484278753869827403710833596886"
        ),
        "exact_period_upper": (
            "16.5403878031809337427421269239857792854309082031635475"
        ),
        "bordered_inverse_norm_upper": (
            "23.3856903454031773370305076754640443238837022658085131"
        ),
        "parent_local_first_order_coefficient_upper": (
            "19.3714298055394719997186598523155250139128830085170599"
        ),
        "parent_local_second_order_coefficient_upper": (
            "232.614166566187522110915264438703941026429941189576357"
        ),
        "minimum_period_lower": (
            "16.5403877931809337427421269239857792854309082030864525"
        ),
        "local_radius": (
            "0.00110371801789578632406620967700529547972127567299941844"
        ),
        "parent_tail_contraction_upper": (
            "0.272118856318640627662391123614771177960023855447509006"
        ),
        "tail_diagonal_gap_lower": (
            "405.265452313083327761680996443055872061434852518475225"
        ),
        "parent_outer_contraction_upper": (
            "0.861565401475725211547698309141911757060102891981325001"
        ),
        "outer_real_part_lower": "128",
    }
    for field, expected in fixed_parent_numbers.items():
        if certificate.get(field) != expected:
            raise ValueError(f"the eta parent numeric bound changed: {field}")
    if certificate.get("carrier_pencil") != (
        "Delta_eta L_s=-2*epsilon*T_*eta*M_(V_*-1)*(1-exp(-s)) "
        "on voltage; zero on recovery"
    ):
        raise ValueError("the eta carrier pencil identity changed")
    numeric_less_than_one = (
        "worst_leaf.selected_eta_contraction_upper",
        "bordered_neumann_contraction_upper",
        "local_first_contraction_upper",
        "local_second_contraction_upper",
        "tail_contraction_at_eta_upper",
        "outer_contraction_at_eta_upper",
    )
    worst = _mapping(certificate.get("worst_leaf"), "eta worst leaf")
    values = {
        "worst_leaf.selected_eta_contraction_upper": worst.get(
            "selected_eta_contraction_upper"
        ),
        **{name: certificate.get(name) for name in numeric_less_than_one[1:]},
    }
    for name in numeric_less_than_one:
        try:
            value = Decimal(str(values[name]))
        except Exception as error:
            raise ValueError(f"eta bound {name} is not decimal") from error
        if not Decimal(0) < value < Decimal(1):
            raise ValueError(f"eta bound {name} is not strict")
    try:
        minimum_radius = Decimal(
            str(certificate.get("minimum_leaf_eta_radius_lower"))
        )
        leaf_radius = Decimal(str(worst.get("eta_radius_lower")))
        replayed_q = Decimal(str(worst.get("replayed_base_contraction_upper")))
        slope = Decimal(str(worst.get("eta_slope_upper")))
        selected = Decimal(str(worst.get("selected_eta_contraction_upper")))
        if not Decimal(ETA_RADIUS) < minimum_radius or minimum_radius != leaf_radius:
            raise ValueError("the selected eta interval exceeds the leaf budget")
        if not Decimal(0) < replayed_q < Decimal(1):
            raise ValueError("the replayed base contraction is not strict")
        expected_slope = _decimal_upper_product(
            str(certificate.get("carrier_coefficient_wiener_upper")),
            str(worst.get("period_lock_factor_split_upper")),
            _decimal_upper_sum(
                str(worst.get("finite_preconditioner_norm_upper")),
                str(worst.get("tail_preconditioner_norm_upper")),
            ),
        )
        if str(worst.get("eta_slope_upper")) != expected_slope:
            raise ValueError("the worst eta slope does not recompose")
        if leaf_radius * slope > Decimal(1) - replayed_q:
            raise ValueError("the public eta leaf budget is not outward")
        expected_selected = _decimal_upper_sum(
            str(worst.get("replayed_base_contraction_upper")),
            _decimal_upper_product(ETA_RADIUS, str(worst.get("eta_slope_upper"))),
        )
        if str(worst.get("selected_eta_contraction_upper")) != expected_selected:
            raise ValueError("the worst eta contraction does not recompose")

        expected_carrier = _decimal_upper_product(
            "2",
            str(certificate.get("epsilon")),
            str(certificate.get("exact_period_upper")),
            str(certificate.get("centered_voltage_wiener_upper")),
        )
        if certificate.get("carrier_coefficient_wiener_upper") != expected_carrier:
            raise ValueError("the carrier Wiener coefficient does not recompose")
        # This is deliberately T-free: Delta b=-2*epsilon*eta*M p.
        expected_period_slope = _decimal_upper_product(
            "2",
            str(certificate.get("epsilon")),
            str(certificate.get("centered_voltage_wiener_upper")),
            str(certificate.get("orbit_tangent_wiener_upper")),
        )
        if (
            certificate.get("bordered_period_column_eta_slope_upper")
            != expected_period_slope
        ):
            raise ValueError("the T-free period-column slope does not recompose")
        expected_bordered_q = _decimal_upper_product(
            str(certificate.get("bordered_inverse_norm_upper")),
            ETA_RADIUS,
            expected_period_slope,
        )
        if certificate.get("bordered_neumann_contraction_upper") != expected_bordered_q:
            raise ValueError("the bordered eta contraction does not recompose")
        expected_perturbed = _decimal_upper_quotient(
            str(certificate.get("bordered_inverse_norm_upper")),
            _decimal_lower_one_minus(expected_bordered_q),
        )
        if certificate.get("perturbed_bordered_inverse_norm_upper") != expected_perturbed:
            raise ValueError("the perturbed bordered inverse does not recompose")
        first_eta = _decimal_upper_sum(
            str(certificate.get("parent_local_first_order_coefficient_upper")),
            _decimal_upper_product(
                ETA_RADIUS,
                str(certificate.get("carrier_coefficient_wiener_upper")),
            ),
        )
        # Regression seam: the quadratic exponential remainder has factor 1/2.
        second_eta = _decimal_upper_sum(
            str(certificate.get("parent_local_second_order_coefficient_upper")),
            _decimal_upper_quotient(
                _decimal_upper_product(
                    ETA_RADIUS,
                    str(certificate.get("carrier_coefficient_wiener_upper")),
                    str(certificate.get("orbit_tangent_wiener_upper")),
                ),
                "2",
            ),
        )
        expected_local_first = _decimal_upper_product(
            expected_perturbed,
            first_eta,
            str(certificate.get("local_radius")),
        )
        expected_local_second = _decimal_upper_quotient(
            _decimal_upper_product(
                expected_perturbed,
                second_eta,
                str(certificate.get("local_radius")),
            ),
            str(certificate.get("minimum_period_lower")),
        )
        if certificate.get("local_first_contraction_upper") != expected_local_first:
            raise ValueError("the first local eta contraction does not recompose")
        if certificate.get("local_second_contraction_upper") != expected_local_second:
            raise ValueError("the second local eta contraction does not recompose")
        common_global_eta = _decimal_upper_product(
            "2",
            ETA_RADIUS,
            str(certificate.get("carrier_coefficient_wiener_upper")),
        )
        expected_tail = _decimal_upper_sum(
            str(certificate.get("parent_tail_contraction_upper")),
            _decimal_upper_quotient(
                common_global_eta,
                str(certificate.get("tail_diagonal_gap_lower")),
            ),
        )
        expected_outer = _decimal_upper_sum(
            str(certificate.get("parent_outer_contraction_upper")),
            _decimal_upper_quotient(
                common_global_eta,
                str(certificate.get("outer_real_part_lower")),
            ),
        )
        if certificate.get("tail_contraction_at_eta_upper") != expected_tail:
            raise ValueError("the tail eta contraction does not recompose")
        if certificate.get("outer_contraction_at_eta_upper") != expected_outer:
            raise ValueError("the outer eta contraction does not recompose")
    except (ArithmeticError, TypeError) as error:
        raise ValueError("an eta public decimal formula is malformed") from error


def load_eta_floquet_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and structurally validate a generated result."""

    payload = _load_bound(path, expected_sha256, "eta Floquet result")
    validate_eta_floquet_payload(payload)
    return payload
