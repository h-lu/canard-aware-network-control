# General-network canards and biological pulse control

Status: **research contract, 2026-08-24**. This document defines the work
needed to move beyond the completed two-module, preparation-indexed local
history-connection theorem. None of the targets below is a claim of the JNS
base paper. That paper is frozen and becomes the proved nonzero model case for
this program.

## 1. Completion standard

The program is complete only after three theorem chains are proved.

1. **General finite-network canard response.** For arbitrary finite \(N\) in
   a declared network class, construct a complete-history reduction, derive a
   topology-resolved canard response, prove its remainder, and verify the
   operator hypotheses for a nontrivial graph family.
2. **Physical pulse bridge.** Prove that a fully normalized compatible outer
   continuation, or a declared causal history-reset protocol, enters the
   local fold problem and that the resulting separator distinguishes
   subthreshold and large-pulse itineraries.  Bounded backward completeness
   alone is not a selection rule.
3. **Biological pulse control.** Derive frequency, amplitude, and pulse-safety
   sensitivities and prove either a quantitative three-actuator inverse on a
   certified operating box or a sharp canard-conditioning no-go theorem.

“Every graph,” “arbitrary topology,” and “global spiking” are not substitutes
for hypotheses. A general network theorem means a theorem for every finite
network satisfying explicit fold, transverse-hyperbolicity, regularity, and
return assumptions. A scalable corollary additionally has constants uniform
in \(N\).

This is one flagship program with three papers after the JNS base paper:

- **Paper II:** general finite-network complete-history canard response;
- **Paper III:** physical maximal canards and observable pulse onset;
- **Paper IV:** frequency--amplitude--pulse-safety control and conditioning.

Papers III and IV may be merged only after both theorem chains are complete.
They remain separate proof gates. Inserting all three chains into the current
41-page paper would hide independent hypotheses and overstate what it proves.

### 1.1 Current theorem ledger

| Component | Current status | Remaining promotion gate |
|---|---|---|
| Dimension-uniform special-flow history graph | Proved abstractly; a complete model fit, compatible traces, and a simple selected root are now proved for the heterogeneous-curvature Dobrushin class | Moving support and closing graph gaps remain outside the theorem |
| Lifted unequal-module network | Exact arbitrary-\(N\) blow-up, canonical gap/root lift, uniform \(\delta^3\eta\) response, pure-breaker nullity, and a non-equitable nonzero combined tangent proved | Pure-breaker quadratic/higher coefficient and general non-equitable residual response |
| Shared-resource Dobrushin class | Uniform transverse graph and a nonzero dimension-uniform selected-root resolvent coefficient are proved. A bounded one-RFDE reset policy transfers that coefficient to controlled detector latency, but uses the exact roots as offline data and is policy dependent | Input-independent physical outer/event comparison and graph families with closing Dobrushin gap remain open |
| Root/periodic model compatibility | Exact two-module restriction audit proves that the earlier lifted selected-root and balanced periodic/control results use different RFDEs. The old linear redistribution is visible on the validated synchronous branch, while an all-history-invisible finite-atom linear direction cannot force its critical history | The nonlinear period-locked extension below supplies a common RFDE, a small-\(\delta\) root response, and a canonical full-network lift for a uniformly Dobrushin class; fixed-\(\varepsilon\) and intrinsic-event promotion remain open |
| Quadratic period-locked common RFDE | Exact carrier algebra, center periodic-orbit and output invariance, qualitative three-parameter periodic IFT, the fixed-scaled-support scalar root law, and its dimension-uniform canonical zero-graph lift to every finite topology with a common Dobrushin gap are proved. The linear carrier's leading pairing is exactly zero. At the exact center gain pair, a full 32,046-leaf replay proves local full-network orbital attraction for \(|\eta|\le3\times10^{-6}\) and every fixed finite \(\tau(Q)\le1/4\) topology | Validate the complete-history root and dynamic-adjoint ratio at \(\varepsilon=1/5\), then prove an input-independent root/event comparison; a joint gain--eta box, arbitrary histories, closing-gap families, and basin uniqueness remain outside the theorem |
| Fixed-\(\varepsilon\) quadratic root gate | The exact blueprint specifies the enlarged-history two-sided BVP, jump complement, advanced adjoint and radii polynomial. A later binary64 two-branch solve closes both flights, phase and the nodewise full-history jump; its endpoint-compatible entry, discrete adjoint and direct tangent give finest \(\rho_N=-0.3463310348\), with second-order mesh behavior. A new audit proves that the raw 194-coefficient history ledger has rank-two endpoint compatibility, a 192-dimensional compatible level, and no rank-193 compatible immersion; it also gives exact same-current, same-\(G\) compatible histories with different futures | Construct the selected attracting zero fibre and the one-dimensional backward-extendible repelling history chart. The repaired raw ledger uses three 192-row projected matches plus six compatibility rows and is arithmetically \(775\)-by-\(774\), but global \(C^1/W^{2,p}\) multicell seams, the actual Fredholm operator, bordered inverse, continuous adjoint and tails remain open. Root-section spread \(0.10229\), response spread \(0.00607\), and wrong endpoint geometry forbid promotion |
| Vector gap/codimension | Abstract Lyapunov--Schmidt theorem proved; independent recoveries have an exact \((N+1)\)-dimensional singular generalized center and \(N-1\) slow transverse roots | Compute the selected-history Fredholm index \(q_N\); the center count alone is not that index |
| Schur--Melnikov response | Banach-scale response link and block/root calculus proved; both the exact quotient and a synchrony-quotient-free heterogeneous-curvature class supply nonzero arbitrary-\(N\) canonical witnesses | Pure-breaker higher response and arbitrary endpoint rules remain open |
| Physical outer continuation | Original backward-complete rule disproved as sufficient; causal released history and memory overwrite proved | Compatible normalized Gate P3-A\(^*\), or reset-to-canard factorization |
| Singular pulse/quiet geometry | Unforced fast-layer channels and a nonempty transition set are proved; the physical lower fold has the ordinary drifting orientation and positive action \(\mathcal A_-\); exact ODE-subclass theorems disprove the fixed-layer shortcut, the all-offset geometric-sign inference, and capture of all late exits by fixed-reset-layer blocks; a collective-recovery clamp gives an exact fixed-\(\delta\) separator | Prove U-SF and the complete-history fold map; for U-CAP first replace the old targets by moving latched detectors, then certify a finite deadband or the global invariant/stable-set exclusions. The exact Airy shift and exact two-channel no-hit band do not by themselves decide the physical RFDE; the controlled separator remains a different operational threshold |
| Balanced-network controlled excursion | For every finite nonnegative balanced two-half-delay topology, bounded exact-model additive feedback prepares \(\Phi_r\), realizes the nodewise zero-recovery decision leaf, and forces nonsynchronous signed detector hits and finite excursions with per-node authority and deadlines independent of \(N\) and topology. At the two center histories, the exact synchronized handoff theorem closes all inputs; a robust extension proves finite terminal capture from explicit asynchronous open cylinders in the full RFDE history space under \(10^{-4}\) state/history errors, arbitrary-sign shutdown residuals below \(10^{-5}\), and declared parameter errors | Robust reachability of the entrance cylinders from the earlier controller, autonomous onset, delay uncertainty, permanent no-return/basin capture, bandwidth/slew/hardware containment, and equality with a selected canard root remain open |
| Quadratic same-plant terminal transfer | An exact stop theorem proves that the root, controlled preparation/handoff and periodic basin modules fail four literal composition gates. A separate go theorem extends the hold to \(T_*\), cancels the carrier before release, closes all additive inputs at handoff, and absorbs the autonomous carrier into the robust residual for every admitted finite balanced topology when \(|\eta|<250000/12972264861\) | The result is policy-dependent finite terminal transfer; it does not prove selected onset, entrance reachability under perturbation, terminal-block basin containment, quiet capture, or permanent no-return |
| Reference-slice pulse/quiet basin audit | Two exact Rouché disks prove that the unique synchronous equilibrium has at least two open-right-half-plane characteristic roots on the microscopic gain box for \(|\eta|\le10^{-3}\). The validated \(\eta=0\) periodic orbit recrosses \(+1,+3/2,-1\) and stays above \(-6/5\), excluding permanent detector-side residence after periodic capture | A different quiet attractor is neither found nor excluded. Preserving literal autonomous dual-basin biology requires a new bistable slice, directed trapping neighborhoods, and terminal-history basin inclusion; latch and post-event switching are separate semantic/hybrid targets |
| Amplitude detector | Abstract quantitative local-chart implication proved | Model landing chart, unique peak branch, and derivative enclosures |
| Frequency--amplitude--safety conditioning | Periodic/event adjoints and a full-network transverse stability criterion are proved; on a microscopic FHN gain box D1 continuation, D3 unique extrema, the D4 fixed-matrix response enclosure, a direct two-output target ball of radius at least \(1.6218727378\times10^{-14}\), and two unsquared-amplitude three-output balls of radius \(2.7513816601\times10^{-15}\) are directed-certified. A 32,046-leaf right-half cover proves zero synchronous nontranslation unstable index and local orbital attraction. The oscillation-norm theorem gives uniform transverse rate \(0.007\) and fixed-network local nonlinear attraction at \(\eta=0\) for every finite balanced topology with \(\tau(Q)\le1/4\); the quadratic eta-Floquet replay extends this at the exact gain pair to \(|\eta|\le3\times10^{-6}\) | Prove a same-model trajectory connection from onset into the local periodic basin, a joint gain--eta box, weaker/closing-gap topology results, autonomous biological capture, and robust hardware containment; second sensitivities remain optional for larger boxes |

