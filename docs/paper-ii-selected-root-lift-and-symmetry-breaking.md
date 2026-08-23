# Arbitrary-size selected-history roots and a non-equitable response direction

Status: **proved for the compatible canonical local selection, 2026-08-23.**
This note closes the first model-specific connection/root gate of Paper II
for the unequal two-module lifts. For every pair of positive module sizes,
the equitable lifted network has exactly the same preparation-indexed
selected-history gap and root as the proved two-module model. The equality is
pointwise in the parameters, not only asymptotic, and the root remainder is
uniform in the node count.

The note also proves a genuinely non-equitable first-response result. A
distributed zero-mean layer perturbation has identically zero first derivative
of every relabeling-invariant selected gap. Adding any fixed multiple of this
perturbation to the already proved module-difference direction produces a
non-equitable tangent whose root derivative is nevertheless the known nonzero
two-module coefficient. A uniform quadratic bound is retained for the pure
symmetry-breaking amplitude. No nonzero coefficient is claimed for that pure
zero-mean direction.

Every conclusion here concerns the canonical prepared-tail selection. It is
not an identification with an unspecified physical outer slow history or with
a biological pulse threshold. No file in manuscript/jns is changed.

## 1. Equivariant lift and the necessary preparation convention

Let \(C_1,C_2\) have sizes \(n_1,n_2\geq1\), put \(N=n_1+n_2\), and use the
replication and averaging maps

\[
 S:\mathbb R^2\longrightarrow\mathbb R^N,
 \qquad
 R:\mathbb R^N\longrightarrow\mathbb R^2,
 \qquad RS=I_2
 \tag{1.1}
\]

from [the lifted class](paper-ii-lifted-two-module-class.md). Let

\[
 \Gamma_N=\mathfrak S(C_1)\times\mathfrak S(C_2)
 \tag{1.2}
\]

act on voltage, recovery, and history coordinates by simultaneous relabeling.
Then

\[
 \operatorname {Fix}(\Gamma_N)=S\mathbb R^2,
 \qquad
 \frac1{|\Gamma_N|}\sum_{P\in\Gamma_N}P=Q:=SR.
 \tag{1.3}
\]

At zero non-equitable residual, the nodewise cubic field, recovery scaffold,
and layers \(SC_k^\eta R\) commute with this action. Their restriction to the
fixed space is the two-module RFDE exactly.

The finite-\(\delta\) canonical root is indexed by a preparation datum, so an
exact lift theorem requires the preparation to be lifted as well. Fix one
admissible two-module datum \(\mathcal P_2\) from the canonical theorem. A
**compatible equivariant lift** \(\mathcal P_N\) means:

1. the critical \((\chi,d)\) cutoff, planar joining, phase \(X=0\), and the
   two tail levels \(\mathscr H=0\) are those of \(\mathcal P_2\);
2. stable-slot preparations are componentwise scalar saturations followed by
   the projectors \(P_c,P_m,P_w\), hence commute with \(\Gamma_N\);
3. on \(S\mathbb R^2\), every prepared finite-dimensional map is the
   \(S\)-lift of its two-module counterpart.

The preparation constructed in Section 7 of
[the arbitrary-\(N\) blow-up note](paper-ii-arbitrary-n-blowup-model-fit.md)
has these properties when the same scalar profiles are used. They are
conditions on the selection device, not additional equations imposed on the
physical RFDE.

### Lemma 1.1 -- exact restriction of the invariant history graph

For every fixed compatible pair \((\mathcal P_2,\mathcal P_N)\), every
allowed \((\delta,\nu,\eta)\), and every \(n_1,n_2\geq1\), the unique lifted
special-flow fixed point satisfies

\[
 \boxed{
 Q_{N,\delta,\nu,\eta}=Q_{2,\delta,\nu,\eta},
 \qquad
 H_{N,\delta,\nu,\eta}=\mathfrak S_N
 H_{2,\delta,\nu,\eta}.}
 \tag{1.4}
\]

Here \(\mathfrak S_N\) sends the two-module stable voltage and recovery
coordinates to their block-constant lifts. In particular, the within-module
part of \(H_N\) is zero. The complete-history embeddings obey

