# Paper III: from the physical outer canard to a pulse event

Status: **the singular two-channel theorem and the event-definition theorem
below are proved.  Persistence of either fast channel on a fixed layer is a
finite-time perturbation result.  The original backward-complete outer rule
is disproved as a sufficient selection principle, and the repaired
parameter-coherent Gate P3-A\(^*\) down to the logarithmic fold tube is open.
The causal one-delay reset history and existence of a positive-\(\varepsilon\)
reset-transition set are proved separately.  The former all-in-one Gate R-S
now splits into the U-SF geometric-history gate, the repaired U-EX
moving-tube/lower-fold event, and the U-CAP capture/no-return gate.  An exact
Airy obstruction shows that an ordinary drifting fold can displace the
lower-fold event root exponentially from the geometric middle-history root;
the physical RFDE comparison remains conditional on its fold-map
factorization.  Consequently this note does not relabel the preparation-indexed
JNS root, the geometric root, the fold-event root, and the biological pulse
root as one object.**

The exact singular algebra and numerical falsifiers are in
`src/canard_control/physical_pulse_bridge.py`; the regression tests are in
`tests/test_physical_pulse_bridge.py`.  Nothing here changes the frozen JNS
manuscript.

## 1. The question and the necessary distinction

The base theorem constructs a simple complete-history connection selected by
a local preparation.  Paper III has two separate tasks:

1. replace that preparation by attracting and repelling histories selected
   by the uncut physical RFDE; and
2. prove what a declared pulse detector does near the resulting physical
   maximal canard.

There are two inequivalent meanings of *pulse threshold*.

- A **channel threshold** classifies an orbit by which of two disjoint exit
  channels it reaches first.  Its event error is exactly zero relative to its
  proved first-hit separator.  For the unforced reset route that separator is
  the lower-fold event root \(\mu_{\rm EX}\) only after U-SF, the complete-history
  fold map, and U-CAP are proved.  Equality with a geometric or maximal-canard
  root is a separate theorem.
- An **amplitude threshold** fixes an observable and a level.  An orbit need
  only shadow a finite portion of the repelling branch to reach that level.
  Its parameter is generally different from the maximal-canard parameter.
  Under an exchange estimate the difference is exponentially small on the
  logarithmic scale, with an action determined by the detector location.

These definitions cannot be interchanged.  In particular, a transverse
finite-time section crossing cannot by itself appear or disappear at an
interior parameter value.  This elementary obstruction is proved in
Section 5 and changes the statement originally proposed for Paper III.

## 2. Exact singular geometry of the two-module model

Write

\[
 \sigma=\sqrt{\frac32},\qquad
 \xi=\ell^T(v-v_*)
      =\frac12(v_1-\sigma)+\frac14v_2,
 \qquad \rho=\ell^T(w-w_*).
\]

At \(\varepsilon=0\), the transverse recovery equation imposes

\[
 w_1=\rho,\qquad w_2=2\sigma+2\rho.
\tag{2.1}
\]

Put \(v_1=\sigma a\) and \(v_2=\sigma b\).  Eliminating \(\rho\) from the
two fast equilibrium equations gives

\[
 G(a,b):=2a^3+2a-4b-b^3-4=0.
\tag{2.2}
\]

Since

\[
 G_b(a,b)=-4-3b^2<0,
\tag{2.3}
\]

(2.2) defines one global smooth graph \(b=b(a)\).  On that graph,

\[
 \xi(a)=\sigma\left(\frac{a-1}{2}+\frac{b(a)}4\right),
 \qquad
 \rho(a)=\frac{\sigma}{2}\bigl(a-a^3+b(a)\bigr).
\tag{2.4}
\]