## 2. General network geometry

### 2.1 One-critical-mode class

Let the network state have dimension \(m_N+2\), let
\(\delta=\sqrt{\varepsilon}\), and represent weak delayed interactions by
matrix-valued measures on the fixed scaled-delay interval
\([0,\Theta_*]\). Near a selected fold, a uniformly conditioned coordinate
change must put the blown-up system into

\[
\begin{aligned}
u'&=q_0(u;\nu)
 +\delta F_N\bigl(u,h,\mathcal Tu,\mathcal Th;
                  \delta,\nu,\mathcal R\bigr),\\
\delta h'&=A_Nh
 +\delta G_N\bigl(u,h,\mathcal Tu,\mathcal Th;
                  \delta,\nu,\mathcal R\bigr),
\end{aligned}
\tag{GN}
\]

where \(u=(X,Y)\in\mathbb R^2\), \(h\in\mathbb R^{m_N}\), and \(q_0\) is
smoothly equivalent to the standard fold problem. The history operator
\(\mathcal T\) retains the complete scaled delays; it is not replaced by a
small-delay Taylor series.

The cleanest non-artificial realization is \(N\) fast nodes coupled through a
connected reversible or normal graph and one shared slow resource or
inhibitor. Then \(m_N=N-1\). A two-state-per-node FHN network is also admitted
when its transverse recovery modes have a proved uniform contraction. The
dual-state scaffold in the base repository is one proof model, not the
definition of generality.

For an admitted sequence of networks, require:

1. one length-two collective Jordan chain, with normalized critical vectors
   \(r_N,\ell_N\), and no other center directions;
2. a dimension-independent transverse semigroup estimate
   \[
   \|e^{A_Nt}\|\le M_Ae^{-\kappa_At},\qquad t\ge0;
   \tag{2.1}
   \]
3. uniformly conditioned critical/transverse projections and coordinates;
4. uniform finite \(C^k\) bounds on the nonlinearities;
5. uniformly bounded operator total variation of all matrix delay measures;
6. finite moving delays treated on a strong orbit space, never as small
   perturbations in the \(C^0\)-operator norm;
7. structural residuals measured after insertion into (GN), not only by an
   adjacency norm.

A graph Poincare gap may help verify (2.1) for reversible/normal graphs. It is
not a replacement for the RFDE semigroup estimate, especially for directed
nonnormal graphs.

There are two conclusion levels:

- a **fixed-\(N\) theorem**, whose constants may depend on the network;
- a **scalable theorem**, with one set of constants for all admitted \(N\).

### 2.2 Multiple critical directions

A standard FHN network with \(N\) independent slow recovery variables need
not have a scalar canard root. If the singular center calculation leaves
\(q_N>1\) unmatched directions, the correct object is a vector gap

\[
d_N:\mathbb R^{k_\mu}\times\mathfrak R_N\longrightarrow\mathbb R^{q_N}.
\tag{2.2}
\]

The full general-network theory must include this index/codimension result:
after phase fixing, the history operator has cokernel dimension \(q_N\), and
the canard set is a \(C^r\) submanifold of codimension \(q_N\) when
\(D_\mu d_N\) has rank \(q_N\). A scalar threshold is the specialization
\(q_N=1\). This yields an actuator-count obstruction: tracking all canard
safety coordinates requires at least \(q_N\) independent effective safety
directions.

For the standard voltage-coupled, independent-recovery model the current-
state obstruction is now exact: the singular generalized center has
dimension \(N+1\), consisting of one length-two fold chain and \(N-1\)
recovery-center eigenvectors, and weak voltage delays preserve an
\(N-1\)-root slow cluster.  This rules out a dimension-uniform
two-dimensional normal graph without changing the model or imposing exact
synchrony.  It does **not** by itself prove that the selected-history
Fredholm cokernel has dimension \(N\); see
[multiple-recovery-center-obstruction.md](multiple-recovery-center-obstruction.md).

Paper II should prove the abstract vector-gap theorem and calculate the
explicit topology response in the \(q_N=1\) class. A title using “one-critical
mode networks” is required if the vector theorem cannot be completed.

## 3. Paper II, Theorem A: dimension-uniform history graph

Under Section 2.1, construct a two-dimensional invariant-history graph

\[
h=H_{N,\delta,\nu,\mathcal R}(u)
\tag{3.1}
\]

and an injective history embedding

\[
\iota_{N,\delta,\nu,\mathcal R}(u)(\sigma)
=\bigl(\Phi_Q^\sigma u,
H_{N,\delta,\nu,\mathcal R}(\Phi_Q^\sigma u)\bigr),
\quad-\Theta_*\le\sigma\le0,
\tag{3.2}
\]

which exactly semiconjugates the reduced flow \(Q_N\) to the full RFDE on the
retained flow hull. Prove mixed parameter jets and a logarithmic-tube
remainder uniformly in \(N\):

\[
Q_N=q_0+\delta Q_{1,N}+\delta^2Q_{2,N}+\delta^3R_{3,N},
\qquad
|D^jR_{3,N}(u)|
\le C\,\operatorname{poly}(|u|)e^{c|u|}.
\tag{3.3}
\]

The primary proof route is the base paper's special-flow/fiber contraction.
Its estimates depend on semigroup, projection, delay-measure, and
nonlinearity bounds rather than the dimension itself. A full \(2N\) Lin BVP
is reserved for weak transverse recovery or multiple center directions.

Every Paper II network class must also prove a model-fitting lemma from its
original node equations to (GN), including \(r_N,\ell_N,A_N\), fold
curvature, unfolding direction, and induced matrix delay measures. This is
now done, with dimension-independent constants, for the shared-resource
Dobrushin class with heterogeneous fold curvature in
[paper-ii-heterogeneous-curvature-selected-root.md](paper-ii-heterogeneous-curvature-selected-root.md).
For any other graph architecture, (GN) remains only a normal-form assumption
until the analogous lemma is supplied.

## 4. Paper II, Theorem B: root response

Let \(D_N(\mu,\mathcal R)\) be the complete-history matching gap after the
transverse graph equations and phase have been solved. Assume

\[
D_N(\mu_{c,N},0)=0,\qquad
|\partial_\mu D_N(\mu_{c,N},0)|\ge m_N>0.
\tag{4.1}
\]

The first result is

\[
\mu_{c,N}(\mathcal R)-\mu_{c,N}(0)
=-
\frac{D_{\mathcal R}D_N(\mu_{c,N},0)[\mathcal R]}
     {\partial_\mu D_N(\mu_{c,N},0)}
+O\!\left(C_{{\rm root},N}\|\mathcal R\|^2\right),
\tag{4.2}
\]

Here \(C_{{\rm root},N}\) contains the second-derivative bounds and all
necessary inverse powers of the simple-root slope; it is not generally
proportional to \(m_N^{-1}\). Lemma 4.1 of
[general-network-schur-melnikov-proof.md](general-network-schur-melnikov-proof.md)
gives the explicit bound
\(\frac{M_N}{2m_N}(1+2B_N/m_N)^2\). The novelty is the
complete-history derivative, its topology decomposition, and a
dimension-controlled remainder, not the scalar implicit-function step.

### 4.1 Exact graph Schur complement

Write the special-flow graph residual as

\[
\mathbf G_{\delta,N}(Q,H;\nu,\mathcal R)
=
\begin{pmatrix}
Q-\mathcal T_Q(Q,H;\nu,\mathcal R)\\
H-\mathcal T_H(Q,H;\nu,\mathcal R)
\end{pmatrix}.
\tag{4.3}
\]

At the reference graph, set

\[
D_{(Q,H)}\mathbf G
=
\begin{pmatrix}
\mathsf A&\mathsf B\\
\mathsf C&\mathsf D
\end{pmatrix},
\qquad
D_{\mathcal R}\mathbf G[\mathcal R]
=
\begin{pmatrix}
g_c[\mathcal R]\\
g_\perp[\mathcal R]
\end{pmatrix},
\qquad
\mathsf S=\mathsf A-\mathsf B\mathsf D^{-1}\mathsf C.
\tag{4.4}
\]

