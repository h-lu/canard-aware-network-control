# Paper III Gate U-SF: an unforced geometric complete-history separator

Status: **the canonical right-fold history has an exact causal forward
continuation, and the singular middle branch, its positive repelling action,
the scalar action-amplification law, and the singular reset transversality
below are proved.  The full positive-\(\delta\) geometric-separator theorem
is proved as an implication of two explicit model hypotheses: an exact (or
action-supercritical) outer tracker and a dominated complete-history
trichotomy.  Those two hypotheses have not yet been verified for the
physical two-module RFDE.  Thus Gate U-SF is reduced to a precise theorem
package but is not marked closed.  No pulse/quiet outcome is claimed here.**

The numerical action, unstable eigenvector pairing, logarithmic matching
test, domination ledger, and reset-root bound are executable in
`src/canard_control/unforced_geometric_separator.py`, with regressions in
`tests/test_unforced_geometric_separator.py`.  The approximate action value
is a diagnostic, not an interval enclosure.  This note does not modify the
frozen JNS manuscript.

## 1. What U-SF must construct

Let \(\bar u\) denote the compact tuple of controls other than the unfolding
parameter.  Fix the declared preparation \(\mathcal P\), set
\(\mu=\mu_{c,\mathcal P}(\delta,\bar u)\), and use \(u\) below as shorthand
for this pulled-back physical parameter tuple.  Put

\[
 \varepsilon=\delta^2,
 \qquad
 \tau_k=\frac{\theta_k}{\delta},
 \qquad
 \rho_R=-\frac12.
\tag{1.1}
\]

At the preparation-indexed simple root, the canonical local theorem gives
one exact retained complete history on the outgoing middle side of the
right-fold chart.  Denote a history on a declared outgoing overlap by

\[
 \phi^{\rm can,out}_{\delta,u}.
\tag{1.2}
\]

It is a history of the **uncut physical RFDE**, not merely a reduced point.
For every fixed positive \(\delta\), ordinary forward well-posedness
therefore defines

\[
 x^m_{\delta,u}(t)
  =\Phi^t_{\delta,u}
    (\phi^{\rm can,out}_{\delta,u})
\tag{1.3}
\]

up to its first exit from the declared outer tube.  This is the only
unambiguous forward construction available from the present theorem.  It
does not invert the retarded semiflow.

Let

\[
 T_R(\delta,u)
 =\inf\{t>0:\rho(x^m_{\delta,u}(t))=\rho_R\}.
\tag{1.4}
\]

If the orbit stays in the middle-branch tube until this hit, its selected
complete history at the reset layer is

\[
 \Gamma^m_{\delta,u}(\rho_R)(s)
 =x^m_{\delta,u}(T_R+s),
 \qquad -\tau_*\le s\le0.
\tag{1.5}
\]

The phrase *if the orbit stays* is the first analytic seam.  Forward
existence is not a repelling slow-tracking theorem.  The distinction is
quantitatively large on the interval from the right fold to \(\rho_R\).

## 2. The singular middle branch and its action

Use the exact critical-curve parameterization from the physical pulse
bridge,

\[
 G(a,b)=2a^3+2a-4b-b^3-4=0,
\tag{2.1}
\]

\[
 \xi(a)=\sqrt{\frac32}
   \left(\frac{a-1}{2}+\frac{b(a)}4\right),
 \qquad
 \rho(a)=\frac12\sqrt{\frac32}
   \bigl(a-a^3+b(a)\bigr).
\tag{2.2}
\]

The exact fold count proves that the segment between the right fold
\(a=1\) and the left fold is a saddle branch.  At \(\rho_R=-1/2\), its
middle point has the numerical values

\[
 a_R=0.02354566467\ldots,
 \qquad
 \xi_R^m=-0.8551590808\ldots,
 \qquad
 \lambda_u(a_R)=0.8437337278\ldots .
\tag{2.3}
\]

Only the exact branch and sign statements are used analytically.  The
decimals are regression values.

At \(\mu=0\), define the singular repelling action from the right fold to
the reset layer by

