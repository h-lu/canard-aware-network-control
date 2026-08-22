# General-network canards and biological pulse control

Status: **research contract, 2026-08-23**. This document defines the work
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
2. **Physical pulse bridge.** Prove that selected physical outer slow
   histories enter the local fold problem and that the resulting maximal
   canard separates subthreshold and large-pulse itineraries.
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

Paper II must also prove a model-fitting lemma from an original node network
to (GN), including \(r_N,\ell_N,A_N\), fold curvature, unfolding direction,
and induced matrix delay measures. Without that lemma, (GN) is only a normal
form assumption.

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
+O\!\left(\frac{C_NG_N^2\|\mathcal R\|^2}{m_N}\right),
\tag{4.2}
\]

where \(G_N\) is the complete transverse graph/range inverse. The novelty is
the complete-history derivative, its topology decomposition, and the
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

If \(\mathfrak m_{\delta,N}=D_QD_N\) is the phase-normal one-sided gap
functional, the exact first derivative is

\[
\boxed{
D_{\mathcal R}D_N[\mathcal R]
=
-\mathfrak m_{\delta,N}\mathsf S^{-1}g_c[\mathcal R]
+
\mathfrak m_{\delta,N}\mathsf S^{-1}
\mathsf B\mathsf D^{-1}g_\perp[\mathcal R].
}
\tag{4.6}
\]

These are the direct critical and transverse history-resolvent/nonlinear
return terms. A strict critical/transverse direct sum would force the return
block \(\mathsf B\) to vanish and therefore cannot serve as the general
mechanism. This is why the older full-network direct-sum Lin specification is
an extension route, not Paper II's principal proof.

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

and returns through the network nonlinearity. Define

\[
\mathfrak M_N[\mathcal R]
=-
\frac{
\displaystyle\int_{-\infty}^{\infty}
\psi(s)^\top
D_{\mathcal R}Q_{2,N}(\gamma_0(s);\nu_0,0)
[\mathcal R]\,ds
+\mathfrak b_N[\mathcal R]
}{
\displaystyle\int_{-\infty}^{\infty}
\psi(s)^\top\partial_\nu Q_{1,N}(\gamma_0(s))\,ds
}.
\tag{4.9}
\]

The term \(\mathfrak b_N\) contains derived history/endpoint contributions;
it cannot be deleted by analogy with an ODE. Formula (4.5) is a nonlinear
Schur complement: projection-invisible forcing enters the transverse RFDE
range solve and returns before the critical adjoint pairing.

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
(4.2), not the special order (4.10), is the theorem. More explicitly, the
weak-delay expansion should separate

\[
\mu_{c,N}(\mathcal R)-\mu_{c,N}(0)
=-\frac{\delta^2}{\kappa_0}
\Lambda_{\parallel,N}[\mathcal R]
-\frac{\delta^3}{\kappa_0}
\Lambda_{\perp,N}[\mathcal R]
+O(\delta^3\|\mathcal R\|+\delta^2\|\mathcal R\|^2).
\tag{4.11}
\]

Only a complete-measure identity eliminating
\(\Lambda_{\parallel,N}\), including the required parameter jets, exposes the
pure \(O(\delta^3)\) transverse law.

### 4.3 Genericity

The two-module paper supplies one witness with
\(\Pi_{\parallel,N}(\Delta\mathbb B)=0\) and
\(\mathfrak M_N[\Delta\mathbb B]\ne0\). Paper II must prove:

> On the admissible projection-neutral space
> \(\ker\Pi_{\parallel,N}\), the functional \(\mathfrak M_N\) is continuous.
> If one admissible transverse-resolvent/nonlinear-return contraction is
> nonzero, then \(\mathfrak M_N\ne0\) off a closed codimension-one kernel.

This converts the bespoke witness into an open constrained mechanism.
Layerwise critical-mode closure kills the delayed source term only when the
current, nonlinear, history, and endpoint operators preserve the same
splitting. Scalar delay moments alone do not determine (4.9).

### 4.4 Nonempty arbitrary-\(N\) verification class

The first scalable corollary should lift the nonuniform two-module
architecture to arbitrary module sizes \(N=n_1+n_2\). Module averaging and
replication operators satisfy \(A_NR_N=I_2\); the reference module subspace
reproduces the two-module dynamics, while within-module differences have
fixed Hurwitz blocks with a common semigroup bound. Small operator-TV
residuals may break equitability, perturb every edge, add fixed-support
heterogeneous delays, and introduce fold-compatible node heterogeneity.

This gives an open class of finite heterogeneous delayed networks near a
nonuniform two-module simple-fold architecture. It is the minimum concrete
family needed to prevent the abstract theorem from merely assuming all
network difficulty away. A shared-slow-resource model on connected
reversible graphs is the second, more biologically natural target.

## 5. Paper III: physical maximal canard and pulse onset

The base paper's preparation-indexed root is not a biological threshold.
Paper III must construct, for the unprepared FHN-type RFDE:

1. parameter-coherent attracting and repelling outer slow-history manifolds;
2. their entry into the logarithmic fold tube with the mixed jets required by
   Paper II;
3. a common complete-history invariant object, so zero gap is a physical
   slow-history intersection;
4. a transverse local exit coordinate whose sign is the physical gap sign;
5. two global channels, one crossing a quiet section and one crossing a
   declared pulse section;
6. exclusion of competing roots, grazing, secondary bifurcations, and peak
   switching on the parameter box.

There is then a unique physical maximal-canard parameter
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

This theorem permits the phrase *pulse threshold*. Inside the exponentially
narrow layer, detector-dependent events remain output-event thresholds.
For a fixed detector \(H_*\), prove the \(C^1\) estimate

\[
\|\mu_{\rm pulse}^{H_*}-\mu_{\rm can}\|_{C^1_u}
\le Ce^{-\Lambda/\varepsilon}.
\tag{5.2}
\]

The positive safety coordinate is fixed by the proved orientation:

\[
S_{\rm p}(u)
=-\sigma_{\rm p}
\bigl(\mu_{\rm op}-\mu_{\mathrm{pulse}}^{H_*}(u)\bigr).
\tag{5.3}
\]

Keep three errors separate:

\[
E_{\rm outer}=o(\varepsilon^{3/2}),\qquad
E_{\rm event}\le Ce^{-\Lambda/\varepsilon},\qquad
E_{\rm Lin/num}\ \text{independently enclosed}.
\tag{5.4}
\]

## 6. Paper IV: frequency--amplitude--pulse control

### 6.1 Model, actuators, and outputs

Use a delayed FHN neural network admitted by Papers II--III. Freeze voltage
and recovery variables, a module-level observable \(h_N\), short- and
long-conduction-delay synaptic layers, a hyperbolic periodic branch, and one
pulse detector covered by (5.2).

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

with input and output scales frozen before computation. Let

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
\sigma_{\min}\bigl(D_u\widehat{\mathcal Q}_\varepsilon(u)\bigr)
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
Paper IV must establish one of three honest outcomes:

1. (6.5) holds on an operating box outside the sharp transition;
2. a phase-fixed stimulus threshold replaces \(S_{\rm p}\) and is proved
   independent of baseline amplitude;
3. an exponential ill-conditioning/no-go theorem holds inside the window.

Either a positive inverse or a sharp no-go theorem has mathematical value.

### 6.4 Structural no-go and robust inverse

A no-go theorem must be neighborhood-wide: if actuator response functionals
lie in a fixed two-dimensional subspace, or the safety row is a fixed
combination of the frequency and amplitude rows throughout a neighborhood,
then the three-output map has rank at most two. Rank loss at one point is not
a theorem.

If

\[
\sigma_{\min}(D_u\widehat{\mathcal Q}(u_0))\ge c_*,
\qquad
\sup_{B_r(u_0)}\|D_u^2\widehat{\mathcal Q}\|\le L_*,
\tag{6.8}
\]

then \(r\le c_*/(2L_*)\) gives a certified local inverse and
\(\|D\widehat{\mathcal Q}^{-1}\|\le2/c_*\). The commanded safety margin must
exceed the sum of outer, event, Lin, numerical, and model errors.

## 7. Stop/go gates

### Paper II

1. prove the original network-to-(GN) fitting lemma;
2. prove the dimension-uniform history graph;
3. derive (4.4)--(4.11), including endpoint/history terms;
4. prove genericity on \(\ker\Pi_{\parallel,N}\);
5. prove the vector-gap/codimension theorem or restrict the title to the
   one-critical-mode class;
6. verify one nontrivial \(N\)-uniform graph family.

### Paper III

1. construct physical outer history families and their \(C^1_\mu C^2_u\)
   boundary jets;
2. prove the gap-to-exit map is transverse;
3. prove the quiet/pulse global channels;
4. prove the operational event estimate (5.2);
5. enclose all three error layers in (5.4).

### Paper IV

1. prove periodic-branch hyperbolicity and unique extrema;
2. derive and independently check all three sensitivity rows;
3. resolve the canard-conditioning alternative in Section 6.3;
4. prove (6.5) or the structural no-go theorem;
5. give a quantitative inverse/network-robustness radius;
6. demonstrate fixed frequency and amplitude while moving a proved pulse
   margin, if the positive theorem holds.

### Required falsifiers

- remove transverse recovery damping so multiple canard directions reappear;
- use graph sequences whose RFDE transverse inverse grows with \(N\);
- perturb inside and outside \(\ker\mathfrak M_N\);
- preserve the projected delay measure while changing transverse layers;
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
- **general-network response target** for Sections 2--4;
- **physical maximal-canard root** only after Paper III's outer-history proof;
- **pulse-onset separator** only after (5.1)--(5.2);
- **pulse-safety controllability** only after (6.5) and its error enclosure.

Failure of a later gate narrows the new theorem or changes the actuator/model.
It does not invalidate the JNS base theorem and must not be hidden by
renaming an output event as a geometric canard.