\[
 \iota_{N,\delta,\nu,\eta}
 =\mathfrak S_N^{\rm hist}
   \iota_{2,\delta,\nu,\eta}.
 \tag{1.5}
\]

**Proof.** The prepared graph transform commutes with every
\(P\in\Gamma_N\). Its fixed point is unique in the common contraction ball,
so \(PH_N(u)=H_N(u)\) for every critical base point \(u\). Equation (1.3)
then puts \(H_N(u)\) in the block-constant stable space. Restricting the
fixed-point equation to that space and applying \(R\) gives exactly the
two-module fixed-point equation, including each delayed history evaluation.
Uniqueness of the latter gives (1.4). The finite-time reduced flows are
therefore identical, and the definition of the history embedding gives
(1.5). \(\square\)

### Lemma 1.2 -- exact restriction of traces and gap

Let \(z_N^a,z_N^r\) be the phase-normal one-sided traces selected using
\(\mathcal P_N\), and let \(D_N\) use the same normalized first-integral
matcher as the two-module theorem. Then

\[
 z_N^\sigma=\mathfrak S_N^{\rm hist}z_2^\sigma,
 \qquad \sigma\in\{a,r\},
 \qquad
 \boxed{D_N(\delta,\nu,\eta)=D_2(\delta,\nu,\eta).}
 \tag{1.6}
\]

**Proof.** By Lemma 1.1 the prepared reduced planar fields are identical.
The two tail levels and the phase condition are identical by compatibility.
Uniqueness in the one-sided Green construction therefore gives the first
identity. The matcher depends only on the common critical coordinates at
the matching section, which proves the second. \(\square\)

## 2. Exact arbitrary-size canonical root theorem

Put

\[
 \alpha=\frac{\sqrt6}{4},\qquad
 c_\eta=\frac{K(\theta_0-\theta_1)}{4\alpha}
       =\frac{K(\theta_0-\theta_1)}{\sqrt6}.
 \tag{2.1}
\]

### Theorem 2.1 -- arbitrary-size selected-history root lift

Fix

\[
 K\ne0,\qquad D_v,D_w>0,\qquad
 0<\theta_0<\theta_1,
 \tag{2.2}
\]

and one compatible bounded preparation class as above. There are
\(\delta_0,\eta_0,c_0,C>0\), independent of \(n_1,n_2\), such that for every

\[
 n_1,n_2\geq1,\qquad
 0<\delta<\delta_0,\qquad |\eta|<\eta_0,
 \tag{2.3}
\]

the normalized gap \(D_N/\delta\) has a unique root
\(\nu_{c,N}(\delta,\eta)\) in

\[
 \left|\nu+\frac{11}{24\alpha}\right|<c_0.
 \tag{2.4}
\]

At that root the selected attracting and repelling complete node histories
are equal. More strongly,

\[
 \boxed{
 \nu_{c,N}(\delta,\eta)=\nu_{c,2}(\delta,\eta),
 \qquad
 \mu_{c,N}(\delta,\eta)=\mu_{c,2}(\delta,\eta),}
 \tag{2.5}
\]

where \(\mu=\delta^2\nu\). Consequently

\[
 \boxed{
 \mu_{c,N}(\delta,\eta)-\mu_{c,N}(\delta,0)
 =c_\eta\delta^3\eta
 +\mathcal E_N(\delta,\eta),}
 \tag{2.6}
\]

with

\[
 |\mathcal E_N(\delta,\eta)|
 \le C\bigl(\delta^4|\eta|+\delta^3\eta^2\bigr)
 \tag{2.7}
\]

uniformly in both module sizes.

**Proof.** Lemma 1.2 identifies the complete normalized gap with the gap in
the proved canonical two-module theorem. Its existence, uniqueness,
simple-root estimate, history equality, coefficient, and remainder therefore
transfer without changing a constant. \(\square\)

This theorem is stronger than a dimension-uniform estimate: the selected
root is literally independent of \(n_1,n_2\). It is also narrower than a
general-network theorem: it uses an equitable two-module quotient and a
single collective fold coordinate.

## 3. A genuinely non-equitable residual family

Assume a receiving module \(C_b\) has \(n_b\geq2\). Let \(u_N\in\ker R\)
be the distributed weighted-unit zero-mean vector and let

