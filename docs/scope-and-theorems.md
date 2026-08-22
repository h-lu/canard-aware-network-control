# Scope and candidate theorem ladder

Status: **working specification, 2026-08-22**. Every theorem below is a target until a proof and its computational checks are merged.

## 1. Canonical network class

For nodes \(i=1,\dots,N\), start from

\[
\dot x_i=f(x_i,y_i;\mu,u)+\varepsilon
\sum_{j=1}^N W_{ij}
q\!\left(x_i(t),x_j(t-\tau_{ij});u\right),
\qquad
\dot y_i=\varepsilon g(x_i,y_i;\mu,u),
\tag{1}
\]

with \(0<\varepsilon\ll1\), weak diffusive network feedback satisfying \(q(x,x;u)=0\), and

\[
\tau_{ij}=\Theta_{ij}/\sqrt{\varepsilon},
\qquad \Theta_{ij}\in[0,\Theta_{\max}].
\tag{2}
\]

The topology is decomposed as

\[
W_N=W_N^{(r)}+E_N,
\tag{3}
\]

where \(W_N^{(r)}\) has an equitable \(r\)-block representation and \(E_N\) is small in a norm chosen to control the delayed coupling operator. Delays are constant on each ordered module pair in the exact skeleton, \(\tau_{ij}=\tau_{ab}\) for \(i\in M_a,j\in M_b\), and may carry a controlled delay-kernel residual in the perturbed network. The retained spectral subspace is separated by a gap \(\gamma_r>0\); directed extensions additionally require a uniformly controlled eigenvector condition number.

Two concrete models anchor the paper:

- **analytic calibration:** the weakly delayed van der Pol equation;
- **biological benchmark:** a two-module delayed FitzHugh--Nagumo network.

The general theorem is stated only at the regularity and spectral strength actually needed by these two cases.

## 2. Fixed observable and threshold definition

Choose one smooth aggregate observable

\[
h_N(X)=\ell_N^\top X,
\tag{4}
\]

where \(\ell_N\) is fixed before parameter continuation. The default is a positive Perron weight or a declared module average. Changing \(\ell_N\) changes the scientific question and may change the threshold.

After blow-up, select attracting and repelling invariant manifolds using the same compact entry data, continue both to one fixed transverse section \(\Sigma\), and define their signed observable splitting

\[
d_N(\mu,u;\varepsilon)=
\mathcal H_N\!\left(M^a_N\cap\Sigma\right)-
\mathcal H_N\!\left(M^r_N\cap\Sigma\right).
\tag{5}
\]

The local observable-projected canard threshold is the simple root

\[
d_N(\mu_{c,N}^{h},u;\varepsilon)=0,
\qquad
|\partial_\mu d_N|=m_{\varepsilon,h}>0.
\tag{6}
\]

At a declared operating point \(\mu_{\rm op}\), define the signed pulse-safety margin

\[
\Delta_{c,N}^{h}=\mu_{c,N}^{h}-\mu_{\rm op}
\tag{7}
\]

with orientation fixed so that \(\Delta_c>0\) is the safe side. Thus assigning \(\Delta_c\) is equivalent to assigning the threshold when \(\mu_{\rm op}\) is fixed. A visually detected amplitude jump is a validation statistic, not the theorem's definition.

This root is not automatically the system's geometric maximal-canard parameter. The latter name is reserved for an actual intersection of the full selected manifolds. If the splitting is effectively one-dimensional, all nonannihilating projections may yield the same root; observable dependence is therefore tested rather than assumed.

## 3. Candidate theorem ladder

### T1. Exact module reduction

**Candidate statement.** If the weight matrix is equitable, delays and node parameters are block-constant, and the initial history is block-synchronous, then the block-synchronous history space is invariant under (1). Its restriction is exactly an \(r\)-module RFDE.

**Proof route.** Direct substitution and uniqueness in the RFDE phase space. Record the precise normalization of row sums; do not infer it from a low-rank approximation alone.

**Falsifier.** Any coupling convention for which equality of within-block histories fails to imply equality of within-block vector fields.

### T2. Observable-projected threshold transfer

Let \(d_r\) denote the splitting of the exact reduced RFDE. For residual size

\[
\eta_N=\frac{\operatorname{cond}(V_r)}{\gamma_r}
\left(\|E_N\|_{\mathrm{delay}}+
\|\Delta\mathcal K_N\|_{\mathrm{delay}}+
\|\Delta p_N\|\right)
+\operatorname{dist}(\ell_N,\operatorname{Ran}P_r^*),
\tag{8}
\]

target a uniform expansion

\[
d_N(\mu,u;\varepsilon)
=d_r(\mu,u;\varepsilon)
+\mathcal L_{\varepsilon,h}[E_N,\Delta\mathcal K_N,\Delta p_N]
+O(\eta_N^2).
\tag{9}
\]

If \(m_{\varepsilon,h}:=|\partial_\mu d_r(\mu_{c,r}^{h})|>0\), the root shift should be

\[
\mu_{c,N}^{h}-\mu_{c,r}^{h}
=-
\frac{\mathcal L_{\varepsilon,h}[E_N,\Delta\mathcal K_N,\Delta p_N]}
{\partial_\mu d_r(\mu_{c,r}^{h})}
+O(\eta_N^2).
\tag{10}
\]

**Proof route.** Uniform graph transform or Lyapunov--Perron control for the selected manifolds, a bounded observable projection, then a quantitative implicit-function argument.

The dependence of \(m_{\varepsilon,h}\) and all constants on \(\varepsilon\) remains explicit; uniform transversality is not assumed for free. To resolve a proposed \(O(\varepsilon^{3/2})\) delay-moment term, require the joint limit \(C_\varepsilon\eta_N=o(\varepsilon^{3/2})\).