The graph contraction must give \(N\)-uniform bounds on
\(\mathsf D^{-1}\) and \(\mathsf S^{-1}\). Then

\[
D_{\mathcal R}Q[\mathcal R]
=-\mathsf S^{-1}g_c[\mathcal R]
+\mathsf S^{-1}\mathsf B\mathsf D^{-1}g_\perp[\mathcal R].
\tag{4.5}
\]

Let the phase-normal one-sided gap before substitution of the graph be
\(\mathscr D_N(Q,H;\nu,\mathcal R)\), and write

\[
\begin{gathered}
m_c=D_Q\mathscr D_N,\qquad m_\perp=D_H\mathscr D_N,\qquad
\beta_N[\mathcal R]=D_{\mathcal R}\mathscr D_N[\mathcal R],\\
\widehat m=m_c-m_\perp\mathsf D^{-1}\mathsf C.
\end{gathered}
\]

The exact first derivative of the reduced gap is

\[
\begin{aligned}
D_{\mathcal R}D_N[\mathcal R]
={}&\beta_N[\mathcal R]
+m_cD_{\mathcal R}Q[\mathcal R]
+m_\perp D_{\mathcal R}H[\mathcal R].
\end{aligned}
\tag{4.6}
\]

Equivalently, emphasizing the exact Schur split,

\[
\boxed{
\begin{aligned}
D_{\mathcal R}D_N[\mathcal R]
={}&\beta_N[\mathcal R]
-\widehat m\mathsf S^{-1}g_c[\mathcal R]\\
&+(\widehat m\mathsf S^{-1}\mathsf B-m_\perp)
\mathsf D^{-1}g_\perp[\mathcal R].
\end{aligned}
}
\tag{4.6a}
\]

If the gap has no explicit structural dependence and factors through \(Q\),
then \(\beta_N=m_\perp=0\), and (4.6) reduces to the shorter two-term formula
previously recorded here.  In general, \(\beta_N\) and \(m_\perp\) retain
the history, moving-section, and endpoint terms.  These are the direct
critical and transverse history-resolvent/nonlinear-return contributions. A
strict critical/transverse direct sum would force the return block
\(\mathsf B\) to vanish and therefore cannot serve as the general mechanism
when the gap is critical-only. This is why the older full-network direct-sum
Lin specification is an extension route, not Paper II's principal proof.

The Banach-space derivation, the full block inverse bound, and the precise
direct-sum audit are proved in
[general-network-schur-melnikov-proof.md](general-network-schur-melnikov-proof.md).
The derivative-loss link from the triangular special-flow Picard jets to
this formula, including the \(C_b^9\to C_b^8\to C_b^7\) response scale,
complete-history extension/restriction, trace elimination, and endpoint
chain rule, is proved abstractly in
[banach-scale-history-schur-link.md](banach-scale-history-schur-link.md).
Its concrete selected-trace hypotheses are verified both for the compatible
canonical unequal-module quotient and for the heterogeneous-curvature
Dobrushin class. Arbitrary endpoint rules remain outside these canonical
selection theorems.

### 4.2 Schur--Melnikov functional

Let \(P_N=r_N\ell_N^\top\), \(P_{\perp,N}=I-P_N\). For a delay-layer
perturbation \(\Delta\mathbb B\), distinguish

\[
\Pi_{\parallel,N}(\Delta\mathbb B)
=\ell_N^\top\Delta\mathbb B\,r_N,\qquad
\Pi_{\perp,N}(\Delta\mathbb B)
=P_{\perp,N}\Delta\mathbb B\,r_N.
\tag{4.7}
\]

The graph response solves

\[
h_{\mathcal R}
=\mathcal L_{\perp,N}^{-1}\mathcal G_N[\mathcal R]
\tag{4.8}
\]

and returns through the network nonlinearity. Conditionally on the
model-specific one-sided trace calculation, define

\[
\mathfrak M_N[\mathcal R]
=-
\frac{
\displaystyle\int_{-\infty}^{\infty}
\psi(s)^\top
D_{\mathcal R}Q_{2,N}(\gamma_0(s);\nu_0,0)
[\mathcal R]\,ds
+\mathfrak b_N^{\rm num}[\mathcal R]
}{
\displaystyle\int_{-\infty}^{\infty}
\psi(s)^\top\partial_\nu Q_{1,N}(\gamma_0(s))\,ds
+\mathfrak b_N^{\rm den}
}.
\tag{4.9}
\]

The terms \(\mathfrak b_N^{\rm num}\) and
\(\mathfrak b_N^{\rm den}\) contain the structural and unfolding
history/endpoint contributions left after the graph response has been
inserted. They cannot be deleted by analogy with an ODE. Formula (4.9) is a
candidate coefficient until the one-sided trace problem proves this
representation and evaluates both boundary terms. Formula (4.5) is a
nonlinear Schur complement: projection-invisible forcing enters the
transverse RFDE range solve and returns before the critical adjoint pairing.

For directions preserving the fold, lower-order unfolding data, and the
complete direct critical delay measure, prove

\[
\mu_{c,N}(\delta,\mathcal R)-\mu_{c,N}(\delta,0)
=\delta^3\mathfrak M_N[\mathcal R]
+O\!\left(
\delta^4\|\mathcal R\|+\delta^3\|\mathcal R\|^2
\right).
\tag{4.10}
\]

General residuals may shift the fold or unfolding at lower orders; for them
(4.2), not the special order (4.10), is the theorem.  Write
\(a_{0,N}\ne0\) for the limiting derivative of the normalized gap with
respect to the unfolding parameter, as in (5.8) of
[general-network-schur-melnikov-proof.md](general-network-schur-melnikov-proof.md).
Under the corresponding anisotropic jet bounds, the general weak-delay
target must instead separate

\[
\mu_{c,N}(\mathcal R)-\mu_{c,N}(0)
=-\frac{\delta^2}{a_{0,N}}
\Lambda_{\parallel,N}[\mathcal R]
-\frac{\delta^3}{a_{0,N}}
\Lambda_{3,N}^{\rm full}[\mathcal R]
+O(\delta^4\|\mathcal R\|+\delta^2\|\mathcal R\|^2).
\tag{4.11}
\]

Only a complete-measure identity eliminating
\(\Lambda_{\parallel,N}\), including the required parameter jets, exposes an
identifiable \(O(\delta^3)\) law. The full cubic functional contains direct,
transverse-resolvent, trace, endpoint, and denominator-correction terms; it
reduces to \(\Lambda_{\perp,N}\) only after the other contributions have been
proved to vanish or remain fixed.

### 4.3 Genericity

The abstract functional-analytic statement is now proved in
[general-network-schur-melnikov-proof.md](general-network-schur-melnikov-proof.md):
on the admissible projection-neutral Banach tangent space, one nonzero
continuous linear response functional has a closed codimension-one kernel,
and its complement is open and dense.  The
[selected-root lift theorem](paper-ii-selected-root-lift-and-symmetry-breaking.md)
now supplies, for every pair of positive module sizes, a projection-neutral
non-equitable tangent with a nonzero canonical root derivative: the tangent
is the lifted module-difference direction plus a distributed zero-mean
breaker.  The latter is itself an exact first-response null direction by
Reynolds averaging. This closes the existence of a dimension-uniform witness
for the exact quotient. The heterogeneous-curvature theorem now closes the
complementary case without a nontrivial synchrony quotient: its full-row
neutral delay direction returns through
\(\pi_N^T\operatorname{diag}(c_N)A_N^{-1}\), and its canonical one-sided
trace calculation includes the history and endpoint terms. A pure
within-module Reynolds breaker still has zero first response; its
quadratic/higher coefficient remains open.

This converts the bespoke witness into an open constrained mechanism.
Layerwise critical-mode closure kills the delayed source term only when the
current, nonlinear, history, and endpoint operators preserve the same
splitting. Scalar delay moments alone do not determine (4.9).

### 4.4 Nonempty arbitrary-\(N\) verification class

The first scalable corollary should lift the nonuniform two-module
architecture to arbitrary module sizes \(N=n_1+n_2\). Module averaging and
replication operators satisfy \(R_NS_N=I_2\); the reference module subspace
reproduces the two-module dynamics, while within-module differences have
fixed Hurwitz blocks with a common semigroup bound. Small operator-TV
residuals may break equitability, perturb every edge, add fixed-support
heterogeneous delays, and introduce fold-compatible node heterogeneity.

For compatible relabeling-covariant canonical selections, the quotient class
has an exact arbitrary-size root and a genuinely non-equitable nonzero
tangent. The pure zero-mean breaker has zero first response, and the
proved finite-amplitude remainder is
\(O(\delta^4|\eta|+\delta^3\eta^2+\delta^2\zeta^2)\); it must not be
relabelled as a nonzero pure-breaker Melnikov law. The second scalable
corollary is now proved for a shared-slow-resource Dobrushin network with
node-dependent fold curvature. Its normalized all-to-all family has no
nontrivial synchrony polydiagonal, and its root coefficient is nonzero and
independent of \(N\). The theorem still excludes closing graph gaps, moving
delay atoms, and arbitrary physical outer selections.