\[
 \rho_a=\sqrt{d_a}R_a,\qquad d_1=\frac12,\quad d_2=\frac18,
 \qquad G_N=u_N\rho_a
 \tag{3.1}
\]

be the rank-one generator in Proposition 6.1 of the lifted-class note. Thus

\[
 RG_N=0,\qquad G_NQ=G_N,\qquad QG_N=0,\qquad G_NS\ne0,
 \tag{3.2}
\]

and

\[
 \|G_N\|_{\infty\to\infty}
 \leq\sqrt{\frac{2d_a}{d_b}}.
 \tag{3.3}
\]

For two structural parameters \((\eta,\zeta)\), set

\[
 \begin{aligned}
 \widetilde A_{0,N}^{\eta,\zeta}
   &=SC_0^\eta R+\zeta G_N,\\
 \widetilde A_{1,N}^{\eta,\zeta}
   &=SC_1^\eta R-\zeta G_N.
 \end{aligned}
 \tag{3.4}
\]

The total current gain is unchanged, constant histories still annihilate the
balanced feedback, and the complete direct critical delay measure is fixed.
When \(\zeta\ne0\), rowwise equitability fails.

If \(|\eta|\leq\eta_*\) lies in a compact subinterval of
\((-1/6,1/12)\), define

\[
 c_*=\min_{|\eta|\leq\eta_*}
      \min_{k\in\{0,1\},\,i,j\in\{1,2\}}
      (C_k^\eta)_{ij}>0.
 \tag{3.5}
\]

Then both complete lifted layers remain entrywise positive whenever

\[
 |\zeta|<c_*\sqrt{\frac{d_b}{2d_a}}.
 \tag{3.6}
\]

This bound is independent of \(n_1,n_2\).

## 4. Reynolds cancellation of the pure breaker

The canonical preparation in Section 1 is relabeling covariant: conjugating
all layer operators by \(P\in\Gamma_N\) conjugates the selected histories but
does not change their scalar gap. Write

\[
 D_N(\delta,\nu,\eta,\zeta;G_N)
 \tag{4.1}
\]

when the generator needs to be displayed. Covariance gives

\[
 D_N(\delta,\nu,\eta,\zeta;PG_NP^{-1})
 =D_N(\delta,\nu,\eta,\zeta;G_N).
 \tag{4.2}
\]

### Lemma 4.1 -- exact first-response nullity

For every fixed \(N,\delta,\nu,\eta\) in the canonical construction,

\[
 \boxed{
 D_{\mathcal R}D_N(\delta,\nu,\eta,0)[(G_N,-G_N)]=0.}
 \tag{4.3}
\]

The same identity holds after one \(\nu\)- or \(\eta\)-derivative.

**Proof.** The graph and trace constructions are Fréchet differentiable in
the fixed-support operator-TV residual. Their scalar first response is a
bounded linear functional \(L_N\) of the pair of layer directions. Equation
(4.2) makes \(L_N\) invariant under conjugation. Write
\(G_N=u_N\rho_a\).  The source covector is fixed by every within-module
relabeling, so

\[
 \frac1{|\Gamma_N|}\sum_{P\in\Gamma_N}PG_NP^{-1}
 =\left(\frac1{|\Gamma_N|}\sum_{P\in\Gamma_N}Pu_N\right)\rho_a
 =(Qu_N)\rho_a=0.
 \tag{4.4}
\]

The tempting identity that the conjugacy average of a general matrix equals
\(QGQ\) is false; the invariant-source rank-one structure is essential
here. Linearity and invariance give
\(L_N(G_N,-G_N)=L_N(0,0)=0\). Parameter
differentiation commutes with the finite group average, proving the last
claim. \(\square\)

If \(n_b\) is even, the distributed vector has equally many positive and
negative entries. A within-module permutation sends \(u_N\) to \(-u_N\).
Then (4.2) gives the stronger exact identity

\[
 D_N(\delta,\nu,\eta,\zeta;G_N)
 =D_N(\delta,\nu,\eta,-\zeta;G_N).
 \tag{4.5}
\]

For odd \(n_b\), (4.3) still holds although no sign-swapping permutation is
available for the declared two-level vector.