**Falsifier.** Loss of normal hyperbolicity outside the designated fold chart, a vanishing transversality denominator, residual growth with \(N\) in the chosen operator norm, or an observable that annihilates the critical splitting direction.

### T3. Topology-weighted delay-moment selection

Define projected moments after fixing the block/Perron weights, for example

\[
M_k(W,\Theta;\ell,r)
=\sum_{i,j}\ell_i W_{ij}r_j\Theta_{ij}^{k}.
\tag{11}
\]

The blow-up calculation should determine, rather than assume, the first nonzero order at which each \(M_k\) enters the reduced splitting:

\[
d_r=d_{r,0}
+\sum_{k\ge1} C_k(\varepsilon,u)M_k
+R_K.
\tag{12}
\]

The paper will report only moments whose coefficients and uniform remainders are proved. No numerical fit will be presented as a selection law.

The scalar delayed van der Pol calibration is now derived independently:

\[
a_c=1-\frac18\varepsilon
+\frac{K\Theta}{8}\varepsilon^{3/2}
+O(\varepsilon^2).
\tag{13}
\]

Thus \(K\Theta/8\) is established for one oscillator. Replacing \(\Theta\) by a projected network moment \(M_1\) remains a guarded hypothesis until transverse delayed modes and the observable normalization are controlled; see [the leading-moment derivation](derivation-leading-moment.md).

**Proof route.** Expand the reduced history functional on the nonlocal center manifold and project it with the adjoint splitting functional. A direct short-delay Taylor expansion is not used because the scaled delay is \(O(1)\).

**Falsifier.** A competing history functional at the same order that cannot be represented by finitely many weighted moments on the stated delay class.

### T4. Frequency--amplitude--safety assignment

For a stable periodic branch on the chosen side of the threshold, define

\[
Q(u)=\bigl(F(u),R_h(u),\Delta_c^h(u)\bigr),
\qquad
F=1/T,
\qquad
R_h=\bigl(\max h_N-\min h_N\bigr)^2.
\tag{14}
\]

Squaring the observable amplitude avoids the square-root singularity of amplitude at a Hopf point. Use three physically distinct controls \(u=(u_{\rm lin},u_{\rm nl},u_{\rm delay})\), where the third changes a realizable weighted delay moment while preserving nonnegative delays and admissible weights.

**Candidate statement.** If \(Q\) is \(C^1\) and

\[
\det D_uQ(u_0)\neq0,
\tag{15}
\]

then every nearby target \((F_*,R_*,\Delta_{c,*}^{h})\) has a unique nearby control. A rank-deficient Jacobian is a local no-go certificate for independent assignment with that actuator set.

**Proof route.** Periodic-orbit sensitivity/adjoint equations for \(F\) and \(R_h\), splitting sensitivity for \(\Delta_c^h\), then the inverse-function theorem.

**Falsifier.** Rank below three across an open admissible control set. In that case the actuator family, not the optimizer, is insufficient.

### T5. Numerical threshold certificate

Let \(\widehat d_N\) combine periodic/history collocation or fixed-step integration, interpolation of delayed histories, projection to the reduced network, and a scalar root solve. If the exact splitting is transverse, target

\[
|\widehat\mu_c^h-\mu_c^h|
\le \frac{1}{m_{\varepsilon,h}}
\left(
C_{\rm RK}h^p
+C_{\rm hist}\Delta_h^q
+C_{\rm red}\eta_N
+|\widehat d_N(\widehat\mu_c^h)|
+C_{\rm int}\mathcal E_{\rm int}
\right).
\tag{16}
\]

Here \(\mathcal E_{\rm int}\) collects demonstrated cross-terms rather than silently treating error sources as additive. For fold-local Runge--Kutta calculations, the chain-tree defect is tracked explicitly.

**Falsifier.** Nonmonotone refinement, a fitted convergence rate inconsistent with the proven regularity, or a certificate wider than the predicted topology/delay shift.

### Stretch corollary. Canard conditioning

The inverse map is expected to become severely ill-conditioned across an exponentially narrow canard window. The first paper will seek upper and lower bounds on the smallest singular value of \(D_uQ\), but it will claim a law such as \(\kappa(D_uQ)\asymp e^{S/\varepsilon}\) only if both directions are proved. Otherwise conditioning remains a measured limitation, not a theorem.

## 4. Claim hierarchy for one paper

| Level | Required evidence | Intended content |
|---|---|---|
| Theorem | complete assumptions, uniform constants, proof | T1, a scoped T2, local T4 |
| Proposition | derivation plus symbolic/numerical cross-check | model-specific T3, T5 specialization |
| Validated conjecture | preregistered convergence and out-of-sample tests | larger heterogeneous networks |
| Extension | qualitative demonstration only | graphon or strongly nonnormal examples |

The abstract must distinguish these levels.

## 5. Stop/go gates

1. **Definition gate:** the splitting root agrees with an independently computed maximal canard in delayed van der Pol.
2. **Moment gate:** the first nonzero weighted delay moment and coefficient survive two independent derivations.
3. **Transfer gate:** threshold error scales with the declared residual norm on held-out networks.
4. **Rank gate:** the smallest singular value of \(D_uQ\) stays separated from zero on a nontrivial admissible neighborhood.
5. **Certification gate:** discretization uncertainty is smaller than the effect being claimed.

Failure at gates 1--3 narrows the theorem. Failure at gate 4 produces a no-go result and actuator redesign. Failure at gate 5 blocks quantitative biological claims.