A downstream policy-composition theorem in
[same-model-shared-resource-root-detector-bridge.md](same-model-shared-resource-root-detector-bridge.md)
keeps that shared-resource RFDE and scalar recovery coordinate fixed.  A
bounded controller prepares a reset depth that explicitly contains the exact
selected-root displacement and thereby obtains a nonzero, dimension-uniform
detector-latency response with the same \(\delta^3\zeta\) scale.  This is an
exact controlled transduction, but it uses the roots and model as offline
data.  An added \(O(\delta^3\zeta)\) policy offset changes the latency
coefficient while leaving the uncontrolled root unchanged.  Hence it is not
an input-independent physical onset comparison and does not close Paper III.

## 5. Paper III: physical maximal canard and pulse onset

The base paper's preparation-indexed root is not a biological threshold.
Paper III must construct, for the unprepared FHN-type RFDE:

1. parameter-coherent attracting and repelling outer slow-history manifolds;
2. their entry into the logarithmic fold tube with the mixed jets required by
   Paper II;
3. a common complete-history invariant object, so zero gap is a physical
   slow-history intersection;
4. a moving slow-base tube whose signed side exits and lower-fold cap cover
   every retained offset, including exponentially small ones;
5. a complete-history lower-fold map with its own transverse event root;
6. two disjoint global first-hit channels and a U-CAP capture/no-return
   theorem, with regular quiet and pulse sections used as witnesses after the
   fold side has been selected;
7. exclusion of competing roots, secondary bifurcations, and competing
   returns on the parameter box.

The singular two-module fast system now has a proved weighted-gradient,
strongly cooperative two-channel geometry; see
[paper-iii-physical-outer-pulse-bridge.md](paper-iii-physical-outer-pulse-bridge.md).
The original backward-complete outer rule is now disproved as sufficient:
it leaves the repelling unstable coefficient free and does not control mixed
history jets.  The repaired compatible-selection Gate P3-A\(^*\), or the
causal one-delay history-reset alternative, and the gap-to-channel exchange
remain the real open gates; see
[paper-iii-outer-selection-blocker-and-repair.md](paper-iii-outer-selection-blocker-and-repair.md).

The causal branch now splits into two mathematically different statements.
For the **unforced** release, recovery drift through an exponentially thin
saddle layer prevents a frozen-equilibrium stable-manifold argument.  An
exact ODE-subclass counterexample proves that a local saddle separator and
the existing fixed-layer blocks do not classify every nonzero reset offset;
it does not disprove a global separator for the physical FHN RFDE.  The
correct replacement is Gate U-SF (outer selected saddle history with uniform
mixed jets, a selected relative-growth history graph, and reset
transversality), followed by the repaired Gate U-EX (moving-tube side/cap
event and complete-history lower-fold map) and the separate U-CAP
capture/no-return gate; see
[paper-iii-unforced-separator-stop-go.md](paper-iii-unforced-separator-stop-go.md).
Gate U-SF is now reduced further in
[paper-iii-unforced-geometric-separator.md](paper-iii-unforced-geometric-separator.md).
The singular repelling action from the right fold to \(\rho=-1/2\) is
positive (numerically \(0.5607898753\ldots\)), so an outer mismatch is
amplified by \(\exp(\mathcal A_R/\varepsilon)\).  Hence algebraic or merely
\(e^{-c/\delta}\) overlap control cannot prove the tracker reaches the reset
layer. Exact common-history gluing, or an action-supercritical exponential
residual, together with the finite-segment \(C^1\) jet contract
U-OUT\({}^+\), are the remaining U-SF inputs. The direct forward
Lyapunov--Perron theorem already converts those jets into a delay-length-
uniform relative-growth history graph and reset covector; no full RFDE
trichotomy or stable foliation is used. Conditional on U-OUT\({}^+\), a
designed transverse reset and its unique geometric intersection follow
relative to the declared future extension, without making a pulse/quiet
claim. See
[paper-iii-strong-unstable-history-splitting.md](paper-iii-strong-unstable-history-splitting.md)
and
[paper-iii-u-out-terminal-matching.md](paper-iii-u-out-terminal-matching.md).
The closure audit
[paper-iii-u-out-action-scale-closure-audit.md](paper-iii-u-out-action-scale-closure-audit.md)
proves two additional scope boundaries. For every fixed logarithmic-chart
power \(p\), its Gaussian endpoint suppression is still algebraic and
cannot certify the fixed outer action \(e^{-A_R/\delta^2}\); moreover an
action-supercritical value residual does not imply uniform parameter jets.
U-OUT\({}^+\) therefore needs either an exact joint-in-parameter match or a
quantitative differentiated-residual ratio that remains small after the
known terminal-family losses. A positive action margin is a robust
sufficient condition, not a necessary one.
Gate U-EX now has a sharper stop/go result in
[paper-iii-unforced-lower-fold-exchange.md](paper-iii-unforced-lower-fold-exchange.md).
The physical singular lower fold is an ordinary drifting saddle-node, and
the reset-to-fold unstable action is positive (numerically
\(\mathcal A_-(0)=0.2792680505\ldots\)). An exact Airy ODE-subclass
calculation shows that exponentially small offsets on one side of the
selected repelling trajectory split into both fold sides. In that exact model
the fold-event root is nonzero and exponentially displaced from the geometric
root; for the physical RFDE the same conclusion is conditional on the stated
nonzero fold-offset factorization. Therefore the repaired intrinsic route uses
moving slow-base side exits, a lower-fold cap and complete-history fold map,
followed by a separate U-CAP capture/no-return theorem. It does not identify
the geometric root with the biological boundary by sign alone.
The U-CAP audit in
[paper-iii-unforced-capture-no-return.md](paper-iii-unforced-capture-no-return.md)
shows that the old fixed-\(\rho_0\) blocks are not valid targets for late
side/cap exits: the singular middle critical branch of the declared physical
model crosses \(H=7/5\) once near \(\rho=-0.9210\), and an exact
two-attractor ODE subclass has a punctured
no-hit interval. A complete-history isolating-chain implication is proved for
a declared outgoing deadband. Exact all-offset capture instead requires a
global two-basin invariant/stable-set certificate, which remains open for the
physical RFDE. A latched first hit needs no literal forever-trapping claim.
For a modified protocol that clamps only the
collective recovery coordinate until a channel is reached,
[paper-iii-collective-clamp-separator.md](paper-iii-collective-clamp-separator.md)
proves an exact clamped saddle history, a delay-independent one-unstable-root
criterion, and a unique local \(C^1\) complete-history separator for every
sufficiently small fixed positive \(\delta\). A fixed deadline resolves only
a declared deadband. This controlled separator is a valid operational pulse
threshold, but it is not \(\mu_{\mathrm{can}}\) and supplies no
reset-to-canard equality.

A second operational branch is now proved in
[paper-iv-balanced-general-topology-bounded-control-chain.md](paper-iv-balanced-general-topology-bounded-control-chain.md).
For every finite nonnegative topology satisfying the common row-mass and
stationary-balance identities, bounded exact-model additive feedback prepares
the complete constant history \(\Phi_r\) in finite time.  After voltage
release, bounded nodewise recovery cancellation maintains \(w=0\), and a
topology-independent weighted-mean comparison forces a nonsynchronous signed
detector hit and a larger finite excursion.  The preparation and decision
bounds are per-node \(\ell^\infty\) bounds independent of \(N\) and the admitted
topology.  This result replaces neither the intrinsic outer-history problem
nor U-CAP: it is a controlled voltage-excursion theorem, not an unforced
biological basin or canard-root identification.

The exact-center follow-up
[paper-iv-autonomous-handoff-excursion.md](paper-iv-autonomous-handoff-excursion.md)
removes every input from the final synchronized segment.  From
\(\Phi_{1/2}\), cancellation closes at \(v=1\) and the baseline RFDE reaches
\(v=3/2\); from \(\Phi_{-1/2}\), the \(-1\) detector is latched,
cancellation continues to \(-28/25\), and the baseline reaches \(-6/5\).
Both terminal hits occur before the shortest delayed layer changes, so exact
rational first-step phase barriers apply.  Closing already at \(-1\) is
proved to cause a reversal before \(-1.17\).  This is a finite autonomous
handoff after controlled onset on the exact synchronous leaf, not autonomous
onset, permanent no-return, asynchronous capture, or U-CAP.