### Why equivariance cannot be omitted

Projection neutrality alone does not imply (4.3). A node-labelled matcher

\[
 L_i(G)=e_i^TG r_N
 \tag{4.6}
\]

is generally nonzero for a receiving node even though
\(\ell_N^TG=0\). Thus a preparation or endpoint rule that singles out a
node can read the pure breaker at first order. Also, the base canonical
theorem explicitly permits its exact finite-\(\delta\) root to depend on the
preparation. The minimal repair is precisely the compatible,
\(\Gamma_N\)-covariant selection fixed in Section 1; no
preparation-independent exact equality is asserted.

## 5. Uniform non-equitable selected-root response

The remaining analytic input is a parameter extension of the already proved
canonical trace construction.

### Lemma 5.1 -- uniform \(C^2_\zeta\) normalized gap

After decreasing \(\delta_0,\eta_0,\zeta_0\), the non-equitable prepared
system (3.4) has canonical one-sided traces and a normalized gap

\[
 \widehat D_N=\frac{D_N}{\delta}
 \tag{5.1}
\]

which is \(C^1_\nu C^2_{(\eta,\zeta)}\). Uniformly in \(n_1,n_2\),

\[
 \left|\partial_\nu\widehat D_N-\sqrt{2\pi}\right|
 \leq C\delta+C|\eta|+C|\zeta|,
 \tag{5.2}
\]

and

\[
 \max_{j=0,1,2}
 \left|\partial_\zeta^j\widehat D_N\right|\leq C
 \tag{5.3}
\]

on the fixed root cylinder. The same bound holds for the mixed derivatives
needed below.

**Proof.** The residual measure consists of the two fixed atoms
\((G_N,-G_N)\), whose maximum-norm TV is bounded uniformly by (3.3). It
annihilates the affine critical anchor because the two atoms have opposite
total layer and \(RG_N=0\). The dimension-uniform graph theorem and its
Banach-scale response theorem therefore give first and second structural
responses of \((Q_N,H_N)\), with

\[
 \|D_\zeta(Q_N,H_N)\|+
 \|D_{\zeta\zeta}(Q_N,H_N)\|
 \leq C\delta\langle s\rangle^m e^{c|s|}
 \tag{5.4}
\]

on the logarithmic core. This is the displayed small-amplitude factor in
the graph transform, not a generic same-space implicit-function estimate.

For completeness, the four trace hypotheses left abstract in the
Banach-scale response theorem are verified here.

1. **Prepared-tail inverse.**  In the canonical tangent--normal frame, the
   leading one-sided trace operator is the same two-dimensional operator as
   at \(N=2\).  Its explicit Green operator \(\mathcal G_R\), with the
   attracting normal coefficient fixed at the left endpoint, the repelling
   normal coefficient fixed at the right endpoint, and the tangent phase
   fixed at \(X=0\), obeys
   \[
      \|\mathcal G_R f\|_{E,R}\le C_G\|f\|_{E,R}.
      \tag{5.4a}
   \]
   The constant is independent of the receding endpoint \(R\) and of
   \(N\); the Gaussian factor in the weighted normal norm cancels the
   growing homogeneous normal mode.

2. **Mixed field jets.**  Substitution of (5.4) into the prepared reduced
   field gives, for \(i\le1\) and every mixed
   \((\eta,\zeta)\)-multi-index \(|\beta|\le2\),
   \[
    \|\partial_\nu^i\partial_{(\eta,\zeta)}^\beta
       (Q_N-q_0)\|_{C^3(|s|\le R)}
       \le \delta P(R)e^{cR},
       \tag{5.4b}
   \]
   with one polynomial \(P\) and constants independent of module size.
   The fixed-support atoms create no moving-evaluation derivative.  With
   \(R=S_\delta+B\) and the logarithmic exponent fixed in the preparation,
   \(C_G\delta P(R)e^{cR}<1/2\).  Hence the perturbed trace operator is
   inverted by a Neumann series uniformly in \(N\).

