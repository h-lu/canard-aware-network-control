# Flagship theorem specification

Status: **working specification, 2026-08-22**. Only the exact synchronous closure and formal polynomial coefficient checks have been completed. The main theorem, uniform remainder, and control corollary below are targets.

## 1. First-paper model class

For nodes \(i=1,\dots,N\), consider

\[
\dot x_i=f(x_i,y_i;\mu,u)+\varepsilon
\sum_{j=1}^N W_{ij}
q\!\left(x_i(t),x_j(t-\tau_{ij});u\right),
\qquad
\dot y_i=\varepsilon g(x_i,y_i;\mu,u),
\tag{1}
\]

with \(0<\varepsilon\ll1\), weak diffusive feedback satisfying \(q(x,x;u)=0\), and

\[
\tau_{ij}=\Theta_{ij}/\sqrt\varepsilon,
\qquad \Theta_{ij}\in[0,\Theta_{\max}].
\tag{2}
\]

After fold blow-up and time rescaling, the scaled history interval is the fixed compact interval \([-\Theta_{\max},0]\). Delay perturbations are measured either on a compatible \(C^1\) solution manifold or by a bounded-Lipschitz/Wasserstein-type norm on delay measures together with a history-derivative bound. The ordinary operator norm on \(C^0\) is not used to declare two nearby point delays close.

The main theorem is frozen to a finite network near one exact equitable **two-module** skeleton. Nodes in the same receiving module have the same row-weighted delay measure from each source module, so block-synchronous histories close exactly. The reduced two-module RFDE has exactly one simple collective canard direction; the module-difference direction and all within-module directions belong to the transverse Lin problem. The common-row-measure rank-one class is used only for the explicit van der Pol proposition.

General rank-\(r\) closure is an extension. An adjacency-matrix spectral gap may help verify hypotheses, but it is not substituted for the RFDE variational estimate along the canard orbit.

Write the structural residual as

\[
\mathcal R_N=(\Delta W_N,\Delta\rho_N,\Delta p_N),
\qquad
\eta_N=\|\mathcal R_N\|_{\mathfrak R},
\tag{3}
\]

where \(\|\cdot\|_{\mathfrak R}\) is fixed before the theorem is stated and controls edge weights, delay measures, and node heterogeneity on the chosen history space.

## 2. The mathematical object: a one-dimensional Lin gap

The threshold is not defined by subtracting two sets such as \(M^a\cap\Sigma\) and \(M^r\cap\Sigma\). Instead:

1. fix compact entry and exit data and one transverse matching section \(\Sigma\);
2. impose a common phase condition;
3. solve the attracting and repelling RFDE boundary-value pieces while matching every transverse coordinate;
4. leave one scalar jump in a fixed cokernel direction \(\psi_\varepsilon\).

Let \(\mathfrak F_\varepsilon(z,\mu,\mathcal R)=0\) denote this Lin boundary-value problem. After the phase condition, assume its reference linearization is Fredholm of index zero, with one declared canard matching direction and a bounded inverse on the transverse complement. Define

\[
G_\perp(\varepsilon)
=
\left\|
\left(D_z\mathfrak F_\varepsilon\vert_{\psi_\varepsilon^\perp}\right)^{-1}
\right\|,
\tag{4}
\]

and define the scalar Lin gap

\[
d_\varepsilon(\mu,\mathcal R)
=\langle\psi_\varepsilon,
\operatorname{jump}(z^a,z^r)\rangle.
\tag{5}
\]

The reference canard parameter is a simple root

\[
d_\varepsilon(\mu_{c,0},0)=0,
\qquad
|\partial_\mu d_\varepsilon(\mu_{c,0},0)|
\ge m_\varepsilon>0.
\tag{6}
\]

If solving all matching equations makes the selected invariant manifolds intersect, \(\mu_c\) is a geometric maximal-canard parameter. A zero of an arbitrary experimental projection is instead called an output-event threshold unless a separate equivalence theorem is proved. Experimental observables remain essential for amplitude and validation, but they do not replace the Lin matching equations.

## 3. Main theorem target: structural transfer of the RFDE canard root

### Hypotheses to prove or verify

- the blown-up RFDE and the Lin map are \(C^2\) in \((z,\mu,\mathcal R)\) on a fixed history domain;
- the fold has one simple canard center direction;
- the reference transverse variational problem admits the bound (4);
- the residual norm (3) makes delay translation differentiable on the chosen solution manifold;
- the Lin gap is transverse as in (6);
- all constants are uniform in \(N\) for the admitted reference class;
- the joint smallness condition
  \[
  \zeta_N(\varepsilon):=G_\perp(\varepsilon)\eta_N\ll1
  \tag{7}
  \]
  holds.