The robust follow-up
[paper-iv-robust-handoff-tube.md](paper-iv-robust-handoff-tube.md)
removes exact synchrony and exact shutdown from this final segment.  It uses
strict open cylinders in
\(C([ -\tau_1,0],\mathbb R^{2N})\), allows current-state and relevant remote
voltage-history errors below \(10^{-4}\), arbitrary-sign residual voltage and
recovery inputs below \(10^{-5}\), and nonzero errors in \(\varepsilon\) and
\(a\).  A Dini--Gronwall tube of radius \(6\times10^{-4}\) leaves the
componentwise speeds bounded by \(\dot v_i\ge0.131\) or
\(\dot v_i\le-0.068\) until finite first entry into explicit terminal blocks,
uniformly over every finite admitted balanced topology.  This is a robust
**entrance-to-terminal** theorem.  It does not prove that the preceding
bounded feedback robustly reaches the entrance cylinder, that the terminal
block is invariant, or that either block is a biological basin.

The following is the still-conditional **intrinsic theorem target**, not a
current conclusion. If the listed outer-history and exchange items above are
proved, there should be a unique physical maximal-canard parameter
\(\mu_{\mathrm{can},N}\) with the response (4.2), and constants
\(A_{\rm small}<A_{\rm pulse}\), \(c,C>0\), and
\(\sigma_{\rm p}\in\{-1,1\}\) such that

\[
\begin{aligned}
\sigma_{\rm p}(\mu-\mu_{\mathrm{can},N})
&\le-Ce^{-c/\varepsilon}
&&\Longrightarrow&&\max h_N\le A_{\rm small},\\
\sigma_{\rm p}(\mu-\mu_{\mathrm{can},N})
&\ge Ce^{-c/\varepsilon}
&&\Longrightarrow&&\max h_N\ge A_{\rm pulse}.
\end{aligned}
\tag{5.1}
\]

The lower-fold audit shows that (5.1), even if proved with a deadband wider
than all omitted exponential shifts, would not identify the exact event
root. Let \(\mu_{\rm EX}\) denote the unique moving-tube/lower-fold event
root after its complete-history transition theorem is proved. Only after
U-CAP identifies its two fold sides with the biological blocks may the
**channel first-hit definition** use

\[
\boxed{\mu_{\rm pulse}^{\rm channel}=\mu_{\rm EX}
\quad\text{(conditional on U-SF, the fold map, and U-CAP)}.}
\tag{5.2}
\]

Under the nonzero fold-offset factorization,
\(\mu_{\rm EX}\) is exponentially displaced from the geometric middle-history
root. Equality with \(\mu_{\rm can}\) is an additional reset-to-canard and
cancellation theorem, not a consequence of channel separation.

A transverse finite-time section crossing cannot itself be an event-set
boundary: by the implicit-function theorem it persists for nearby
parameters.  A fixed-observable amplitude detector must instead be defined
by a peak condition
\[
 \max_{0\le t\le T_*(\varepsilon)}H(z(t;\mu))=H_*,
\]
where \(T_*(\varepsilon)=O(\varepsilon^{-1})\) in fast time covers a fixed
slow-time detector interval.  The maximizing time must be unique, interior,
and nondegenerate, with no peak switching.  A logarithmic
displacement theorem additionally requires a local landing equation whose
target, propagation prefactor, simple gap slope, and inverses have uniform
two-sided subexponential bounds, together with a normalized remainder small
in \(C^1\).  Under those quantitative hypotheses its honest displacement is
\[
 \varepsilon\log
 |\mu_{\rm pulse}^{H_*}-\mu_{\rm can}|
 \longrightarrow-\mathcal A_H,
\tag{5.2a}
\]
and a \(C^1\) exponential upper bound follows only on a box with a uniform
positive action and the stated derivative bounds.  A merely nonzero landing
coefficient is insufficient: an exponentially small detector target can add
a different action to (5.2a).  The precise abstract implication and the
remaining model-specific landing obligations are stated in
[paper-iii-physical-outer-pulse-bridge.md](paper-iii-physical-outer-pulse-bridge.md).

For the smooth channel coordinate, the positive safety orientation is,
conditionally on the fold-event theorem and U-CAP,

\[
S_{\rm p}(u)
=-\sigma_{\rm p}
\bigl(\mu_{\rm op}-\mu_{\rm EX}(u)\bigr).
\tag{5.3}
\]

Keep the root-transfer and event errors separate:

\[
E_{\rm outer}=o(\varepsilon^{3/2}),\qquad
E_{\rm fold}=|\mu_{\rm EX}-\mu_{\rm geo}|,
\quad \varepsilon\log E_{\rm fold}\to-\mathcal A_-,
\]

\[
E_{\rm event}^{\rm channel}
=|\mu_{\rm pulse}^{\rm channel}-\mu_{\rm EX}|=0
\quad\text{after U-CAP},
\qquad
\varepsilon\log E_{\rm event}^{H}\to-\mathcal A_H,\qquad
E_{\rm Lin/num}\ \text{independently enclosed}.
\tag{5.4}
\]

## 6. Paper IV: frequency--amplitude--pulse control

### 6.1 Model, actuators, and outputs

Use a delayed FHN neural network admitted by Papers II--III. Freeze voltage
and recovery variables, a module-level observable \(h_N\), short- and
long-conduction-delay synaptic layers, a hyperbolic periodic branch, and the
physical pulse/quiet channel separator covered by (5.2).  An
amplitude-detector threshold is a different, generally grazing event and is
used only after its peak/landing hypotheses have been proved.

Use three independently realizable actuator directions:

1. \(u_f\): recovery-rate or tonic-current modulation with nonzero period
   response;
2. \(u_a\): fold-centered nonlinear feedback with an amplitude response
   independent of \(u_f\);
3. \(u_s\): redistribution of short/long delay layers in
   \(\ker\Pi_{\parallel,N}\), with
   \(\mathfrak M_N[\partial_{u_s}\mathbb B]\ne0\).

The last is the topology-resolved safety actuator. A common delay shift is an
alternative only if the physical architecture supports it; it is not a
projection-invisible topology control.

No current theorem realizes all three *physical* roles in this paragraph.
The quadratic period-locked common RFDE now realizes a structural third
column at the small-\(\delta\) canonical-root level while making the center
periodic \((F,A)\) column exactly zero.  It does not yet realize the physical
safety output \(S_{\rm p}\), because its root derivative has not been
validated at \(\varepsilon=1/5\) and its selected root has not been identified
with an input-independent event.  The
[Dobrushin full-network lift](quadratic-period-lock-dobrushin-full-network.md)
supplies the size-uniform canonical zero-graph theorem, while the
[fixed-parameter BVP note](fixed-epsilon-quadratic-root-bvp.md) records the
exact validation blueprint.  The
[two-sided candidate](fixed-epsilon-two-sided-candidate.md) advances this to
an actual full-jump discrete adjoint calculation but proves, through its
endpoint-dimension audit, why it is still not a selected root.  The
[physical-onset stop/go theorem](quadratic-physical-onset-capture-stop-go.md)
then proves the exact failure of direct module composition and retains one
controlled same-plant terminal transfer under its strict small-\(|\eta|\)
bound.  The
exact
[root/periodic compatibility audit](paper-iv-root-periodic-model-compatibility.md)
proves that the arbitrary-size selected-root plant is not the balanced
dual-scaffold periodic/control plant. Its present redistribution direction
acts nontrivially on the periodic synchronous vector. Conversely, within the
restricted class of two distinct fixed delay atoms and linear layer
redistribution, exact invisibility on every scalar synchronous history forces
that direct critical action to vanish.  The nonlinear quadratic carrier is
the proved escape from this restricted obstruction; Paper IV must validate
its finite-\(\varepsilon\) complete-history response rather than import the
incompatible old \(\eta\) coefficient into (6.1).

On a phase-fixed hyperbolic periodic orbit \(z_u(t)\), define

\[
\mathcal Q_\varepsilon(u)
=\bigl(F(u),A_h(u),S_{\rm p}(u)\bigr),\qquad
F=1/T,\quad
A_h=\max_t h_N(z_u(t))-\min_t h_N(z_u(t)).
\tag{6.1}
\]

Unique nondegenerate extrema and absence of peak switching are hypotheses.
Squaring the amplitude does not repair an extrema switch.
The proved adjoint and no-go packages use the squared range
\(R_h=A_h^2\).  On a declared box with \(A_h\ge a_*>0\), this is a regular
\(C^1\) reparametrization, so the corresponding rank and inverse statements
are equivalent after the explicit row scaling \(D R_h=2A_hD A_h\).

Derive all rows:

- the periodic RFDE adjoint/phase BVP for \(D_uF\);
- the periodic variational BVP and moving-extremum cancellation for \(D_uA_h\);
- the complete-history root/event formula for \(D_uS_{\rm p}\), including
  endpoint, return, and moving-delay derivatives.

### 6.2 Scaled response and Schur complement

For a delay-induced safety response of order \(\varepsilon^{3/2}\), use the
dimensionless output

