# Frozen finite-network promotion specification

Status: **future-work contract, not the current paper, 2026-08-22**. The correctly augmented
\(\mathbb R^4\) reference-gap template, dual-scaffold \(2N\)-state operator
contract, and concrete control benchmark are frozen, and exact/formal
algebraic checks are executable. The actual endpoint bundles, model-specific
Fredholm proof, uniform remainder, and control corollary remain targets.

## 1. Future-promotion model class

For nodes \(i=1,\dots,N\), consider

\[
\dot x_i=f(x_i,y_i;\mu,u)
+\mathcal S^x_{N,i}(x)
+\varepsilon
\sum_{j=1}^N W_{ij}
q\!\left(x_i(t),x_j(t),x_j(t-\tau_{ij});u\right),
\qquad
\dot y_i=\varepsilon g(x_i,y_i;\mu,u)
+\mathcal S^y_{N,i}(y),
\tag{1}
\]

with \(0<\varepsilon\ll1\), weak delayed feedback satisfying
\(q(x,x,x;u)=0\), and

\[
\tau_{ij}=\Theta_{ij}/\sqrt\varepsilon,
\qquad \Theta_{ij}\in[0,\Theta_{\max}].
\tag{2}
\]

The fixed instantaneous scaffolds \(\mathcal S_N^x,\mathcal S_N^y\) vanish on
the selected collective history. The concrete FHN benchmark uses
\(D(P-I)x\) and \(E(P-I)y\), with fixed \(D,E>0\). The voltage scaffold
isolates one fast fold direction; the recovery scaffold removes the
\(N-1\) transverse slow centers that otherwise survive at
\(\varepsilon=0\). Neither is an actuator, and neither alters the collective
weak-delay calibration. The voltage-only case is a negative control, not the
proof reference.

Off synchrony, the concrete dual-scaffold benchmark is not an
\(N\)-slow-neuron system: transverse recovery differences relax on an
\(O(1)\) physical time scale and only the collective recovery coordinate is
slow. This restriction would be disclosed as part of the future-promotion model class;
the original \(N\)-slow voltage-only network remains a harder extension.

After fold blow-up and time rescaling, the scaled history interval is the fixed compact interval \([-\Theta_{\max},0]\). Version 1 treats moving point delays as finitely many smooth parameters on a strong Sobolev orbit space and permits infinite-dimensional measure perturbations only on fixed delay support. The ordinary operator norm on \(C^0\) is not used to declare two nearby point delays close. Freely moving measure support in a bounded-Lipschitz/Wasserstein space is an extension unless the required \(C^2\) theorem is supplied.

The future theorem target is a finite network near one exact equitable
**two-module** skeleton. Nodes in the same receiving module have the same
row-weighted delay measure from each source module, so block-synchronous
histories close exactly. One collective canard direction is a hypothesis to
be verified by the augmented Lin BVP; equitability and the instantaneous
singular-Jacobian calculation alone do not imply it. The concrete control
benchmark uses the dual-state scaffold above. The identical-module weak-only
and voltage-only classes are retained as negative controls.

General rank-\(r\) closure is an extension. An adjacency-matrix spectral gap may help verify hypotheses, but it is not substituted for the RFDE variational estimate along the canard orbit.

Write the raw structural residual as

\[
\mathcal R_N=(\Delta W_N,\Delta\rho_N,\Delta p_N),
\qquad
\eta_N^{\rm raw}=\|\mathcal R_N\|_{\mathfrak R},
\tag{3}
\]

where \(\|\cdot\|_{\mathfrak R}\) is fixed before the theorem is stated and controls edge weights, fixed-support delay measures, finite delay-location parameters, and node heterogeneity. The range-equation smallness uses the induced blown-up BVP residual

\[
\eta_N^{\rm op}
=\|\mathfrak F_{\delta,N}(\cdot,\nu,\mathcal R_N)
-\mathfrak F_{\delta,N}(\cdot,\nu,0)\|_{\mathscr Y_N},
\tag{4}
\]

not the raw norm by itself. For weak weight coupling, for example,
\(\eta_N^{\rm op}=O(\sqrt\varepsilon |K|\eta_W^{\rm raw})\).

## 2. The mathematical object: a one-dimensional Lin gap

