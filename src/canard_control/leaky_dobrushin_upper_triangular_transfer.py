"""Upper-triangular root transfer without delay-layer left balance.

The synchronized line of a nonnegative row-mass network is invariant even
when the delayed layers do not share the stationary left vector of the
instantaneous Markov layer.  In stationary-mean/transverse coordinates the
linearized complete-history operator is then upper triangular, rather than
a direct sum.  The quotient transverse block retains the same Dobrushin--
Halanay estimate, so a bounded triangular row operation reduces the Lin
operator to the scalar block plus the invertible transverse block.

This module records that analytic theorem and the corresponding nonlinear
collective imbalance budget.  It does not manufacture the still-open scalar
leaky complete-history canard root or identify it with physical pulse onset.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2

from canard_control.leaky_dobrushin_collective_defect import (
    RESULT_RELATIVE_PATH as DEFECT_RESULT_RELATIVE_PATH,
    validate_collective_defect_result,
)
from canard_control.leaky_dobrushin_complete_line_inverse import (
    RESULT_RELATIVE_PATH as INVERSE_RESULT_RELATIVE_PATH,
    validate_leaky_complete_line_inverse_result,
)
from canard_control.leaky_dobrushin_nonlinear_synchronization import (
    RESULT_RELATIVE_PATH as SYNC_RESULT_RELATIVE_PATH,
    validate_nonlinear_synchronization_result,
)
from canard_control.leaky_dobrushin_transverse_halanay import (
    RESULT_RELATIVE_PATH as HALANAY_RESULT_RELATIVE_PATH,
    validate_leaky_dobrushin_transverse_result,
)


SCHEMA_ID = "leaky-dobrushin-upper-triangular-root-transfer-v2"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_dobrushin_upper_triangular_transfer.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_dobrushin_upper_triangular_transfer.py"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-dobrushin-upper-triangular-root-transfer.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_dobrushin_upper_triangular_transfer.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_dobrushin_upper_triangular_transfer.json"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_dobrushin_upper_triangular_transfer.py"
)
ARITHMETIC_SCOPE = (
    "exact rational row-mass, triangular-Fredholm and stationary-measure "
    "oscillation calculus composed with the source-validated Dobrushin "
    "rate 1/10 and complete-line Green bound 10; the forward nonlinear "
    "forcing budget retains the exact 4*sqrt(5),5*sqrt(5) delayed-history "
    "residence; no scalar leaky canard root, stable-sheet onset, basin "
    "routing, signed coupling, moving delay support, or closing-gap theorem"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
PARENT_RESULTS = (
    HALANAY_RESULT_RELATIVE_PATH,
    INVERSE_RESULT_RELATIVE_PATH,
    SYNC_RESULT_RELATIVE_PATH,
    DEFECT_RESULT_RELATIVE_PATH,
)

PROVED_FLAGS = (
    "delay_layer_left_balance_not_required_proved",
    "synchronized_scalar_restriction_remains_exact_proved",
    "quotient_transverse_halanay_constants_unchanged_proved",
    "complete_line_quotient_green_bound_ten_proved",
    "upper_triangular_complete_history_lin_factorization_proved",
    "uniform_bounded_triangular_reduction_to_direct_sum_proved",
    "fredholm_index_kernel_and_cokernel_dimensions_transfer_proved",
    "conditional_collective_simple_root_location_slope_orientation_exact",
    "corrected_full_cokernel_functional_formula_proved",
    "nonlinear_node_diameter_decay_unchanged_proved",
    "linear_collective_imbalance_forcing_bound_proved",
    "quadratic_collective_defect_bound_retained_proved",
    "delayed_history_residence_accounted_exactly",
    "componentwise_resolved_linear_accumulated_bound_proved",
    "delta_b_only_worst_accumulated_bound_proved",
    "conditional_accumulated_collective_forcing_bound_proved",
    "constants_uniform_in_finite_network_size_and_delay_topology_proved",
    "strictly_nonbalanced_delay_layer_witness_proved",
)
OPEN_FLAGS = (
    "scalar_leaky_complete_history_canard_root_validated",
    "unconditional_network_canard_connection_validated",
    "signed_or_negative_coupling_covered",
    "closing_dobrushin_gap_families_covered",
    "moving_delay_support_covered",
    "heterogeneous_node_vector_fields_covered",
    "topology_uniform_invariant_strip_or_basin_validated",
    "physical_pulse_onset_or_two_sided_routing_validated",
)

CERTIFICATE_KEYS = {
    "schema_id",
    "model_id",
    "network_class",
    "stationary_coordinate",
    "delay_balance_defect",
    "delay_balance_components",
    "delay_balance_defect_range",
    "fixed_delays",
    "quotient_transverse_norm",
    "quotient_halanay_statement",
    "complete_line_green_norm_upper",
    "lin_block_form",
    "triangular_reduction",
    "full_cokernel_functional",
    "collective_parameter_gap_identity",
    "uniform_off_diagonal_bound",
    "fredholm_and_root_transfer_scope",
    "retained_history_diameter_envelope",
    "componentwise_pointwise_collective_forcing_bound",
    "pointwise_collective_forcing_bound",
    "accumulated_collective_forcing_bound",
    "delta_b_only_accumulated_collective_forcing_bound",
    "imbalance_linear_coefficient_exact",
    "imbalance_accumulated_coefficient_exact",
    "imbalance_accumulated_delta_b_worst_exact",
    "quadratic_componentwise_pointwise_coefficients_exact",
    "quadratic_pointwise_coefficient_exact",
    "quadratic_accumulated_coefficient_exact",
    "quadratic_accumulated_coefficient_rational_upper",
    "nonbalanced_exact_witness",
    "strict_boundary",
    *PROVED_FLAGS,
    *OPEN_FLAGS,
}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "certificate_sha256",
    "source_sha256",
    "parent_result_sha256",
    "environment",
}


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _clear_parent_validation_caches() -> None:
    """Make formal replay insensitive to warm dependency caches."""

    from canard_control import leaky_dobrushin_collective_defect as defect
    from canard_control import leaky_dobrushin_nonlinear_synchronization as sync
    from canard_control import leaky_dobrushin_transverse_halanay as halanay

    _load_parents.cache_clear()
    defect._validated_parent.cache_clear()
    sync._validated_parent.cache_clear()
    halanay._validated_floquet_payload.cache_clear()
    halanay.build_leaky_dobrushin_transverse_certificate.cache_clear()


def _matmul(left: Sequence[Sequence[Fraction]], right: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("incompatible exact witness matrices")
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def _row_times_matrix(row: Sequence[Fraction], matrix: Sequence[Sequence[Fraction]]) -> list[Fraction]:
    return [
        sum((row[k] * matrix[k][j] for k in range(len(row))), Fraction(0))
        for j in range(len(matrix[0]))
    ]


def _fraction_row(values: Sequence[Fraction]) -> list[str]:
    return [str(value) for value in values]


def _exact_nonbalanced_witness() -> dict[str, Any]:
    q = [
        [Fraction(1), Fraction(0)],
        [Fraction(1, 2), Fraction(1, 2)],
    ]
    b0 = [
        [Fraction(0), Fraction(1, 2)],
        [Fraction(1, 2), Fraction(0)],
    ]
    b1 = [
        [Fraction(1, 2), Fraction(0)],
        [Fraction(1, 2), Fraction(0)],
    ]
    pi = [Fraction(1), Fraction(0)]
    projector = [
        [Fraction(0), Fraction(0)],
        [Fraction(-1), Fraction(1)],
    ]
    ones = [[Fraction(1)], [Fraction(1)]]
    pi_q = _row_times_matrix(pi, q)
    pi_b0 = _row_times_matrix(pi, b0)
    pi_b1 = _row_times_matrix(pi, b1)
    half_pi = [value / 2 for value in pi]
    lower_left_b0 = _matmul(_matmul(projector, b0), ones)
    upper_right_b0 = _row_times_matrix(pi_b0, projector)
    tau_q = Fraction(1, 2) * sum(abs(q[0][j] - q[1][j]) for j in range(2))
    delta0 = Fraction(1, 2) * sum(abs(pi_b0[j] - half_pi[j]) for j in range(2))
    delta1 = Fraction(1, 2) * sum(abs(pi_b1[j] - half_pi[j]) for j in range(2))
    if pi_q != pi or tau_q != Fraction(1, 2):
        raise ArithmeticError("the exact witness Markov layer changed")
    if pi_b0 == half_pi or pi_b1 != half_pi:
        raise ArithmeticError("the exact witness balance status changed")
    if lower_left_b0 != [[Fraction(0)], [Fraction(0)]]:
        raise ArithmeticError("synchrony no longer gives a zero lower-left block")
    if upper_right_b0 == [Fraction(0), Fraction(0)]:
        raise ArithmeticError("the exact witness lost its upper-right coupling")
    if delta0 + delta1 != Fraction(1, 2):
        raise ArithmeticError("the exact witness imbalance changed")
    return {
        "Q": [_fraction_row(row) for row in q],
        "B0": [_fraction_row(row) for row in b0],
        "B1": [_fraction_row(row) for row in b1],
        "stationary_pi": _fraction_row(pi),
        "dobrushin_tau_Q": str(tau_q),
        "piT_B0": _fraction_row(pi_b0),
        "half_piT": _fraction_row(half_pi),
        "B0_is_not_left_balanced": True,
        "B1_is_left_balanced": True,
        "P_B0_one": [str(row[0]) for row in lower_left_b0],
        "piT_B0_P": _fraction_row(upper_right_b0),
        "strictly_upper_triangular_coupling_nonzero": True,
        "delay_balance_defect_delta0": str(delta0),
        "delay_balance_defect_delta1": str(delta1),
        "delay_balance_defect_delta_B": str(delta0 + delta1),
    }


@lru_cache(maxsize=1)
def _load_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    validators = {
        HALANAY_RESULT_RELATIVE_PATH: validate_leaky_dobrushin_transverse_result,
        INVERSE_RESULT_RELATIVE_PATH: validate_leaky_complete_line_inverse_result,
        SYNC_RESULT_RELATIVE_PATH: validate_nonlinear_synchronization_result,
        DEFECT_RESULT_RELATIVE_PATH: validate_collective_defect_result,
    }
    parents: dict[str, Mapping[str, Any]] = {}
    for relative, validator in validators.items():
        payload = _mapping(
            json.loads((repository / relative).read_bytes()),
            f"parent {relative}",
        )
        validator(payload, repository)
        parents[relative] = payload
    return parents


def build_upper_triangular_transfer_certificate(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    parents = _load_parents(repository)
    halanay = _mapping(
        parents[HALANAY_RESULT_RELATIVE_PATH].get("certificate"),
        "Halanay certificate",
    )
    bounds = _mapping(halanay.get("bounds"), "Halanay bounds")
    inverse = _mapping(
        parents[INVERSE_RESULT_RELATIVE_PATH].get("certificate"),
        "complete-line inverse certificate",
    )
    synchronization = _mapping(
        parents[SYNC_RESULT_RELATIVE_PATH].get("certificate"),
        "nonlinear synchronization certificate",
    )
    defect = _mapping(
        parents[DEFECT_RESULT_RELATIVE_PATH].get("certificate"),
        "collective defect certificate",
    )

    if bounds.get("exponential_rate") != "0.1":
        raise ValueError("the source Dobrushin rate changed")
    if inverse.get("complete_line_green_norm_upper") != "10":
        raise ValueError("the source complete-line Green bound changed")
    if synchronization.get("conditional_exponential_node_synchronization_proved") is not True:
        raise ValueError("the source nonlinear synchronization theorem is absent")
    if defect.get("pointwise_defect_constant_exact") != "703/200":
        raise ValueError("the source quadratic defect constant changed")
    if defect.get("accumulated_defect_constant_exact") != (
        "703/40+27*sqrt(5)/800"
    ):
        raise ValueError("the source accumulated defect constant changed")
    if defect.get("accumulated_defect_constant_rational_upper") != (
        "56483/3200"
    ):
        raise ValueError("the source rational defect upper bound changed")
    if defect.get("delayed_history_residence_accounted_exactly") is not True:
        raise ValueError("the source delayed-history correction is absent")

    epsilon = gmpy2.mpq(1, 5)
    kappa_1 = gmpy2.mpq(1, 250)
    kappa_3 = gmpy2.mpq(1, 200)
    delayed_h_prime = gmpy2.mpq(75, 4)
    imbalance_linear = epsilon * (kappa_1 + delayed_h_prime * kappa_3)
    if imbalance_linear != gmpy2.mpq(391, 20000):
        raise ArithmeticError("the imbalance coefficient changed")
    rate = gmpy2.mpq(1, 10)
    complete_line_row_bound = imbalance_linear / rate
    if complete_line_row_bound != gmpy2.mpq(391, 2000):
        raise ArithmeticError("the complete-line row bound changed")
    triangular_bound = 10 * imbalance_linear
    if triangular_bound != complete_line_row_bound:
        raise ArithmeticError("the triangular reduction bound changed")
    # Forward integration starts at t0 with an arbitrary retained history.
    # Thus the jth delayed linear term contributes delta_j*(tau_j+1/rate),
    # not merely delta_j/rate.  If only delta_B is retained, tau_1 is the
    # sharp worst case because tau_1>tau_0.
    if imbalance_linear * 5 != gmpy2.mpq(391, 4000):
        raise ArithmeticError("the worst-delay simplification changed")

    values: dict[str, Any] = {name: True for name in PROVED_FLAGS}
    values.update({name: False for name in OPEN_FLAGS})
    certificate = {
        "schema_id": SCHEMA_ID,
        "model_id": "finite-directed-leaky-recovery-two-delay-fhn",
        "network_class": (
            "Q>=0, Q*1=1, tau(Q)<=1/2; pi is any stationary probability "
            "of Q; B_j>=0 and B_j*1=(1/2)*1; no identity "
            "pi^T*B_j=(1/2)*pi^T is required"
        ),
        "stationary_coordinate": (
            "bar_x=pi^T*x and z=(I-1*pi^T)x; zero entries of pi are "
            "allowed and no pi_min enters the diameter estimates"
        ),
        "delay_balance_defect": (
            "delta_B=sum_{j=0,1} (1/2)*||pi^T*B_j-(1/2)*pi^T||_1"
        ),
        "delay_balance_components": (
            "delta_j=(1/2)*||pi^T*B_j-(1/2)*pi^T||_1 and "
            "delta_B=delta0+delta1"
        ),
        "delay_balance_defect_range": "0<=delta_B<=1",
        "fixed_delays": "tau0=4*sqrt(5), tau1=5*sqrt(5)",
        "quotient_transverse_norm": (
            "max{diam z_v,3 diam z_w} on the quotient by span{1}, "
            "represented in ker(pi^T)"
        ),
        "quotient_halanay_statement": (
            "the projection I-1*pi^T changes no diameter; row mass alone "
            "gives diam(B_j z)<=(1/2)diam(z), hence rate 1/10 and the "
            "source strict residual are unchanged"
        ),
        "complete_line_green_norm_upper": "10",
        "lin_block_form": "L_N=[[L_parallel,C_N],[0,L_{perp,N}]]",
        "triangular_reduction": (
            "T_N(y_parallel,y_perp)=(y_parallel-C_N*G_{perp,N}*y_perp,"
            "y_perp), so T_N*L_N=L_parallel direct_sum L_{perp,N}"
        ),
        "full_cokernel_functional": (
            "Psi_N(y_parallel,y_perp)=psi(y_parallel-"
            "C_N*G_{perp,N}*y_perp), normalized by the same collective "
            "complement e_N=(e_parallel,0), so psi(e_parallel)="
            "Psi_N(e_N)=1"
        ),
        "collective_parameter_gap_identity": (
            "for a collective parameter/inhomogeneity (g_parallel,0), "
            "Psi_N(g_parallel,0)=psi(g_parallel); therefore the normalized "
            "root, slope, and orientation equal the scalar data"
        ),
        "uniform_off_diagonal_bound": (
            "on complete-line sup norms, time translation has norm one, so "
            "||C_N*G_{perp,N}|| <= (391/2000)*delta_B <= 391/2000"
        ),
        "fredholm_and_root_transfer_scope": (
            "conditional on the same scalar phase-fixed complete-history "
            "Lin root and collective endpoint/phase/gap preparation used "
            "by the canonical transfer theorem"
        ),
        "retained_history_diameter_envelope": (
            "H_M(t)=sup_{t-r<=s<=t}M(s), with "
            "M0=sup_{t0-r<=s<=t0}M(s)"
        ),
        "componentwise_pointwise_collective_forcing_bound": (
            "|R_coll(t)| <= (391/20000)*"
            "[delta0*M(t-tau0)+delta1*M(t-tau1)] "
            "+(1403/400)*M(t)^2+(3/800)*"
            "[M(t-tau0)^2+M(t-tau1)^2]"
        ),
        "pointwise_collective_forcing_bound": (
            "|R_coll(t)| <= (391/20000)*delta_B*H_M(t) "
            "+(703/200)*H_M(t)^2 while the voltage strip holds"
        ),
        "accumulated_collective_forcing_bound": (
            "integral_[t0,infinity) |R_coll(t)|dt <= (391/20000)*"
            "[delta0*(10+4*sqrt(5))+delta1*(10+5*sqrt(5))]*M0 "
            "+(703/40+27*sqrt(5)/800)*M0^2"
        ),
        "delta_b_only_accumulated_collective_forcing_bound": (
            "integral_[t0,infinity) |R_coll(t)|dt <= "
            "[391*(2+sqrt(5))/4000]*delta_B*M0 "
            "+(56483/3200)*M0^2"
        ),
        "imbalance_linear_coefficient_exact": str(imbalance_linear),
        "imbalance_accumulated_coefficient_exact": (
            "391/20000*[delta0*(10+4*sqrt(5))+"
            "delta1*(10+5*sqrt(5))]"
        ),
        "imbalance_accumulated_delta_b_worst_exact": (
            "391*(2+sqrt(5))/4000"
        ),
        "quadratic_componentwise_pointwise_coefficients_exact": (
            "current=1403/400; each_delay=3/800"
        ),
        "quadratic_pointwise_coefficient_exact": "703/200",
        "quadratic_accumulated_coefficient_exact": (
            "703/40+27*sqrt(5)/800"
        ),
        "quadratic_accumulated_coefficient_rational_upper": "56483/3200",
        "nonbalanced_exact_witness": _exact_nonbalanced_witness(),
        "strict_boundary": (
            "the theorem removes common left balance only from the fixed "
            "nonnegative half-row-mass delay layers; strip invariance, the "
            "scalar leaky canard root, onset, routing, signed coupling, "
            "moving delays, and closing-gap families remain open"
        ),
        **values,
    }
    if set(certificate) != CERTIFICATE_KEYS:
        raise ArithmeticError("the upper-triangular certificate schema changed")
    return certificate


def build_upper_triangular_transfer_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = build_upper_triangular_transfer_certificate(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in PARENT_RESULTS
            },
            "environment": {
                "python": platform.python_version(),
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
            },
        },
    }


def validate_upper_triangular_transfer_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    _clear_parent_validation_caches()
    repository = repository.resolve()
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("upper-triangular transfer result requires two records")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if set(certificate) != CERTIFICATE_KEYS:
        raise ValueError("upper-triangular certificate keys changed")
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("upper-triangular manifest keys changed")
    if manifest.get("schema_id") != SCHEMA_ID or certificate.get("schema_id") != SCHEMA_ID:
        raise ValueError("upper-triangular schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("upper-triangular result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("upper-triangular replay command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("upper-triangular arithmetic scope changed")
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("upper-triangular source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"upper-triangular source changed: {relative}")
    parent_hashes = _mapping(manifest.get("parent_result_sha256"), "parent hashes")
    if set(parent_hashes) != set(PARENT_RESULTS):
        raise ValueError("upper-triangular parent manifest changed")
    for relative in PARENT_RESULTS:
        if parent_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"upper-triangular parent changed: {relative}")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("upper-triangular certificate digest changed")
    for name in PROVED_FLAGS:
        if certificate.get(name) is not True:
            raise ValueError(f"proved upper-triangular claim changed: {name}")
    for name in OPEN_FLAGS:
        if certificate.get(name) is not False:
            raise ValueError(f"open upper-triangular claim was promoted: {name}")
    if certificate.get("delay_balance_defect_range") != "0<=delta_B<=1":
        raise ValueError("delay balance-defect range changed")
    if certificate.get("complete_line_green_norm_upper") != "10":
        raise ValueError("upper-triangular Green bound changed")
    if certificate.get("quadratic_accumulated_coefficient_exact") != (
        "703/40+27*sqrt(5)/800"
    ) or certificate.get(
        "quadratic_accumulated_coefficient_rational_upper"
    ) != "56483/3200":
        raise ValueError("upper-triangular delayed quadratic budget changed")
    if "H_M(t)" not in str(certificate.get("pointwise_collective_forcing_bound")):
        raise ValueError("upper-triangular history envelope changed")
    if certificate.get("imbalance_accumulated_delta_b_worst_exact") != (
        "391*(2+sqrt(5))/4000"
    ):
        raise ValueError("upper-triangular worst-delay coefficient changed")
    witness = _mapping(certificate.get("nonbalanced_exact_witness"), "witness")
    if witness != _exact_nonbalanced_witness():
        raise ValueError("the exact nonbalanced witness changed")
    expected = build_upper_triangular_transfer_result(repository)
    if payload != expected:
        raise ValueError("the upper-triangular transfer replay changed")
