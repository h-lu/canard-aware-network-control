# Paper III Gate U-CAP: what can be captured after the lower fold

Status: **the original all-offset U-CAP claim with the old fixed-reset-layer
pulse/quiet blocks does not follow from the proved singular channels or from a
complete-history lower-fold event map.  A physical singular calculation below
shows that a cap-tracking orbit reaches the declared voltage level a fixed
slow distance away from those blocks.  An exact ODE, hence RFDE-subclass,
counterexample has a simple separator and two attracting channels but a
punctured set of nonzero offsets that misses both fixed-layer target sections.
A finite-deadband complete-history isolating-chain theorem and an exact
two-basin implication are proved below.  Their model-specific inequalities
and invariant-set exclusions have not been verified for the two-module RFDE.
Thus biological U-CAP remains open; the repaired one-passage fold score is an
operational coordinate, not yet a biological pulse boundary.**

The executable physical-level calculation and exact counterexample are in
`src/canard_control/unforced_capture_audit.py`; regressions are in
`tests/test_unforced_capture_audit.py`.  Nothing here changes the frozen JNS
manuscript.

## 1. The three inputs do not yet imply capture

Assume for this note that the preceding gates have supplied:

1. the two singular frozen-layer heteroclinic channels;
2. a U-SF selected middle history and its signed relative-growth graph
   coordinate; and
3. the repaired U-EX moving tube, side exits, lower-fold cap, and conditional
   complete-history fold map.

Let \(\mathcal E_{\varepsilon,u}^{-}\) and
\(\mathcal E_{\varepsilon,u}^{+}\) denote the signed complete histories on the
outer side faces and fold outgoing section.  U-CAP was intended to prove

\[
 \mathcal E_{\varepsilon,u}^{-}\longrightarrow\mathfrak B_{\rm p}^\varepsilon,
 \qquad
 \mathcal E_{\varepsilon,u}^{+}\longrightarrow\mathfrak B_{\rm q}^\varepsilon,
 \tag{1.1}
\]

with no third outcome, no earlier competing hit, and no ambiguity for
arbitrarily small nonzero fold score.  There are two independent problems.

- The old blocks \(\mathfrak B_j^\varepsilon\) live in an
  \(O(\varepsilon)\) recovery tube about the reset layer
  \(\rho_0=-1/2\).  A late side exit or lower-fold passage occurs a fixed slow
  distance away.
- Even after replacing those blocks by moving targets, local fold data do not
  exclude a third invariant set, a grazing hit, a delay-induced instability,
  or a later global itinerary.  Those are global complete-history statements.

The word *no-return* also needs care.  The event in the causal-reset note is a
**latched first hit**.  A later biological recovery or another pulse cannot
change which block was hit first.  If instead the target is required to trap
the state forever, that is a different and usually inappropriate theorem for
an oscillator; it requires a positively invariant target cylinder.

## 2. The old physical passage blocks are at the wrong slow base

The collective recovery equation is exact:

\[
 \dot\rho=\ell^T\dot w=\varepsilon(\xi-\mu).
 \tag{2.1}
\]

For the declared reset and \(\mu=0\), the middle equilibrium has

\[
 \rho_0=-\frac12,\qquad
 H_m(\rho_0)=-\xi_m(\rho_0)=0.8551590808\ldots.
 \tag{2.2}
\]

At the lower fold,

\[
 \rho_-=-0.9221564931\ldots,\qquad
 H_-=-\xi_-=1.4259744890\ldots.
 \tag{2.3}
\]

The declared pulse witness is \(H=7/5\).  Since \(\xi(a)\) is strictly
increasing on the middle segment, it has one middle-branch crossing.  Direct
evaluation of the exact critical graph gives

\[
 a_H=-0.7101925628\ldots,\qquad
 \rho_H=-0.9209995693\ldots,\qquad
 |\rho_H-\rho_0|=0.4209995693\ldots.
 \tag{2.4}
\]

The decimal locates the obstruction; it is not an interval enclosure.
Monotonicity and the exact fold bounds prove the existence and uniqueness of
the crossing.