### Candidate statement

For \(\mu\) in a fixed root neighborhood and \(\zeta_N\) sufficiently small,

\[
d_\varepsilon(\mu,\mathcal R_N)
=d_\varepsilon(\mu,0)
+D_{\mathcal R}d_\varepsilon(\mu,0)[\mathcal R_N]
+O\!\left(C_\varepsilon\zeta_N^2\right),
\tag{8}
\]

and there is one nearby root satisfying

\[
\boxed{
\mu_{c,N}-\mu_{c,0}
=-
\frac{D_{\mathcal R}d_\varepsilon(\mu_{c,0},0)[\mathcal R_N]}
{\partial_\mu d_\varepsilon(\mu_{c,0},0)}
+O\!\left(\frac{C_\varepsilon}{m_\varepsilon}\zeta_N^2\right).
}
\tag{9}
\]

The mathematical contribution is the RFDE Lin-gap differentiability, the computable first-variation functional, and the explicit dependence on \(G_\perp(\varepsilon)\), not the final scalar implicit-function step.

To resolve an \(O(\varepsilon^{3/2})\) physical delay effect against the unperturbed reference, require

\[
\frac{
|D_{\mathcal R}d_\varepsilon[\mathcal R_N]|
+C_\varepsilon\zeta_N^2
}{m_\varepsilon}
=o(\varepsilon^{3/2}).
\tag{10}
\]

### Primary falsifiers

- all node-fold directions remain critical and \(G_\perp(\varepsilon)\) grows too rapidly;
- the chosen delay residual is not differentiable on the history space;
- the Lin problem has more than one unmatched direction;
- \(m_\varepsilon\) vanishes at the proposed operating point;
- the first variation depends on matrix-valued transverse delay measures that cannot be represented by the proposed scalar moment.

Failure narrows the theorem to the exact invariant row-measure class or forces a different coupling scaling. It is not hidden by trajectory-level agreement.

## 4. Explicit proposition target: the first weighted delay moment

For the weakly delayed van der Pol calibration, suppose \(W\) is row-stochastic and every row has the same scaled-delay measure

\[
\rho_i=\sum_jW_{ij}\delta_{\Theta_{ij}}=\rho,
\qquad
m_k(\rho)=\int\theta^k\,d\rho(\theta).
\tag{11}
\]

The synchronous history space is then exactly invariant and reduces to one distributed-delay RFDE. The formal van der Pol solvability calculation gives

\[
a_c
=1-\frac18\varepsilon
+\frac K8m_1(\rho)\varepsilon^{3/2}
+O(\varepsilon^2).
\tag{12}
\]

This calibration is complete only after proving an estimate

\[
\left|
a_c-1+\frac18\varepsilon
-\frac K8m_1(\rho)\varepsilon^{3/2}
\right|
\le C\varepsilon^2
\tag{13}
\]

uniformly in \(N\) and in a declared compact class of measures \(\rho\). At this order \(m_2\) changes the formal critical graph but cancels from the parameter solvability condition.

For the exact two-module skeleton, let \(\rho_{ab}\) be the row-weighted delay measure from source module \(b\) to receiving module \(a\), and set

\[
 m_{1,ab}=\int\theta\,d\rho_{ab}(\theta),
\qquad
M_1^{(2)}
=\sum_{a,b=1}^2(\ell_c)_aB_{ab}(r_c)_b m_{1,ab},
\tag{14}
\]

where \(r_c,\ell_c\) are the dynamical critical right and left module modes, normalized by \(\ell_c^\top r_c=1\). They are not experimental observable weights.

The proposition targets

\[
\mu_{c,2}
=\mu_{c,0}+c_0\varepsilon
+C_{\rm model}K M_1^{(2)}\varepsilon^{3/2}
+O(\varepsilon^2),
\tag{15}
\]

uniformly over a declared compact module-pair measure class. A sufficient leading-order closure condition is

\[
P_\perp\mathbb B(d\theta)r_c=0
\quad\text{as a measure identity}.
\tag{16}
\]

Here \(\mathbb B(d\theta)\) is the two-module operator-valued delay measure and \(P_\perp\) projects away from the critical collective mode. Without this condition, eliminating transverse histories may produce another same-order resolvent functional, which must be written explicitly rather than hidden inside \(M_1^{(2)}\). The Dirac scalar case reproduces Zhang et al. (2026) with \(c_0=-1/8\) and \(C_{\rm VdP}=1/8\); that case is a calibration, not a novelty claim.

## 5. Concrete corollary target: three actuators in two-module FHN

