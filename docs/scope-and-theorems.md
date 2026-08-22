# Flagship theorem specification

Status: **working specification, 2026-08-22**. The Lin gap is now defined by a correctly augmented Fredholm problem, the concrete control benchmark is frozen, and exact/formal algebraic checks are executable. The model-specific Fredholm proof, uniform remainder, and control corollary remain targets.

## 1. First-paper model class

For nodes \(i=1,\dots,N\), consider

\[
\dot x_i=f(x_i,y_i;\mu,u)
+\mathcal S_{N,i}(x)
+\varepsilon
\sum_{j=1}^N W_{ij}
q\!\left(x_i(t),x_j(t-\tau_{ij});u\right),
\qquad
\dot y_i=\varepsilon g(x_i,y_i;\mu,u),
\tag{1}
\]

with \(0<\varepsilon\ll1\), weak delayed feedback satisfying
\(q(x,x;u)=0\), and

\[
\tau_{ij}=\Theta_{ij}/\sqrt\varepsilon,
\qquad \Theta_{ij}\in[0,\Theta_{\max}].
\tag{2}
\]

The instantaneous scaffold \(\mathcal S_N\) vanishes on the selected
collective history. It is included only where needed to isolate one fast fold
direction; the concrete FHN benchmark uses \(D(P-I)x\) with fixed \(D>0\).
It therefore does not alter the collective weak-delay calibration.

After fold blow-up and time rescaling, the scaled history interval is the fixed compact interval \([-\Theta_{\max},0]\). Version 1 treats moving point delays as finitely many smooth parameters on a strong Sobolev orbit space and permits infinite-dimensional measure perturbations only on fixed delay support. The ordinary operator norm on \(C^0\) is not used to declare two nearby point delays close. Freely moving measure support in a bounded-Lipschitz/Wasserstein space is an extension unless the required \(C^2\) theorem is supplied.

The main theorem is frozen to a finite network near one exact equitable **two-module** skeleton. Nodes in the same receiving module have the same row-weighted delay measure from each source module, so block-synchronous histories close exactly. One collective canard direction is a hypothesis to be verified by the augmented Lin BVP; equitability alone does not imply it. The concrete control benchmark uses the scaffold above. The identical-module weak-only class is retained as a negative control because all node-fold directions coalesce at \(\varepsilon=0\).

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
=\|\mathfrak F_\delta(\cdot,\nu,\mathcal R_N)
-\mathfrak F_\delta(\cdot,\nu,0)\|_{\mathscr Y},
\tag{4}
\]

not the raw norm by itself. For weak weight coupling, for example,
\(\eta_N^{\rm op}=O(\sqrt\varepsilon |K|\eta_W^{\rm raw})\).

## 2. The mathematical object: a one-dimensional Lin gap

The threshold is not defined by subtracting two sets such as \(M^a\cap\Sigma\) and \(M^r\cap\Sigma\). Instead:

1. fix compact entry and exit data and one transverse matching section \(\Sigma\), which supplies the phase condition;
2. solve the attracting and repelling RFDE boundary-value pieces while matching every transverse coordinate;
3. leave one scalar jump in a fixed cokernel direction \(\psi_\delta\).

Let \(\mathfrak F_\delta(z,\nu,\mathcal R)=0\) denote the full-history Lin
boundary-value problem specified in
[the feasibility note](lin-gap-feasibility.md), where
\(a=1+\delta^2\nu\). After its single phase condition, require

\[
L_\delta=D_z\mathfrak F_\delta,
\qquad
\ker L_\delta=\{0\},
\qquad
\dim\operatorname{coker}L_\delta=1,
\qquad
\operatorname{ind}L_\delta=-1.
\tag{5}
\]

Choose \(\psi_\delta\in\mathscr Y^*\) and
\(e_\delta\in\mathscr Y\) such that

\[
\operatorname{Range}L_\delta=\ker\psi_\delta,
\qquad
\psi_\delta(e_\delta)=1,
\tag{6}
\]

with \(e_\delta\) supported only in the history-jump component. The
index-zero augmented operator

\[
\widehat L_\delta(\zeta,\gamma)
=L_\delta\zeta-\gamma e_\delta
\tag{7}
\]

must be invertible. Define

\[
G_\perp(\delta)
=\left\|
(L_\delta:\mathscr X\to\operatorname{Range}L_\delta)^{-1}
\right\|.
\tag{8}
\]

Solving

\[
\mathfrak F_\delta(z(\nu,\mathcal R),\nu,\mathcal R)
=d_\delta(\nu,\mathcal R)e_\delta
\tag{9}
\]

defines the strict scalar gap

\[
d_\delta(\nu,\mathcal R)
=\psi_\delta\mathfrak F_\delta
(z(\nu,\mathcal R),\nu,\mathcal R).
\tag{10}
\]

The reference parameter is a simple root

\[
d_\delta(\nu_{c,0},0)=0,
\qquad
|\partial_\nu d_\delta(\nu_{c,0},0)|
\ge m_\delta^{(\nu)}>0.
\tag{11}
\]