> **Proposition 2.1 (fixed-layer detector mismatch).**  Fix the old recovery
> tube
> \[
>   |\rho-\rho_0|<c_{\rm out}\varepsilon
>   \tag{2.5}
> \]
> with \(c_{\rm out}\) independent of \(\varepsilon\).  For every
> \(\varepsilon<|\rho_H-\rho_0|/c_{\rm out}\), the middle-branch crossing
> \(H=7/5\) lies outside (2.5).  More generally, a retained moving-tube
> trajectory that leaves (2.5), remains in a region
> \(\xi-\mu\le-c_\rho<0\), and reaches the lower-fold cap cannot hit either
> old block before the cap.

**Proof.**  The first statement is the displayed distance comparison.  For
the second, (2.1) makes \(\rho\) strictly decreasing.  Both old blocks require
(2.5), so after its outward crossing no later point before the cap can enter
either block. \(\square\)

This proposition does not say what happens after a full relaxation return.
It says something more basic: the old blocks are finite fast-passage witnesses
for exits prepared at \(\rho_0\), not global targets for exponentially delayed
exits.  Reusing them in (1.1) is an event-definition error.

There is also no local two-channel theorem after an ordinary saddle-node.
In the exact dynamic-fold normal form

\[
 \dot x=x^2-y,\qquad \dot y=-\varepsilon,
 \tag{2.6}
\]

both signs of \(x\) at \(y=0\) ultimately move toward increasing \(x\) once
\(y<0\).  The fold-side score distinguishes passage timing and finite-section
location, but its two signs are not automatically two different asymptotic
channels.  The physical RFDE may have additional transverse geometry, but
that must be proved by its complete-history landing map; the ordinary-fold
orientation alone supplies no such conclusion.

## 3. An exact two-channel counterexample to fixed-layer capture

The obstruction does not require a third attractor.  Consider

\[
 \dot z=z(1-z^2),\qquad
 \dot r=-\varepsilon c,\qquad
 \varepsilon,c>0.
 \tag{3.1}
\]

This ODE is an RFDE whose functional ignores the history for every declared
delay.  The sheet \(z=0\) is a simple separator, \(z=-1\) and \(z=1\) are
the two attracting channels, and an upstream fold map may be appended with
the identity outgoing coordinate \(z_0=a\).

Fix \(0<R<1\), \(h>0\), and the two target sections

\[
\begin{aligned}
 \mathcal T_-&=\{z=-R,\ |r-r_0|<h\varepsilon\},\\
 \mathcal T_+&=\{z= R,\ |r-r_0|<h\varepsilon\}.
\end{aligned}
\tag{3.2}
\]

For \(0<|a|<R\), the assigned channel section is reached at

\[
 T_R(a)=\frac12\log
 \frac{R^2(1-a^2)}{a^2(1-R^2)}.
 \tag{3.3}
\]

At that time the recovery displacement is
\(\varepsilon cT_R(a)\).  The exact critical initial magnitude is

\[
 a_*=\frac{R}{\sqrt{R^2+(1-R^2)e^{2h/c}}}.
 \tag{3.4}
\]

> **Theorem 3.1 (two asymptotic channels but a punctured no-hit set).**  In
> (3.1)--(3.2), every \(a<0\) converges to the negative channel and every
> \(a>0\) converges to the positive channel.  Nevertheless, for
> \[
>    0<|a|<a_*,
>    \tag{3.5}
> \]
> the trajectory hits neither target in (3.2).  This holds for every fixed
> \(\varepsilon>0\).  The no-hit set is a punctured neighborhood of the exact
> separator.

**Proof.**  Separating variables in \(\dot z=z(1-z^2)\) gives (3.3).
Condition \(cT_R(a)<h\) is equivalent to \(|a|>a_*\).  If
\(|a|<a_*\), recovery has already left the band in (3.2) when \(z\) first
reaches its assigned section.  Afterwards \(r\) is strictly decreasing and
\(|z|\) is strictly increasing toward one, so neither section can be recovered
later.  The signs and limits of \(z\) are immediate from (3.1). \(\square\)

Adding any number of equations \(\dot y_j=-y_j\) gives genuine stable
directions without changing the conclusion.  Thus a simple event root, two
stable channels, complete-history well-posedness, and even the absence of a
third attractor do not imply all-offset capture by fixed-slow-base targets.

For large \(h/c\), (3.4) has the transparent scale