The threshold is not defined by subtracting two sets such as \(M^a\cap\Sigma\) and \(M^r\cap\Sigma\). Instead:

1. fix compact entry and exit data and one transverse matching section \(\Sigma\), which supplies the phase condition;
2. solve the attracting and repelling RFDE boundary-value pieces while matching every transverse coordinate;
3. leave one scalar jump in a fixed cokernel direction \(\psi_{\delta,N}\).

Let \(\bar{\mathfrak F}_\delta\) denote the \(\mathbb R^4\) reference
template in [the feasibility note](lin-gap-feasibility.md). For an \(N\)-node
residual, the theorem still has to construct its full-history extension
\(\mathfrak F_{\delta,N}(z_N,\nu,\mathcal R_N)=0\) on
\(C([-\Theta_{\max},0],\mathbb R^{2N})\), with a complete \(2N\)-state jump,
where \(a=1+\delta^2\nu\). After its single phase condition, require

\[
L_{\delta,N}=D_{z_N}\mathfrak F_{\delta,N},
\qquad
\ker L_{\delta,N}=\{0\},
\qquad
\dim\operatorname{coker}L_{\delta,N}=1,
\qquad
\operatorname{ind}L_{\delta,N}=-1.
\tag{5}
\]

The domain/codomain, full jump, and transverse trace-index contract are fixed
in [the full-network operator note](full-network-lin-operator.md). In
particular, the reduced two-dimensional current-state skeleton has the
necessary diagnostic \(d_-+d_+=2\). The actual RFDE theorem must construct a
history-space Fredholm trace pair of index zero; the skeleton count is not a
substitute for that proof.

Choose \(\psi_{\delta,N}\in\mathscr Y_N^*\) and
\(e_{\delta,N}\in\mathscr Y_N\) such that

\[
\operatorname{Range}L_{\delta,N}=\ker\psi_{\delta,N},
\qquad
\psi_{\delta,N}(e_{\delta,N})=1,
\tag{6}
\]

with \(e_{\delta,N}\) supported only in the history-jump component. The
index-zero augmented operator

\[
\widehat L_{\delta,N}(\zeta,\gamma)
=L_{\delta,N}\zeta-\gamma e_{\delta,N}
\tag{7}
\]

must be invertible. The claimed transverse/range bound must be uniform in the
admitted network sizes:

\[
\left\|
(L_{\delta,N}:\mathscr X_N\to\operatorname{Range}L_{\delta,N})^{-1}
\right\|
\le G_\perp(\delta).
\tag{8}
\]

Solving

\[
\mathfrak F_{\delta,N}(z_N(\nu,\mathcal R_N),\nu,\mathcal R_N)
=d_{\delta,N}(\nu,\mathcal R_N)e_{\delta,N}
\tag{9}
\]

defines the strict scalar gap

\[
d_{\delta,N}(\nu,\mathcal R_N)
=\psi_{\delta,N}\mathfrak F_{\delta,N}
(z_N(\nu,\mathcal R_N),\nu,\mathcal R_N).
\tag{10}
\]

The reference parameter is a simple root

\[
d_{\delta,N}(\nu_{c,0},0)=0,
\qquad
|\partial_\nu d_{\delta,N}(\nu_{c,0},0)|
\ge m_\delta^{(\nu)}>0.
\tag{11}
\]

Because every other BVP residual has been solved and the Lin direction is
supported only in the jump component, \(d_{\delta,N}=0\) is equivalent to a
zero complete-history jump. Calling that root a selected local geometric
maximal-canard parameter additionally requires the endpoint zero-fiber
implication in the
[full-network contract](full-network-lin-operator.md): a matched fiber
connection must collapse to an intersection of the selected slow histories.
A zero of an arbitrary experimental projection is instead an output-event
threshold unless a separate equivalence theorem is proved.

## 3. Frozen future theorem target: structural transfer of the RFDE canard root

### Hypotheses to prove or verify