3. **Parameter and moving-hit equations.**  Differentiating the trace fixed
   point orders the current highest jet linearly; all lower jets are already
   bounded by (5.4b).  Applying the inverse in (5.4a) successively gives the
   rectangular \(C^1_\nu C^2_{(\eta,\zeta)}\) trace bounds.  The endpoint
   tail equations and the phase equation are the same scalar equations as
   in the two-module construction.  Their leading derivatives are bounded
   away from zero, so the implicit equations for the two moving hit times
   have the same mixed bounds.  This verifies the trace and endpoint
   inverse hypotheses rather than assuming a full-network Lin inverse.

4. **Differentiated tails.**  The preparation profiles themselves are
   parameter independent.  Every differentiated boundary term is therefore
   a trace or hit-time jet bounded by \(P(R)e^{cR}\), multiplied by the
   Gaussian factor from the normal Green pairing.  Uniformly for all the
   derivatives just listed,
   \[
      e^{-R^2/2}P(R)e^{cR}=o(\delta^m)
      \tag{5.4c}
   \]
   at the finite order \(m\) required here, after the already declared
   logarithmic exponent is chosen.  Thus no unrecorded endpoint term enters
   (5.2)--(5.3).

The differentiated Green equations now give
\(D_\zeta^jD_N=O(\delta)\) for \(j=0,1,2\), which proves (5.3). The
\(\nu\)-slope at \(\zeta=0\) is the two-module value by Lemma 1.2;
(5.4a)--(5.4c) and continuity give (5.2). \(\square\)

### Theorem 5.2 -- non-equitable root branch and its sharp proved remainder

There are fixed \(\delta_0,\eta_0,\zeta_0,c_0,C>0\), independent of
module size, such that for

\[
 0<\delta<\delta_0,\qquad
 |\eta|<\eta_0,\qquad |\zeta|<\zeta_0,
 \tag{5.5}
\]

the normalized canonical gap has a unique root
\(\nu_{c,N}(\delta,\eta,\zeta)\) in (2.4). It is
\(C^1\) in \((\eta,\zeta)\), and zero gap is equality of the two selected
complete node histories. Moreover,

\[
 \boxed{
 \partial_\zeta\mu_{c,N}(\delta,\eta,0)=0,
 \quad
 |\partial_{\zeta\zeta}\mu_{c,N}(\delta,\eta,0)|
 \leq C\delta^2,
 \quad
 |\mu_{c,N}(\delta,\eta,\zeta)
   -\mu_{c,N}(\delta,\eta,0)|
 \leq C\delta^2\zeta^2.}
 \tag{5.6}
\]

Consequently

\[
 \boxed{
 \begin{aligned}
 &\mu_{c,N}(\delta,\eta,\zeta)
   -\mu_{c,N}(\delta,0,0)\\
 &\quad=c_\eta\delta^3\eta
 +O\!\left(
     \delta^4|\eta|+\delta^3\eta^2+\delta^2\zeta^2
   \right),
 \end{aligned}}
 \tag{5.7}
\]

with one remainder constant for all \(n_1,n_2\). When \(n_b\) is even,
the root is exactly even in \(\zeta\).

**Proof.** Equations (5.2)--(5.3) and the quantitative implicit-function
argument give a unique uniform root branch. Differentiate once
\(\widehat D_N(\nu_c,\eta,\zeta)=0\). Lemma 4.1 and the nonzero
\(\nu\)-slope give \(\partial_\zeta\nu_c=0\) at \(\zeta=0\). A second
directional expansion at \(\zeta=0\) then gives

\[
 \partial_{\zeta\zeta}\nu_c
 =-\frac{\partial_{\zeta\zeta}\widehat D_N}
         {\partial_\nu\widehat D_N}
 \quad\text{at }\zeta=0.
 \tag{5.8}
\]

No \(\nu\nu\)-derivative is used in (5.8), because the first root derivative
vanishes at the base point. We do not claim a second root derivative away
from \(\zeta=0\). For the finite-amplitude estimate, keep
\(\nu_{c,N}(\delta,\eta,0)\) fixed and Taylor-expand the gap only in
\(\zeta\). Lemma 4.1 kills its linear term, (5.3) bounds the quadratic
remainder, and the uniform lower bound on \(\partial_\nu\widehat D_N\)
gives