\[
 a_*\sim\frac{R}{\sqrt{1-R^2}}e^{-h/c}.
 \tag{3.6}
\]

This is the same logarithmic dwell-time mechanism that invalidated the old
fixed-layer R-S shortcut, now with two genuine attracting channels attached.

## 4. Why finite-time perturbation can certify only a deadband

Let \(S\) be a signed coordinate on an outgoing complete-history section.
If the separating history \(S=0\) does not hit either target and histories
with \(S\ne0\) approach it, their capture times cannot remain uniformly
bounded.

> **Lemma 4.1 (no uniform all-offset finite capture).**  Let
> \(\Phi_t\) be a continuous semiflow, let \(\mathcal T\) be closed, and let
> \(\phi_n\to\phi_0\).  If every \(\phi_n\) hits \(\mathcal T\) by one common
> time \(T\), and the hits have a convergent time subsequence, then
> \(\Phi_t\phi_0\in\mathcal T\) for some \(0\le t\le T\).  Consequently, if
> the separator trajectory avoids \(\mathcal T\) on every bounded interval,
> capture times of nearby captured histories must diverge.

**Proof.**  Choose hit times \(t_n\in[0,T]\), pass to
\(t_n\to t_*\), and use joint continuity of the semiflow and closedness of
\(\mathcal T\). \(\square\)

Thus Corollary 3.2 of the physical-pulse note can handle a compact outgoing
deadband

\[
 |S|\ge\gamma_\varepsilon>0,
 \tag{4.1}
\]

but cannot be iterated finitely to prove an exact boundary at \(S=0\).  In
the counterexample, the worst hit time on
\(\gamma\le|z_0|<R\) is exactly \(T_R(\gamma)\).

## 5. A verifiable complete-history isolating-chain theorem

The negative delayed derivative prevents use of cooperative order, but it
does not prevent a direct boundary-flux certificate.  Write the RFDE as

\[
 \dot x(t)=\mathcal F_{\varepsilon,u}(x_t),\qquad
 x_t\in\mathcal C_{\tau_*}.
 \tag{5.1}
\]

A **history cylinder** specifies a current-state box and independent bounds
for every delayed sample used by \(\mathcal F_{\varepsilon,u}\).  If
\(b(x(0))=0\) is a current-state face, its RFDE flux is

\[
 \dot b=Db(x(0))\mathcal F_{\varepsilon,u}(\phi).
 \tag{5.2}
\]

The sign in (5.2) must be enclosed for **every** history \(\phi\) in the
cylinder.  This includes the negatively signed matrices
\(-\varepsilon K C_j^\eta\phi_v(-\tau_j)\) on a positive-gain box; for
either sign of \(K\), no quasimonotonicity substitution is made.

Fix a deadband \(\gamma_\varepsilon>0\).  For each label
\(j\in\{{\rm p},{\rm q}\}\), suppose there is a finite chain
\(\mathcal N_{j,1},\ldots,\mathcal N_{j,m_j}\) of history cylinders with:

1. the signed U-EX incoming histories with \(|S|\ge\gamma_\varepsilon\) and
   label \(j\) enter \(\mathcal N_{j,1}\);
2. each cylinder has a method-of-steps enclosure closed under history
   translation until its declared exit; every delayed sample therefore stays
   in its stated range.  Every current-state side face has a strict inward
   flux, every declared exit face has a strict outward flux, and all
   entrance/exit intersections have one fixed priority rule and a nonzero
   flux margin;
3. a \(C^1\) progress coordinate \(L_{j,k}\) satisfies
   \(\dot L_{j,k}\ge c_{j,k}>0\) throughout the cylinder, and its range has
   length at most \(\Delta_{j,k}\);
4. the exit of \(\mathcal N_{j,k}\) lies in the entrance of
   \(\mathcal N_{j,k+1}\), while the last exit lies in the transverse target
   block \(\mathfrak B_j\); and
5. the whole chain is disjoint from the competing target block.

> **Theorem 5.1 (finite-deadband complete-history capture).**  Under items
> 1--5, every retained incoming history with
> \(|S|\ge\gamma_\varepsilon\) hits its assigned target first and transversely.
> Its hit time is at most
> \[
>   T_j\le\sum_{k=1}^{m_j}\frac{\Delta_{j,k}}{c_{j,k}}.
>   \tag{5.3}
> \]
> No third outcome or grazing occurs before the latched hit.  If the final
> target cylinder also has inward flux on every non-entrance face, the target
> is trapping and the stronger unlatching no-return statement holds.