Because every other BVP residual has been solved and (9) matches complete
histories when \(d_\delta=0\), the root is a selected local geometric
maximal-canard parameter. A zero of an arbitrary experimental projection is
instead an output-event threshold unless a separate equivalence theorem is
proved.

## 3. Main theorem target: structural transfer of the RFDE canard root

### Hypotheses to prove or verify

- the blown-up RFDE and the Lin map are \(C^2\) in \((z,\nu,\mathcal R)\) on the declared strong spaces and fixed history domain;
- the fold has one simple canard center direction;
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
d_\delta(\nu,\mathcal R_N)
=d_\delta(\nu,0)
+D_{\mathcal R}d_\delta(\nu,0)[\mathcal R_N]
+O\!\left(C_\delta\zeta_N^2\right),
\tag{13}
\]

and there is one nearby root satisfying

\[
\boxed{
\nu_{c,N}-\nu_{c,0}
=-
\frac{D_{\mathcal R}d_\delta(\nu_{c,0},0)[\mathcal R_N]}
{\partial_\nu d_\delta(\nu_{c,0},0)}
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
|D_{\mathcal R}d_\delta[\mathcal R_N]|
+C_\delta\zeta_N^2
}{m_\delta^{(\nu)}}
=o(\delta).
\tag{15}
\]

### Primary falsifiers

- all node-fold directions remain critical and \(G_\perp(\delta)\) grows too rapidly;
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

For the exact two-module skeleton, let \(\rho_{ab}\) be the row-weighted delay measure from source module \(b\) to receiving module \(a\), and set

\[
 m_{1,ab}=\int\theta\,d\rho_{ab}(\theta),
\qquad
M_1^{(2)}
=\sum_{a,b=1}^2(\ell_c)_aB_{ab}(r_c)_b m_{1,ab},
\tag{19}
\]

where \(r_c,\ell_c\) are the dynamical critical right and left module modes, normalized by \(\ell_c^\top r_c=1\). They are not experimental observable weights.

The proposition targets

\[
a_{c,2}
=1+c_0\varepsilon
+C_{\rm model}K M_1^{(2)}\varepsilon^{3/2}
+O(\varepsilon^2),
\tag{20}
\]

uniformly over a declared compact module-pair measure class. A sufficient leading-order closure condition is

\[
P_\perp\mathbb B(d\theta)r_c=0
\quad\text{as a measure identity}.
\tag{21}
\]

Here \(\mathbb B(d\theta)\) is the two-module operator-valued delay measure and \(P_\perp\) projects away from the critical collective mode. Without this condition, eliminating transverse histories may produce another same-order resolvent functional, which must be written explicitly rather than hidden inside \(M_1^{(2)}\). The Dirac scalar case reproduces Zhang et al. (2026) with \(c_0=-1/8\) and \(C_{\rm VdP}=1/8\); that case is a calibration, not a novelty claim. The symmetric scaffolded FHN benchmark reduces exactly to a scalar two-delay RFDE and is reserved for Corollary C; it is not presented as the nontrivial modular instance of this proposition.

## 5. Concrete corollary target: three actuators in two-module FHN

Use the exact symmetric benchmark in
[the reference note](two-module-reference.md): a fixed rank-one averaging
matrix, fixed \(D(P-I)v\) synchronization scaffold, within/cross delays, and
weak delayed actuators. On a declared hyperbolic periodic branch, fix
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

The target is not the generic statement “\(\det D_uQ\ne0\) implies invertibility.” The paper must derive the three sensitivity rows and prove on a nonempty admissible region \(U_*\) that

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

| Role | First-paper content | Evidence required |
|---|---|---|
| Main theorem | RFDE Lin-gap/root transfer, (13)--(14) | complete proof with \(G_\perp(\delta)\), \(m_\delta^{(\nu)}\), and \(N\)-uniform constants |
| Explicit proposition | two-module first-moment law calibrated by (17)--(18) | mode closure, nonlocal reduction, and uniform remainder for (20) |
| Concrete corollary | two-module FHN three-actuator result, (25)--(26) | derived sensitivities and certified singular-value lower bound |
| Validation | numerical root enclosure and negative controls | independent refinement and reproducible residual bounds |
| Extension | general rank-\(r\), graphons, strong/nonnormal delay networks | not claimed in v1 |

## 8. Stop/go gates

1. **Definition gate (passed at specification level):** prove the frozen-model Lin BVP has exactly one unmatched direction.
2. **Transverse gate:** obtain or numerically falsify a usable \(G_\perp(\delta)\) scaling.
3. **Moment gate:** prove the uniform remainder and mode closure behind (20); the formal scalar coefficient alone is insufficient.
4. **Transfer gate:** verify the first variation and quadratic normalized remainder for controlled residual directions.
5. **Control gate:** prove (25) for the frozen FHN actuators or report a structural obstruction.
6. **Validation gate:** require numerical uncertainty to be smaller than every reported physical shift.

Failure at gates 1--3 narrows the main theorem before large simulations. Failure at gate 5 changes the control corollary, not the transfer theorem.