\[
\widehat{\mathcal Q}_\varepsilon(u)
=\left(
\frac{F-F_0}{q_F},
\frac{A_h-A_0}{q_A},
\frac{S_{\rm p}-S_0}{\varepsilon^{3/2}}
\right),
\tag{6.2}
\]

with positive input and output scales frozen before computation. Let

\[
 \sigma_{\rm sur}(M)
 :=\inf_{\|y\|_2=1}\|M^\top y\|_2
 =\lambda_{\min}(MM^\top)^{1/2}
\]

for every \(3\times m\) response matrix.  This is its row-surjectivity
modulus and equals the usual smallest singular value when \(m=3\).  Now let

\[
A_{FA}=D_{(u_f,u_a)}(\widehat F,\widehat A_h)
\tag{6.3}
\]

and

\[
\mathcal S_{\rm p}^{\rm Schur}
=\varepsilon^{-3/2}\left[
\partial_{u_s}S_{\rm p}
-D_{(u_f,u_a)}S_{\rm p}\,
A_{FA}^{-1}\partial_{u_s}(\widehat F,\widehat A_h)
\right].
\tag{6.4}
\]

The positive theorem must prove on a nonempty biological box \(U_*\)

\[
\inf_{u\in U_*}
\sigma_{\rm sur}\bigl(D_u\widehat{\mathcal Q}_\varepsilon(u)\bigr)
\ge c_*>0,
\tag{6.5}
\]

by lower bounds for \(\sigma_{\min}(A_{FA})\) and
\(|\mathcal S_{\rm p}^{\rm Schur}|\). A determinant heatmap is not a proof.
A quantitative inverse theorem then gives a target radius and robustness
margin.

### 6.3 Mandatory canard-conditioning gate

Independent control cannot be assumed. In a canard-explosion window of width
\(w_\varepsilon\sim e^{-\Lambda/\varepsilon}\), amplitude may satisfy

\[
A_h(u)\approx
\mathcal A\!\left(
\frac{\mu_{\rm op}-\mu_{\rm can}(u)}{w_\varepsilon},u
\right),
\tag{6.6}
\]

and hence

\[
D_uA_h\approx
-\frac{\mathcal A_\xi}{w_\varepsilon}D_u\mu_{\rm can}
+D_u^{\rm shape}\mathcal A.
\tag{6.7}
\]

The amplitude and safety rows can therefore be asymptotically collinear.
This mechanism now has an exact linear-algebra bound.  If \(f,a,s\) are the
unscaled frequency, amplitude, and safety rows, then for every scalar \(c\),

\[
 \sigma_{\rm sur}\!\begin{pmatrix}f\\a\\s\end{pmatrix}
 \le \frac{\|a-cs\|_2}{\sqrt{1+c^2}}.
 \tag{6.7a}
\]