**Proof.**  History-translation closure excludes loss through an unmonitored
old-history face.  At an alleged first current-state side exit, (5.2) and the
strict inward sign contradict outward crossing.  The progress inequality
forces the declared exit within \(\Delta_{j,k}/c_{j,k}\); the strict exit sign
excludes grazing.  Induction through the finite chain proves (5.3), and item
5 excludes an earlier competing hit.  The same first-exit argument proves the
optional trapping statement. \(\square\)

The theorem is \(\varepsilon\)-uniform only when the number of cylinders,
all flux margins, history bounds, and (5.3) are uniform.  For each fixed
\(\varepsilon>0\), interval evaluation of (5.2) is a finite certification
problem.  As \(\gamma_\varepsilon\downarrow0\), Lemma 4.1 normally forces the
time bound or a flux margin to degenerate.

Slow drift must be built into the cylinders by moving their recovery base.
On compact attracting outer segments away from folds, a Halanay inequality
may help control history width, but it is not a substitute for (5.2), and its
constants degenerate near a fold.  The fold chart must therefore be a
separate cylinder family.  A characteristic-root count at one frozen state
does not exclude a secondary instability along the whole itinerary.

## 6. The strongest exact all-offset implication

An exact all-offset result is necessarily global.  The following formulation
makes the missing content explicit without assuming a uniform capture time.

Fix \(\varepsilon>0\) and a control \(u\).  Let the semiflow be asymptotically
compact on a closed positively invariant absorbing history set
\(\mathcal K\).  Let \(\mathcal W\subset\mathcal K\) be a closed invariant
codimension-one set such that

\[
 \mathcal K\setminus\mathcal W
 =\mathcal K_{\rm p}\mathbin{\dot\cup}\mathcal K_{\rm q},
 \tag{6.1}
\]

where the two components are relatively open, the targets satisfy
\(\overline{\mathfrak B_j}\subset\mathcal K_j\), and an orbit remains in its
component until hitting its assigned target.  Suppose the maximal compact
invariant sets obey

\[
\begin{aligned}
 \operatorname{Inv}
 (\overline{\mathcal K_{\rm p}}\setminus\mathfrak B_{\rm p})
 &\subset\mathcal W,\\
 \operatorname{Inv}
 (\overline{\mathcal K_{\rm q}}\setminus\mathfrak B_{\rm q})
 &\subset\mathcal W,
\end{aligned}
\tag{6.2}
\]

and that the relative stable set of \(\mathcal W\) contains no off-separator
history:

\[
 W^s_{\mathcal K}(\mathcal W)=\mathcal W.
 \tag{6.3}
\]

The complements in (6.2) are taken closed relative to the relevant isolating
neighborhoods.  Finally suppose the two signed U-EX exit sets lie in the two
components and the zero exit lies on \(\mathcal W\).

> **Theorem 6.1 (conditional exact two-basin capture).**  Under
> (6.1)--(6.3), every nonzero signed exit hits exactly its assigned target
> first.  The zero exit is their relative boundary.  Capture time need not be
> bounded as the signed exit approaches zero.

**Proof.**  Suppose an orbit in \(\mathcal K_{\rm p}\) never reaches its
target.  Asymptotic compactness gives a nonempty compact invariant omega-limit
set in the closed target complement.  The first line of (6.2) puts it in
\(\mathcal W\), so the initial history belongs to
\(W^s_{\mathcal K}(\mathcal W)\).  Equation (6.3) would then put that history
on \(\mathcal W\), contradicting membership in \(\mathcal K_{\rm p}\).  The
quiet argument is identical.  Component preservation and target containment
give the first-hit ordering.  The component boundary is \(\mathcal W\),
proving the final claim. \(\square\)

For a parameter-uniform theorem, \(\mathcal K\), its asymptotic compactness,
the separating history set, its relative stable set, and the invariant-set
exclusions must all be
uniform on the control box.  This is much stronger than a fixed-\(\varepsilon\)
stable-manifold theorem.  A practical proof of (6.2) could use a strict
Lyapunov--Krasovskii functional, a complete interval isolating-segment cover,
or a Conley-index/Morse decomposition with every other invariant set
excluded.  None has been constructed for the declared physical RFDE.

