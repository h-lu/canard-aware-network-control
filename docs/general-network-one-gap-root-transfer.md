# One-gap transfer of selected complete-history roots in finite RFDE networks

Status: **the graph-first implication in Theorem 5.1 is a proved conditional
synthesis of existing abstract results; its joint \((\nu,\mathcal R)\)
second-derivative and simple-root assumptions remain explicit additional
hypotheses.**  A
synchrony-quotient-free, shared-resource Dobrushin instance is already proved
for its declared fixed-support structural direction.  The corresponding open
general-topology neighborhood of the dual-state scaffold is **not** proved:
its full RFDE transverse trace/dichotomy, selected-trace continuation, and
uniform inverse estimates remain open.  No theorem in this note identifies a
selected local root with physical pulse onset.

This note fixes the minimum theorem that genuinely promotes the two-module
complete-history result.  An arbitrary-size rank-one lift is a useful
reference family, but it is not itself a general-network theorem.  Generality
means that every finite network satisfying the stated one-critical-mode,
history-regularity, transverse-hyperbolicity, trace, and simple-root
hypotheses is covered.  Scalability additionally requires one set of
constants for all admitted network sizes.

## 1. Object and quantifiers

Fix a delay horizon \(\Theta_*>0\), \(1<p<\infty\), and a set
\(\mathfrak N\) of finite network sizes.  For each \(N\in\mathfrak N\), let

\[
 U=\mathbb R^2,\qquad X_N=U\oplus E_N,
 \qquad
 \|(u,h)\|_{X_N}=\max\{|u|,\|h\|_{E_N}\},
 \tag{1.1}
\]

where \(U\) is the fold plane and \(E_N\) is the network-transverse stable
fiber.  The phrase **one critical mode** means one scalar canard defect after
phase fixing.  At the singular fold the corresponding generalized center is
a length-two Jordan chain, not a one-dimensional center space.

The continuous RFDE semiflow acts on

\[
 H_N^0=C([-\Theta_*,0],X_N),
 \tag{1.2}
\]

and classical compatible histories lie in