- the blown-up RFDE and the Lin map are \(C^2\) in \((z,\nu,\mathcal R)\) on the declared strong spaces and fixed history domain;
- the layer problem has one simple fast fold direction;
- every transverse block has a geometrically derived history-space dichotomy/fiber trace pair proved Fredholm of index zero and is an isomorphism; any finite-defect reduction obeys the diagnostic \(d_-+d_+=2\); equivalently, a two-dimensional center-manifold construction is supplied with a complete-history fiber lift;
- the reference transverse variational problem admits the bound (8);
- the finite delay parameters and fixed-support residual class induce (4);
- the Lin gap is transverse as in (11);
- all constants are uniform in \(N\) for the admitted reference class;
- the joint smallness condition
  \[
  \zeta_N(\delta):=G_\perp(\delta)\eta_N^{\rm op}\ll1
  \tag{12}
  \]
  holds.

### Candidate statement

For \(\nu\) in a fixed root neighborhood and \(\zeta_N\) sufficiently small,

\[
d_{\delta,N}(\nu,\mathcal R_N)
=d_{\delta,N}(\nu,0)
+D_{\mathcal R}d_{\delta,N}(\nu,0)[\mathcal R_N]
+O\!\left(C_\delta\zeta_N^2\right),
\tag{13}
\]

and there is one nearby root satisfying

\[
\boxed{
\nu_{c,N}-\nu_{c,0}
=-
\frac{D_{\mathcal R}d_{\delta,N}(\nu_{c,0},0)[\mathcal R_N]}
{\partial_\nu d_{\delta,N}(\nu_{c,0},0)}
+O\!\left(\frac{C_\delta}{m_\delta^{(\nu)}}\zeta_N^2\right).
}
\tag{14}
\]

The mathematical contribution is the RFDE Lin-gap differentiability, the computable first-variation functional, and the explicit dependence on \(G_\perp(\delta)\), not the final scalar implicit-function step.

Since \(a=1+\delta^2\nu\), resolving an \(O(\delta^3)\) physical delay
effect requires the error in the blown-up root to be \(o(\delta)\). In
particular, require

\[
\frac{
|D_{\mathcal R}d_{\delta,N}[\mathcal R_N]|
+C_\delta\zeta_N^2
}{m_\delta^{(\nu)}}
=o(\delta).
\tag{15}
\]

### Primary falsifiers

- all node-fold directions remain critical and \(G_\perp(\delta)\) grows too rapidly;
- the fixed dual-state scaffold fails to produce an \(N\)-uniform transverse RFDE isomorphism once the long-delay spectrum and endpoint bundles are included;
- the proposed history-space endpoint pair is not Fredholm of index zero, or defines only a hard-synchronized restricted event;
- the chosen delay residual is not differentiable on the history space;
- the Lin problem has more than one unmatched direction;
- \(m_\delta^{(\nu)}\) vanishes at the proposed operating point;
- the first variation depends on matrix-valued transverse delay measures that cannot be represented by the proposed scalar moment.

Failure narrows the theorem to the exact invariant row-measure class or forces a different coupling scaling. It is not hidden by trajectory-level agreement.

## 4. Explicit proposition target: the first weighted delay moment

For the weakly delayed van der Pol calibration, suppose \(W\) is row-stochastic and every row has the same scaled-delay measure

\[
\rho_i=\sum_jW_{ij}\delta_{\Theta_{ij}}=\rho,
\qquad
m_k(\rho)=\int\theta^k\,d\rho(\theta).
\tag{16}
\]

The synchronous history space is then exactly invariant and reduces to one distributed-delay RFDE. The formal van der Pol solvability calculation gives

\[
a_c
=1-\frac18\varepsilon
+\frac K8m_1(\rho)\varepsilon^{3/2}
+O(\varepsilon^2).
\tag{17}
\]

This calibration is complete only after proving an estimate

\[
\left|
a_c-1+\frac18\varepsilon
-\frac K8m_1(\rho)\varepsilon^{3/2}
\right|
\le C\varepsilon^2
\tag{18}
\]

uniformly in \(N\) and in a declared compact class of measures \(\rho\). At this order \(m_2\) changes the formal critical graph but cancels from the parameter solvability condition.

For the exact two-module skeleton, let \(\mathbb B(d\theta)\) be the
operator-valued row-weighted delay measure, including the module-pair gain in
each entry, and set

\[
M_1^{(2)}
=\ell_c^\top
\left(\int\theta\,\mathbb B(d\theta)\right)r_c
=\sum_{a,b=1}^2
(\ell_c)_a(r_c)_b
\int\theta\,d\mathbb B_{ab}(\theta),
\tag{19}
\]