The Poincare--Bendixson theorem of
[Mallet-Paret and Sell](https://doi.org/10.1006/jdeq.1996.0036) applies to a
special monotone cyclic-feedback delay class.  The present two-voltage,
two-delay matrix feedback has not been conjugated into that class; its
negative delayed derivatives alone do not supply the required discrete
Lyapunov structure.  Delay relaxation oscillations themselves require global
analysis, as illustrated by
[Fowler and Mackey](https://doi.org/10.1137/S0036139901393512).  Neither
reference closes (6.2) for this model.

## 7. Minimal honest repairs

There are four distinct theorem targets.

### 7.1 Unforced one-passage three-event alternative

Stop at the first moving side exit or lower-fold outgoing section and record

\[
 \{\text{negative side},\ \text{positive side},\ \text{fold cap/score}\}.
 \tag{7.1}
\]

This is causal and avoids a global return theorem.  The fold-score zero is a
new operational safety coordinate.  It is not a biological pulse threshold.

### 7.2 Deadband biological certificate

Choose \(\gamma_\varepsilon>0\), replace the fixed-reset-layer blocks by
moving, latched detector cylinders, and certify Theorem 5.1.  Report
\(|S|<\gamma_\varepsilon\) as unresolved.  This is the shortest unforced
result that can be validated with finite-time interval computations.

### 7.3 Exact unforced biological boundary

Construct moving detector sets first, then prove Theorem 6.1.  The irreducible
new work is the invariant-set/stable-set assertion (6.2)--(6.3), including
exclusion of delay-induced periodic orbits, secondary saddles, grazing, and
competing returns.  A fold-map derivative or frozen fast potential cannot
replace it.

### 7.4 Controlled exact separator

If an exact two-valued operational threshold is more important than unforced
dynamics, retain the already-proved collective-recovery clamp until a channel
is hit.  That protocol removes the slow-base drift responsible for Theorem
3.1.  It remains a controlled safety coordinate and must not be called the
unforced canard or biological threshold.

A fixed-observable amplitude threshold is another legitimate biological
choice, but it is a peak/tangency problem.  It belongs to the quantitative
landing theorem in the physical-pulse note, not to channel U-CAP.

## 8. Stop/go ledger

| Statement | Status | Reason |
|---|---|---|
| The singular middle critical branch of the declared physical model crosses \(H=7/5\) once, near \(\rho=-0.9210\) | **Exact existence/uniqueness proved; decimal diagnostic** | Exact singular-graph monotonicity; executable root calculation |
| Old fixed-\(\rho_0\) passage blocks capture every late side/cap exit | **False as an implication** | Proposition 2.1 and exact Theorem 3.1 |
| A fold-side sign automatically gives two asymptotic channels | **False as an ordinary-fold inference** | Both Airy fold sides have the same post-fold escape direction |
| Deadband histories can be certified by finite isolating chains | **Proved implication** | Theorem 5.1; physical flux enclosures open |
| Exact all-offset capture follows from local finite-time persistence | **False** | Lemma 4.1; capture times diverge near a non-hitting separator |
| Exact all-offset two-basin theorem | **Proved implication** | Theorem 6.1; physical invariant/stable-set exclusions (6.2)--(6.3) open |
| Delay-negative feedback is harmless because it is \(O(\varepsilon)\) | **False on slow horizons** | It accumulates over \(O(\varepsilon^{-1})\) time and breaks cooperative RFDE order |
| Existing first-hit event needs literal no-return forever | **False** | A latched first hit is immutable; trapping is a separate optional theorem |
| Physical fold-event root equals the pulse/quiet boundary | **Not asserted** | Requires repaired detector sets, physical fold map, and exact U-CAP |
| Either root equals the canonical canard root | **Not asserted** | Requires the separate reset-to-canard factorization |

The publishable mathematical conclusion is therefore a stop/go theorem, not
a false closure: the current physical blocks prove robust **early** channel
passages, while exact **late** biological capture is a global RFDE basin
problem.  A finite-deadband isolating-chain certificate is achievable; an
exact unforced boundary requires the new global exclusions (6.2)--(6.3).