\[
 \boxed{
 \mathcal A_R
 =\int_1^{a_R}
   \lambda_u(a)\frac{\rho'(a)}{\xi(a)}\,da .}
\tag{2.4}
\]

On the open middle branch,
\(\lambda_u>0\), \(\rho'>0\), and \(\xi<0\).  The orientation in (2.4)
is from \(1\) down to \(a_R\), so \(\mathcal A_R>0\).  The fold
expansions show that the integrand is integrable at \(a=1\).  Numerical
quadrature gives

\[
 \mathcal A_R=0.5607898753\ldots .
\tag{2.5}
\]

For an actual middle-branch entry \(a_{\rm out}\in(a_R,1)\), put

\[
 \mathcal A(a_{\rm out},a_R)
 =\int_{a_{\rm out}}^{a_R}
   \lambda_u(a)\frac{\rho'(a)}{\xi(a)}\,da .
\tag{2.5a}
\]

This is positive and converges to \(\mathcal A_R\) as
\(a_{\rm out}\uparrow1\).  In particular, the logarithmic outgoing section
of the inner theorem has
\(\mathcal A(a_{{\rm out},\delta},a_R)=\mathcal A_R-o(1)\).

> **Proposition 2.1 (exact outer action amplification).**  On a scalar
> normal comparison along the singular middle branch,
>
> \[
>  \dot z=\lambda_u(\rho(t))z,
>  \qquad
>  \dot\rho=\varepsilon\xi^m(\rho),
> \tag{2.6}
> \]
>
> a nonzero entry error \(z_{\rm out}\) at \(a_{\rm out}\)
> satisfies
>
> \[
>  |z(\rho_R)|
>  =|z_{\rm out}|
>    \exp(\mathcal A(a_{\rm out},a_R)/\varepsilon).
> \tag{2.7}
> \]
>
> Consequently, to arrive in a reset tube \(|z|\le r_R\), one needs
>
> \[
>  \log|z_{\rm out}|
>  \le \log r_R
>      -\frac{\mathcal A(a_{\rm out},a_R)}{\varepsilon}.
> \tag{2.8}
> \]

**Proof.**  Divide the two equations in (2.6), use \(a\) as the branch
coordinate, and integrate:

\[
 \frac{d\log|z|}{da}
 =\frac1\varepsilon
   \lambda_u(a)\frac{\rho'(a)}{\xi(a)}.
\]

Equations (2.7)--(2.8) follow from (2.5a). \(\square\)

The same leading action is obtained for
\(\mu=O(\varepsilon)\); proving the required uniform nonlinear remainder is
part of the outer tracker estimate.

> **Corollary 2.2 (algebraic and weakly flat overlap errors do not close
> U-SF).**  For every fixed \(p,c>0\), the upper bounds
> \(|z_{\rm out}|=O(\delta^p)\) and
> \(|z_{\rm out}|=O(e^{-c/\delta})\), by themselves, do not imply a
> bounded error at \(\rho_R\).  Indeed, saturating either scale gives the
> respective outgoing logarithms on the logarithmic inner/outer overlap
>
> \[
>  p\log\delta+\frac{\mathcal A_R-o(1)}{\delta^2}
>  \longrightarrow+\infty,
> \qquad
>  -\frac c\delta+\frac{\mathcal A_R-o(1)}{\delta^2}
>  \longrightarrow+\infty.
> \tag{2.9}
> \]
>
> An action-supercritical estimate
> \(|z_{\rm out}|\le Ce^{-(\mathcal A_R+\chi)/\varepsilon}\),
> \(\chi>0\), instead leaves
> \(O(e^{-\chi/\varepsilon})\) at the reset layer.

This is the minimal quantitative blocker.  The canonical theorem proves an
exact common history **inside its retained local graph**.  It does not prove
exact equality with an outer repelling history curve.  Superalgebraic
agreement without an action constant is insufficient.

## 3. The narrow outer tracker gate

The full compatible-selection Gate P3-A\(^*\) asks for attracting and
repelling outer families and mixed \(C^1_\mu C^2_\eta\) jets.  U-SF needs a
narrower, one-sided object.

> **Gate U-OUT (selected forward middle-history tracker; open).**  On an
> interval extending from the outgoing right-fold overlap past
> \(\rho_R\), construct a parameter-coherent exact curve
>
> \[
>  \mathcal K^m_{\delta,u}:J_\rho\longrightarrow\mathbb R^4,
>  \qquad \pi_\rho\mathcal K^m_{\delta,u}(r)=r,
> \tag{3.1}
> \]
>
> with scalar base speed
>
> \[
>  q_{\delta,u}(r)
>  =\pi_\xi\mathcal K^m_{\delta,u}(r)-\mu,
> \tag{3.2}
> \]
>
> whose curve-restricted histories
>
> \[
>  \mathfrak I^m_{\delta,u}(r)(\vartheta)
>  =\mathcal K^m_{\delta,u}
>    (\Phi_q^{\delta\vartheta}(r)),
>  \qquad -\theta_*\le\vartheta\le0,
> \tag{3.3}
> \]
>
> solve the exact physical parameterization equation
>
> \[
>  D\mathcal K^m_{\delta,u}(r)q_{\delta,u}(r)
>  =\mathcal V_{\delta,u}
>    (\mathfrak I^m_{\delta,u}(r)).
> \tag{3.4}
> \]
>
> Require:
>
> 1. every base backtrack in (3.3) remains in the uncut middle tube;
> 2. (3.3) equals the canonical retained history on one outgoing overlap,
>    not merely at present evaluation;
> 3. \(q_{\delta,u}<0\) from that overlap through \(\rho_R\);
> 4. the curve and its strong histories have the uniform
>    \(C^1_rC^1_u\) bounds used by the reset theorem; and
> 5. the curve extends a fixed positive slow distance on both sides of
>    \(\rho_R\), and a fixed parameter-coherent overflowing or terminal
>    Lyapunov--Perron normalization is declared on the longer interval,
>    with local invariance required on its interior.
>    This normalization selects the center-stable sheet; no
>    preparation-independent finite-\(\delta\) sheet is asserted.

Exact equality in item 2 may be replaced by an action-supercritical
complete-history matching estimate, but then its nonlinear propagation and
parameter derivative bounds must be included explicitly.  An
\(O(\delta^p)\) overlap estimate is not a substitute by Corollary 2.2.

> **Lemma 3.1 (U-OUT gives the selected reset tracker).**  If Gate U-OUT
> holds, then the forward orbit (1.3) remains on (3.3), hits \(\rho_R\)
> exactly once, and (1.5) equals \(\mathfrak I^m_{\delta,u}(\rho_R)\).
> For every fixed \(\delta>0\), the hit and the complete reset-layer
> history are \(C^1\) in \(u\).

**Proof.**  The exact curve-restricted lift theorem turns (3.3) into an
RFDE solution.  Item 2 gives the same complete initial history as (1.3), so
forward uniqueness makes the two solutions equal.  Item 3 makes \(\rho\)
strictly monotone and gives the unique hit.  Fixed-\(\delta\) RFDE parameter
dependence and the implicit-function theorem at

\[
 \dot\rho(T_R)=\varepsilon q_{\delta,u}(\rho_R)\ne0
\]

give the last assertion. \(\square\)

This lemma is constructive and causal.  Its open content is containment and
exact outer matching, not forward uniqueness.

## 4. The long-delay variational problem

Along the tracker, the variational RFDE has the form

\[
 \dot y(t)=A_{\delta,u}(t)y(t)
 +\varepsilon\sum_{k=0}^1
 L_{k,\delta,u}(t)y(t-\tau_k).
\tag{4.1}
\]

On a compact singular middle segment away from both folds, the current
fast voltage matrix has one positive and one negative eigenvalue;
\(-D_w\) is the transverse recovery rate, and the tangent recovery mode is
slow.  The delayed functional in (4.1) has norm \(O(\varepsilon)\),
independently of \(\tau_k\), on the sup-history space.  These facts strongly
suggest a one-dimensional strong-unstable bundle.  They are not themselves
a nonautonomous complete-history trichotomy.

Use the fixed scaled phase space

\[
 \widehat{\mathcal X}
 =C([ -\theta_*,0],\mathbb R^4),
 \qquad \widehat y_t(\vartheta)=y(t+\vartheta/\delta).
\tag{4.2}
\]

No derivative in \(\delta\) is requested.

> **Gate U-TR (dominated long-delay trichotomy; open for the physical
> tracker).**  Fix a compact middle-branch subinterval
> \(J_R\Subset(\rho_-,0)\) that contains \(\rho_R\) in its interior and is
> separated from both folds.  Along the restriction of a slightly extended
> version of (3.3) to \(J_R\), prove a
> parameter-\(C^1\) invariant splitting
>
> \[
>  \widehat{\mathcal X}
>  =E^u_{\delta,u}(r)
>   \oplus E^c_{\delta,u}(r)
>   \oplus E^s_{\delta,u}(r),
> \qquad
>  \dim E^u=\dim E^c=1,
> \tag{4.3}
> \]
>
> with the following properties.
>
> 1. The unstable evolution is invertible on \(E^u\) and, for one
>    \(\beta>0\) independent of \(\delta\),
>    \[
>      \|T^u(s,t)\|\le M e^{-\beta(t-s)},
>      \qquad t\ge s.
>    \tag{4.4}
>    \]
> 2. The center is tangent to the selected history curve and has rates
>    \(O(\varepsilon)\).
> 3. For each fixed \(\delta>0\), \(E^s\) has a positive decay rate that
>    dominates the center rate for that \(\delta\).  The decay rate and
>    its semigroup constant may deteriorate as \(\delta\downarrow0\); no
>    uniform stable gap is claimed.
> 4. The coarser center-stable evolution obeys the uniform domination
>    estimate
>    \[
>      \|T^{cs}(t,s)\|\le M e^{\alpha(t-s)},
>      \qquad 0\le\alpha<\beta,\quad t\ge s.
>    \tag{4.5}
>    \]
> 5. The projectors and evolution estimates act on complete scaled
>    histories, include old-history translation, and have the \(C^1_u\)
>    bounds required by the nonlinear graph transform.
> 6. After normalizing the unstable quotient covector, its action on
>    constant voltage tangents converges uniformly to the left unstable
>    covector of the singular fast saddle at \(\rho_R\).

The separate stable rate in item 3 cannot be taken uniformly negative under
the present scaling: the exact Lambert-\(W\) calculation in the clamped
separator note exhibits stable pseudo-continuous roots approaching the
imaginary axis.  The useful uniform gap is the strong-unstable versus
center-stable gap in (4.4)--(4.5).

The following abstract calculation makes the roughness input checkable.

> **Lemma 4.1 (weighted Green roughness bound).**  Suppose a base
> complete-history evolution has a Green representation with
> center-stable forward rate \(\alpha_0\), unstable backward rate
> \(\beta_0>\alpha_0\), and common bound \(M\).  Let a perturbation be
> admissible in its variation-of-constants formula with norm at most \(b\).
> For
>
> \[
>  \alpha_0<\eta<\beta_0
> \]
>
> define
>
> \[
>  \kappa_\eta
>  =Mb\left[
>    \frac1{\eta-\alpha_0}
>    +\frac1{\beta_0-\eta}
>  \right].
> \tag{4.5a}
> \]
>
> If \(\kappa_\eta<1\), the weighted
> Lyapunov--Perron equation has a unique solution and
>
> \[
>  \|(I-\mathcal G_\eta\mathcal B)^{-1}\|
>  \le\frac1{1-\kappa_\eta}.
> \tag{4.5b}
> \]
>
> If, in addition, the base Green operator and the perturbation are
> \(C^1_u\) and
>
> \[
>  \|D_u(\mathcal G_\eta\mathcal B)\|\le d_\eta,
> \tag{4.5c}
> \]
>
> then the inverse is \(C^1_u\) and
>
> \[
>  \left\|D_u
>   (I-\mathcal G_\eta\mathcal B)^{-1}\right\|
>  \le\frac{d_\eta}{(1-\kappa_\eta)^2}.
> \tag{4.5d}
> \]
>
> Thus parameter control requires differentiated Green/projector bounds,
> not only a derivative of the delayed atom.  Applying the criterion at two
> weights strictly between \(\alpha_0\) and \(\beta_0\), together with the
> standard Green characterization of a dichotomy, gives a perturbed
> strong-unstable/center-stable splitting with rates between those weights.

**Proof.**  After conjugation by the weight \(e^{-\eta t}\), the
center-stable part of the Green kernel has integral norm at most
\(M/(\eta-\alpha_0)\), while the backward unstable part has integral norm
at most \(M/(\beta_0-\eta)\).  Hence
\(\|\mathcal G_\eta\mathcal B\|\le\kappa_\eta\).  The Neumann series gives
(4.5b) and uniqueness.  Put
\(R_\eta=(I-\mathcal G_\eta\mathcal B)^{-1}\).  Differentiating the
inverse identity gives
\[
 D_uR_\eta
 =R_\eta D_u(\mathcal G_\eta\mathcal B)R_\eta,
\]
which proves (4.5d).  The final claim is the usual Green-operator
characterization applied at the two
weights; the Banach-space roughness step is the standard one in
[Ju--Wiggins](https://doi.org/10.1006/jmaa.2001.7496). \(\square\)

The executable Green budget evaluates (4.5a).  Its physical input is the
**admissible** norm \(b\), not just the matrix norm of a frozen delay atom.
Old-history translation must already be included in the base Green
operator, and the sun--star/variation-of-constants insertion of the delayed
functional must be bounded independently of \(\tau_*=\theta_*/\delta\).
Establishing precisely that bound, together with the differentiated base
Green/projector bounds in (4.5c), is the central linear task in U-TR.

A checkable route to U-TR is a moving-coordinate roughness estimate.  Let
\(\lambda_*>0\) be a lower bound for the current strong-unstable rate on a
fixed outer segment, let \(\alpha_0\ge0\) bound the unperturbed
center-stable growth, and prove that the delayed and moving-frame terms
cost at most \(r_\delta\) in each exponent.  Then one may take

\[
 \beta=\lambda_*-r_\delta,
 \qquad
 \alpha=\alpha_0+r_\delta,
\tag{4.6}
\]

and domination reduces to

\[
 \lambda_*-\alpha_0-2r_\delta>0.
\tag{4.7}
\]

The executable rate ledger checks (4.6)--(4.7) once a genuine RFDE
roughness estimate supplies \(r_\delta\).  It does not manufacture that
estimate from frozen eigenvalues.  The needed nonlinear invariant-manifold
machinery is consistent with the RFDE moving-coordinate theory of
[Magalhães](https://doi.org/10.1137/0518051); applying it here still
requires the scaled-history hypotheses above.

## 5. Complete-history center-stable foliation

The tracker segment must be extended through the reset layer before an
invariant sheet is defined.  A finite-time orbit segment alone does not
select a unique codimension-one manifold: a terminal boundary condition can
change the sheet.  Gate U-OUT item 5 deliberately makes the overflowing or
terminal normalization part of the selected data, and Gate U-TR supplies
its normal splitting.  The sheet below is unique in that normalized graph
class, not preparation independent.

> **Theorem 5.1 (center-stable history sheet under U-OUT and U-TR).**
> Suppose Gates U-OUT and U-TR hold and the physical RFDE is \(C^2\) in
> history and \(C^1\) in \(u\) on one common scaled-history neighborhood.
> Then, after shrinking that neighborhood, the selected middle-history
> curve has a parameter-\(C^1\) local center-stable manifold
>
> \[
>  W^{cs}_{\delta,u,\mathrm{loc}}
>  \subset\widehat{\mathcal X}
> \tag{5.1}
> \]
>
> of codimension one.  Near
> \(\Gamma^m_{\delta,u}(\rho_R)\), it has a scalar complete-history
> defining function
>
> \[
>  G_{\delta,u}:\mathcal N\to\mathbb R,
>  \qquad
>  G_{\delta,u}^{-1}(0)=W^{cs}_{\delta,u,\mathrm{loc}},
> \tag{5.2}
> \]
>
> with
> \(D G_{\delta,u}\) nonzero on the strong unstable direction.  Normalize
> \(G\) so that its derivative at the tracker is the normalized strong
> unstable quotient covector.  For each
> fixed \(\delta\), the sheet is foliated by the local stable fibers over
> the selected history curve.  If the constants and parameter jets in
> U-TR are uniform, the local product radius and the \(C^1_u\) norms in
> (5.2) can be chosen uniformly.

**Proof.**  Work in moving coordinates along the exact curve (3.3).  The
invariant splitting (4.3) puts the linearized history evolution in
strong-unstable, tangent, and stable blocks.  The gap (4.4)--(4.5) makes the
Lyapunov--Perron graph transform for the center-stable graph a contraction;
the \(C^2\) history bound makes its derivative transform a contraction as
well.  This gives a \(C^1\) codimension-one graph over \(E^{cs}\).  Applying
the fixed-\(\delta\) stable graph transform inside that graph produces the
stable fibers over the one-dimensional base curve.  Parameter dependence
follows by differentiating the contractions.  A normalized coordinate on
the one-dimensional unstable quotient gives (5.2).  Uniform constants
follow from the uniform versions of the same contraction estimates.
\(\square\)

This theorem uses the complete history splitting.  Replacing (5.2) by the
sign of current voltage discards delayed endpoint terms and is not valid.

## 6. A reset whose singular transversality is exact

Let \(J_R\) be the two-by-two fast voltage Jacobian at the singular middle
point on \(\rho_R\).  It is irreducible Metzler and has a simple positive
eigenvalue.  Choose its positive right and left unstable vectors
\(e_u^0,p_u^0\) so that

\[
 \|e_u^0\|_2=1,
 \qquad
 (p_u^0)^Te_u^0=1.
\tag{6.1}
\]

This gives a nondegenerate voltage-reset direction.  Center a one-delay
causal reset at the current voltage of the selected tracker and put

\[
 \gamma_{\delta,u}(a)
 =v^m_{\delta,u}(\rho_R)+a e_u^0.
\tag{6.2}
\]

Use the exact hold history from the causal reset theorem, with terminal
collective recovery \(\rho_R\):

\[
 \widehat{\mathcal R}_{\delta,u}(a)(\vartheta)
 =\binom{
   \gamma_{\delta,u}(a)
 }{
   w_*+r[\rho_R+\delta(\xi_a-\mu)\vartheta]
      +q\delta^2\zeta_a/D_w
 },
 \qquad -\theta_*\le\vartheta\le0.
\tag{6.3}
\]

Because the reset voltage is held constant while a slow tracker changes by
\(O(\varepsilon)\) per fast-time unit, (6.3) is generally not the same
complete history as (1.5).  Under the U-OUT history bounds,

\[
 d_{\delta,u}
 :=\left\|
  \widehat{\mathcal R}_{\delta,u}(0)
  -\Gamma^m_{\delta,u}(\rho_R)
 \right\|_{\widehat{\mathcal X}}
 \le C\delta.
\tag{6.4}
\]

The \(O(\delta)\) scale is the slow displacement over one physical delay:
\(\varepsilon\tau_*=O(\delta)\).  A stronger bound may hold in selected
components, but is not needed below.

Indeed, (3.2) and the uniform \(C^1_r\) bound give
\[
 |\Phi_q^{\delta\vartheta}(\rho_R)-\rho_R|\le C\delta
\]
on the fixed scaled interval, and hence the tracker voltage history differs
from its endpoint by \(O(\delta)\).  Along the exact outer curve, the
transverse recovery equation gives
\[
 \varepsilon q_{\delta,u}(r)\partial_r\kappa(r)
 =\varepsilon\zeta(r)-D_w\kappa(r),
\]
so
\[
 \kappa(r)-\frac{\varepsilon}{D_w}\zeta(r)
 =-\frac{\varepsilon}{D_w}
   q_{\delta,u}(r)\partial_r\kappa(r)
 =O(\varepsilon).
\]
The collective reset history and the tracker both have endpoint
\(\rho_R\); integrating their \(C^1\) slow slopes over a scaled interval of
length \(O(1)\) contributes at most \(O(\delta)\).  These componentwise
bounds prove (6.4).

> **Lemma 6.1 (designed reset transversality).**  Suppose the normalized
> unstable covectors furnished by U-TR converge on constant voltage
> tangents to \(p_u^0\), uniformly on the parameter box.  Then
>
> \[
>  \left|D G_{\delta,u}
>   (\Gamma^m_{\delta,u}(\rho_R))
>   \partial_a\widehat{\mathcal R}_{\delta,u}(0)
>  \right|\ge\frac12
> \tag{6.5}
> \]
>
> after reducing \(\delta_0\).

**Proof.**  At \(\delta=0\), delayed feedback disappears and the reset
tangent in the fast voltage block is \(e_u^0\).  The limiting pairing is
one by (6.1).  U-TR convergence of the normalized unstable covector and the
\(C^1\) reset convergence make the left side of (6.5) tend uniformly to
one. \(\square\)

The singular pairing in (6.1) is proved and executable.  Its transfer to
the physical complete-history covector is part of U-TR, just as in the
clamped equilibrium proof.

## 7. The geometric separator theorem

Define the scalar reset-to-sheet map

\[
 g_{\delta,u}(a)
 =G_{\delta,u}(\widehat{\mathcal R}_{\delta,u}(a)).
\tag{7.1}
\]

> **Theorem 7.1 (unique selected unforced geometric reset separator,
> conditional model theorem).**  Suppose Gates U-OUT and U-TR hold,
> including the declared normalization and the
> uniform history bounds used in (6.4), and use the designed reset
> (6.2)--(6.3).  Then there are \(\delta_0,r,c_a,C>0\) such that, for
> every \(0<\delta\le\delta_0\) and every declared parameter \(u\),
> \(g_{\delta,u}\) has exactly one zero in \((-r,r)\):
>
> \[
>  a_{\rm sep}(\delta,u):
>  \widehat{\mathcal R}_{\delta,u}(a_{\rm sep})
>  \in W^{cs}_{\delta,u,\mathrm{loc}}.
> \tag{7.2}
> \]
>
> The root is \(C^1\) in \(u\),
>
> \[
>  |\partial_a g_{\delta,u}(a)|\ge c_a
> \tag{7.3}
> \]
>
> on a common root tube, and
>
> \[
>  |a_{\rm sep}(\delta,u)|
>  \le \frac{L_G}{c_a}d_{\delta,u}
>  \le C\delta.
> \tag{7.4}
> \]
>
> If a mathematical history reset is instead chosen to pass exactly through
> \(\Gamma^m_{\delta,u}(\rho_R)\), then
> \(a_{\rm sep}=0\) exactly.

**Proof.**  Theorem 5.1 gives \(G\), while Lemma 6.1 gives a derivative
bounded away from zero at the tracker.  The common \(C^1\) bounds preserve
its sign on a fixed tube.  Since \(G(\Gamma^m)=0\), (6.4) and the mean-value
bound give

\[
 |g_{\delta,u}(0)|\le L_Gd_{\delta,u}.
\]

A scalar monotonicity argument gives a zero within
\(L_Gd_{\delta,u}/c_a\), uniqueness follows from (7.3), and the
parameter-dependent implicit-function theorem gives \(C^1_u\) regularity.
This proves (7.2)--(7.4).  Exact centering makes \(g(0)=0\), proving the
last assertion. \(\square\)

The theorem is deliberately geometric and selection indexed.  It says that
one causal reset curve crosses one selected complete-history center-stable
sheet once.  It
does **not** say that the two signs of \(g\) reach the pulse and quiet
blocks.  Offsets of order \(e^{-A/\varepsilon}\) can shadow the middle
branch to the lower fold.  The companion
[lower-fold exchange audit](paper-iii-unforced-lower-fold-exchange.md)
shows a nonzero exponentially small displacement in the exact Airy normal
form.  Whether the physical RFDE root is displaced is conditional on its
complete-history nonzero fold-offset factorization; that fold map and the
downstream capture theorem remain separate from U-SF.

## 8. Exact next lemmas and stop/go decision

The shortest route to closing U-SF is now explicit.

1. **U-OUT-A (outer action matching).**  Construct the repelling
   curve-restricted history solution on the interval from a fixed outer
   section through \(\rho_R\).  Prove exact common-history overlap with the
   canonical graph.  A weaker version must prove a full
   \(C^1_u\) residual
   \[
     C\delta^{-M}e^{-(\mathcal A_R+\chi)/\delta^2+C_0/\delta}
   \]
   and a nonlinear action estimate preserving the positive margin
   \(\chi\).
2. **U-TR-A (scaled-history roughness).**  In moving modal coordinates,
   prove the unperturbed current equation has a one-dimensional unstable
   rate \(\lambda_*\), center-stable growth \(\alpha_0=O(\varepsilon)\),
   and that the delayed/moving-frame perturbation has a roughness loss
   \(r_\delta\) satisfying (4.7), including old-history translation and
   \(C^1_u\) projector bounds.
3. **U-SF-R (reset projection).**  Use the resulting unstable covector to
   verify its convergence on the explicit tangent (6.2).  The limiting
   value is already fixed to one by (6.1), so this step is a perturbation
   estimate rather than a new genericity assumption.

**STOP on declaring Gate U-SF proved for the physical RFDE.**  The exact
action shows why the missing U-OUT estimate cannot be replaced by the
existing algebraic retained-history bounds.  U-TR also needs an evolution
splitting, not a frozen root count.

**GO on the conditional theorem architecture.**  Once U-OUT-A and U-TR-A
are supplied, Theorem 7.1 gives the unique geometric separator without any
additional global pulse claim.  The repaired moving-tube/lower-fold map and
Gate U-CAP remain separate.

## 9. Proof-status ledger

| Statement | Status | Reason |
|---|---|---|
| Exact canonical outgoing retained history at the simple local root | Proved elsewhere | Canonical long-delay theorem |
| Unique causal forward orbit from that history | Proved for each fixed \(\delta\) | RFDE forward well-posedness |
| Singular middle branch reaches \(\rho_R=-1/2\) | Proved | Exact two-fold critical graph |
| Positive repelling action \(\mathcal A_R\) | Proved; decimal diagnostic only | Sign of (2.4), executable quadrature |
| Algebraic overlap control is sufficient for the outer tracker | False as an implication | Proposition 2.1 and Corollary 2.2 |
| Canonical physical orbit stays in the middle tube to \(\rho_R\) | Open | Gate U-OUT / exponential action matching |
| One unstable frozen current eigenvalue on the middle branch | Proved at the singular level | Exact fast Jacobian signs |
| Dominated nonautonomous complete-history trichotomy | Open | Gate U-TR; pointwise roots are insufficient |
| Center-stable history sheet from U-OUT and U-TR | Proved conditional implication | Theorem 5.1 |
| Singular reset direction is transverse | Proved exactly | Positive eigenvectors and pairing (6.1) |
| Positive-\(\delta\) complete-history reset transversality | Conditional on U-TR convergence | Lemma 6.1 |
| Unique geometric reset separator | Conditional model theorem | Theorem 7.1 |
| Separator is the pulse/quiet first-hit boundary | Not asserted; equality need not hold in the exact Airy model and is undecided for the physical RFDE | Requires the repaired fold-event map followed by U-CAP; physical noncoincidence requires the nonzero fold-offset factorization |
| Separator equals the canonical or physical maximal-canard root | Not asserted | Requires a separate reset-to-canard factorization |

The new mathematical content is the action budget: reaching the biological
reset layer is an exponentially stronger problem than matching on the
logarithmic right-fold tube.  It also isolates a publishable intermediate
result.  U-SF can yield a unique complete-history geometric separator before
the much harder lower-fold outcome theorem is attempted, but only after the
outer action and long-delay trichotomy are actually verified.