where \(r_c,\ell_c\) are the dynamical critical right and left module modes,
normalized by \(\ell_c^\top r_c=1\). They are not experimental observable
weights. If \(\mathbb B_{ab}=B_{ab}\widehat\rho_{ab}\), then
\(\widehat\rho_{ab}\) is a conditional probability measure; this alternative
normalization introduces one factor \(B_{ab}\), not two.

The proposition targets the two-term structure

\[
a_{c,2}
=1+c_0\varepsilon
+K\varepsilon^{3/2}
\left(
C_\parallel M_1^{(2)}
+\mathcal J_{\perp,\delta}[\mathbb B]
\right)
+O(\varepsilon^2),
\tag{20}
\]

uniformly over a declared compact module-pair measure class, **conditional on**
\(\mathcal J_{\perp,\delta}=O(1)\). If it grows with \(\delta^{-1}\), the
ordering must be revised rather than hidden in the remainder. The transverse
functional composes delayed translation, the transverse RFDE range inverse,
and dynamic critical-adjoint solvability. A sufficient condition that closes
the delayed-source part is

\[
P_\perp\mathbb B(d\theta)r_c=0
\quad\text{as a measure identity}.
\tag{21}
\]

Here \(P_\perp\) projects away from the critical collective mode. Vanishing of
the complete leading delay-induced \(\mathcal J_{\perp,\delta}\) additionally
requires the current, instantaneous, nonlinear, and endpoint/Lin operators to
respect the same critical/transverse splitting. The exact family in
[the moment counterexample](two-module-moment-counterexample.md) keeps the
total gain and \(M_1^{(2)}\) fixed while changing
\(P_\perp\mathbb B r_c\), and has a nonzero local nonlinear return channel.
It proves that \(M_1^{(2)}\) alone does not determine the transverse range
equation; the dynamic adjoint must calculate
\(\mathcal J_{\perp,\delta}\) or prove a further cancellation. Its original
two-recovery formulation is only a range-forcing counterexample, because it
also has an extra transverse slow center. A scalar dynamic-adjoint coefficient
must be derived in a shared-recovery or compatible dual-scaffold repair before
it enters (20). The [shared-recovery inner audit](shared-recovery-moment.md)
computes the formal local value
\(\mathcal J_{\perp,0}=\eta(\theta_0-\theta_1)/4\) and exposes its endpoint
term, but does not yet supply the full-history RFDE theorem. For nonnegative
receiver-self diffusion, a Perron no-go lemma
further shows that positive-mode exact layerwise closure collapses to the
common-row-measure class. The Dirac scalar case reproduces Zhang et al. (2026)
with \(c_0=-1/8\) and \(C_{\rm VdP}=1/8\); that case is a calibration, not a
novelty claim. The symmetric dual-scaffold FHN benchmark reduces exactly to a
scalar two-delay RFDE and is reserved for Corollary C.

## 5. Concrete corollary target: three actuators in two-module FHN

Use the exact symmetric benchmark in
[the reference note](two-module-reference.md): a fixed rank-one averaging
matrix, fixed \(D(P-I)v\) and \(E(P-I)w\) synchronization scaffolds,
within/cross delays, and weak delayed actuators. On a declared hyperbolic
periodic branch, fix
\(a_{\rm op}\), set the positive-side safety margin

\[
S_c(u)=a_{\rm op}-a_c(u),
\]

and define

\[
Q(u)=\bigl(F(u),R_h(u),S_c(u)\bigr),
\qquad
F=1/T,
\qquad
R_h=(\max h_N-\min h_N)^2.
\tag{22}
\]

The experimental observable is frozen as
\(h_N=2\bar v_1/3+\bar v_2/3\), distinct from the static critical weight and
from the dynamic Lin adjoint. Differentiability of \(R_h\) requires unique
nondegenerate extrema and no peak switching. For module voltages \(v_a\), set
\(v_*=1\) and freeze the actuator family

\[
\Phi_1(v_a,v_b^\tau)=v_b^\tau-v_a,
\qquad
\Phi_3(v_a,v_b^\tau)
=(v_b^\tau-v_*)^3-(v_a-v_*)^3,
\tag{23}
\]