Indeed, multiply on the left by the unit vector
\((0,1,-c)^\top/\sqrt{1+c^2}\).  Under the exact layer representation
\(A_h=\mathscr A(S_{\rm p}/w_\varepsilon)+R_\varepsilon\), take
\(c=\mathscr A'/w_\varepsilon\).  Suppose, uniformly for
\(0<\varepsilon\le\varepsilon_0\) and on the declared operating boxes, that
\(|\mathscr A'|\ge a_*>0\) and \(\|D_uR_\varepsilon\|\le C_R\), with
\(a_*,C_R\) independent of \(\varepsilon\).  For the scaled outputs in
(6.2), put \(\kappa_\varepsilon=\varepsilon^{3/2}\).  Their rows obey

\[
 \widehat a
 =\frac{\kappa_\varepsilon\mathscr A'}{q_Aw_\varepsilon}
   \widehat s+\frac{D_uR_\varepsilon}{q_A},
\]

and therefore

\[
 \sigma_{\rm sur}(D_u\widehat{\mathcal Q}_\varepsilon)
 \le \frac{C_Rw_\varepsilon}{
              \sqrt{q_A^2w_\varepsilon^2+
                     a_*^2\kappa_\varepsilon^2}}
 \le \frac{C_Rw_\varepsilon}{a_*\varepsilon^{3/2}}.
 \tag{6.7b}
\]

Thus an exponentially narrow window rules out an
\(\varepsilon\)-uniformly bounded family of linear right inverses unless a
genuine shape response enters on the same large scale.  This is a necessary,
not sufficient, escape condition: the sheared shape row must also remain
quantitatively transverse to the frequency and safety rows.  Pointwise
invertibility for each fixed \(\varepsilon>0\) may still hold.  The proof,
determinant row-shear identity, and unit-sensitive interpretation are given in
[paper-iv-canard-conditioning-no-go.md](paper-iv-canard-conditioning-no-go.md).
The network application remains conditional on the physical outputs and the
layer representation.

Paper IV must therefore establish one of three honest outcomes:

1. (6.5) holds on an operating box outside the sharp transition;
2. a phase-fixed stimulus threshold replaces \(S_{\rm p}\) and is proved
   independent of baseline amplitude;
3. an exponential ill-conditioning/no-go theorem holds inside the window.

Either a positive inverse or a sharp no-go theorem has mathematical value.

### 6.4 Structural no-go and robust inverse

A structural no-go theorem must be neighborhood-wide: if actuator response
functionals lie in a fixed two-dimensional subspace, or the safety row is a
fixed combination of the frequency and amplitude rows throughout a
neighborhood, then its derivative has rank at most two there and no \(C^1\)
local right inverse exists. Rank loss at one point is not a nonlinear
reachability theorem.

If

\[
\sigma_{\rm sur}(D_u\widehat{\mathcal Q}(u_0))\ge c_*,
\qquad
\sup_{B_r(u_0)}\|D_u^2\widehat{\mathcal Q}\|\le L_*,
\tag{6.8}
\]

then choose \(r\le c_*/(2L_*)\), with the closed input ball contained in the
operating box.  For exactly three actuator coordinates, every target with

\[
 \|\widehat y-\widehat{\mathcal Q}(u_0)\|
 \le c_*r/2
\]

is handled by the standard Newton self-map on that ball, giving the unique
local solution there and
\(\|D\widehat{\mathcal Q}^{-1}\|\le2/c_*\).  With more than three actuators,
one must first fix a three-dimensional actuator slice with invertible central
response and replace \(c_*\) by the restricted response's lower bound; the
conclusion is a local right section, not an inverse on the full actuator
space.  The commanded safety margin must exceed the sum of
outer, event, Lin, numerical, and model errors.

### 6.5 Proved no-go and reset-only repair

The declared three-baseline-actuator design now has a model-specific negative
theorem in
[paper-iv-fhn-control-no-go.md](paper-iv-fhn-control-no-go.md). The full
two-module network variational equation splits exactly into collective,
module-difference, and within-module blocks; an explicit Halanay condition
makes every noncollective multiplier stable uniformly in module size. Thus
the control obstruction is not a transverse desynchronization. If the
physical safety root has its declared \(C^1\)
\(\varepsilon^{3/2}\) jet and the amplitude lies in a one-coordinate canard
layer of width \(w_\varepsilon\), every right inverse grows at least like
\(\varepsilon^{3/2}/w_\varepsilon\), even after natural safety scaling. The
root and layer hypotheses remain conditional on Paper III/global branch
geometry; the linear-algebra and transverse-stability implications are
proved and sharp.

A positive operational repair is proved in
[paper-iv-reset-only-block-control.md](paper-iv-reset-only-block-control.md).
Use two baseline controls \(b=(b_1,b_2)\) for frequency and amplitude, and a
reset-only stimulus \(a_{\rm op}\) that is absent from the baseline RFDE.
For the controlled complete-history threshold \(a_c(b)\),

\[
 D\mathcal Q=
 \begin{pmatrix}
  D_b(F,A)&0\\
  D_ba_c&-1
 \end{pmatrix}.
 \tag{6.9}
\]

If \(\sigma_{\min}(D_b(F,A))\ge\beta>0\) and
\(\|D_ba_c\|\le\gamma\), the theorem gives an explicit positive lower
bound for \(\sigma_{\min}(D\mathcal Q)\), an explicit inverse-norm bound,
and, under a derivative Lipschitz estimate, a covered target ball. An exact
cubic Hopf family verifies that the two-by-two condition is nonempty. For
the declared synchronous FHN RFDE, the directed parameter-box certificate
now supplies the periodic branch, unique extrema, moving-delay sensitivities,
and the two-by-two response with \(\beta_U\ge0.0162187\). Ordinary
floating-point SVD remains only a precursor; the proved statement is tied to
the microscopic MPFR-directed box.

For that microscopic FHN box, the later fixed-derivative-box theorem gives a
stronger route than the generic Lipschitz hypothesis: all matrices
\(D_b(F,R_h)\) lie within a radius \(r_B<s_0\) of one fixed invertible
matrix \(B_0\). The nonlinear remainder is therefore \(r_B\)-Lipschitz, and
the periodic response covers a directed output ball of radius at least
\(1.6218727378\times10^{-14}\). No second sensitivity is used in this
conclusion.

A sharper protocol-coordinate version is proved in
[paper-iv-calibrated-reset-coordinate.md](paper-iv-calibrated-reset-coordinate.md).
The local diffeomorphism

\[
 (a_{\rm op},b)\longmapsto
 \bigl(G_b(\mathcal R(a_{\rm op},b)),b\bigr)
 \tag{6.9a}
\]

uses the signed complete-history gap itself as a calibrated stimulus
coordinate \(s\). In that coordinate the response is exactly

\[
 D\mathcal Q_{\rm cal}=\operatorname{diag}
   \bigl(D_b(F,A),-1\bigr),
 \tag{6.9b}
\]

so its smallest singular value is
\(\min\{\sigma_{\min}(D_b(F,A)),1\}\). This removes the threshold-gradient
penalty in calibrated coordinates but not the physical calibration cost:
the raw preset realizing \(s\) depends on \(b\), and both the usable
calibration half-width and the Jacobian of this command map must be
validated. A small raw transversality derivative cannot be hidden by
rescaling \(s\). If such feed-forward calibration is unavailable, (6.9)
remains the correct raw-actuator theorem.

The executable candidate in
[paper-iv-fhn-periodic-box-candidate.md](paper-iv-fhn-periodic-box-candidate.md)
provides a concrete stop/go point for this gate. At 129 odd Fourier nodes it
has a positive center response singular value and a positive nine-sample
floating Weyl margin; a 193-node rerun sharply reduces the off-grid residual.
Its JSON record preserves the arithmetic and software provenance. These
facts neither enclose the continuum between gain samples nor the Fourier
tail, and the finite bordered inverse is not an RFDE operator inverse. The
note therefore retains the label *candidate* and gives two honest proof
routes: direct parametric RFDE validation, preferred at this point, and an
adaptation of the Chebyshev ODE-persistence method for multiple constant
delays. The latter is not a direct application of the published single-delay
theorem and its six interval polynomial inequalities have not been verified.

The directed follow-up
[paper-iv-directed-periodic-validation.md](paper-iv-directed-periodic-validation.md)
now proves a narrower, exact result: at the declared center parameters, the
97-node phase-fixed nodal map has a unique root in an explicit MPFR-directed
box and its finite bordered Jacobian is uniformly invertible there. Directed
DFT and finite convolution give two-sided bounds on the complete residual
through mode \(3K\), proving that essentially half of its Wiener mass lies
outside the original collocation band. A tail-diagonal Neumann gate passes,
but the de-aliased finite--tail cross blocks and nonlinear correction-tail
bound are not supplied. Consequently no infinite radii polynomial is
evaluated, no periodic RFDE orbit is claimed, and issue 15 remains open.

The de-aliased finite--tail follow-up
[paper-iv-infinite-periodic-validation.md](paper-iv-infinite-periodic-validation.md)
closes precisely that center-orbit seam. Its \(M=144\) de-aliased weighted
real-conjugate coefficient block, two finite--tail cross bounds, tail inverse,
and moving-delay-aware
nonlinear majorant give a negative radii polynomial at radius \(10^{-7}\).
This proves the center periodic RFDE orbit and phase-bordered inverse only.
The separate transfer theorem in
[paper-iv-fredholm-monodromy-transfer.md](paper-iv-fredholm-monodromy-transfer.md)
uses the exact moving-delay period column to prove algebraic simplicity of
the autonomous unit multiplier and excludes a directed punctured arc about
it. The later full-complex parameter-box theorem validates 319 connected
positive Bloch cells through directed \(\pi\), with
\(\max q_I\le0.7026326\), and proves synchronous orbital hyperbolicity.

The parameter-box follow-up
[paper-iv-periodic-parameter-box.md](paper-iv-periodic-parameter-box.md)
now proves D1 continuation, D3 unique nondegenerate voltage extrema, and the
directed D4 response bound

\[
 \inf_{b\in U}\sigma_{\min}D_b(F,R_h)\ge0.0162187
\]

on the declared nonempty box of gain half-width \(10^{-12}\). Its analytic
bridge proves a \(C^1\) derivative-domain branch without differentiating the
raw shift on the unweighted Wiener space; its executable record separately
encloses finite-center, finite-interval, and analytic-tail sensitivity
residuals. This is a real but deliberately local response theorem. The
separate outer-arc certificate now closes the synchronous unit-circle gate.
The direct fixed-matrix inverse theorem now also closes the microscopic
two-output target-radius gate.  Exact-orbit amplitude conversion and the
independent reset coordinate then give two three-dimensional
\((F,A,S_{\rm op})\) target balls.  The balanced-network theorem transfers
these outputs to the invariant synchronous branch of every admitted topology
and supplies, for the same parameter/reset triple, a bounded controlled
excursion; this is parameter-linked, not a trajectory connection to the
periodic branch.  At the two exact center resets, a separate synchronized
   handoff theorem closes all inputs on the final excursion segment.  Its robust
   open-cylinder extension covers asynchronous perturbations and bounded
   shutdown residuals, but neither theorem lands on the periodic branch.  A
   transverse Halanay estimate first proves uniform transverse decay for the
   fixed rank-one topology.  A later weighted-oscillation theorem extends the
   decay and fixed-network local attraction at \(\eta=0\) to every finite
   balanced topology with \(\tau(Q)\le1/4\), at uniform transverse rate
   \(0.007\) but without a topology-uniform nonlinear basin.  The logarithmic
   Riesz reduction and a complete
   32,046-leaf directed right-half cover now prove that the synchronous
   nontranslation unstable index is zero and give local nonlinear orbital
   attraction with asymptotic phase.  Composing the synchronous and
   Dobrushin transverse blocks gives local full-network attraction for every
   fixed finite admitted strongly mixing topology.  A
   same-model onset-to-basin connection, robust entrance reachability and
   hardware containment remain open. An exact
   compatibility certificate proves that the earlier selected-root RFDE and
   this periodic/control RFDE are not the same plant and that their old
   parameter directions cannot be composed.  The quadratic period-locked
   extension now provides a common dual-scaffold RFDE and a proved
   small-\(\delta\) root column with zero center periodic column.  Its
   Dobrushin lift proves canonical full-network uniqueness on the exact
   anisotropic zero-transverse graph.  Thus the structural same-model
   obstruction, the declared uniformly mixing full-network root gate, and
   the stable-index gate are closed; fixed-\(\varepsilon\) root validation,
   arbitrary-history/basin uniqueness, and the biological-trajectory gate
   remain open.

## 7. Stop/go gates

### Paper II

1. retain the now-proved heterogeneous-curvature Dobrushin theorem as the
   synchrony-quotient-free one-critical-mode result, including its explicit
   model fit, endpoint terms, genericity, and all-\(N\) nonzero witness;
2. decide whether Paper II stops at this declared uniformly mixing graph
   class or adds a sparse/closing-gap theorem with correspondingly
   nonuniform constants;
3. evaluate the pure-breaker quadratic/higher response only if a separate
   arbitrary symmetry-breaking claim is retained;
4. compute the concrete vector-gap index or restrict the title to the
   one-critical-mode class;
5. retain the exact quotient theorem as an independent regression class.

### Paper III

1. for the intrinsic unforced route, prove normalized compatible outer continuation
   P3-A\(^*\), including its \(C^1_\mu C^2_u\) strong-history jets and exact
   common-graph gluing;
2. close Gate U-SF through U-OUT\({}^+\): prove exact common-history outer
   continuation (or an action-supercritical residual beyond the right-fold-
   to-reset action), a differentiated-residual ratio strong enough after
   the declared terminal-family losses (unless the match is an exact joint
   identity), and the finite-segment mixed
   tracker jets. The existing fixed-\(p\) logarithmic endpoint estimate is
   proved insufficient for this step. Then invoke
   the proved selected-extension and direct relative-history-graph theorem,
   designed reset-transversality, and unique geometric-intersection theorem;
3. replace the false all-offset sign form of U-EX by a complete-history
   moving-tube and lower-fold-cap transition theorem, including the
   conditionally displaced fold-event root. For U-CAP, discard the old
   fixed-reset-layer targets for late exits, construct moving latched detector
   cylinders, and either certify a stated deadband by the isolating-chain
   theorem or prove the global invariant/stable-set exclusions needed for an
   exact boundary. Only then may the fold event, not automatically the
   geometric U-SF root, be identified with the unforced first-hit boundary.
   Retain the proved one-delay release/memory theorem and fixed-\(\delta\)
   collective-clamp separator as a distinct operational branch;
4. if equality with the canard root is claimed, prove the reset-to-canard
   factorization and its small preparation error separately;
5. prove the full exchange-and-basin separator that makes the intrinsic
   channel identity (5.2) a theorem;
6. independently, if an amplitude-detector coordinate is used, verify the
   quantitative landing-chart hypotheses that yield (5.2a);
7. enclose all three error layers in (5.4).

### Paper IV

1. retain the proved microscopic-box D1/D3/D4 certificate, including its
   de-aliased finite--tail inverse, moving-delay majorants, unique extrema,
   and \(\beta_U\ge0.0162187\);
2. retain the proved simple unit multiplier, 319-cell full-complex Bloch
   exclusion, and complete 32,046-leaf right-half zero-free cover.  Claim
   synchronous local attraction only on the certified microscopic box.  For
   full networks, compose with the Dobrushin transverse theorem on
   \(\eta=0\) and \(\tau(Q)\le1/4\).  At the exact center gain pair, retain
   the separately replayed quadratic carrier box
   \(|\eta|\le3\times10^{-6}\).  Keep the uniform transverse rate but do not
   infer a topology-uniform nonlinear basin or a joint gain--eta box;
3. retain the proved fixed-matrix two-output target ball, exact unsquared-
   amplitude transfer, and two \((F,A,S_{\rm op})\) target balls; compute
   second sensitivities only to enlarge the box or quantify raw-coordinate
   curvature;
4. retain the balanced-general-topology bounded preparation, nodewise
   decision control and signed excursion theorem as an exact-model staged
   result.  State explicitly that its periodic outputs belong separately to
   the invariant synchronous branch.  Retain the exact-center synchronized
   all-inputs-off handoff corridors and the negative unit-face reversal as a
   separate finite-horizon theorem, not a target-neighborhood or basin claim.
   Retain the robust open-cylinder handoff as a separate entrance-to-terminal
   theorem and prove robust entrance reachability before composing it with the
   earlier controller.  Retain the quadratic stop/go successor separately:
   its extended \(T_*\) hold, exact pre-release cancellation, and strict
   \(|\eta|<250000/12972264861\) bound prove same-plant finite terminal
   transfer, not input-independent onset or basin capture.  Retain the
   reference-slice no-go separately: the synchronous rest is unstable for
   \(|\eta|\le10^{-3}\), while convergence to the validated periodic orbit
   forbids permanent residence on the four declared detector sides.  Do not
   call a latched label a basin or hide a post-event parameter switch;
5. use the quadratic period-locked common RFDE, not the incompatible old
   two-atom \(\eta\)-direction.  Retain its proved uniform Dobrushin
   canonical-graph lift.  Validate its selected complete-history BVP,
   augmented inverse and dynamic adjoint at \(\varepsilon=1/5\); then add an
   input-independent event comparison and a trajectory connection if a
   canard-to-periodic pulse theorem is claimed;
6. extend the present shutdown-residual and parameter tube to delay error,
   measurement/model error, bandwidth, slew, energy and saturation margins
   before making a hardware statement;
7. retain the proved two-scale no-go for the original canard-layer outputs
   under its explicit root/layer hypotheses, and do not relabel the controlled
   operational margin as an unforced canard margin.

### Required falsifiers

- remove transverse recovery damping so multiple canard directions reappear;
- use graph sequences whose RFDE transverse inverse grows with \(N\);
- perturb inside and outside \(\ker\mathfrak M_N\);
- preserve the projected delay measure while changing transverse layers;
- attempt the proposed same-model actuator on arbitrary scalar synchronous
  histories, not only at the equilibrium or one sampled orbit phase;
- compare the exactly cancelling linear carrier with the quadratic carrier,
  and vary the older-history extension to verify that the advertised root is
  explicitly preparation indexed;
- use trajectory-close reductions that predict the wrong root;
- force an extrema switch;
- compare two- and three-actuator families;
- compare the geometric root with multiple pulse detectors.

## 8. Computation and reproducibility

Required deliverables are:

1. symbolic fold, projection, and transverse-return audits for arbitrary
   matrix layers and generated \(N\);
2. independent invariant-graph and RFDE collocation/Lin root computations;
3. residual-over-derivative root enclosures with separate mesh, history
   interpolation, delay quadrature, graph truncation, and continuation errors;
4. held-out \(N=2,8,32\) networks and a larger sparse case, checked against
   theorem constants rather than selected after fitting;
5. periodic RFDE adjoints cross-checked against centered differences;
6. an interval or radii-polynomial enclosure of (6.5), if the positive
   control branch survives;
7. machine-readable configurations, checksums, and one-command reproduction.

The earlier Runge--Kutta chain-tree theorem is only an ODE map--flow baseline.
It does not certify delayed-history interpolation or an RFDE root.
The floating FHN periodic JSON remains the response/centered-difference
precursor. The finite directed JSON proves the exact nodal root/inverse and
exposes the unresolved tail at that stage; the center infinite JSON closes
the finite/tail orbit proof; and the parameter-box JSON closes D1, D3, and
the response part of D4 while retaining its stage-local later-gate flags.
The separate Bloch and direct-target artifacts close synchronous orbital
hyperbolicity and the microscopic frequency--squared-range target radius,
respectively.  The amplitude, three-output, bounded-preparation,
balanced-sign-cone and balanced-control-chain artifacts then close the
unsquared-amplitude target balls and the exact-model controlled-excursion
branch.  The shared-resource policy artifact records an exact root-linked
latency transduction while forcing its input-independent-onset flags false.
The autonomous-handoff artifact closes every input on two exact synchronized
terminal corridors and records the negative unit-face reversal obstruction.
The robust-handoff artifact upgrades that final segment to explicit
asynchronous open RFDE entrance cylinders and bounded shutdown residuals while
keeping entrance reachability, terminal invariance and biology flags false.
The quadratic stop/go artifact proves four exact non-composition seams and,
on a separate controlled branch, preserves both terminal transfers after
release for \(|\eta|<250000/12972264861\); it forces every onset, basin,
capture and permanent-no-return flag false.
The reference-slice dual-basin artifact proves two open-right-half-plane
equilibrium roots on the microscopic gain/\(\eta\) box and the periodic
detector-face recurrence obstruction.  It explicitly leaves the existence
or exclusion of a different quiet attractor, global uniqueness, and every
bistable or switched repair open.
The first transverse Halanay artifact proves fixed-rank-one transverse decay.
The Dobrushin successor proves, on \(\eta=0\) and \(\tau(Q)\le1/4\), a uniform
rate \(0.007\) for arbitrary finite admitted balanced topologies.  The Riesz
and right-half-cover artifacts rigorously remove the infinite spectral tail,
certify every dyadic keyhole leaf, prove exact zero winding and close the
synchronous nontranslation stable-index/attraction gate.  Their composition
with the Dobrushin artifact promotes local full-network attraction for each
fixed finite strongly mixing topology, without a uniform nonlinear basin.
The quadratic eta-Floquet successor replays every one of those base leaves,
closes the period-length active-horizon bridge, and extends the exact-center
full-network conclusion to \(|\eta|\le3\times10^{-6}\); it does not provide a
joint gain--eta box.
All corresponding records deliberately keep a same-trajectory
onset-to-periodic connection, autonomous biological capture, joint-gain
nonzero-\(\eta\) attraction, weaker/closing-gap topologies, robust hardware
actuation and the relevant biological flags false.

## 9. Literature boundary and value

- Scalar delayed van der Pol work supplies direct weak-delay calibration, not
  a transverse network range equation.
- Classical RFDE center manifolds and Lin methods supply tools, not the
  singular, topology-resolved, dimension-controlled root response.
- Spectral network reductions provide collective coordinates but do not prove
  that a projected trajectory or delay kernel determines a nonhyperbolic
  threshold.
- Existing frequency--amplitude feedback gives two-output modulation, not a
  complete-history pulse-safety row or the conditioning result above.
- Existing canard-control results do not establish independent
  frequency--amplitude--pulse assignment in a delayed network.

The completed program's reusable mathematical chain is

\[
\text{network delay layer}
\longrightarrow
\text{transverse RFDE range solve}
\longrightarrow
\text{nonlinear critical return}
\longrightarrow
\text{physical canard/pulse boundary}
\longrightarrow
\text{quantitative control or no-go}.
\]

## 10. Claim discipline

Until the corresponding gates pass, use:

- **prepared local history-connection root** for the completed base theorem;
- **proved heterogeneous-curvature Dobrushin prepared-root response** for
  that declared subclass in Sections 2--4, and **general-network response
  target** for the remaining architectures;
- **physical maximal-canard root** only after Paper III's outer-history proof;
- **pulse-onset separator** only after (5.1)--(5.2);
- **pulse-safety controllability** only after (6.5) and its error enclosure.

Failure of a later gate narrows the new theorem or changes the actuator/model.
It does not invalidate the JNS base theorem and must not be hidden by
renaming an output event as a geometric canard.