\[
 |\nu_{c,N}(\delta,\eta,\zeta)
   -\nu_{c,N}(\delta,\eta,0)|\le C\zeta^2.
 \tag{5.8a}
\]

Multiplication by \(\delta^2\) proves all of (5.6). Combining (5.8a) with
Theorem 2.1 on \(\zeta=0\) proves (5.7). Equation
(4.5) and uniqueness give exact evenness. \(\square\)

### Corollary 5.3 -- a genuinely non-equitable nonzero tangent

Fix \(\kappa\ne0\) and set

\[
 \eta=a,\qquad \zeta=\kappa a.
 \tag{5.9}
\]

For every nonzero sufficiently small \(a\), the two layers are non-equitable.
Nevertheless,

\[
 \boxed{
 \left.\frac{d}{da}\mu_{c,N}(\delta,a,\kappa a)
 \right|_{a=0}
 =c_\eta\delta^3+O(\delta^4),}
 \tag{5.10}
\]

uniformly in \(N\), and this derivative is nonzero for all sufficiently small
\(\delta\). At finite amplitude,

\[
 \mu_{c,N}(\delta,a,\kappa a)-\mu_{c,N}(\delta,0,0)
 =c_\eta\delta^3a
 +O\!\left(
   \delta^4|a|+\delta^3a^2+\kappa^2\delta^2a^2
 \right).
 \tag{5.11}
\]

This witness is uniformly normalized. If
\(C_G=\sqrt{2d_a/d_b}\), then the two-atom TV norm of its layer tangent
obeys

\[
 2\|T\|_{\infty\to\infty}
 \leq
 \|(S T R+\kappa G_N,-S T R-\kappa G_N)\|_{\rm TV,\infty}
 \leq2\bigl(\|T\|_{\infty\to\infty}+|\kappa|C_G\bigr).
 \tag{5.12}
\]

The lower bound follows by applying \(R(\cdot)S\), while the upper bound is
the triangle inequality. Hence normalization cannot make the nonzero
coefficient in (5.10) disappear along a sequence of module sizes.

Thus the nonzero coefficient survives in a truly non-equitable tangent, but
the strongest presently proved two-parameter remainder contains
\(\delta^2\zeta^2\). To obtain a leading asymptotic along a joint limit one
may take \(a=o(\delta)\), or use the explicitly scaled non-equitable family
\(\zeta=\kappa\delta a\). Removing this wedge by evaluating a nonzero pure
within-module quadratic coefficient would require graph and trace jets beyond
those currently established.

## 6. What this closes, and what it does not

The following statements are now **proved** for every pair of positive module
sizes (with \(n_b\ge2\) when the non-equitable breaker is used).

1. The compatible canonical complete-history graph, selected traces, scalar
   gap, and root restrict exactly to the two-module objects.
2. The nonzero \(\delta^3\eta\) root coefficient and its full remainder are
   uniform in \(N\).
3. Distributed non-equitable layer residuals admit a uniform operator-TV and
   positivity radius.
4. The pure zero-mean residual has zero first selected-gap and root response
   by a Reynolds argument; for even receiving modules the whole root is even.
5. A combined module-plus-zero-mean direction is genuinely non-equitable and
   has the inherited nonzero first root response, with the honest remainder
   (5.11).

The following remain **open**.

1. A nonzero leading coefficient for the pure within-module generator
   \(G_N\). Its first coefficient is ruled out by Lemma 4.1; a quadratic or
   higher response needs additional graph/trace orders and may depend on the
   receiving module.
2. A response theorem for arbitrary non-equitable operator-TV directions,
   rather than the explicit rank-one family and its combined tangent.
3. A root theorem for the shared-resource Dobrushin class without an exact
   two-module quotient.
4. Identification of any canonical local root in this note with a physical
   outer maximal canard, spike onset, frequency, amplitude, or safety
   threshold.

## 7. Reproduction

Run

    PYTHONPATH=build/testdeps:src python3 -m pytest -q \
      tests/test_lifted_selected_root_response.py

The tests check the exact module restriction, complete projected-measure
neutrality, failure of equitability, Reynolds projection, literal finite-group
average, even-module sign swap, inherited coefficient, and the node-labelled
counterexample showing why relabeling covariance is essential.