and the realizable common shift of the within/cross scaled delays

\[
\Theta_0(s)=\Theta_0^0+s,
\qquad
\Theta_1(s)=\Theta_1^0+s,
\qquad
\partial_sM_1^{(2)}=1,
\qquad
u=(\kappa_1,\kappa_3,s).
\tag{24}
\]

The operating point must satisfy \(\kappa_1^0\ne0\), since the formal leading
safety derivative is
\(\partial_s S_c=(\kappa_1/8)\varepsilon^{3/2}+O(\varepsilon^2)\).

The target is not the generic statement “\(\det D_uQ\ne0\) implies invertibility.” A future project would have to derive the three sensitivity rows and prove on a nonempty admissible region \(U_*\) that

\[
\inf_{u\in U_*}\sigma_{\min}(D_uQ(u))
\ge c_Q(\varepsilon)>0,
\tag{25}
\]

with the transferred-threshold uncertainty smaller than the induced safety-margin change. A useful proof factorization is the Schur complement

\[
A_\varepsilon=D_{(\kappa_1,\kappa_3)}(F,R_h),
\qquad
S_{c,\varepsilon}^{\rm Schur}
=\partial_sS_c
-D_{(\kappa_1,\kappa_3)}S_c\,
A_\varepsilon^{-1}\partial_s(F,R_h),
\tag{26}
\]

for which \(\det D_uQ=\det A_\varepsilon\,S_{c,\varepsilon}^{\rm Schur}\). The task is to derive nonzero leading coefficients for both factors, not merely plot a determinant. The inverse-function theorem is then a corollary. A no-go result requires a structural rank bound on a neighborhood or an explicit functional dependence; rank loss at one point alone is not a no-go theorem.

## 6. Supporting validation, not a second theorem program

For a computed Lin gap \(\widehat d\) on a root interval \(I\), the basic certificate is

\[
|\widehat\mu_c-\mu_c|
\le
\frac{\sup_{\mu\in I}|\widehat d(\mu)-d(\mu)|}
{\inf_{\mu\in I}|\partial_\mu d(\mu)|}.
\tag{27}
\]

The numerator must be enclosed or bounded through demonstrated contributions from RFDE discretization, delayed-history interpolation, delay quadrature, Lin-BVP residual, center-manifold truncation, and network reduction. Constants are not assumed uniform in \(\varepsilon\). The earlier ODE Runge--Kutta chain-tree result is cited only for its covered map--flow component and is not extended to histories without a new proof.

## 7. Claim hierarchy

| Role | Future-project content | Evidence required |
|---|---|---|
| Main theorem target | RFDE Lin-gap/root transfer, (13)--(14) | complete proof with \(G_\perp(\delta)\), \(m_\delta^{(\nu)}\), and \(N\)-uniform constants |
| Explicit proposition | two-module first-moment law calibrated by (17)--(18) | mode closure, nonlocal reduction, and uniform remainder for (20) |
| Concrete corollary | two-module FHN three-actuator result, (25)--(26) | derived sensitivities and certified singular-value lower bound |
| Validation | numerical root enclosure and negative controls | independent refinement and reproducible residual bounds |
| Extension | general rank-\(r\), graphons, strong/nonnormal delay networks | not claimed in the future base case |

## 8. Stop/go gates

1. **Reference-template gate (passed):** the \(\mathbb R^4\) jump augmentation and index bookkeeping are fixed.
2. **Full-definition gate (operator contract fixed; geometry open):** construct the declared history-space endpoint bundles, prove every transverse trace pair is Fredholm of index zero and every block is an isomorphism, and leave exactly one unmatched collective direction.
3. **Transverse gate:** obtain or numerically falsify a usable \(G_\perp(\delta)\) scaling.
4. **Moment gate:** prove the uniform remainder and mode closure behind (20); the formal scalar coefficient alone is insufficient.
5. **Transfer gate:** verify the first variation and quadratic normalized remainder for controlled residual directions.
6. **Control gate:** prove (25) for the frozen FHN actuators or report a structural obstruction.
7. **Validation gate:** require numerical uncertainty to be smaller than every reported physical shift.

Failure at gates 2--4 would narrow the future theorem before large
simulations. Failure at gate 6 would change the future control corollary, not
the transfer target.
