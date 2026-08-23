"""Exact arbitrary-size lift of the final two-module fold model.

This module performs finite-dimensional algebra only.  It supplies an exact
``N=n1+n2`` node realization of the final two-module model, a uniformly
conditioned critical/transverse splitting in the node maximum norm, and
certified finite-atomic delay-residual bounds.  The weighted Hilbert metric is
retained as an exact algebraic diagnostic, but it is not the model-fitting
norm used for the dimension-uniform RFDE theorem.

The calculations do *not* construct an RFDE invariant-history graph, a Lin
operator, a canard root, or a physical pulse threshold.  Those analytic
steps require an exact blown-up normal-form fit, a bounded preparation, and
the separate graph and gap arguments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import sympy as sp


Matrix = sp.ImmutableMatrix


def _immutable(matrix: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(matrix)


def _validate_module_size(size: int, name: str) -> None:
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise ValueError(f"{name} must be a positive integer")


def _positive(expression: sp.Expr, name: str) -> sp.Expr:
    expression = sp.sympify(expression)
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be known to be positive")
    return expression


def _nonnegative(expression: sp.Expr, name: str) -> sp.Expr:
    expression = sp.sympify(expression)
    if expression.is_nonnegative is not True:
        raise ValueError(f"{name} must be known to be nonnegative")
    return expression


def matrix_infinity_operator_norm(matrix: sp.MatrixBase) -> sp.Expr:
    r"""Return the induced matrix norm from ``ell_infinity`` to itself.

    The formula is the maximum absolute row sum and is valid for rectangular
    matrices as an operator between maximum-norm coordinate spaces.  It is
    kept symbolic so the audit can distinguish exact finite-size values from
    the dimension-uniform upper bounds stated separately.
    """

    matrix = sp.Matrix(matrix)
    if matrix.rows < 1 or matrix.cols < 1:
        raise ValueError("matrix must have at least one row and one column")
    row_sums = [
        sp.simplify(sum((sp.Abs(entry) for entry in matrix.row(row)), sp.Integer(0)))
        for row in range(matrix.rows)
    ]
    return sp.simplify(sp.Max(*row_sums))


@dataclass(frozen=True)
class LiftedTwoModuleNetwork:
    """Exact data for the unequal-size lift of the final two-module model."""

    n1: int
    n2: int
    within_voltage_rate: sp.Expr
    recovery_rate: sp.Expr
    module_redistribution: sp.Expr
    embedding: Matrix
    module_average: Matrix
    module_projector: Matrix
    module_metric: Matrix
    node_metric: Matrix
    critical_module_right: Matrix
    critical_module_left: Matrix
    module_transverse_right: Matrix
    module_transverse_left: Matrix
    critical_right: Matrix
    critical_left: Matrix
    module_transverse_right_lift: Matrix
    module_transverse_left_lift: Matrix
    critical_projector: Matrix
    module_transverse_projector: Matrix
    within_projector: Matrix
    transverse_projector: Matrix
    equilibrium_voltage: Matrix
    equilibrium_recovery: Matrix
    base_fast_jacobian: Matrix
    fast_voltage_jacobian: Matrix
    recovery_jacobian: Matrix
    singular_jacobian: Matrix
    state_critical_projector: Matrix
    state_transverse_projector: Matrix
    critical_hessian_vector: Matrix
    fold_curvature: sp.Expr
    module_layer_0: Matrix
    module_layer_1: Matrix
    module_total_layer: Matrix
    layer_0: Matrix
    layer_1: Matrix
    total_layer: Matrix

    @property
    def node_count(self) -> int:
        return self.n1 + self.n2


def lifted_final_two_module_network(
    n1: int,
    n2: int,
    *,
    within_voltage_rate: sp.Expr = sp.Integer(2),
    recovery_rate: sp.Expr = sp.Integer(1),
    module_redistribution: sp.Expr = sp.Integer(0),
) -> LiftedTwoModuleNetwork:
    r"""Lift the final two-module simple fold to unequal module sizes.

    ``S`` replicates a module value at every node and ``R`` takes an
    unweighted average inside each module.  Thus ``R*S=I_2`` for every
    positive ``n1,n2``.  The node metric

    .. math::
       W_N=\operatorname{diag}((2n_1)^{-1}I_{n_1},
                               (8n_2)^{-1}I_{n_2})

    is the lift of ``diag(1/2,1/8)``.  In this metric the critical vector
    ``S*(1,2)`` and the module-transverse vector ``S*(1,-2)`` are orthonormal,
    and the within-module subspace ``ker(R)`` is orthogonal to both.

    The lifted fast field used by :func:`lifted_fast_field` has a nodewise
    cubic, the final model's two cross-module mean couplings, and a linear
    within-module scaffold.  It restricts exactly to ``S*F(z,y)`` on
    ``(v,w)=(S*z,S*y)``.  Its displayed Jacobians, fold curvature, and delay-
    layer identities are therefore exact.  The recovery equation is
    scaffolded by
    ``-Dw*(I-Pc)*(w-w*)``.  Positivity of ``Dv,Dw`` is required here so the
    returned transverse semigroup certificate has an honest domain.
    """

    _validate_module_size(n1, "n1")
    _validate_module_size(n2, "n2")
    voltage_rate = _positive(within_voltage_rate, "within_voltage_rate")
    recovery = _positive(recovery_rate, "recovery_rate")
    redistribution = sp.sympify(module_redistribution)
    node_count = n1 + n2

    embedding = sp.zeros(node_count, 2)
    for row in range(n1):
        embedding[row, 0] = 1
    for row in range(n1, node_count):
        embedding[row, 1] = 1

    module_average = sp.zeros(2, node_count)
    for column in range(n1):
        module_average[0, column] = sp.Rational(1, n1)
    for column in range(n1, node_count):
        module_average[1, column] = sp.Rational(1, n2)

    module_projector = embedding * module_average
    module_metric = sp.diag(sp.Rational(1, 2), sp.Rational(1, 8))
    node_metric = sp.diag(
        *(
            [sp.Rational(1, 2 * n1)] * n1
            + [sp.Rational(1, 8 * n2)] * n2
        )
    )

    critical_module_right = sp.Matrix([1, 2])
    critical_module_left = sp.Matrix(
        [sp.Rational(1, 2), sp.Rational(1, 4)]
    )
    module_transverse_right = sp.Matrix([1, -2])
    module_transverse_left = sp.Matrix(
        [sp.Rational(1, 2), -sp.Rational(1, 4)]
    )
    critical_right = embedding * critical_module_right
    critical_left = module_average.T * critical_module_left
    module_transverse_right_lift = embedding * module_transverse_right
    module_transverse_left_lift = (
        module_average.T * module_transverse_left
    )
    critical_projector = critical_right * critical_left.T
    module_transverse_projector = (
        module_transverse_right_lift * module_transverse_left_lift.T
    )
    within_projector = sp.eye(node_count) - module_projector
    transverse_projector = sp.eye(node_count) - critical_projector

    sigma = sp.sqrt(sp.Rational(3, 2))
    equilibrium_voltage = embedding * sp.Matrix([sigma, 0])
    equilibrium_recovery = embedding * sp.Matrix([0, 2 * sigma])
    base_fast_jacobian = sp.Matrix(
        [[-1, sp.Rational(1, 2)], [2, -1]]
    )
    fast_voltage_jacobian = (
        embedding * base_fast_jacobian * module_average
        - voltage_rate * within_projector
    )
    recovery_jacobian = -recovery * transverse_projector
    singular_jacobian = sp.Matrix.vstack(
        sp.Matrix.hstack(fast_voltage_jacobian, -sp.eye(node_count)),
        sp.Matrix.hstack(sp.zeros(node_count), recovery_jacobian),
    )
    state_critical_projector = sp.diag(
        critical_projector, critical_projector
    )
    state_transverse_projector = sp.diag(
        transverse_projector, transverse_projector
    )

    # D_v^2 F(v_*,w_*)[r,r]=(-2*sigma,0)^T in the base model.
    critical_hessian_vector = embedding * sp.Matrix([-2 * sigma, 0])
    fold_curvature = sp.simplify(
        (critical_left.T * critical_hessian_vector)[0]
    )

    layer_0_base = sp.Matrix(
        [
            [sp.Rational(1, 6), sp.Rational(1, 12)],
            [sp.Rational(1, 6), sp.Rational(1, 4)],
        ]
    )
    layer_1_base = sp.Matrix(
        [
            [sp.Rational(1, 3), sp.Rational(1, 6)],
            [sp.Rational(1, 2), sp.Rational(5, 12)],
        ]
    )
    module_direction = sp.Matrix([[1, 0], [-2, 0]])
    module_layer_0 = layer_0_base + redistribution * module_direction
    module_layer_1 = layer_1_base - redistribution * module_direction
    module_total_layer = layer_0_base + layer_1_base
    layer_0 = embedding * module_layer_0 * module_average
    layer_1 = embedding * module_layer_1 * module_average
    total_layer = embedding * module_total_layer * module_average

    return LiftedTwoModuleNetwork(
        n1=n1,
        n2=n2,
        within_voltage_rate=voltage_rate,
        recovery_rate=recovery,
        module_redistribution=redistribution,
        embedding=_immutable(embedding),
        module_average=_immutable(module_average),
        module_projector=_immutable(module_projector),
        module_metric=_immutable(module_metric),
        node_metric=_immutable(node_metric),
        critical_module_right=_immutable(critical_module_right),
        critical_module_left=_immutable(critical_module_left),
        module_transverse_right=_immutable(module_transverse_right),
        module_transverse_left=_immutable(module_transverse_left),
        critical_right=_immutable(critical_right),
        critical_left=_immutable(critical_left),
        module_transverse_right_lift=_immutable(
            module_transverse_right_lift
        ),
        module_transverse_left_lift=_immutable(
            module_transverse_left_lift
        ),
        critical_projector=_immutable(critical_projector),
        module_transverse_projector=_immutable(
            module_transverse_projector
        ),
        within_projector=_immutable(within_projector),
        transverse_projector=_immutable(transverse_projector),
        equilibrium_voltage=_immutable(equilibrium_voltage),
        equilibrium_recovery=_immutable(equilibrium_recovery),
        base_fast_jacobian=_immutable(base_fast_jacobian),
        fast_voltage_jacobian=_immutable(fast_voltage_jacobian),
        recovery_jacobian=_immutable(recovery_jacobian),
        singular_jacobian=_immutable(singular_jacobian),
        state_critical_projector=_immutable(state_critical_projector),
        state_transverse_projector=_immutable(state_transverse_projector),
        critical_hessian_vector=_immutable(critical_hessian_vector),
        fold_curvature=fold_curvature,
        module_layer_0=_immutable(module_layer_0),
        module_layer_1=_immutable(module_layer_1),
        module_total_layer=_immutable(module_total_layer),
        layer_0=_immutable(layer_0),
        layer_1=_immutable(layer_1),
        total_layer=_immutable(total_layer),
    )


@dataclass(frozen=True)
class MaxNormProjectionAudit:
    """Exact and dimension-uniform maximum-norm projection constants."""

    embedding_norm: sp.Expr
    module_average_norm: sp.Expr
    module_projector_norm: sp.Expr
    critical_projector_norm: sp.Expr
    module_transverse_projector_norm: sp.Expr
    within_projector_norm: sp.Expr
    transverse_projector_norm: sp.Expr
    critical_injection_norm: sp.Expr
    critical_extraction_norm: sp.Expr
    module_transverse_injection_norm: sp.Expr
    module_transverse_extraction_norm: sp.Expr
    uniform_within_projector_bound: sp.Expr
    uniform_transverse_projector_bound: sp.Expr
    uniform_coordinate_extraction_bound: sp.Expr
    uniform_coordinate_reconstruction_bound: sp.Expr


def max_norm_projection_audit(
    network: LiftedTwoModuleNetwork,
) -> MaxNormProjectionAudit:
    r"""Audit the critical/transverse split in ``ell_infinity``.

    The stable coordinate is ``P_perp x`` with
    ``P_perp=I-P_c`` and the critical coordinate is ``ell_N^T x``.  With the
    maximum product norm, coordinate extraction is bounded by ``5/2`` and
    reconstruction ``(a,h) -> r_N*a+h`` by ``3``, uniformly in both module
    sizes.  These are the conditioning constants relevant to the abstract
    dimension-uniform history-graph theorem.
    """

    return MaxNormProjectionAudit(
        embedding_norm=matrix_infinity_operator_norm(network.embedding),
        module_average_norm=matrix_infinity_operator_norm(
            network.module_average
        ),
        module_projector_norm=matrix_infinity_operator_norm(
            network.module_projector
        ),
        critical_projector_norm=matrix_infinity_operator_norm(
            network.critical_projector
        ),
        module_transverse_projector_norm=matrix_infinity_operator_norm(
            network.module_transverse_projector
        ),
        within_projector_norm=matrix_infinity_operator_norm(
            network.within_projector
        ),
        transverse_projector_norm=matrix_infinity_operator_norm(
            network.transverse_projector
        ),
        critical_injection_norm=matrix_infinity_operator_norm(
            network.critical_right
        ),
        critical_extraction_norm=matrix_infinity_operator_norm(
            network.critical_left.T
        ),
        module_transverse_injection_norm=matrix_infinity_operator_norm(
            network.module_transverse_right_lift
        ),
        module_transverse_extraction_norm=matrix_infinity_operator_norm(
            network.module_transverse_left_lift.T
        ),
        uniform_within_projector_bound=sp.Integer(2),
        uniform_transverse_projector_bound=sp.Rational(5, 2),
        uniform_coordinate_extraction_bound=sp.Rational(5, 2),
        uniform_coordinate_reconstruction_bound=sp.Integer(3),
    )


def lifted_fast_field(
    network: LiftedTwoModuleNetwork,
    voltage: sp.MatrixBase,
    recovery: sp.MatrixBase,
) -> Matrix:
    r"""Evaluate the exact nodewise-cubic fast field of the lifted class.

    A node in module one receives

    ``v_i-v_i^3/3-w_i + (mean_2(v)-v_i)/2``;

    a node in module two receives

    ``v_i-v_i^3/3-w_i + 2*(mean_1(v)-v_i)``.

    The additional term ``-(Dv-1)*(I-SR)*(v-v_*)`` sets every within-module
    voltage rate to ``-Dv`` without changing the module-constant restriction.
    Hence the field is a genuine nodewise nonlinear realization, not merely a
    nonlinear function of the two averages.
    """

    voltage = sp.Matrix(voltage)
    recovery = sp.Matrix(recovery)
    expected_shape = (network.node_count, 1)
    if voltage.shape != expected_shape or recovery.shape != expected_shape:
        raise ValueError(
            f"voltage and recovery must both have shape {expected_shape}"
        )
    means = network.module_average * voltage
    within_voltage = network.within_projector * (
        voltage - network.equilibrium_voltage
    )
    values = sp.zeros(network.node_count, 1)
    for index in range(network.node_count):
        value = voltage[index]
        local = value - value**3 / 3 - recovery[index]
        if index < network.n1:
            coupling = (means[1] - value) / 2
        else:
            coupling = 2 * (means[0] - value)
        values[index] = (
            local
            + coupling
            - (network.within_voltage_rate - 1) * within_voltage[index]
        )
    return _immutable(values)


def lifted_recovery_slow_field(
    network: LiftedTwoModuleNetwork,
    voltage: sp.MatrixBase,
    unfolding: sp.Expr,
) -> Matrix:
    r"""Return the unscaled nodewise slow field before recovery scaffolding.

    Module-one entries are ``v_i-sigma-mu`` and module-two entries are
    ``v_i-2*mu``.  On ``v=v_*+r_N X`` this equals ``r_N*(X-mu)`` exactly.
    The full recovery equation multiplies this field by ``epsilon`` and adds
    ``-Dw*(I-Pc)*(w-w_*)``.
    """

    voltage = sp.Matrix(voltage)
    expected_shape = (network.node_count, 1)
    if voltage.shape != expected_shape:
        raise ValueError(f"voltage must have shape {expected_shape}")
    unfolding = sp.sympify(unfolding)
    sigma = sp.sqrt(sp.Rational(3, 2))
    values = sp.zeros(network.node_count, 1)
    for index in range(network.node_count):
        if index < network.n1:
            values[index] = voltage[index] - sigma - unfolding
        else:
            values[index] = voltage[index] - 2 * unfolding
    return _immutable(values)


@dataclass(frozen=True)
class MaxNormLocalJetAudit:
    """Dimension-uniform local jets on a coordinatewise box."""

    voltage_box_radius: sp.Expr
    recovery_box_radius: sp.Expr
    unfolding_box_radius: sp.Expr
    absolute_voltage_bound: sp.Expr
    absolute_recovery_bound: sp.Expr
    fast_jet_bounds: tuple[sp.Expr, ...]
    slow_jet_bounds: tuple[sp.Expr, ...]
    critical_output_bound: sp.Expr
    transverse_output_bound: sp.Expr


def max_norm_local_jet_audit(
    network: LiftedTwoModuleNetwork,
    *,
    voltage_box_radius: sp.Expr,
    recovery_box_radius: sp.Expr,
    unfolding_box_radius: sp.Expr,
    jet_order: int = 12,
) -> MaxNormLocalJetAudit:
    r"""Return uniform ``C^jet_order`` bounds in the maximum product norm.

    The box is centered at ``(v_*,w_*,mu=0)`` and is coordinatewise:

    ``||v-v_*||_infinity <= L_v``, ``||w-w_*||_infinity <= L_w``, and
    ``|mu| <= L_mu``.

    The domain norm for the fast field is
    ``max(||Delta v||_infinity,||Delta w||_infinity)``.  For the slow field it
    is ``max(||Delta v||_infinity,|Delta mu|)``.  Entries ``k`` of the returned
    tuples bound the induced norm of the ``k``th Frechet derivative.  Since
    the only nonlinearity is the diagonal nodewise cubic, the fast derivatives
    vanish from order four onward and the slow derivatives vanish from order
    two onward.  No coordinate sum, and hence no factor depending on ``N``,
    appears.

    These are local model-fitting estimates.  They do not construct the
    bounded preparation required by the global fixed-point statement.
    """

    if not isinstance(jet_order, int) or isinstance(jet_order, bool):
        raise ValueError("jet_order must be a nonnegative integer")
    if jet_order < 0:
        raise ValueError("jet_order must be a nonnegative integer")
    voltage_radius = _nonnegative(voltage_box_radius, "voltage_box_radius")
    recovery_radius = _nonnegative(
        recovery_box_radius, "recovery_box_radius"
    )
    unfolding_radius = _nonnegative(
        unfolding_box_radius, "unfolding_box_radius"
    )

    sigma = sp.sqrt(sp.Rational(3, 2))
    absolute_voltage = sigma + voltage_radius
    absolute_recovery = 2 * sigma + recovery_radius
    scaffold = 2 * sp.Abs(network.within_voltage_rate - 1)

    fast_bounds = [sp.Integer(0)] * (jet_order + 1)
    fast_bounds[0] = sp.simplify(
        5 * absolute_voltage
        + absolute_voltage**3 / 3
        + absolute_recovery
        + scaffold * voltage_radius
    )
    if jet_order >= 1:
        # D_v: diagonal cubic (1+B^2), cross-module coupling (4), and
        # within-module scaffold; D_w contributes one in the max product norm.
        fast_bounds[1] = sp.simplify(
            6 + absolute_voltage**2 + scaffold
        )
    if jet_order >= 2:
        fast_bounds[2] = 2 * absolute_voltage
    if jet_order >= 3:
        fast_bounds[3] = sp.Integer(2)

    slow_bounds = [sp.Integer(0)] * (jet_order + 1)
    slow_bounds[0] = voltage_radius + 2 * unfolding_radius
    if jet_order >= 1:
        slow_bounds[1] = sp.Integer(3)

    return MaxNormLocalJetAudit(
        voltage_box_radius=voltage_radius,
        recovery_box_radius=recovery_radius,
        unfolding_box_radius=unfolding_radius,
        absolute_voltage_bound=absolute_voltage,
        absolute_recovery_bound=absolute_recovery,
        fast_jet_bounds=tuple(fast_bounds),
        slow_jet_bounds=tuple(slow_bounds),
        critical_output_bound=sp.Rational(3, 4),
        transverse_output_bound=sp.Rational(5, 2),
    )


@dataclass(frozen=True)
class TransverseSemigroupCertificate:
    """Diagnostic weighted-Hilbert bound for the transverse semigroup."""

    module_voltage_rate: sp.Expr
    within_voltage_rate: sp.Expr
    recovery_rate: sp.Expr
    minimum_rate: sp.Expr
    decay_rate: sp.Expr
    multiplicative_constant: sp.Expr


def transverse_semigroup_certificate(
    network: LiftedTwoModuleNetwork,
) -> TransverseSemigroupCertificate:
    r"""Return diagnostic ``W_N`` semigroup constants.

    In the weighted orthogonal decomposition, the only two block types are

    ``[[-2,-1],[0,-Dw]]`` and ``[[-Dv,-1],[0,-Dw]]``.

    Put ``rho=min(2,Dv,Dw)``.  Variation of constants gives an off-diagonal
    entry bounded by ``t*exp(-rho*t)``.  Since
    ``t*exp(-rho*t/2) <= 2/(e*rho)``, one may take
    ``kappa=rho/2`` and ``M=1+2/(e*rho)``.  Neither constant contains the
    module sizes.
    """

    minimum_rate = sp.Min(
        sp.Integer(2),
        network.within_voltage_rate,
        network.recovery_rate,
    )
    return TransverseSemigroupCertificate(
        module_voltage_rate=sp.Integer(2),
        within_voltage_rate=network.within_voltage_rate,
        recovery_rate=network.recovery_rate,
        minimum_rate=minimum_rate,
        decay_rate=minimum_rate / 2,
        multiplicative_constant=1 + 2 / (sp.E * minimum_rate),
    )


@dataclass(frozen=True)
class MaxNormTransverseSemigroupCertificate:
    """Dimension-independent singular semigroup bound in max-product norm."""

    module_voltage_rate: sp.Expr
    within_voltage_rate: sp.Expr
    recovery_rate: sp.Expr
    minimum_rate: sp.Expr
    decay_rate: sp.Expr
    projector_sum_bound: sp.Expr
    multiplicative_constant: sp.Expr


def max_norm_transverse_semigroup_certificate(
    network: LiftedTwoModuleNetwork,
) -> MaxNormTransverseSemigroupCertificate:
    r"""Bound the transverse singular semigroup in the Gate A norm.

    On ``range(I-P_c)`` the voltage semigroup is

    ``exp(-2t) P_m + exp(-D_v t) P_w``.

    The recovery-to-voltage convolution has the same projector decomposition.
    In ``ell_infinity``, ``||P_m||=3/2`` and ``||P_w||<=2``.  Thus, with
    ``C_P=7/2`` and ``rho=min(2,D_v,D_w)``, the maximum-product state norm
    obeys

    ``||T_perp(t)|| <= C_P (1+t) exp(-rho*t)``.

    Using ``t*exp(-rho*t/2)<=2/(e*rho)`` gives the returned exponential bound.
    Its constants are independent of both module sizes.  This is the singular
    stable-semigroup input to the graph-first argument, not by itself a
    complete normal-form fit.
    """

    minimum_rate = sp.Min(
        sp.Integer(2),
        network.within_voltage_rate,
        network.recovery_rate,
    )
    projector_sum = sp.Rational(7, 2)
    return MaxNormTransverseSemigroupCertificate(
        module_voltage_rate=sp.Integer(2),
        within_voltage_rate=network.within_voltage_rate,
        recovery_rate=network.recovery_rate,
        minimum_rate=minimum_rate,
        decay_rate=minimum_rate / 2,
        projector_sum_bound=projector_sum,
        multiplicative_constant=projector_sum
        * (1 + 2 / (sp.E * minimum_rate)),
    )


def weighted_frobenius_squared(
    matrix: sp.MatrixBase,
    metric: sp.MatrixBase,
) -> sp.Expr:
    r"""Return ``||W^(1/2) A W^(-1/2)||_F^2`` exactly.

    Its square root bounds the induced weighted Euclidean operator norm.  For
    a rank-one matrix the two norms agree.
    """

    matrix = sp.Matrix(matrix)
    metric = sp.Matrix(metric)
    if matrix.rows != matrix.cols:
        raise ValueError("matrix must be square")
    if metric.shape != matrix.shape or not metric.is_diagonal():
        raise ValueError("metric must be a diagonal matrix of matching size")
    if any(entry.is_positive is not True for entry in metric.diagonal()):
        raise ValueError("metric diagonal entries must be known positive")
    transformed_square = (
        metric.inv() * matrix.T * metric * matrix
    ).trace()
    return sp.simplify(transformed_square)


@dataclass(frozen=True)
class MaxNormLiftedDelayAudit:
    """Exact maximum-norm bounds for the equitable lifted delay layers."""

    module_layer_norms: tuple[sp.Expr, sp.Expr]
    lifted_layer_norms: tuple[sp.Expr, sp.Expr]
    module_total_layer_norm: sp.Expr
    lifted_total_layer_norm: sp.Expr
    delayed_operator_tv: sp.Expr
    balanced_feedback_bound: sp.Expr


def max_norm_lifted_delay_audit(
    network: LiftedTwoModuleNetwork,
) -> MaxNormLiftedDelayAudit:
    r"""Return exact ``ell_infinity`` norms of ``S C_k R``.

    Because replication and averaging both have maximum-norm operator norm
    one, ``||S C_k R||_infinity=||C_k||_infinity`` exactly.  Equality follows
    by testing module-constant sign vectors.  When the two atom locations are
    distinct, the delayed atomic measure has total variation
    ``sum_k ||S C_k R||``.  If atoms coincide, this sum remains an upper
    bound but cancellation must be taken before claiming equality.  Adding
    the current term ``SBR`` gives the displayed balanced-feedback upper
    bound.
    """

    module_norms = (
        matrix_infinity_operator_norm(network.module_layer_0),
        matrix_infinity_operator_norm(network.module_layer_1),
    )
    lifted_norms = (
        matrix_infinity_operator_norm(network.layer_0),
        matrix_infinity_operator_norm(network.layer_1),
    )
    module_total = matrix_infinity_operator_norm(network.module_total_layer)
    lifted_total = matrix_infinity_operator_norm(network.total_layer)
    delayed_tv = sp.simplify(module_norms[0] + module_norms[1])
    return MaxNormLiftedDelayAudit(
        module_layer_norms=module_norms,
        lifted_layer_norms=lifted_norms,
        module_total_layer_norm=module_total,
        lifted_total_layer_norm=lifted_total,
        delayed_operator_tv=delayed_tv,
        balanced_feedback_bound=sp.simplify(delayed_tv + lifted_total),
    )


@dataclass(frozen=True)
class AtomicDelayResidualAudit:
    """Exact projections and computable TV bounds for atomic residual layers."""

    delays: tuple[sp.Expr, ...]
    residual_layers: tuple[Matrix, ...]
    module_restrictions: tuple[Matrix, ...]
    average_output_residuals: tuple[Matrix, ...]
    equitability_residuals: tuple[Matrix, ...]
    critical_output_residuals: tuple[Matrix, ...]
    total_layer_residual: Matrix
    infinity_operator_norms: tuple[sp.Expr, ...]
    operator_tv_infinity_upper: sp.Expr
    balanced_feedback_infinity_upper: sp.Expr
    weighted_frobenius_squares: tuple[sp.Expr, ...]
    operator_tv_frobenius_upper: sp.Expr
    balanced_feedback_frobenius_upper: sp.Expr


def audit_atomic_delay_residual(
    network: LiftedTwoModuleNetwork,
    residual_layers: Iterable[sp.MatrixBase],
    delays: Iterable[sp.Expr],
) -> AtomicDelayResidualAudit:
    r"""Audit a finite atomic matrix-measure residual.

    If ``E_k`` is attached to delay ``theta_k``, then

    ``D_E phi = sum_k E_k phi(-theta_k)``

    has operator norm at most ``sum_k ||E_k||_infinity`` from the nodewise
    maximum history norm to node space.  This is the primary Gate A audit.
    The function also retains the computable weighted-Hilbert upper bound
    obtained by replacing each induced norm by its weighted Frobenius norm;
    that second bound is diagnostic only.  The balanced feedback

    ``(sum E_k) phi(0) - sum E_k phi(-theta_k)``

    is bounded by the TV bound plus ``||sum E_k||_infinity``.  These
    inequalities are exact functional-analytic estimates for fixed atoms;
    they are not an RFDE graph or root theorem.
    """

    layers = tuple(sp.Matrix(layer) for layer in residual_layers)
    delay_tuple = tuple(sp.sympify(delay) for delay in delays)
    if not layers:
        raise ValueError("at least one residual layer is required")
    if len(layers) != len(delay_tuple):
        raise ValueError("residual_layers and delays must have equal length")
    node_count = network.node_count
    if any(layer.shape != (node_count, node_count) for layer in layers):
        raise ValueError(
            f"each residual layer must be {node_count}-by-{node_count}"
        )

    module_restrictions = tuple(
        network.module_average * layer * network.embedding
        for layer in layers
    )
    average_outputs = tuple(network.module_average * layer for layer in layers)
    equitability = tuple(
        network.within_projector * layer * network.embedding
        for layer in layers
    )
    critical_outputs = tuple(
        network.critical_left.T * layer for layer in layers
    )
    total = sum(layers, sp.zeros(node_count))
    infinity_norms = tuple(
        matrix_infinity_operator_norm(layer) for layer in layers
    )
    infinity_tv = sp.simplify(
        sum(infinity_norms, sp.Integer(0))
    )
    infinity_feedback = sp.simplify(
        infinity_tv + matrix_infinity_operator_norm(total)
    )
    frobenius_squares = tuple(
        weighted_frobenius_squared(layer, network.node_metric)
        for layer in layers
    )
    tv_upper = sp.simplify(
        sum((sp.sqrt(value) for value in frobenius_squares), sp.Integer(0))
    )
    total_bound = sp.sqrt(
        weighted_frobenius_squared(total, network.node_metric)
    )
    feedback_upper = sp.simplify(tv_upper + total_bound)

    return AtomicDelayResidualAudit(
        delays=delay_tuple,
        residual_layers=tuple(_immutable(layer) for layer in layers),
        module_restrictions=tuple(
            _immutable(value) for value in module_restrictions
        ),
        average_output_residuals=tuple(
            _immutable(value) for value in average_outputs
        ),
        equitability_residuals=tuple(
            _immutable(value) for value in equitability
        ),
        critical_output_residuals=tuple(
            _immutable(value) for value in critical_outputs
        ),
        total_layer_residual=_immutable(total),
        infinity_operator_norms=infinity_norms,
        operator_tv_infinity_upper=infinity_tv,
        balanced_feedback_infinity_upper=infinity_feedback,
        weighted_frobenius_squares=frobenius_squares,
        operator_tv_frobenius_upper=tv_upper,
        balanced_feedback_frobenius_upper=feedback_upper,
    )


@dataclass(frozen=True)
class EquitabilityBreakingRedistribution:
    """Rank-one, projection-invisible two-delay redistribution."""

    receiving_module: int
    source_module: int
    receiving_pattern: str
    amplitude: sp.Expr
    unit_within_vector: Matrix
    unit_source_functional: Matrix
    generator: Matrix
    residual_layer_0: Matrix
    residual_layer_1: Matrix
    exact_layer_weighted_operator_norm: sp.Expr
    exact_operator_tv_weighted: sp.Expr
    exact_layer_infinity_operator_norm: sp.Expr
    exact_operator_tv_infinity: sp.Expr
    dimension_uniform_infinity_generator_bound: sp.Expr
    affected_entry_symmetric_radius: sp.Expr
    dimension_uniform_affected_radius_lower_bound: sp.Expr
    unaffected_base_positivity_status: bool | None
    all_base_positivity_status: bool | None
    certified_full_positivity_radius: sp.Expr
    certified_dimension_uniform_full_positivity_lower_bound: sp.Expr


def equitability_breaking_redistribution(
    network: LiftedTwoModuleNetwork,
    amplitude: sp.Expr,
    *,
    receiving_module: int = 1,
    source_module: int = 1,
    receiving_pattern: str = "distributed",
) -> EquitabilityBreakingRedistribution:
    r"""Construct arbitrarily small layers that break module equitability.

    The receiving module must contain at least two nodes.  By default ``u``
    is a distributed weighted-unit zero-mean vector: its first
    ``floor(n/2)`` entries are equal and positive and the remainder are equal
    and negative.  ``receiving_pattern="sparse"`` instead uses the first-two-
    node difference as a finite-size contrast.  Let ``rho`` be the weighted-
    unit module-average source functional.  Then ``G=u*rho`` has weighted
    operator norm one and rank one.  The two residual atoms
    ``(+a*G,-a*G)`` satisfy, exactly,

    ``R E_k = 0``, ``ell_N^T E_k = 0``, and ``E_0+E_1=0``,

    while ``(I-SR)E_k S`` is nonzero for ``a != 0``.  Thus the reduced
    two-module layers, complete direct critical projection, and total gain
    stay fixed although equitability fails.  Their exact weighted-Hilbert
    operator-TV norm is ``2*Abs(a)``; the maximum-norm value is returned in a
    separate field.

    ``affected_entry_symmetric_radius`` concerns only entries changed by
    ``(+aG,-aG)`` and is meaningful under positivity of those base entries.
    Full entrywise positivity additionally requires *every unaffected entry*
    of both base layers to be strictly positive.  The returned positivity
    status records that separate condition; a positive affected-entry radius
    alone is never reported as a full-layer certificate.  For the distributed
    pattern, the maximum-norm generator and affected-entry radius have bounds
    uniform in the module sizes.  The sparse contrast has neither property.
    """

    if receiving_module not in (1, 2):
        raise ValueError("receiving_module must be 1 or 2")
    if source_module not in (1, 2):
        raise ValueError("source_module must be 1 or 2")
    if receiving_pattern not in ("distributed", "sparse"):
        raise ValueError(
            "receiving_pattern must be 'distributed' or 'sparse'"
        )
    receiving_size = network.n1 if receiving_module == 1 else network.n2
    if receiving_size < 2:
        raise ValueError("receiving module must contain at least two nodes")

    node_count = network.node_count
    offset = 0 if receiving_module == 1 else network.n1
    raw_within = sp.zeros(node_count, 1)
    if receiving_pattern == "sparse":
        raw_within[offset, 0] = 1
        raw_within[offset + 1, 0] = -1
    else:
        positive_count = receiving_size // 2
        negative_count = receiving_size - positive_count
        negative_value = -sp.Rational(positive_count, negative_count)
        for local_index in range(positive_count):
            raw_within[offset + local_index, 0] = 1
        for local_index in range(positive_count, receiving_size):
            raw_within[offset + local_index, 0] = negative_value
    within_norm_squared = sp.simplify(
        (raw_within.T * network.node_metric * raw_within)[0]
    )
    unit_within = raw_within / sp.sqrt(within_norm_squared)

    raw_source = network.module_average.row(source_module - 1)
    source_norm_squared = sp.simplify(
        (raw_source * network.node_metric.inv() * raw_source.T)[0]
    )
    unit_source = raw_source / sp.sqrt(source_norm_squared)
    generator = sp.simplify(unit_within * unit_source)
    amplitude = sp.sympify(amplitude)
    residual_0 = amplitude * generator
    residual_1 = -amplitude * generator

    ratios: list[sp.Expr] = []
    affected_positions: set[tuple[int, int, int]] = set()
    for base_layer, sign in (
        (network.layer_0, sp.Integer(1)),
        (network.layer_1, sp.Integer(-1)),
    ):
        layer_index = 0 if sign == 1 else 1
        for row in range(node_count):
            for column in range(node_count):
                coefficient = sp.simplify(sign * generator[row, column])
                if coefficient != 0:
                    affected_positions.add((layer_index, row, column))
                    ratios.append(
                        sp.simplify(base_layer[row, column] / sp.Abs(coefficient))
                    )
    affected_radius = sp.Min(*ratios) if ratios else sp.oo

    def positivity_status(expressions: Iterable[sp.Expr]) -> bool | None:
        statuses = [sp.sympify(value).is_positive for value in expressions]
        if any(status is False for status in statuses):
            return False
        if all(status is True for status in statuses):
            return True
        return None

    base_layers = (network.layer_0, network.layer_1)
    unaffected_entries = [
        base_layer[row, column]
        for layer_index, base_layer in enumerate(base_layers)
        for row in range(node_count)
        for column in range(node_count)
        if (layer_index, row, column) not in affected_positions
    ]
    all_base_entries = [
        entry for base_layer in base_layers for entry in base_layer
    ]
    unaffected_status = positivity_status(unaffected_entries)
    all_base_status = positivity_status(all_base_entries)

    if receiving_pattern == "distributed":
        receiving_weight = (
            sp.Rational(1, 2)
            if receiving_module == 1
            else sp.Rational(1, 8)
        )
        source_weight = (
            sp.Rational(1, 2)
            if source_module == 1
            else sp.Rational(1, 8)
        )
        affected_module_entries = (
            network.module_layer_0[
                receiving_module - 1, source_module - 1
            ],
            network.module_layer_1[
                receiving_module - 1, source_module - 1
            ],
        )
        uniform_affected_radius = sp.simplify(
            sp.Min(*affected_module_entries)
            * sp.sqrt(receiving_weight / (2 * source_weight))
        )
        infinity_generator_bound = sp.sqrt(
            2 * source_weight / receiving_weight
        )
    else:
        uniform_affected_radius = sp.Integer(0)
        infinity_generator_bound = sp.oo

    generator_infinity_norm = matrix_infinity_operator_norm(generator)
    if all_base_status is True:
        certified_full_radius = sp.simplify(affected_radius)
        certified_uniform_radius = sp.simplify(uniform_affected_radius)
    else:
        certified_full_radius = sp.Integer(0)
        certified_uniform_radius = sp.Integer(0)

    return EquitabilityBreakingRedistribution(
        receiving_module=receiving_module,
        source_module=source_module,
        receiving_pattern=receiving_pattern,
        amplitude=amplitude,
        unit_within_vector=_immutable(unit_within),
        unit_source_functional=_immutable(unit_source),
        generator=_immutable(generator),
        residual_layer_0=_immutable(residual_0),
        residual_layer_1=_immutable(residual_1),
        exact_layer_weighted_operator_norm=sp.Abs(amplitude),
        exact_operator_tv_weighted=2 * sp.Abs(amplitude),
        exact_layer_infinity_operator_norm=sp.simplify(
            sp.Abs(amplitude) * generator_infinity_norm
        ),
        exact_operator_tv_infinity=sp.simplify(
            2 * sp.Abs(amplitude) * generator_infinity_norm
        ),
        dimension_uniform_infinity_generator_bound=sp.simplify(
            infinity_generator_bound
        ),
        affected_entry_symmetric_radius=sp.simplify(affected_radius),
        dimension_uniform_affected_radius_lower_bound=uniform_affected_radius,
        unaffected_base_positivity_status=unaffected_status,
        all_base_positivity_status=all_base_status,
        certified_full_positivity_radius=certified_full_radius,
        certified_dimension_uniform_full_positivity_lower_bound=(
            certified_uniform_radius
        ),
    )
