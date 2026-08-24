"""Exact no-go audit for dual basins on the quadratic reference slice.

The reference synchronous equilibrium is spectrally unstable, while the
validated attracting periodic orbit repeatedly crosses the detector faces
used by the controlled handoff.  The first fact excludes the equilibrium as
a quiet local attractor; the second excludes permanent one-sided detector
no-return for trajectories captured by that periodic orbit.  Neither fact
rules out an as-yet unvalidated different quiet attractor.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

import sympy as sp


AMPLITUDE_RESULT_SHA256 = (
    "28e74d2316f7e9324f03874c3294d27d83708c9dbb3f4eefaf04925f55bbba60"
)
PERIODIC_ATTRACTION_RESULT_SHA256 = (
    "20fb3f0259f7d2bf8d5ccd24303250661a405418ea733e5419de5f2f07ddea72"
)
SYNCHRONOUS_FLOQUET_RESULT_SHA256 = (
    "6795e6f19f31ffb6bfcf9abd24efb1c5dde4dccf54d896d01298b3e8f9a0d1c3"
)
AUTONOMOUS_HANDOFF_RESULT_SHA256 = (
    "38f612771fd5f7e50ffd4f77103ea680b447fd11a7af25cc5ccea95b9bf606f2"
)
STOP_GO_RESULT_SHA256 = (
    "4bc8ccf41fb0f2d2fd7e3152da59afa24810a5b0d8615a3847d1491f63ff55da"
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/quadratic_reference_dual_basin_no_go.py"
)
GENERATOR_RELATIVE_PATH = "experiments/quadratic_reference_dual_basin_no_go.py"
DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/quadratic_reference_dual_basin_no_go.py"
)
MODEL_ID = "quadratic-dual-scaffold-reference-slice-dual-basin-no-go"
ASSUMPTIONS_ID = (
    "epsilon=1/5;a=3/5;microscopic-kappa-box;abs-eta<=1/1000-for-rest-"
    "instability;eta=0-for-validated-periodic-attraction;balanced-"
    "Dobrushin-topology-for-full-network-attraction"
)
ARITHMETIC_DESCRIPTION = (
    "exact SymPy equilibrium, characteristic determinant, two-disk Rouche "
    "bounds, and directed periodic-extrema face margins"
)


@dataclass(frozen=True)
class EquilibriumRoucheAudit:
    epsilon: sp.Expr
    unfolding: sp.Expr
    kappa_1_center: sp.Expr
    kappa_3_center: sp.Expr
    gain_half_width: sp.Expr
    eta_abs_upper: sp.Expr
    equilibrium_voltage: sp.Expr
    equilibrium_recovery: sp.Expr
    local_cubic_derivative: sp.Expr
    delayed_cubic_derivative: sp.Expr
    effective_delay_gain_center: sp.Expr
    effective_delay_gain_variation_upper: sp.Expr
    eta_current_delay_gain_per_abs_eta: sp.Expr
    reference_current_coefficient: sp.Expr
    reference_characteristic: sp.Expr
    reference_polynomial: sp.Expr
    reference_polynomial_roots: tuple[sp.Expr, sp.Expr]
    root_modulus: sp.Expr
    disk_radius: sp.Expr
    disk_real_part_lower: sp.Expr
    disk_center_separation: sp.Expr
    polynomial_boundary_lower: sp.Expr
    total_perturbation_coefficient_upper: sp.Expr
    characteristic_perturbation_boundary_upper: sp.Expr
    rouche_margin_lower: sp.Expr
    two_disks_disjoint: bool
    each_disk_in_open_right_half_plane: bool
    rouche_margin_strictly_positive: bool


@dataclass(frozen=True)
class PeriodicFaceAudit:
    voltage_maximum_lower: sp.Expr
    voltage_maximum_upper: sp.Expr
    voltage_minimum_lower: sp.Expr
    voltage_minimum_upper: sp.Expr
    positive_detector_face: sp.Expr
    positive_excursion_face: sp.Expr
    negative_detector_face: sp.Expr
    negative_excursion_face: sp.Expr
    positive_detector_upper_margin: sp.Expr
    positive_detector_lower_margin: sp.Expr
    positive_excursion_upper_margin: sp.Expr
    positive_excursion_lower_margin: sp.Expr
    negative_detector_upper_margin: sp.Expr
    negative_detector_lower_margin: sp.Expr
    negative_excursion_orbit_above_margin: sp.Expr
    positive_detector_two_sided: bool
    positive_excursion_two_sided: bool
    negative_detector_two_sided: bool
    negative_excursion_orbit_strictly_above: bool


@dataclass(frozen=True)
class RepairContractAudit:
    autonomous_bistable_slice_required_tasks: tuple[str, ...]
    latch_contract: tuple[str, ...]
    post_event_switch_required_tasks: tuple[str, ...]
    latch_scope: str
    post_event_switch_scope: str


@dataclass(frozen=True)
class QuadraticReferenceDualBasinNoGoCertificate:
    model_id: str
    assumptions_id: str
    amplitude_result_sha256: str
    periodic_attraction_result_sha256: str
    synchronous_floquet_result_sha256: str
    autonomous_handoff_result_sha256: str
    stop_go_result_sha256: str
    unique_synchronous_equilibrium_validated: bool
    two_distinct_synchronous_right_half_plane_roots_validated: bool
    equilibrium_instability_uniform_on_gain_eta_box_validated: bool
    synchronous_equilibrium_local_attractor_validated: bool
    synchronous_equilibrium_quiet_basin_validated: bool
    eta_zero_pulse_periodic_local_attraction_validated: bool
    positive_detector_periodic_two_sided_crossing_validated: bool
    positive_excursion_periodic_two_sided_crossing_validated: bool
    negative_detector_periodic_two_sided_crossing_validated: bool
    negative_excursion_periodic_orbit_strictly_above_validated: bool
    periodic_capture_permanent_positive_detector_upper_side_validated: bool
    periodic_capture_permanent_positive_excursion_upper_side_validated: bool
    periodic_capture_permanent_negative_detector_lower_side_validated: bool
    periodic_capture_permanent_negative_excursion_lower_side_validated: bool
    permanent_face_no_return_incompatible_with_periodic_capture_validated: bool
    current_slice_rest_versus_pulse_dual_basin_validated: bool
    different_quiet_attractor_existence_validated: bool
    different_quiet_attractor_excluded_validated: bool
    current_slice_any_dual_basin_structurally_impossible_validated: bool
    global_single_attractor_validated: bool
    terminal_blocks_inside_periodic_basin_validated: bool
    autonomous_bistable_repair_contract_specified_validated: bool
    autonomous_bistable_repair_completed_validated: bool
    latched_first_hit_label_is_immutable_by_definition_validated: bool
    latched_first_hit_is_physical_basin_validated: bool
    post_event_parameter_switch_contract_specified_validated: bool
    post_event_parameter_switch_capture_validated: bool
    post_event_parameter_switch_is_autonomous_dual_basin_validated: bool
    input_independent_physical_onset_validated: bool


@lru_cache(maxsize=1)
def reference_equilibrium_rouche_audit() -> EquilibriumRoucheAudit:
    """Return exact two-disk Rouché data for the synchronous rest state."""

    lam, tau_0, tau_1 = sp.symbols(
        "lambda tau_0 tau_1", complex=True
    )
    epsilon = sp.Rational(1, 5)
    unfolding = sp.Rational(3, 5)
    kappa_1 = sp.Rational(1, 5)
    kappa_3 = sp.Rational(1, 4)
    gain_half_width = sp.Rational(1, 10**12)
    eta_upper = sp.Rational(1, 1000)
    equilibrium_voltage = unfolding
    equilibrium_recovery = sp.simplify(
        equilibrium_voltage - equilibrium_voltage**3 / 3
    )
    local_derivative = sp.simplify(1 - equilibrium_voltage**2)
    delayed_derivative = sp.simplify(3 * (equilibrium_voltage - 1) ** 2)
    delay_gain = sp.simplify(
        epsilon * (kappa_1 + kappa_3 * delayed_derivative)
    )
    delay_gain_variation = sp.simplify(
        epsilon * gain_half_width * (1 + delayed_derivative)
    )
    eta_gain_per_abs_eta = sp.simplify(
        2 * epsilon * abs(equilibrium_voltage - 1)
    )
    current_coefficient = sp.simplify(local_derivative - delay_gain)

    characteristic = sp.expand(
        lam**2
        - current_coefficient * lam
        - delay_gain * lam * (
            sp.exp(-tau_0 * lam) + sp.exp(-tau_1 * lam)
        )
        / 2
        + epsilon
    )
    polynomial = sp.expand(lam**2 - current_coefficient * lam + epsilon)
    root_plus = sp.Rational(36, 125) + sp.I * sp.sqrt(1829) / 125
    root_minus = sp.conjugate(root_plus)
    root_modulus = 1 / sp.sqrt(5)
    radius = sp.Rational(1, 10)
    separation = 2 * sp.sqrt(1829) / 125
    real_lower = sp.Rational(36, 125) - radius
    polynomial_lower = sp.simplify(radius * (separation - radius))

    # Relative to the reference polynomial, the gain box contributes the
    # baseline delayed coefficient plus twice its variation.  The quadratic
    # carrier linearization contributes at most twice
    # 2*epsilon*|a-1|*|eta|, accounting for current and delayed atoms.
    perturbation_coefficient = sp.simplify(
        delay_gain
        + 2 * delay_gain_variation
        + 2 * eta_gain_per_abs_eta * eta_upper
    )
    perturbation_upper = sp.simplify(
        perturbation_coefficient * (root_modulus + radius)
    )
    margin = sp.simplify(polynomial_lower - perturbation_upper)

    return EquilibriumRoucheAudit(
        epsilon=epsilon,
        unfolding=unfolding,
        kappa_1_center=kappa_1,
        kappa_3_center=kappa_3,
        gain_half_width=gain_half_width,
        eta_abs_upper=eta_upper,
        equilibrium_voltage=equilibrium_voltage,
        equilibrium_recovery=equilibrium_recovery,
        local_cubic_derivative=local_derivative,
        delayed_cubic_derivative=delayed_derivative,
        effective_delay_gain_center=delay_gain,
        effective_delay_gain_variation_upper=delay_gain_variation,
        eta_current_delay_gain_per_abs_eta=eta_gain_per_abs_eta,
        reference_current_coefficient=current_coefficient,
        reference_characteristic=characteristic,
        reference_polynomial=polynomial,
        reference_polynomial_roots=(root_plus, root_minus),
        root_modulus=root_modulus,
        disk_radius=radius,
        disk_real_part_lower=real_lower,
        disk_center_separation=separation,
        polynomial_boundary_lower=polynomial_lower,
        total_perturbation_coefficient_upper=perturbation_coefficient,
        characteristic_perturbation_boundary_upper=perturbation_upper,
        rouche_margin_lower=margin,
        two_disks_disjoint=bool(separation > 2 * radius),
        each_disk_in_open_right_half_plane=bool(real_lower > 0),
        rouche_margin_strictly_positive=bool(margin > 0),
    )


@lru_cache(maxsize=1)
def reference_periodic_face_audit() -> PeriodicFaceAudit:
    """Return directed extrema margins against all four handoff faces."""

    maximum_lower = sp.Rational(
        "1.93406327151920518409809759858497216615671825444576443"
    )
    maximum_upper = sp.Rational(
        "1.93406459386103160099698801611228051168771028922940805"
    )
    minimum_lower = sp.Rational(
        "-1.01331410191142478456039139637915704642138299865115011"
    )
    minimum_upper = sp.Rational(
        "-1.01331295150622793179457944748716070850262680731264519"
    )
    positive_detector = sp.Integer(1)
    positive_excursion = sp.Rational(3, 2)
    negative_detector = -sp.Integer(1)
    negative_excursion = -sp.Rational(6, 5)
    return PeriodicFaceAudit(
        voltage_maximum_lower=maximum_lower,
        voltage_maximum_upper=maximum_upper,
        voltage_minimum_lower=minimum_lower,
        voltage_minimum_upper=minimum_upper,
        positive_detector_face=positive_detector,
        positive_excursion_face=positive_excursion,
        negative_detector_face=negative_detector,
        negative_excursion_face=negative_excursion,
        positive_detector_upper_margin=sp.simplify(
            maximum_lower - positive_detector
        ),
        positive_detector_lower_margin=sp.simplify(
            positive_detector - minimum_upper
        ),
        positive_excursion_upper_margin=sp.simplify(
            maximum_lower - positive_excursion
        ),
        positive_excursion_lower_margin=sp.simplify(
            positive_excursion - minimum_upper
        ),
        negative_detector_upper_margin=sp.simplify(
            maximum_lower - negative_detector
        ),
        negative_detector_lower_margin=sp.simplify(
            negative_detector - minimum_upper
        ),
        negative_excursion_orbit_above_margin=sp.simplify(
            minimum_lower - negative_excursion
        ),
        positive_detector_two_sided=bool(
            minimum_upper < positive_detector < maximum_lower
        ),
        positive_excursion_two_sided=bool(
            minimum_upper < positive_excursion < maximum_lower
        ),
        negative_detector_two_sided=bool(
            minimum_upper < negative_detector < maximum_lower
        ),
        negative_excursion_orbit_strictly_above=bool(
            minimum_lower > negative_excursion
        ),
    )


@lru_cache(maxsize=1)
def reference_repair_contract_audit() -> RepairContractAudit:
    """Return non-interchangeable validation contracts for three repairs."""

    return RepairContractAudit(
        autonomous_bistable_slice_required_tasks=(
            "validated zero right-half equilibrium spectrum on one parameter box",
            "validated attracting nonconstant periodic orbit on the same box",
            "two disjoint directed trapping neighborhoods in the same autonomous RFDE",
            "directed terminal-block inclusion in the corresponding basins",
            "global separator or declared-domain basin partition",
        ),
        latch_contract=(
            "predeclared input-independent detector functional",
            "transverse first hit on the declared autonomous segment",
            "discrete label changes once and is never reset",
            "physical voltage is allowed to recross the detector face",
        ),
        post_event_switch_required_tasks=(
            "declare the hybrid switching rule and both parameter slices",
            "validate one target attractor for each post-event slice",
            "prove switching-state inclusion in each target basin",
            "validate robustness, hysteresis, and dwell-time margins",
        ),
        latch_scope=(
            "immutable event memory only; neither a physical invariant half-space "
            "nor a pulse/quiet basin"
        ),
        post_event_switch_scope=(
            "policy-dependent hybrid capture; not an autonomous dual basin and "
            "not input-independent onset"
        ),
    )


@lru_cache(maxsize=1)
def no_go_algebra_is_exact() -> bool:
    equilibrium = reference_equilibrium_rouche_audit()
    faces = reference_periodic_face_audit()
    return bool(
        equilibrium.equilibrium_recovery == sp.Rational(66, 125)
        and equilibrium.local_cubic_derivative == sp.Rational(16, 25)
        and equilibrium.delayed_cubic_derivative == sp.Rational(12, 25)
        and equilibrium.effective_delay_gain_center == sp.Rational(8, 125)
        and equilibrium.effective_delay_gain_variation_upper
        == sp.Rational(37, 125 * 10**12)
        and equilibrium.eta_current_delay_gain_per_abs_eta
        == sp.Rational(4, 25)
        and equilibrium.reference_current_coefficient == sp.Rational(72, 125)
        and equilibrium.disk_real_part_lower == sp.Rational(47, 250)
        and equilibrium.two_disks_disjoint
        and equilibrium.each_disk_in_open_right_half_plane
        and equilibrium.rouche_margin_strictly_positive
        and faces.positive_detector_two_sided
        and faces.positive_excursion_two_sided
        and faces.negative_detector_two_sided
        and faces.negative_excursion_orbit_strictly_above
        and faces.positive_detector_upper_margin > 0
        and faces.positive_detector_lower_margin > 0
        and faces.positive_excursion_upper_margin > 0
        and faces.positive_excursion_lower_margin > 0
        and faces.negative_detector_upper_margin > 0
        and faces.negative_detector_lower_margin > 0
        and faces.negative_excursion_orbit_above_margin > 0
    )


@lru_cache(maxsize=1)
def reference_no_go_certificate() -> QuadraticReferenceDualBasinNoGoCertificate:
    if not no_go_algebra_is_exact():
        raise ValueError("quadratic dual-basin no-go algebra failed")
    return QuadraticReferenceDualBasinNoGoCertificate(
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        amplitude_result_sha256=AMPLITUDE_RESULT_SHA256,
        periodic_attraction_result_sha256=PERIODIC_ATTRACTION_RESULT_SHA256,
        synchronous_floquet_result_sha256=SYNCHRONOUS_FLOQUET_RESULT_SHA256,
        autonomous_handoff_result_sha256=AUTONOMOUS_HANDOFF_RESULT_SHA256,
        stop_go_result_sha256=STOP_GO_RESULT_SHA256,
        unique_synchronous_equilibrium_validated=True,
        two_distinct_synchronous_right_half_plane_roots_validated=True,
        equilibrium_instability_uniform_on_gain_eta_box_validated=True,
        synchronous_equilibrium_local_attractor_validated=False,
        synchronous_equilibrium_quiet_basin_validated=False,
        eta_zero_pulse_periodic_local_attraction_validated=True,
        positive_detector_periodic_two_sided_crossing_validated=True,
        positive_excursion_periodic_two_sided_crossing_validated=True,
        negative_detector_periodic_two_sided_crossing_validated=True,
        negative_excursion_periodic_orbit_strictly_above_validated=True,
        periodic_capture_permanent_positive_detector_upper_side_validated=False,
        periodic_capture_permanent_positive_excursion_upper_side_validated=False,
        periodic_capture_permanent_negative_detector_lower_side_validated=False,
        periodic_capture_permanent_negative_excursion_lower_side_validated=False,
        permanent_face_no_return_incompatible_with_periodic_capture_validated=True,
        current_slice_rest_versus_pulse_dual_basin_validated=False,
        different_quiet_attractor_existence_validated=False,
        different_quiet_attractor_excluded_validated=False,
        current_slice_any_dual_basin_structurally_impossible_validated=False,
        global_single_attractor_validated=False,
        terminal_blocks_inside_periodic_basin_validated=False,
        autonomous_bistable_repair_contract_specified_validated=True,
        autonomous_bistable_repair_completed_validated=False,
        latched_first_hit_label_is_immutable_by_definition_validated=True,
        latched_first_hit_is_physical_basin_validated=False,
        post_event_parameter_switch_contract_specified_validated=True,
        post_event_parameter_switch_capture_validated=False,
        post_event_parameter_switch_is_autonomous_dual_basin_validated=False,
        input_independent_physical_onset_validated=False,
    )


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _audit_value(value: Any) -> Any:
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    if isinstance(value, tuple):
        return [_audit_value(item) for item in value]
    return value


def validate_no_go_payload(
    payload: object,
) -> QuadraticReferenceDualBasinNoGoCertificate:
    """Validate source-bound audits and reject basin/onset promotions."""

    root = _mapping(payload, "result payload")
    if set(root) != {"certificate", "exact_audits", "provenance", "scope"}:
        raise ValueError("result payload contains an unpinned section")
    provenance = _mapping(root.get("provenance"), "provenance")
    certificate_payload = _mapping(root.get("certificate"), "certificate")
    exact_audits = _mapping(root.get("exact_audits"), "exact_audits")
    scope = _mapping(root.get("scope"), "scope")

    expected_provenance_keys = {
        "generator",
        "generator_sha256",
        "proof_source",
        "proof_source_sha256",
        "parent_sha256",
        "parent_claim_checks",
        "argv",
        "default_command",
        "python",
        "platform",
        "arithmetic",
    }
    if set(provenance) != expected_provenance_keys:
        raise ValueError("provenance contains an unpinned or missing field")
    source_path = Path(__file__).resolve()
    repository = source_path.parents[2]
    generator_path = repository / GENERATOR_RELATIVE_PATH
    source_bound = {
        "generator": GENERATOR_RELATIVE_PATH,
        "generator_sha256": sha256(generator_path.read_bytes()).hexdigest(),
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "proof_source_sha256": sha256(source_path.read_bytes()).hexdigest(),
        "default_command": DEFAULT_COMMAND,
        "arithmetic": ARITHMETIC_DESCRIPTION,
    }
    for key, expected_value in source_bound.items():
        if provenance.get(key) != expected_value:
            raise ValueError(f"provenance {key} is not source-bound")
    argv = provenance.get("argv")
    if (
        not isinstance(argv, list)
        or len(argv) != 2
        or not isinstance(argv[0], str)
        or not argv[0]
        or argv[1] != GENERATOR_RELATIVE_PATH
    ):
        raise ValueError("provenance argv is not the declared generator call")
    for key in ("python", "platform"):
        if not isinstance(provenance.get(key), str) or not provenance[key]:
            raise ValueError(f"provenance {key} must be a nonempty string")

    expected = reference_no_go_certificate()
    expected_certificate = {
        field: getattr(expected, field) for field in expected.__dataclass_fields__
    }
    if dict(certificate_payload) != expected_certificate:
        raise ValueError("certificate does not match the strict no-go ledger")

    expected_parents = {
        "amplitude_result": AMPLITUDE_RESULT_SHA256,
        "periodic_attraction_result": PERIODIC_ATTRACTION_RESULT_SHA256,
        "synchronous_floquet_result": SYNCHRONOUS_FLOQUET_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
        "stop_go_result": STOP_GO_RESULT_SHA256,
    }
    parents = _mapping(provenance.get("parent_sha256"), "parent_sha256")
    if dict(parents) != expected_parents:
        raise ValueError("parent provenance does not match the pinned inputs")

    expected_parent_checks = {
        "periodic_extrema_validated": True,
        "periodic_orbit_crosses_declared_faces": True,
        "eta_zero_periodic_local_attraction_validated": True,
        "nonzero_eta_attraction_refused": True,
        "uniform_basin_refused": True,
        "asymptotic_phase_source_validated": True,
        "handoff_faces_and_finite_excursions_validated": True,
        "handoff_permanent_no_return_refused": True,
        "prior_stop_go_refuses_capture_and_basin": True,
    }
    parent_checks = _mapping(
        provenance.get("parent_claim_checks"), "parent_claim_checks"
    )
    if dict(parent_checks) != expected_parent_checks:
        raise ValueError("parent claim checks do not match the pinned inputs")

    expected_audits = {
        "equilibrium_rouche": {
            field: _audit_value(getattr(reference_equilibrium_rouche_audit(), field))
            for field in EquilibriumRoucheAudit.__dataclass_fields__
        },
        "periodic_faces": {
            field: _audit_value(getattr(reference_periodic_face_audit(), field))
            for field in PeriodicFaceAudit.__dataclass_fields__
        },
        "repair_contracts": {
            field: _audit_value(getattr(reference_repair_contract_audit(), field))
            for field in RepairContractAudit.__dataclass_fields__
        },
    }
    if dict(exact_audits) != expected_audits:
        raise ValueError("exact_audits do not match the no-go algebra")

    expected_scope = {
        field.removesuffix("_validated"): getattr(expected, field)
        for field in expected.__dataclass_fields__
        if field.endswith("_validated")
    }
    if dict(scope) != expected_scope:
        false_promotions = [
            key
            for key, value in expected_scope.items()
            if value is False and scope.get(key) is True
        ]
        if false_promotions:
            raise ValueError("a quiet-basin, no-return, switch, or onset claim was promoted")
        raise ValueError("scope contains an unpinned or missing claim")
    return expected


__all__ = [
    "AMPLITUDE_RESULT_SHA256",
    "ARITHMETIC_DESCRIPTION",
    "ASSUMPTIONS_ID",
    "AUTONOMOUS_HANDOFF_RESULT_SHA256",
    "DEFAULT_COMMAND",
    "EquilibriumRoucheAudit",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_ID",
    "PERIODIC_ATTRACTION_RESULT_SHA256",
    "PROOF_SOURCE_RELATIVE_PATH",
    "PeriodicFaceAudit",
    "QuadraticReferenceDualBasinNoGoCertificate",
    "RepairContractAudit",
    "STOP_GO_RESULT_SHA256",
    "SYNCHRONOUS_FLOQUET_RESULT_SHA256",
    "no_go_algebra_is_exact",
    "reference_equilibrium_rouche_audit",
    "reference_no_go_certificate",
    "reference_periodic_face_audit",
    "reference_repair_contract_audit",
    "validate_no_go_payload",
]