\[
 \mathcal M_N=
 \{\phi\in C^1([-\Theta_*,0],X_N):
   \phi'(0)=\mathcal F_N(\phi)\}.
 \tag{1.3}
\]

Parameter derivatives and complete-history matching are taken on strong
spaces.  A fixed-interval Lin realization may use

\[
\begin{aligned}
 \mathscr X_N^{\mathrm{Lin}}={}&
 W^{2,p}(I_-^{\Theta_*},X_N)
 \times W^{2,p}(I_+^{\Theta_*},X_N)
 \times A_{-,N}\times A_{+,N}\times\mathbb R^2,\\
 \mathscr Y_N^{\mathrm{Lin}}={}&
 L^p(I_-,X_N)\times L^p(I_+,X_N)
 \times Z_{-,N}\times Z_{+,N}\times\mathbb R
 \times W^{1,p}([-\Theta_*,0],X_N),
 \tag{1.4}
\end{aligned}
\]

where the extended orbit intervals include the complete delay window.  The
last factor of \(\mathscr Y_N^{\mathrm{Lin}}\) is the **complete** history
jump.  The graph--trace construction uses its separate scales
\(\mathcal W_N^2\hookrightarrow\mathcal W_N^1\hookrightarrow\mathcal W_N^0\)
and
\(\mathcal V_N^2\hookrightarrow\mathcal V_N^1\hookrightarrow\mathcal V_N^0\);
these are not identified with the Lin domain and codomain.  Current-state,
module-average, or observable-only matching is not an RFDE connection.
The trace-coordinate spaces \(A_{\pm,N}\) and residual spaces
\(Z_{\pm,N}\) must come from a proved history-space Fredholm trace pair;
endpoint coordinates may not be counted once in the chart and again in the
codomain.  A finite current-state defect count is only a diagnostic, not the
RFDE index asserted below.

For each fixed \(0<\delta\le\delta_0\), a uniformly conditioned fold chart
and a recentering of the perturbed fold put the network into

\[
\begin{aligned}
 u'={}&q_0(u;\nu)
 +\delta F_N(u,h,\mathscr D_Nx_s;
             \delta,\nu,\mathcal R_N),\\
 \delta h'={}&A_Nh
 +\delta G_N(u,h,\mathscr D_Nx_s;
             \delta,\nu,\mathcal R_N),
 \tag{1.5}
\end{aligned}
\]

where \(u=(X,Y)\in U\), \(h\in E_N\), and \(\mathscr D_N\) retains the
complete scaled delay.  The theorem below is uniform in \(N\).  Uniformity
as \(\delta\to0\) is claimed only after a declared normalization of the gap
and uniform estimates in the resulting \(\delta\)-wedge are supplied.

## 2. Structural residual and the strong operator norm

All physical data are first pulled back by the uniformly conditioned fold
and critical/transverse coordinates in (1.5).  On that fixed splitting, a
raw structural residual may contain

\[
 \mathcal R_N=
 (\Delta A_N,\Delta\mathbb B_N,
  \Delta F_N,\Delta G_N,\Delta\vartheta_N,\Delta p_N),
 \tag{2.1}
\]

where \(\mathbb B_N\) is an operator-valued delay measure, \(\vartheta_N\)
is a finite vector of moving delay locations when admitted, and \(p_N\)
denotes node or local-field heterogeneity.  Use a dimension-controlled raw
norm of the form

\[
\begin{aligned}
 \|\mathcal R_N\|_{\mathrm{net},N}
 :={}&\|\Delta A_N\|_{\mathcal L(E_N)}
 +\|\Delta\mathbb B_N\|_{\mathrm{TV},N}\\
 &+\|(\Delta F_N,\Delta G_N)\|_{C^{12}_{\mathrm{op}},N}
 +|\Delta\vartheta_N|
 +\|\Delta p_N\|_{\mathrm{loc},N}.
 \tag{2.2}
\end{aligned}
\]

The norms in (2.2) are operator and multilinear norms induced by (1.1), not
uncontrolled Euclidean or Frobenius norms.  If endpoint preparation is itself
allowed to vary independently rather than being derived from one fixed
canonical selection rule, its trace-scale \(C^2\) norm must be added to
(2.2), and the resulting root is explicitly preparation indexed.
For the graph and its first two structural responses, the data map must in
addition be \(C_\nu^1C_{\mathcal R}^2\) on a larger open parameter cylinder,
with all corresponding total-variation and operator-jet bounds uniform in
\(N\).  Pointwise smallness in (2.2) alone gives none of these derivatives.
The quadratic root estimate in Theorem 5.1 has one further requirement: the
*gap itself* must be jointly \(C^2\) in \((\nu,\mathcal R)\).  If that joint
regularity is to be derived from the transformed data rather than imposed
directly on the gap, the data/trace construction must also supply the pure
\(\nu\nu\) derivative and the mixed derivatives used in (5.3).  The
abstract special-flow theorem, whose rectangular parameter range is only
\(C_\nu^1C_{\mathcal R}^2\), does not supply the missing pure
\(\nu\nu\) derivative.

The term \(\Delta A_N\) is admissible only under one of the following
conditions:

1. it is a weak bounded term that can be placed in \(G_N\); or
2. a separate model-fitting lemma proves uniform \(C^2\) semigroup or
   resolvent dependence for the order-one family \(A_N(\mathcal R_N)\).

The existing abstract special-flow theorem keeps \(A_N\) fixed.  An
order-one change of instantaneous topology cannot be hidden in (1.5)
without the second lemma.

If the operator-valued measure depends on \((\nu,\mathcal R)\), total
variation of its derivatives is not by itself sufficient on the unbounded
affine critical history.  With \(\iota_Uu=(u,0)\), require the balanced-anchor
identity

\[
 \left(
 \partial_\nu^iD_{\mathcal R}^e\mathbb B_{N,\nu,\mathcal R}
 [R_1,\ldots,R_e]
 \right)([-\Theta_*,0])\iota_U=0,
 \quad 1\le i+e,\quad i\le1,\quad e\le2,
 \tag{2.2a}
\]

or prove a uniform bound for the actual differentiated transformed-data
composite.  A fixed measure satisfies (2.2a) automatically.  Fixed support
alone does not imply (2.2a) for a parameter-dependent measure.
The index range in (2.2a) is the one used by the
\(C_\nu^1C_{\mathcal R}^2\) graph theorem.  If the joint \(C^2\) root
regularity is derived through a parameter-dependent measure, the analogous
anchor or direct-composite bound is also required for the pure
\(\partial_{\nu\nu}\) derivative.  This extra bound is automatic in the
fixed-measure Dobrushin instance of Section 7.

Let \(\mathfrak F_N\) denote either the selected trace residual or the full
Lin residual on the declared scale.  The residual that enters the range
equation is

\[
 \eta_N^{\mathrm{op}}
 =\max_{0\le j\le2}
 \|\mathfrak F_N(\cdot,\cdot,\mathcal R_N)
   -\mathfrak F_N(\cdot,\cdot,0)\|_{\mathrm{op},j},
 \tag{2.3}
\]

where the \(j\)-th norm is taken between the appropriate response levels,
so one derivative of loss is visible rather than suppressed by a false
same-space \(C^2\) assertion.  A model-fitting theorem must prove

\[
 \boxed{
 \eta_N^{\mathrm{op}}
 \le C_{\mathrm{fit}}
       \|\mathcal R_N\|_{\mathrm{net},N}}
 \tag{2.4}
\]

with \(C_{\mathrm{fit}}\) independent of \(N\).

### Fixed support and moving point delays

For fixed-support measure perturbations, the correct bound is operator total
variation.  If an atom moves, then

\[
 \|\delta_{-\vartheta}-\delta_{-\vartheta_0}\|_{\mathrm{TV}}=2
 \qquad(\vartheta\ne\vartheta_0),
 \tag{2.5}
\]

and moving evaluation is not differentiable in the ordinary operator norm on
\(C^0\).  Thus \(|\Delta\vartheta_N|\) is included in (2.2) only if a
separate strong-space composition result proves the required first and
second derivatives, for example

\[
 W^{2,p}(I^{\Theta_*},X_N)\ni x
 \longmapsto x(\,\cdot-\vartheta\,)
 \in L^p(I,X_N).
 \tag{2.6}
\]

Without that result, the theorem is restricted to fixed delay support.

## 3. Uniform transverse hypotheses

The reference family has uniformly conditioned critical and transverse
projections and a stable generator satisfying

\[
 \|e^{A_Nt}\|_{\mathcal L(E_N)}
 \le M_Ae^{-\kappa_At},
 \qquad t\ge0,\quad N\in\mathfrak N,
 \tag{3.1}
\]

for common \(M_A\ge1\) and \(\kappa_A>0\).  A graph spectral gap may verify
(3.1) for reversible or normal graphs, but is not a replacement for (3.1)
in a directed nonnormal family.

For a full Lin realization, the transverse variational equations along the
selected attracting and repelling pieces must additionally have compatible
history-space trace bundles.  Their finite-interval Green operators satisfy

\[
 \|\mathcal G_{\perp,N}\|
 \le G_\perp(\delta),
 \tag{3.2}
\]

uniformly in \(N\) and block multiplicity.  The bundles must form a
Fredholm pair of index zero and give zero kernel and zero cokernel in every
network-transverse block.  The RFDE semiflow is not inverted on all of
\(H_N^0\); the repelling trace is constructed on a backward-extendible
center or center-unstable solution manifold.

The current-state eigenvalues \(-D_v,-D_w\) of the dual-state scaffold are
only algebraic input to (3.1)--(3.2).  They do not prove the RFDE dichotomy,
the trace bundles, or the uniform Green bound.

## 4. Admissible one-gap packages

There are two sufficient constructions.  The main theorem uses the scalar
gap produced by either one; it does not identify the two constructions as
formally equivalent in settings where both have not been built.

### 4.1 Graph-first package

The special-flow transform supplies a unique invariant complete-history
graph

\[
 h=H_{N,\delta,\nu,\mathcal R_N}(u)
 \tag{4.1}
\]

and an injective history embedding

\[
 \iota_{N,\delta,\nu,\mathcal R_N}(u)(\sigma)
 =\bigl(\Phi_Q^\sigma u,
 H_{N,\delta,\nu,\mathcal R_N}(\Phi_Q^\sigma u)\bigr),
 \quad -\Theta_*\le\sigma\le0.
 \tag{4.2}
\]

An admissible trace problem then has levelwise linear inverses

\[
 \|(T_{W,N}^j)^{-1}\|\le K_{\mathrm{tr}},
 \qquad j=0,1,
 \tag{4.3}
\]

and controlled second difference quotients, endpoint maps, phase, and
complete-history matcher.  The graph--trace construction yields a scalar
gap \(d_N(\nu,\mathcal R_N)\) with uniformly bounded first and second
Fréchet responses.  Equality of retained planar states at zero gap,
planar uniqueness, and injectivity of (4.2) must imply equality of the two
retained complete histories.

This is the primary one-critical-mode route.  It does not require a full
\(2N\)-state Lin boundary-value problem merely to slave a uniformly stable
fiber.  It does require a complete prepared field \(q_0\), the uniform
\(C^{12}\) and affine-anchor hypotheses, and a preparation that agrees with
the physical RFDE on every retained point and its entire delay-support
backtrack.  The graph theorem alone neither selects the one-sided traces nor
proves a root.

### 4.2 Full Lin--Fredholm package

Alternatively, let \(\mathfrak F_N(z_N,\nu,\mathcal R_N)\) contain both
orbit equations, compatible complete-history endpoint maps, exactly one
phase condition, and the full history jump.  At the reference root put

\[
 L_N=D_{z_N}\mathfrak F_N(z_{0,N},\nu_{0,N},0).
 \tag{4.4}
\]

Thus
\(L_N:\mathscr X_N^{\mathrm{Lin}}\to
\mathscr Y_N^{\mathrm{Lin}}\).

Assume first that the RFDE solution manifold, orbit map, endpoint maps,
phase, and jump give a \(C^2\) residual on the declared strong spaces,
including the stated parameter dependence.  Then assume

\[
 \ker L_N=\{0\},\qquad
 \dim\operatorname{coker}L_N=1,
 \qquad \operatorname{ind}L_N=-1.
 \tag{4.5}
\]

Assume that one can choose
\(\psi_N\in(\mathscr Y_N^{\mathrm{Lin}})^*\) and
\(e_N\in\mathscr Y_N^{\mathrm{Lin}}\) with

\[
 \operatorname{Range}L_N=\ker\psi_N,
 \qquad \|\psi_N\|=1,
 \qquad \psi_N(e_N)=1,
 \tag{4.6}
\]

where \(e_N\) has only a complete-history-jump component, and require

\[
 \sup_{N\in\mathfrak N}\|e_N\|_{\mathscr Y_N^{\mathrm{Lin}}}
 \le C_e<\infty.
 \tag{4.6a}
\]

The existence of such a jump-supported column is not a consequence of
\(\dim\operatorname{coker}L_N=1\): the cokernel functional must not
annihilate the jump subspace, and a uniformly bounded normalization must be
proved.  Next require

\[
 \widehat L_N(\zeta,\gamma)
 =L_N\zeta-\gamma e_N
 \tag{4.7}
\]

to be an isomorphism satisfying

\[
 \|\widehat L_N^{-1}\|
 \le G_{\mathrm{Lin}}(\delta)
 \tag{4.8}
\]

uniformly in \(N\).  The conditional direct-sum criterion in the
full-network specification records a common bound for the range inverse;
(4.6a) and the augmented bound (4.8) additionally control the chosen jump
column and its cokernel normalization, so they are stated here as separate
hypotheses.  Solving

\[
 \mathfrak F_N(z_N(\nu,\mathcal R_N),
               \nu,\mathcal R_N)
 =d_N(\nu,\mathcal R_N)e_N
 \tag{4.9}
\]

then defines the strict Lin gap.  Since every other residual has been solved,

\[
 d_N=0\quad\Longleftrightarrow\quad
 \text{the complete history jump vanishes}.
 \tag{4.10}
\]

Calling this zero an intersection of selected slow histories additionally
requires the endpoint zero-fiber implication.  Calling it physical pulse
onset requires a further outer-selection and global-return theorem.

## 5. Uniform one-gap root-transfer theorem

### Theorem 5.1 -- structural transfer and quantitative remainder

For each \(N\in\mathfrak N\), suppose Sections 1--3 and one of the packages
in Section 4 produce a normalized gap

\[
 \widetilde d_N:
 [\nu_{0,N}-r_\nu,\nu_{0,N}+r_\nu]
 \times\overline B_{\mathfrak R_N}(0,r_{\mathcal R})
 \longrightarrow\mathbb R.
 \tag{5.1}
\]

The radii \(r_\nu\), \(r_{\mathcal R}\), and the range-solve radius
\(\eta_*\) below are common to the admitted \(N\)-family; for a fixed-
\(\delta\) theorem they may depend on \(\delta\).

Assume this map extends \(C^2\) to an open neighborhood of the whole closed
cylinder in (5.1), jointly in \((\nu,\mathcal R)\), including the
\(\nu\nu\) and \(\nu\mathcal R\) derivatives.  The abstract graph--trace
theorem supplies the first and second **structural** derivatives; it does not
by itself supply this additional root regularity or the simple-root slope.

Assume, with constants independent of \(N\),

\[
 \widetilde d_N(\nu_{0,N},0)=0,
 \qquad
 a_N:=\partial_\nu\widetilde d_N(\nu_{0,N},0),
 \qquad |a_N|\ge m_*>0,
 \tag{5.2}
\]

\[
 \sup_{\|\mathcal R\|\le r_{\mathcal R}}
 \|D_{\mathcal R}\widetilde d_N
       (\nu_{0,N},\mathcal R)\|
 \le B_*,
 \qquad
 \sup_{\substack{|\nu-\nu_{0,N}|\le r_\nu\\
                  \|\mathcal R\|\le r_{\mathcal R}}}
 \|D^2\widetilde d_N(\nu,\mathcal R)\|\le M_*.
 \tag{5.3}
\]

The Hessian in (5.3) uses the sum norm
\(|\nu-\nu_{0,N}|+\|\mathcal R\|_{\mathrm{net},N}\).  Define

\[
 \rho_{\mathrm{fit}}=
 \begin{cases}
  \eta_*/C_{\mathrm{fit}},&C_{\mathrm{fit}}>0,\\
  +\infty,&C_{\mathrm{fit}}=0,
 \end{cases}
 \tag{5.3a}
\]

where \(\eta_*\) is the common radius on which the graph/trace or Lin range
solve is valid.  Set

\[
 \rho_*=
 \min\left\{
 r_{\mathcal R},
 \frac{m_*r_\nu}{2B_*},
 \frac{m_*}{2M_*(1+2B_*/m_*)},
 \rho_{\mathrm{fit}}
 \right\},
 \tag{5.4}
\]

where a quotient involving \(B_*=0\) or \(M_*=0\) is interpreted as
\(+\infty\).  Then, for every

\[
 r=\|\mathcal R_N\|_{\mathrm{net},N}\le\rho_*,
 \tag{5.5}
\]

there is exactly one root \(\nu_{c,N}(\mathcal R_N)\) in

\[
 |\nu-\nu_{0,N}|
 \le\frac{2B_*}{m_*}r.
 \tag{5.6}
\]

If

\[
 \ell_N=D_{\mathcal R}\widetilde d_N(\nu_{0,N},0),
 \tag{5.7}
\]

then

\[
 \boxed{
 \left|
 \nu_{c,N}(\mathcal R_N)-\nu_{0,N}
 +\frac{\ell_N[\mathcal R_N]}{a_N}
 \right|
 \le
 \frac{M_*}{2m_*}
 \left(1+\frac{2B_*}{m_*}\right)^2r^2.}
 \tag{5.8}
\]

All constants in (5.3a)--(5.8) are independent of \(N\).  Uniqueness is
asserted only in the interval (5.6), not throughout the full cylinder and
not globally.  If \(B_*=0\), the fundamental theorem of calculus gives
\(\widetilde d_N(\nu_{0,N},\mathcal R)=0\) on the admitted residual ball;
the interval (5.6) is then the singleton \(\{\nu_{0,N}\}\), consistently
with the quantitative root lemma.  If the selected pieces satisfy the
zero-fiber implication, the root is a selected local
geometric canard root.  Without it, the conclusion is a selected
complete-history connection.  Neither conclusion is a physical pulse
threshold without an outer-history and event-equivalence theorem.

**Proof.**  The dimension-uniform special-flow theorem supplies the graph
and its first and second structural responses.  The Banach-scale
graph--trace theorem transfers those responses to \(\widetilde d_N\), or
the augmented Lin implicit-function theorem supplies the same scalar gap
from (4.5)--(4.9).  The bounds (5.2)--(5.3) place this gap under the
quantitative scalar root lemma.  Together with the separate fitting
condition (2.4), that lemma gives (5.4), contraction on (5.6), uniqueness
there, and (5.8).  More explicitly, its contraction proof is run with
\(|a_N|\ge m_*\): on the possibly larger uniform interval (5.6),

\[
 \frac{M_*}{|a_N|}
 \left(1+\frac{2B_*}{m_*}\right)r\le\frac12,
\]

so replacing the exact slope by its common lower bound does not enlarge the
uniqueness claim without control.  The matching interpretation follows
from (4.2) in the graph route or (4.10) in the Lin route.  \(\square\)

### Exact first variation

In the Lin realization, let
\(\widetilde d_N=s_{\delta,N}^{-1}d_N\) denote the normalization used in
(5.1), where the positive scale \(s_{\delta,N}\) is fixed independently of
\((\nu,\mathcal R)\).  Then

\[
 \ell_N[\mathcal R_N]
 =s_{\delta,N}^{-1}\psi_ND_{\mathcal R}\mathfrak F_N
 (z_{0,N},\nu_{0,N},0)[\mathcal R_N].
 \tag{5.9}
\]

The right side includes dynamic, entry, exit, phase, moving-hit, and history
jump derivatives.  It is not generally equal to a static network pairing
\(\ell_N^\top\Delta B_Nr_N\).

In graph-first coordinates the exact Schur form is the following, with
\(\beta_N,\widehat m_N,m_{\perp,N}\) understood as derivatives of the
same normalized matcher:

\[
\begin{aligned}
 \ell_N[\mathcal R]
 ={}&\beta_N[\mathcal R]
 -\widehat m_N\mathsf S_N^{-1}g_{c,N}[\mathcal R]\\
 &+\left(
 \widehat m_N\mathsf S_N^{-1}\mathsf B_N-m_{\perp,N}
 \right)
 \mathsf D_N^{-1}g_{\perp,N}[\mathcal R].
 \tag{5.10}
\end{aligned}
\]

Thus projection-invisible forcing may enter the transverse range solve and
return to the critical gap.  The theorem does not assert that (5.9) or
(5.10) is nonzero.  If \(\ell_N\ne0\) as a continuous functional on an
admissible residual space, its kernel is a closed codimension-one subspace;
proving one nonzero witness is model-specific.

If the physical parameter is \(a=a_f+\delta^2\nu\), multiply (5.6) and
(5.8) by \(\delta^2\).  A special law

\[
 a_{c,N}(\mathcal R)-a_{c,N}(0)
 =\delta^3\mathfrak M_N[\mathcal R]
 +O(\delta^4\|\mathcal R\|
     +\delta^3\|\mathcal R\|^2)
 \tag{5.11}
\]

requires separate fold-preserving and projection-neutral cancellations,
anisotropic jet bounds, endpoint terms, and a nonzero witness.  It is not a
consequence of Theorem 5.1 alone.

## 6. Quantitative corollary for an exact two-module lift

### Corollary 6.1 -- conditional open-neighborhood promotion

Suppose that, for every \(N=n_1+n_2\), an exact block lift of the two-module
reference satisfies

\[
 \widetilde d_N(\nu,0)=\widetilde d_2(\nu,0),
 \qquad \nu_{0,N}=\nu_{c,2},
 \tag{6.1}
\]

and suppose the **full** hypotheses of Theorem 5.1 have been verified for a
Banach ball of topology-breaking residuals.  Then every admissible residual
in that ball has one root and

\[
 \boxed{
 \nu_{c,N}(\mathcal R_N)-\nu_{c,2}
 =-\frac{\ell_N[\mathcal R_N]}{a_2}
 +\mathcal E_N,}
 \tag{6.2}
\]

where

\[
 |\mathcal E_N|
 \le
 \frac{M_*}{2m_*}
 \left(1+\frac{2B_*}{m_*}\right)^2
 \|\mathcal R_N\|_{\mathrm{net},N}^2
 \tag{6.3}
\]

uniformly in \(N\).

The admissible ball may contain non-rank-one, non-equitable, directed,
nonnormal, fixed-support heterogeneous network operators.  Nonnormal members
are admitted because they satisfy the actual semigroup and trace estimates,
not merely because their adjacency eigenvalues appear separated.

**Current status.**  Equations (6.2)--(6.3) are a conditional corollary for
the dual-state scaffold, not a completed application.  The exact arbitrary-
\(N\) lift, its invariant graph, its canonical quotient root, and specified
non-equitable directions are proved.  The following promotion hypotheses
remain **OPEN** for an arbitrary topology-breaking neighborhood:

1. the full RFDE transverse dichotomy or an equivalent uniform selected-
   trace continuation;
2. compatible complete-history endpoint bundles;
3. a uniform full-network trace or augmented Lin inverse;
4. the zero-fiber implication if a geometric slow-history intersection is
   claimed;
5. uniform \(C^2\) response for arbitrary operator-TV directions;
6. semigroup/resolvent parameter dependence if the order-one scaffold
   generator itself varies.

No numerical value is assigned to \(\rho_*\), \(m_*\), \(B_*\), \(M_*\),
\(G_\perp\), or \(G_{\mathrm{Lin}}\) for this missing dual-scaffold
application.

## 7. A proved synchrony-quotient-free general-topology instance

The shared-resource heterogeneous-curvature theorem gives a separate,
already proved graph-first instance.  It quantifies over finite
row-stochastic directed Markov matrices \(P_N\) with strictly positive stationary vector
\(\pi_N\) and one common Dobrushin margin

\[
 \tau(P_N)\le1-\gamma,
 \tag{7.1}
\]

the norm

\[
 \|x\|_N=|\pi_N^\top x|+\operatorname{osc}(x)
 \tag{7.2}
\]

and

\[
 E_N=\ker\pi_N^\top,
 \qquad A_N=D(P_N-I)|_{E_N},
 \tag{7.2a}
\]

give the uniform stable estimates

\[
 \|e^{A_Nt}\|_{E_N\to E_N}
 \le e^{-D\gamma t},
 \qquad
 \|A_N^{-1}\|_{E_N\to E_N}
 \le(D\gamma)^{-1}.
 \tag{7.3}
\]

With one shared recovery resource, a fixed number of delay atoms, the common
curvature normalization

\[
 0<c_-\le c_{i,N}\le c_+,
 \qquad \pi_N^\top c_N=\alpha>0,
 \tag{7.3a}
\]

uniform operator-TV bounds, and the atomwise full-row-neutral direction

\[
 \pi_N^\top R_{k,N}=0,
 \tag{7.4}
\]

and the first structural delay moment

\[
 \dot M_{1,N}=\sum_{k=0}^m\theta_kR_{k,N},
 \tag{7.4a}
\]

the cited theorem constructs the exact invariant history graph, canonical
one-sided traces, a unique preparation-indexed complete-history root, and
the response

\[
\begin{aligned}
 \mu_{c,N}(\delta,\zeta)-\mu_{c,N}(\delta,0)
 ={}&\mathscr C_N\delta^3\zeta
 +O(\delta^4|\zeta|+\delta^3\zeta^2),\\
 \mathscr C_N={}&-
 \frac{K}{2\alpha^2}
 \pi_N^\top\operatorname{diag}(c_N)
 A_N^{-1}P_{\perp,N}\dot M_{1,N}\mathbf1,
 \tag{7.5}
\end{aligned}
\]

with one remainder constant for all \(N\).  Under the stated nondegeneracy,
\(\inf_N|\mathscr C_N|>0\).  This family need not possess a nontrivial
synchrony quotient and therefore is a genuine general-topology instance of
the one-critical-mode mechanism **within the uniformly one-step
Dobrushin-mixing class**.  The theorem varies the fixed-support delayed layer
in the direction \((R_{k,N})\); it quantifies over the admissible base
matrices \(P_N\), but does not prove differentiability of the root with
respect to arbitrary changes of \(P_N\).

The quantifier here is familywise and preparation indexed.  After fixing
the common Dobrushin, curvature, operator-TV, delay-support, parameter-box,
and preparation-jet bounds, one obtains common
\(\delta_0,\zeta_0,c_0,C>0\) that work for every admitted \(N\).  The exact
root may depend on the \(N\)-th canonical preparation; the coefficient in
(7.5) and its uniform remainder bound do not depend on that choice within
the declared bounded preparation class.  The accompanying SymPy source and
tests verify the finite-dimensional projector, Poisson-inverse, coefficient,
positivity, and no-quotient witness identities only.  They do not
numerically construct the invariant graph or one-sided traces.  Those
analytic objects and the uniform remainder are supplied by the model-fitting
lemma, the dimension-uniform logarithmic graph theorem, and the phase-normal
one-sided Green/trace theorem used in the proof of the cited result.

The proved scope of (7.5) is nevertheless specific:

- shared slow resource rather than the dual-state scaffold;
- fixed delay support;
- a canonical prepared-tail selection;
- a declared full-row-neutral structural direction;
- a common Dobrushin gap and uniform operator-TV bounds.

It does not prove a root response for every possible topology direction,
closing mixing gaps, moving delay atoms, or a physical outer selection.  In
particular, (7.1) is a substantial one-step mixing hypothesis and excludes
many sparse directed graph families; “general topology” here does not mean
arbitrary topology.

## 7A. A concrete complete-line transverse block for the leaky model

The autonomous leaky-recovery model supplies a second, logically different
finite-network instance.  It does not yet supply the scalar canard root, but
it closes the complete-line transverse inverse required by the canonical
synchronized Lin construction.

Fix the leaky coefficients

\[
 \varepsilon=\frac15,\quad a=\frac14,\quad
 \kappa_1=\frac1{250},\quad \kappa_3=\frac1{200},
 \quad (\tau_0,\tau_1)=(4\sqrt5,5\sqrt5),
 \qquad r=5\sqrt5.                                      \tag{7A.0}
\]

For every finite network, let \(Q,B_0,B_1\) satisfy

\[
 Q\mathbf1=\mathbf1,\quad \pi^TQ=\pi^T,\quad
 \tau(Q)\le\frac12,
 \qquad
 B_j\mathbf1=\frac12\mathbf1,\quad
 \pi^TB_j=\frac12\pi^T,                                 \tag{7A.1}
\]

with \(Q,B_j\ge0\) and strictly positive \(\pi\).  The collective line and
\(\ker\pi^T\) are invariant for every current and delayed variational block;
simultaneous diagonalization is not assumed.  On the complex transverse
space use

\[
 m(x,y)=\max\{\operatorname{diam}x,
                   3\operatorname{diam}y\},
 \qquad
 \|\phi\|_{1/10}=
 \sup_{-r\le\theta\le0}e^{\theta/10}m(\phi(\theta)).     \tag{7A.2}
\]

For any complete synchronous trajectory \(V:\mathbb R\to\mathbb R\)
satisfying

\[
 \sup_{t\in\mathbb R}|V(t)-1|\le\frac52,               \tag{7A.3}
\]

the directed Halanay constants give

\[
 \alpha-\frac1{10}-\beta e^{r/10}
 >0.00766645053564.                                     \tag{7A.4}
\]

Hence the transverse evolution family satisfies

\[
 \|U_{\perp,N}(t,s)\|_{1/10}
 \le e^{-(t-s)/10},\qquad t\ge s,                       \tag{7A.5}
\]

with constant one, independently of \(N\) and of the admitted topology.
For every bounded complete transverse forcing, forward zero-history
solutions begun at \(S\) form a Cauchy family as \(S\to-\infty\).  This
constructs the unique bounded complete forced solution without inverting an
RFDE semiflow backward and gives the causal Green bound

\[
 \boxed{\|G_{\perp,N}\|\le10.}                          \tag{7A.6}
\]

On its classical graph domain the transverse differential operator is
therefore an isomorphism.  In the canonical synchronized Lin realization,
where endpoint traces, phase, cokernel normalization, gap, parameter forcing,
and inhomogeneity all act only on the collective block, one has the exact
direct sum

\[
 \mathcal L_N=\mathcal L_\parallel\oplus
                    \mathcal L_{\perp,N}.                \tag{7A.7}
\]

It follows that the full operator has the same Fredholm index, kernel and
cokernel dimensions as the scalar block.  Extending the normalized scalar
cokernel functional by zero gives

\[
 d_N(\nu)=d(\nu).                                       \tag{7A.8}
\]

Thus a separately proved simple scalar complete-history canard root transfers
with exactly the same location, slope, and orientation to every network in
(7A.1).  Unlike the abstract implication in Section 4.2, the transverse
Green hypothesis in this canonical leaky realization is now verified with
an explicit dimension-independent constant.

The remaining condition is scalar, not a hidden network estimate: the leaky
RFDE complete-history connection, its phase-fixed Fredholm realization, and
the nonzero scalar gap slope have not yet been proved.  Equations
(7A.5)--(7A.8) also do not treat independently chosen noncollective traces,
asynchronous forcing, nonlinear persistence away from synchrony, or a
topology-uniform nonlinear neighborhood.  The proof and source-bound record
are in
[the complete-line transverse inverse](leaky-dobrushin-complete-line-inverse.md).

## 7B. A nonlinear stripwise synchronization theorem

The leaky Dobrushin constants also control the true nonlinear network, not
only its variational equation.  For a real node vector set

\[
 \operatorname{osc}z=\max_i z_i-\min_i z_i,
 \qquad M=\max\{\operatorname{osc}v,3\operatorname{osc}w\}.
\]

The instantaneous scalar map has global one-sided slope

\[
 \frac{d}{ds}\left(s-\frac{s^3}{3}
 -\varepsilon\kappa_1s-\varepsilon\kappa_3(s-1)^3\right)
 \le1-\varepsilon\kappa_1=0.9992,
\]

the current cubic term is dissipative, and on
\(|v_i-1|\le5/2\) the delayed cubic has Lipschitz constant at most
\(75/4\).  The nonlinear maximum--minimum Dini calculation therefore gives
the same Halanay inequality and the same strict residual (7A.4).  Hence,
for every real network solution that remains in the declared strip,

\[
 M(t)\le e^{-(t-t_0)/10}
 \sup_{t_0-r\le s\le t_0}M(s).                         \tag{7B.1}
\]

The constant and rate are uniform in every finite \(N\) and every admitted
topology.  This is a nonlinear synchronization theorem: no transverse
pattern can persist inside the strip.  It is stronger than the linear
Green-block statement but weaker than a topology-uniform nonlinear basin.
All nodes may still leave the strip together through the uncontrolled
collective component.  Consequently (7B.1) does not yet prove asynchronous
canard persistence or an asynchronous pulse threshold.

The exact proof and source-bound claim ledger are in
[the nonlinear synchronization certificate](leaky-dobrushin-nonlinear-synchronization.md).

## 8. General topology as an open class

For fixed \(N\), augmented invertibility and a simple root are open under
sufficiently small bounded perturbations on fixed domain and codomain.
Exponential stability is likewise robust in the bounded generator/data
topology for which the required roughness estimate has been proved.  Thus,
**after** a model-fitting map with these properties is supplied, Theorem 5.1
covers a relative open neighborhood in the Banach manifold determined by the
row-balance, fold, and fixed-support constraints.  Such a neighborhood can
contain small changes on arbitrarily selected edges and can destroy rank-one
structure and equitability.  This paragraph does not supply the missing
order-one generator-response lemma identified after (2.2).

For a scalable theorem, this neighborhood has one common radius only if

\[
 K_{\mathrm{pr}},\ M_A,\ \kappa_A^{-1},\ B_{\mathrm{TV}},\
 K_{12},\ K_{\mathrm{tr}},\ G_\perp(\delta),\
 C_e,\ G_{\mathrm{Lin}}(\delta),\ m_*^{-1},\ B_*,\ M_*,\
 C_{\mathrm{fit}},\
 r_\nu^{-1},\ r_{\mathcal R}^{-1},\ \eta_*^{-1}
 \tag{8.1}
\]

have common bounds.  If a graph gap closes, transient growth diverges, the
stationary/critical projections become ill-conditioned, or the trace inverse
grows with \(N\), Theorem 5.1 remains a possible fixed-\(N\) result but its
dimension-uniform conclusion is lost.

A Dobrushin family is one verified nonempty class for the declared
shared-resource model and structural direction.  Reversible or normal
families with an actual uniform semigroup estimate provide another
**candidate** class until their model-specific graph/trace/root package is
proved.  Sparse or directed nonnormal families are not excluded by the
abstract implication, but their RFDE semigroup and trace bounds must be
proved rather than inferred from a static spectral plot.

## 9. Proof-dependency graph

```text
nondegenerate fold recentering + uniformly conditioned projections
                              |
fixed-support TV + anchor ----+-- strong-space moving-delay lemma
                              |
                    uniform model fit (1.5)
                              |
          actual transverse semigroup/dichotomy estimates
                              |
               exact invariant complete-history graph
                              |
        canonical one-sided traces + complete endpoints
                              |
             +----------------+----------------+
             |                                 |
   graph/trace inverse package       full Lin Fredholm package
             |                                 |
             +--------- strict scalar gap -----+
                              |
             C^2 gap bounds + simple-root slope
                    /                         \
      Schur/dynamic-adjoint response       root lemma
                    |                         |
       topology-response functional   unique root + O(r^2)
                    |
        model-specific nonzero witness

complete-history equality
             |
endpoint zero-fiber implication
             |
selected local geometric canard
             |
parameter-coherent outer history + global event equivalence
             |
physical maximal canard / biological pulse onset
```

The last two arrows are not used to prove Theorem 5.1.  They are separate
Paper III hypotheses.

## 10. Existing-result decomposition

The graph-first implication in Theorem 5.1 is not an unsupported future
assertion, but neither is it a theorem that manufactures the missing
model-specific root hypotheses.  Its components and seams are as follows.

1. [The dimension-uniform special-flow theorem](dimension-uniform-special-flow-history-graph.md),
   Theorem 2.1, proves the fixed-tube invariant complete-history graph and
   mixed structural jets under its abstract normal-form hypotheses;
   Corollary 4.1 supplies the logarithmic fold-tube version under its
   additional preparation and transformed-data bounds.
2. [The Banach-scale graph--trace theorem](banach-scale-history-schur-link.md)
   Theorem 5.1 proves the derivative-loss-aware transfer of first and second
   **structural** responses to a complete-history endpoint gap and gives the
   exact Schur formula (5.10) under an admissible trace package.  Its own
   scope explicitly leaves \(\nu\nu\), mixed root bounds, and a uniform
   simple-root slope to the concrete model.
3. [The Schur--Melnikov note](general-network-schur-melnikov-proof.md)
   Lemma 4.1 proves the quantitative scalar root lemma, including the local
   uniqueness interval and the explicit quadratic constant in (5.8).
4. [The lifted two-module model fit](paper-ii-arbitrary-n-blowup-model-fit.md)
   and [selected-root lift](paper-ii-selected-root-lift-and-symmetry-breaking.md)
   prove the exact arbitrary-size quotient root in Theorem 2.1, the specified
   two-parameter non-equitable branch in Theorem 5.2, and the combined
   non-equitable nonzero tangent in Corollary 5.3.  They do not prove the
   open dual-scaffold neighborhood in Corollary 6.1 or an arbitrary
   operator-TV direction.
5. [The heterogeneous-curvature Dobrushin theorem](paper-ii-heterogeneous-curvature-selected-root.md)
   Theorem 4.1 proves the synchrony-quotient-free, preparation-indexed
   instance summarized in Section 7 for its uniformly Dobrushin
   shared-resource class and fixed-support structural direction.  Its
   analytic inputs are the dimension-uniform logarithmic graph theorem and
   [the phase-normal one-sided Green theorem](green-phase-selected-traces.md),
   while the exact source and tests certify only the finite-dimensional
   coefficient and witness algebra.
6. [The full-network Lin specification](full-network-lin-operator.md)
   fixes the correct dual-scaffold domain, codomain, index, and endpoint
   contract.  Its Theorem 6.1 is a conditional direct-sum criterion whose
   assumptions include the still-unproved history-space endpoint,
   Fredholm, transverse-isomorphism, and uniform-inverse hypotheses.
7. [The leaky complete-line transverse theorem](leaky-dobrushin-complete-line-inverse.md)
   proves the transverse-isomorphism part of that direct-sum mechanism for
   the canonical synchronized leaky network, uniformly over its finite
   balanced Dobrushin class.  It leaves the scalar connection, scalar
   Fredholm realization, and scalar simple root as explicit hypotheses.

The older [finite-network promotion specification](scope-and-theorems.md)
is a historical contract.  The active graph-first division of labor is in
[the general-network program](general-network-canard-pulse-control-program.md).

## 11. Claim ledger

| Claim | Status | Authoritative support | Boundary |
|---|---|---|---|
| Abstract dimension-uniform invariant history graph | **PROVED under stated abstract hypotheses** | `dimension-uniform-special-flow-history-graph.md`, Theorem 2.1 and Corollary 4.1 | Requires model fitting, affine-anchor control, and physical-hull preparation for each node class |
| Banach-scale graph/trace/gap structural response and Schur formula | **PROVED under an admissible trace package** | `banach-scale-history-schur-link.md`, Theorem 5.1 | Does not construct a model's traces or supply joint \((\nu,\mathcal R)\) root regularity/simple slope |
| Quantitative unique-root radius and quadratic displacement | **PROVED for a scalar \(C^2\) gap** | `general-network-schur-melnikov-proof.md`, Lemma 4.1 | Constants must be derived for the model |
| Graph-first branch of Theorem 5.1 | **PROVED conditional synthesis** | the preceding three results plus explicit hypotheses (5.1)--(5.3) | Joint root \(C^2\) bounds and simple slope are assumptions, not consequences of Schur algebra |
| Full Lin branch of Theorem 5.1 | **ABSTRACT CONDITIONAL IMPLICATION** | augmented \(C^2\) implicit-function theorem and scalar root lemma | Requires a uniformly bounded jump-supported cokernel column in addition to the Fredholm, endpoint, and inverse hypotheses; no dual-scaffold realization is proved |
| Exact arbitrary-\(N\) rank-one/two-module lifted root | **PROVED** | `paper-ii-selected-root-lift-and-symmetry-breaking.md`, Theorem 2.1 | Exact quotient class, not general topology |
| Specified non-equitable branch and combined tangent for the lift | **PROVED** | same source, Theorem 5.2 and Corollary 5.3 | Does not cover arbitrary operator-TV directions; pure breaker has zero first response |
| Dual-scaffold current-state one-chain/stable-block algebra | **PROVED** | `full-network-lin-operator.md`, Lemma 2.1 | Does not imply an RFDE dichotomy or Lin inverse |
| Dual-scaffold open general-topology neighborhood, Corollary 6.1 | **CONDITIONAL / OPEN** | hypotheses listed after Corollary 6.1 | No numerical \(\rho_*\) or full-history inverse is certified |
| Shared-resource Dobrushin general-topology selected root | **PROVED for the declared uniformly mixing class** | `paper-ii-heterogeneous-curvature-selected-root.md`, Theorem 4.1 | Fixed support, canonical preparation, declared residual direction; not arbitrary topology or arbitrary variation of \(P_N\) |
| Leaky canonical synchronized transverse complete-line inverse | **PROVED for every finite network in the declared balanced Dobrushin class** | `leaky-dobrushin-complete-line-inverse.md`, Sections 1--3 | \(\|G_{\perp,N}\|\le10\); scalar leaky connection/Fredholm root and asynchronous persistence remain open |
| Moving point-delay version | **OPEN** | strong-space requirement (2.6) | Ordinary \(C^0\) operator norm is inadmissible |
| Preparation-independent physical maximal canard | **OPEN** | requires outer selection | A prepared local root is not a physical threshold |
| Biological pulse onset/event equivalence | **OPEN** | requires global channel/separator theorem | No conclusion from Theorem 5.1 alone |

## 12. Naming discipline

The following names are supported:

- **selected complete-history root** for Theorem 5.1 without zero-fiber or
  outer-selection hypotheses;
- **selected local geometric canard root** after the zero-fiber implication;
- **general finite-network one-critical-mode root transfer** only for a
  theorem quantified over every finite network satisfying Sections 1--5;
- **dimension-uniform** only when every constant in (8.1) is uniform in
  \(N\);
- **physical maximal-canard root** or **biological pulse onset** only after
  the outer-history and global event-equivalence arrows in Section 9 are
  proved.

An arbitrary-size rank-one lift must not be described as an arbitrary-
topology theorem.  Conversely, the Dobrushin shared-resource theorem is a
genuine general-topology instance, but it must not be silently relabelled as
a result for the dual-state scaffold.