On a declared hyperbolic periodic branch of the two-module delayed FitzHugh--Nagumo benchmark, fix an operating parameter \(\mu_{\rm op}\), set \(\Delta_c(u)=\mu_c(u)-\mu_{\rm op}\), and define

\[
Q(u)=\bigl(F(u),R_h(u),\Delta_c(u)\bigr),
\qquad
F=1/T,
\qquad
R_h=(\max h_N-\min h_N)^2.
\tag{17}
\]

The experimental observable \(h_N\) is fixed and is distinct from the critical adjoint mode \(\ell_c\). Differentiability of \(R_h\) requires unique nondegenerate extrema and no peak switching. For module voltages \(v_a\), freeze the actuator family

\[
\Phi_1(v_a,v_b^\tau)=v_b^\tau-v_a,
\qquad
\Phi_3(v_a,v_b^\tau)
=(v_b^\tau-v_*)^3-(v_a-v_*)^3,
\tag{18}
\]

and a realizable delay deformation

\[
\Theta_{ab}(s)=\Theta_{ab}^0+s\Xi_{ab},
\qquad
\partial_sM_1^{(2)}\ne0,
\qquad
u=(\kappa_1,\kappa_3,s).
\tag{19}
\]

The target is not the generic statement “\(\det D_uQ\ne0\) implies invertibility.” The paper must derive the three sensitivity rows and prove on a nonempty admissible region \(U_*\) that

\[
\inf_{u\in U_*}\sigma_{\min}(D_uQ(u))
\ge c_Q(\varepsilon)>0,
\tag{20}
\]

with the transferred-threshold uncertainty smaller than the induced safety-margin change. A useful proof factorization is the Schur complement

\[
A_\varepsilon=D_{(\kappa_1,\kappa_3)}(F,R_h),
\qquad
S_{\Delta,\varepsilon}
=\partial_s\Delta_c
-D_{(\kappa_1,\kappa_3)}\Delta_c\,
A_\varepsilon^{-1}\partial_s(F,R_h),
\tag{21}
\]

for which \(\det D_uQ=\det A_\varepsilon\,S_{\Delta,\varepsilon}\). The task is to derive nonzero leading coefficients for both factors, not merely plot a determinant. The inverse-function theorem is then a corollary. A no-go result requires a structural rank bound on a neighborhood or an explicit functional dependence; rank loss at one point alone is not a no-go theorem.

## 6. Supporting validation, not a second theorem program

For a computed Lin gap \(\widehat d\) on a root interval \(I\), the basic certificate is

\[
|\widehat\mu_c-\mu_c|
\le
\frac{\sup_{\mu\in I}|\widehat d(\mu)-d(\mu)|}
{\inf_{\mu\in I}|\partial_\mu d(\mu)|}.
\tag{22}
\]

The numerator must be enclosed or bounded through demonstrated contributions from RFDE discretization, delayed-history interpolation, delay quadrature, Lin-BVP residual, center-manifold truncation, and network reduction. Constants are not assumed uniform in \(\varepsilon\). The earlier ODE Runge--Kutta chain-tree result is cited only for its covered map--flow component and is not extended to histories without a new proof.

## 7. Claim hierarchy

| Role | First-paper content | Evidence required |
|---|---|---|
| Main theorem | RFDE Lin-gap/root transfer, (8)--(9) | complete proof with \(G_\perp(\varepsilon)\), \(m_\varepsilon\), and \(N\)-uniform constants |
| Explicit proposition | two-module first-moment law calibrated by (12)--(13) | mode closure, nonlocal reduction, and uniform remainder for (15) |
| Concrete corollary | two-module FHN three-actuator result, (20)--(21) | derived sensitivities and certified singular-value lower bound |
| Validation | numerical root enclosure and negative controls | independent refinement and reproducible residual bounds |
| Extension | general rank-\(r\), graphons, strong/nonnormal delay networks | not claimed in v1 |

## 8. Stop/go gates

1. **Definition gate:** construct a well-posed Lin BVP with exactly one unmatched direction.
2. **Transverse gate:** obtain or numerically falsify a usable \(G_\perp(\varepsilon)\) scaling.
3. **Moment gate:** prove the uniform remainder and mode closure behind (15); the formal scalar coefficient alone is insufficient.
4. **Transfer gate:** verify the first variation and quadratic normalized remainder for controlled residual directions.
5. **Control gate:** prove (20) for the frozen FHN actuators or report a structural obstruction.
6. **Validation gate:** require numerical uncertainty to be smaller than every reported physical shift.

Failure at gates 1--3 narrows the main theorem before large simulations. Failure at gate 5 changes the control corollary, not the transfer theorem.