The fold equation \(\rho'(a)=0\) is

\[
 F(a,b):=2+b^2-2a^2-3a^2b^2=0.
\tag{2.5}
\]

Eliminating \(b\) gives

\[
 \operatorname{Res}_b(G,F)=-4(a-1)Q(a),
\tag{2.6}
\]

where

\[
\begin{aligned}
Q(a)={}&27a^{11}+27a^{10}+54a^9-54a^8-72a^7-72a^6\\
 &+76a^5+148a^4-23a^3-55a^2+2a+6.
\end{aligned}
\tag{2.7}
\]

The exact Sturm chain for \(Q\) has six sign variations at \(-\infty\) and
five at \(+\infty\).  It therefore has one real root.  The variations at
\(-743/1000\) and \(-742/1000\) are respectively six and five, so that root
lies in this rational interval.  The linear subresultant recovers the unique
common value of \(b\); its reality can also be checked directly from

\[
 b^2=\frac{2(a^2-1)}{1-3a^2}>0
\]

throughout that rational interval.  Thus this resultant root lifts to a
real point of (2.2)--(2.5).  Hence the critical graph has exactly two folds:

\[
\begin{array}{c|c|c|c}
 &a&\xi&\rho\\ \hline
 \mathfrak f_-&-0.7423089465\ldots&-1.4259744889\ldots
        &-0.9221564930\ldots\\
 \mathfrak f_0&1&0&0.
\end{array}
\tag{2.8}
\]

The decimals in (2.8) are diagnostics; the exact fold count is (2.3),
(2.6), and the rational Sturm calculation.

### 2.1 Stability and absence of competing fast cycles

For fixed \(w\), the fast voltage field is

\[
\begin{aligned}
 f_1(v,w)&=v_1-v_1^3/3-w_1+(v_2-v_1)/2,\\
 f_2(v,w)&=v_2-v_2^3/3-w_2+2(v_1-v_2).
\end{aligned}
\tag{2.9}
\]

It is a weighted gradient system.  Define

\[
\begin{aligned}
 U(v;w)={}&\frac13v_1^4-v_1^2-2v_1v_2+4w_1v_1\\
 &+\frac12v_2^2+\frac1{12}v_2^4+w_2v_2.
\end{aligned}
\tag{2.10}
\]

Then

\[
 (4f_1,f_2)^T=-\nabla_vU,
 \qquad
 \frac{dU}{dt}=-4f_1^2-f_2^2.
\tag{2.11}
\]

The potential is coercive.  Thus the fast subsystem has no nonconstant
periodic orbit, recurrent competing attractor, or escape to infinity.
Moreover its Jacobian has positive off-diagonal entries, so the flow is
strongly cooperative.

Along the critical graph,

\[
 \operatorname{tr}D_vf=-\frac12-v_1^2-v_2^2<0,
 \qquad
 \det D_vf=-\frac34F(a,b).
\tag{2.12}
\]

It follows from (2.8)--(2.12) that the two outer branches are attracting and
the branch between the folds is a saddle branch.

## 3. A proved singular pulse/quiet channel theorem

Let \(\rho_-\) denote the recovery value at \(\mathfrak f_-\).  For every
\(\rho_0\in(\rho_-,0)\), the fast layer (2.9) with (2.1) has exactly three
equilibria

\[
 v^-(\rho_0)<v^m(\rho_0)<v^+(\rho_0)
\tag{3.1}
\]

in componentwise order.  The outer equilibria are attracting nodes and the
middle equilibrium is a saddle.

> **Theorem 3.1 (singular two-channel separator).**  At every
> \(\rho_0\in(\rho_-,0)\), the two components of
> \(W^u(v^m(\rho_0))\setminus\{v^m(\rho_0)\}\) are heteroclinic orbits.  The
> lower component converges to \(v^-(\rho_0)\), and the upper component
> converges to \(v^+(\rho_0)\).  Both voltage components, and hence
> \(\xi\), are strictly monotone along either orbit.  Therefore every level
> of the fixed weighted observable
> \[
> H(v):=-\ell^T(v-v_*)=-\xi(v)
> \tag{3.2}
> \]
> strictly between its saddle and endpoint values is crossed exactly once
> and transversely.  There is no competing fast return.

**Proof.**  The monotonicity of \(\rho(a)\), the two-fold count, and its
limits at infinity give exactly three equilibria.  Equation (2.12) gives
their stability.  The positive eigenvalue at the saddle has a strictly
positive eigenvector because the Jacobian is irreducible Metzler.  On the
upper unstable branch, \(\dot v\) is eventually componentwise positive as
time tends to \(-\infty\).  It solves the strongly positive variational
equation \(\dot y=D_vf(v(t),w)y\), and is therefore componentwise positive
for every finite time.  The lower branch is analogously componentwise
negative.  Coercivity and (2.11) make either forward orbit precompact and
force its omega limit to be an equilibrium.  Strict order and (3.1) identify
the upper and lower limits.  Since \(\ell\) has positive entries, (3.2) is
strictly monotone on the two connections.  This proves uniqueness and
transversality of every stated crossing.  Equation (2.11) excludes a fast
cycle or another recurrent return. \(\square\)

For a concrete fixed layer, take \(\rho_0=-1/2\).  The three critical
coordinates are

\[
 \xi^-=-1.8891168\ldots,\qquad
 \xi^m=-0.8551591\ldots,\qquad
 \xi^+=0.6580668\ldots.
\tag{3.3}
\]

Thus the lower connection crosses the pulse witness

\[
 \Sigma_{\rm p}^{0}=\{H=7/5\},
\tag{3.4}
\]

and the upper connection crosses the quiet witness

\[
 \Sigma_{\rm q}^{0}=\{H=0\}.
\tag{3.5}
\]

The executable integration gives

\[
 \dot\xi|_{\Sigma_{\rm p}^{0}}=-0.32215\ldots,
 \qquad
 \dot\xi|_{\Sigma_{\rm q}^{0}}=0.49894\ldots,
\tag{3.6}
\]

and monotonically decreasing potential.  These numbers falsify sign and
grazing mistakes; they are not interval enclosures.

> **Corollary 3.2 (fixed-layer finite-time persistence).**  Fix compact
> parameter sets with \(D_w\ge d_0>0\), compact pieces of the two singular
> connections containing (3.4)--(3.5) but not their equilibria, and a fixed
> fast-time existence interval.  Require the singular crossing times to stay
> a fixed positive distance from its endpoints, the section functions at
> those endpoints to have opposite signs separated from zero by \(c_0>0\),
> and require \(\dot H\) to have a fixed sign with
> \(|\dot H|\ge c_0\) on each entire retained singular piece.  Let the initial
> compatible histories be uniformly bounded on the full physical history
> interval by a declared constant \(M_h\), let all weak gains and delay atoms
> lie in a fixed compact set, let their current endpoints be
> \(O(\varepsilon)\)-close to the
> selected singular initial points, and let their transverse recovery
> components be \(O(\varepsilon)\).  Then, for sufficiently small
> \(\varepsilon>0\), the corresponding full-RFDE orbit pieces exist on that
> fixed interval, remain uniformly close to the singular pieces, and each
> cross its corresponding section exactly once and transversely.

**Proof.**  The history bound and compact parameter set make the delayed
feedback uniformly \(O(\varepsilon)\) on the declared interval, while
\(\rho\) changes by \(O(\varepsilon)\).  The lower bound on \(D_w\) gives a
uniform transverse recovery estimate.  Finite-time continuous dependence
and Gronwall's inequality therefore give uniform state and velocity
closeness to the two singular compact orbit pieces.  The uniform fixed-sign
bound for \(\dot H\) persists, so each perturbed piece is monotone in \(H\);
the endpoint signs give existence and monotonicity gives uniqueness of the
corresponding crossing. \(\square\)

Corollary 3.2 does **not** say that the physical attracting canard trace
lands on one of these pieces.  That missing implication is exponentially
sensitive and is the purpose of the outer-history and exchange estimates.

## 4. The physical outer-history theorem still required

In slow time \(T=\varepsilon t\), the physical delays satisfy

\[
 T(t)-T(t-\theta_k/\delta)=\delta\theta_k.
\tag{4.1}
\]

Thus the delay is short along a slow orbit even though it is long in fast
time.  This observation is not by itself a history-manifold theorem.  The
repelling selection in particular must consist of backward-extendible
complete histories, whereas a retarded semiflow is not invertible on an
ambient history neighborhood.

The originally proposed rule is underdetermined.  Bounded complete backward
extension leaves the coefficient of the repelling forward-unstable normal
mode free; even exponentially close choices may have arbitrarily large
mixed parameter derivatives.  The exact RFDE-subclass counterexample and a
curve-restricted repair are proved in
[paper-iii-outer-selection-blocker-and-repair.md](paper-iii-outer-selection-blocker-and-repair.md).
The well-posed replacement is the following.

> **Gate P3-A\(^*\) (compatible physical outer continuation; open).**  On
> fixed compact attracting and repelling branch segments, solve the
> curve-restricted Lyapunov--Perron equations with declared stable and
> unstable boundary coordinates, phase, and one common-history-graph
> compatibility normalization.  Prove existence and uniqueness in this
> normalized class and \(C^1_\nu C^2_\eta\) strong-history regularity.  The
> selected curves reach the matching
> radius
> \[
> r_\delta=\frac12\delta S_\delta
>       (1+O(S_\delta^{-2})),\qquad
> S_\delta=\sqrt{2p\log(1/\delta)},
> \tag{4.2}
> \]
> and every retained delay backtrack lies in the uncut physical tube.  In
> fold coordinates their traces and the indicated parameter derivatives
> obey
> \[
> C\delta^{-M}\langle S_\delta\rangle^m e^{cS_\delta},
> \tag{4.3}
> \]
> with \(c,m,M,C\) fixed before \(p\) is chosen.  On the overlap they lie on
> the same exact complete-history graph as the local fold construction.  The
> fixed outer-to-inner boundary influence obeys the stronger target
> \[
> C\delta^{-M_0}e^{-A_*/\delta^2+C_0/\delta},
> \qquad A_*>0,
> \tag{4.3a}
> \]
> including the declared mixed history jets.

If Gate P3-A\(^*\) holds, the Gaussian endpoint estimate already proved for the
canonical connection gives, after increasing fixed \(p\),

\[
 \|d_{\rm phys}-d_{\mathcal P}\|_{C^1_\nu C^2_\eta}
 =O(\delta^N)
\tag{4.4}
\]

for any preassigned finite \(N\).  Since
\(\partial_\nu d_{\mathcal P}=\sqrt{2\pi}\delta+O(\delta^2)\), the physical
gap then has one root and

\[
 \mu_{\rm can}(\delta,\eta)-\mu_{c,\mathcal P}(\delta,\eta)
 =O(\delta^{N+1}).
\tag{4.5}
\]

Taking \(N>2\) makes this outer-selection error
\(o(\delta^3)=o(\varepsilon^{3/2})\), so the base response coefficient
transfers to the physical maximal canard.

The missing proof is not ordinary fixed-distance Fenichel theory.  It must
first close the normalized curve-wise dichotomy and exact common-graph
gluing; backward completeness alone supplies neither.  Down to
(4.2), a fixed fold-chart delay backtrack has a derivative loss
\(e^{cS_\delta}\).  One must prove the tame bound (4.3), rather than allow an
uncontrolled \(e^{c/\delta^2}\), and must do so for the full history and its
mixed parameter jets.  A characteristic-root count or current-state slow
manifold does not provide this statement.

For a biological pulse experiment, the causal alternative is developed in
`paper-iii-causal-reset-separator.md`.  A voltage hold of at least
one maximal physical delay, together with a declared collective-recovery
preset, produces an explicit released complete history and removes the
nonunique outer-family choice.  Opposite pulse/quiet endpoint outcomes and a
nonempty transition set are proved.  A voltage hold by itself does not erase
collective recovery error, and the transition set is not yet proved to be a
single basin boundary; that is the signed-exchange Gate R-S.

## 5. What can and cannot define an operational threshold

Let \(x(t;\mu)\) be a \(C^1\) family of solutions and let a section be
\(\Sigma=\{S(x)=0\}\).

> **Lemma 5.1 (transverse crossing is not an event boundary).**  If
> \(t_0\) and \(\mu_0\) are interior points of their declared time and
> parameter intervals,
> \(S(x(t_0;\mu_0))=0\) and
> \(D S(x(t_0;\mu_0))\dot x(t_0;\mu_0)\ne0\), then every \(\mu\) in a
> neighborhood of \(\mu_0\) also has a unique crossing in a fixed local
> time neighborhood of \(t_0\).  Hence
> \(\mu_0\) is an interior point, not a boundary, of the event
> \(\{\mu:x(\cdot;\mu)\text{ crosses }\Sigma\}\).

**Proof.**  Apply the implicit-function theorem to
\(F(t,\mu)=S(x(t;\mu))\) at \((t_0,\mu_0)\). \(\square\)

Consequently, “define a threshold by a transverse pulse section, exclude
grazing and competing exits, and solve for the first parameter at which the
section is crossed” is not a coherent local theorem.  One must choose one of
the following definitions.

### 5.1 Channel threshold: three roots that must not be identified

Choose a declared one-parameter family of complete entry histories and two
disjoint pulse and quiet exit blocks, and classify locally by the first block
hit.  There are three different roots in the unforced construction.

1. Gate U-SF, if closed, gives the **geometric middle-history root**
   \(\mu_{\rm geo}\), the zero of a complete-history unstable coordinate on the
   selected saddle tracker.
2. The moving outer tube, lower-fold cap, and complete-history fold map in the
   repaired Gate U-EX give the **fold-event root** \(\mu_{\rm EX}\), if their
   conditional transition hypotheses are verified.
3. Only Gate U-CAP can identify the two signed outer/fold exits with the
   biological pulse and quiet first-hit blocks.

The exact Airy ordinary-fold calculation in
`paper-iii-unforced-lower-fold-exchange.md` shows that, for fixed positive
\(\varepsilon\), the first two roots need not agree.  Under that note's
uniform factorization hypotheses and a simple parameter pullback,

\[
 \varepsilon\log|\mu_{\rm EX}-\mu_{\rm geo}|
 \longrightarrow-\mathcal A_-.
\]

Now suppose U-SF and the complete-history fold map hold, \(\mu_{\rm EX}\) is
the unique transverse root in an open interval \(I_u\), and U-CAP proves that
its two signs reach the two declared blocks first.  Then the relative boundary
is

\[
 \partial_{I_u}\{\mu\in I_u:\text{pulse block is reached first}\}
 =\{\mu_{\rm EX}\}.
\tag{5.1}
\]

For this definition,

\[
 \boxed{\mu_{\rm pulse}^{\rm channel}=\mu_{\rm EX}.}
\tag{5.2}
\]

Equation (5.2) is an exact event-definition identity relative to the proved
fold-event separator.  It is not an assertion that
\(\mu_{\rm EX}=\mu_{\rm geo}\) or \(\mu_{\rm EX}=\mu_{\rm can}\).  The latter
comparisons require separate reset-to-canard factorization and, for exact
equality across an ordinary fold, an additional cancellation not supplied by
channel separation.

### 5.2 Fixed-observable amplitude threshold

Fix a weighted observable \(H\) and a level \(A_*\).  On a specified entry
history define, over a declared slow-time horizon
\(T_*(\varepsilon)=O(\varepsilon^{-1})\) in fast time,

\[
 M_H(\mu)=\max_{0\le t\le T_*}H(x(t;\mu)).
\tag{5.3}
\]

To make \(M_H\) differentiable, prove that the maximizing time is unique,
interior, and nondegenerate, and exclude peak switching.  If
\(\partial_\mu M_H\ne0\) at \(M_H=A_*\), this equation defines
\(\mu_{\rm pulse}^{H,A_*}\).  The maximum is a tangency in time; it should
not be called a transverse section threshold.

The singular action along the middle branch is explicit.  Let \(a_H\) be a
detector-determined point between the folds and let \(\lambda_u(a)>0\) be
the positive fast eigenvalue there.  Then

\[
 \mathcal A_H
 =\int_{1}^{a_H}
   \lambda_u(a)\frac{\rho'(a)}{\xi(a)}\,da>0.
\tag{5.4}
\]

On the middle branch, \(\xi<0\), \(\rho'>0\), and \(\lambda_u>0\), while
the integral is oriented from \(1\) down to \(a_H\); hence its sign is
positive.  The fold-end singularity in this slow coordinate is removable,
so the displayed action is finite.

For example, the point \(H=-\xi=1\) on the saddle branch gives

\[
 a_H=-0.1797305256\ldots,\qquad
 \mathcal A_H=0.7047846186\ldots.
\tag{5.5}
\]

Here a positive family \(g_\varepsilon\) is called uniformly two-sided
subexponential on \(U\) if, for every \(\kappa>0\), both
\(\sup_U g_\varepsilon\) and
\(\sup_U g_\varepsilon^{-1}\) are at most
\(C_\kappa e^{\kappa/\varepsilon}\) for sufficiently small
\(\varepsilon\).

> **Theorem 5.2 (quantitative local detector chart).**  Let \(U\) be a
> compact control box.  Assume Gate P3-A\(^*\) and let
> \(d_\varepsilon(\mu,u)\) be the physical gap with simple local root
> \(\mu_{\rm can}(u)\).  Suppose a proved exchange/landing chart produces a
> detector equation
> \[
> \mathscr E_\varepsilon(\mu,u)
> =P_\varepsilon(u)e^{\mathcal A_H(u)/\varepsilon}
>  d_\varepsilon(\mu,u)-b_\varepsilon(u)
>  +R_\varepsilon(\mu,u)=0
> \tag{5.6}
> \]
> on the explicit tube
> \[
> \mathcal T_\varepsilon
> =\left\{(\mu,u):u\in U,\quad
> |\mu-\mu_{\rm can}(u)|
> \le K_\varepsilon(u)e^{-\mathcal A_H(u)/\varepsilon}
> \right\},
> \tag{5.6a}
> \]
> contained in the simple-gap chart.  Put
> \(m_\varepsilon^-(u)=\inf_{\mathcal T_\varepsilon(u)}
> |\partial_\mu d_\varepsilon|\), with constant derivative sign.  Assume
> \(\mathcal A_H\in C^1(U)\), \(\inf_U\mathcal A_H>0\), and
> \[
> K_\varepsilon(u)m_\varepsilon^-(u)
> \ge2\left|\frac{b_\varepsilon(u)}{P_\varepsilon(u)}\right|.
> \tag{5.6b}
> \]
> The positive families \(K_\varepsilon,|P_\varepsilon|,
> |b_\varepsilon|,m_\varepsilon^-\) are uniformly two-sided
> subexponential.  The \(C^1_u\) norms of
> \(K_\varepsilon,P_\varepsilon,b_\varepsilon,
> \mathcal A_H,\mu_{\rm can}\) and the \(C^1_uC^2_\mu\) norm of
> \(d_\varepsilon\) have uniform subexponential upper bounds.  Finally assume
> \[
> \left\|R_\varepsilon/b_\varepsilon\right\|_{C^1_{\mu,u}}
> \longrightarrow0
> \tag{5.7}
> \]
> on that tube.  Then (5.6) has a unique local root branch
> \(\mu_H(u)\), and, uniformly on \(U\),
> \[
> \varepsilon\log|\mu_H(u)-\mu_{\rm can}(u)|
> \longrightarrow-\mathcal A_H(u).
> \tag{5.8}
> \]
> For every \(0<\Lambda<\inf_U\mathcal A_H\),
> \[
> \|\mu_H-\mu_{\rm can}\|_{C^1(U)}
> \le C_\Lambda e^{-\Lambda/\varepsilon}.
> \tag{5.9}
> \]

**Proof.**  Divide (5.6) by \(b_\varepsilon\).  The two-sided
subexponential bounds and (5.7) give, at a root,

\[
 d_\varepsilon(\mu,u)
 =e^{-\mathcal A_H(u)/\varepsilon}
  \frac{b_\varepsilon(u)}{P_\varepsilon(u)}
  \bigl(1+o_{C^1}(1)\bigr).
\tag{5.10}
\]

With \(m_{0,\varepsilon}(u)=
\partial_\mu d_\varepsilon(\mu_{\rm can}(u),u)\), use the frozen-slope map

\[
 \mathcal N_\varepsilon(\mu,u)
 =\mu-
 \frac{\mathscr E_\varepsilon(\mu,u)}{
 P_\varepsilon(u)e^{\mathcal A_H(u)/\varepsilon}
 m_{0,\varepsilon}(u)}.
 \tag{5.10a}
\]

Condition (5.6b), (5.7), and the derivative lower bound make (5.10a) a
self-map of (5.6a).  The subexponential derivative bounds times
\(e^{-\inf\mathcal A_H/\varepsilon}\) make its derivative smaller than
\(1/2\) after reducing \(\varepsilon_0\).  Thus it has exactly one local
fixed point.  Equivalently, the \(\mu\)-derivative of the leading term in
(5.6) dominates \(\partial_\mu R_\varepsilon\), so the implicit-function
theorem continues this root over \(U\).  Taylor expansion of the simple gap at
\(\mu_{\rm can}\), with its two-sided subexponential slope and quadratic
bound, converts (5.10) into the same formula for
\(\mu_H-\mu_{\rm can}\) with a two-sided subexponential prefactor.  This
proves (5.8).  Differentiation in \(u\) introduces at most the factor
\(\varepsilon^{-1}\|D_u\mathcal A_H\|\) and the declared subexponential
losses.  Every such factor is absorbed by
\(e^{-(\inf\mathcal A_H-\Lambda)/\varepsilon}\), proving (5.9).
\(\square\)

The present work does **not** derive the model-specific chart (5.6) or
determine its algebraic prefactor.  A nonzero landing derivative alone is
not enough: the target \(b_\varepsilon\), propagation factor
\(P_\varepsilon\), gap slope, and their inverses all need two-sided
subexponential control, and the normalized remainder must satisfy (5.7).
These data depend on the inner-to-outer conversion and detector landing map.
The conclusion can fail if a target is itself exponentially small on a
different action scale, the peak switches, or the detector is placed in a
channel whose threshold is exactly (5.2).

## 6. The positive-epsilon theorem chain

The shortest honest Paper III chain is now:

1. **Choose the preparation.**  For an intrinsic physical maximal canard,
   construct the normalized common-graph outer histories in open Gate
   P3-A\(^*\).  For an operational theorem, use the proved causal released
   history in `paper-iii-causal-reset-separator.md`.
2. **Intrinsic physical root transfer.**  Under P3-A\(^*\), use the proved
   Gaussian trace-to-gap theorem to obtain (4.4)--(4.5) and the physical
   maximal-canard response.
3. **Geometric middle-history coordinate.**  Close U-SF to construct the
   complete-history saddle tracker, its selected codimension-one
   relative-growth history graph and defining covector, and the simple reset
   intersection \(\mu_{\rm geo}\).  Its sign may classify transverse
   side exits before the lower-fold cap; it does not classify every
   exponentially small offset through the fold.
4. **Moving-tube and lower-fold event.**  Close the repaired U-EX hypotheses:
   propagate the complete history to the moving side/cap event and prove the
   cap-to-outgoing-section fold map.  Under its declared nonzero fold-offset
   factorization this gives \(\mu_{\rm EX}\) with
   \[
   \varepsilon\log|\mu_{\rm EX}-\mu_{\rm geo}|
   \longrightarrow-\mathcal A_-.
   \tag{6.1}
   \]
5. **Physical capture and no return.**  Close U-CAP by proving that each
   signed outer side exit and lower-fold outgoing history reaches a valid
   moving, latched pulse or quiet target first.  The old fixed-\(\rho_0\)
   passage blocks do not cover late exits; the exact obstruction and the
   finite-deadband/global-basin alternatives are in
   `paper-iii-unforced-capture-no-return.md`.  The frozen
   weighted-gradient/cooperative fast layer does not by itself prove this
   RFDE statement.
6. **Choose the event definition.**  Only after step 5 use (5.2) for a
   channel safety coordinate.  Alternatively, prove the full quantitative
   chart hypotheses (5.6)--(5.7) and use (5.8)--(5.9) for an amplitude safety
   coordinate.

The errors must remain separate:

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
 \varepsilon\log E_{\rm event}^{H}\to-\mathcal A_H,
\tag{6.2}
\]

with the Lin and numerical enclosure errors reported independently.

## 7. What is analytic and what needs certification

| Claim | Status | Evidence still required |
|---|---|---|
| Unique global critical graph, exactly two folds | Proved | Exact elimination and Sturm count are executable |
| Outer stable branches and middle saddle branch | Proved | Exact trace/determinant identities |
| Two singular fast channels, no fast cycle, no fast grazing of regular weighted levels | Proved | Weighted gradient and strong cooperation |
| Concrete fixed-layer section signs | Numerically checked, analytically implied by the channel theorem | Interval enclosures are desirable for publication constants |
| Fixed-time persistence of compact fast pieces | Proved by RFDE continuous dependence | Publication version should declare the history tube and uniform constants |
| Original backward-complete outer selection | Disproved as sufficient | It leaves the repelling unstable coefficient and mixed jets undetermined |
| Compatible attracting/repelling history selection to the logarithmic tube | Open Gate P3-A\(^*\) | Normalized curve-wise dichotomy, mixed strong-history jets, fixed-to-log trace estimate, and exact common-graph gluing |
| Physical complete-history maximal canard | Conditional on Gate P3-A\(^*\) | Gaussian root transfer is already available |
| Causal one-delay released history | Proved exactly | Explicit voltage-hold/recovery-preset history and exact memory-erasure identity |
| Unknown collective recovery is erased by the hold | False | Its error is invariant; it must be preset, measured, or controlled |
| Opposite reset outcomes and a nonempty transition set | Proved for small positive \(\varepsilon\) | Singular channel endpoints, finite-time persistence, and connectedness |
| Unique unforced reset separator/simple event root | Decomposed into U-SF, repaired U-EX, and U-CAP | U-SF gives only the geometric root; U-EX gives the conditional fold-event root; U-CAP is still open |
| Geometric-gap sign classifies every channel outcome | False as an all-offset shortcut | Exact Airy ordinary-fold obstruction; replace by the moving tube, fold map, and U-CAP |
| Old fixed-\(\rho_0\) blocks capture every late exit | False as an implication | Physical detector-drift mismatch and exact two-channel no-hit counterexample |
| Deadband U-CAP | Conditional finite-chain implication proved | Moving latched targets and full-history flux enclosures remain to be certified |
| Exact U-CAP | Open global RFDE gate | Requires the two-basin invariant/stable-set exclusions, not a finite-time perturbation argument |
| Channel threshold error | Exactly zero relative to \(\mu_{\rm EX}\) only after exact U-CAP | The conditional fold factorization gives an exponential comparison with \(\mu_{\rm geo}\); equality with \(\mu_{\rm can}\) is not asserted |
| Amplitude-detector threshold error | Abstract quantitative chart implication proved; model chart open | Two-sided subexponential target/prefactor bounds, \(C^1\)-small normalized landing remainder, unique local peak branch, no peak switching, interval/DDE certification |

The executable tests deliberately fail if the potential identity, fold
count, branch stability, crossing orientation, or action sign changes.  They
do not certify Gate P3-A\(^*\) or the exchange/landing hypotheses.
