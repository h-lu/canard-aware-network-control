# Paper III: stop/go theorem for the unforced reset separator

Status: **The proposed shortcut from the proved special-flow history graph to
the unforced Gate R-S does not close.  Proposition 3.1 gives an exact
ODE-subclass counterexample: even an exact low-dimensional saddle trajectory,
a unique codimension-one separator, and two signed unstable exits do not make
fixed-layer passage blocks classify every nonzero reset offset when the slow
layer drifts.  This does not disprove a global separator for the physical
two-module RFDE.  It proves that such a theorem additionally needs the outer
saddle-history continuation, a complete-history stable foliation, and a
global drifting exchange/return result stated in Section 5.**

The executable identities are in
`src/canard_control/unforced_separator_obstruction.py`, with regressions in
`tests/test_unforced_separator_obstruction.py`.  This note does not modify the
frozen JNS manuscript.

## 1. The proposed reduction and the verdict

The tempting route is:

1. use the exact special-flow embedding near the right fold to replace the
   RFDE by its reduced planar field;
2. continue the repelling planar canard to the reset layer
   \(\rho_0=-1/2\);
3. take the stable set of that saddle-type slow history as a codimension-one
   separator; and
4. use the two singular fast branches to label its two sides as pulse and
   quiet.

Steps 1 and the singular part of step 4 are already available.  They do not
imply steps 2--3, and even steps 1--3 together would not imply the all-offset
first-hit statement in step 4.  There are three distinct seams.

First, the proved fold graph is local.  In the exact blow-up coordinates,

\[
 \rho=-\delta^2Y.
\tag{1.1}
\]

On the logarithmic graph tube \(|Y|\le C(1+S_\delta^2)\), with
\(S_\delta^2=2p\log(1/\delta)\), it therefore covers only

\[
 |\rho|=O\!\left(\delta^2\log(1/\delta)\right).
\tag{1.2}
\]

The reset layer \(\rho_0=-1/2\) is a fixed positive slow distance away.
Thus present evaluation already proves that the reset histories are not in
the domain of the existing fold graph for small \(\delta\).

Second, a graph is not a foliation.  The map

\[
 \iota_{\delta,u}:z\longmapsto
 \bigl(\Phi_Q^\vartheta z,H(\Phi_Q^\vartheta z)\bigr)_{
 -\theta_*\le\vartheta\le0}
\tag{1.3}
\]

embeds the selected special-flow histories.  Its proved uniqueness is
uniqueness among bounded special-flow graph solutions in a contraction
class.  It does not assign an arbitrary causal reset history to a stable
fiber of (1.3), and it does not prove that the reset curve intersects such a
fiber once.

Third, the singular saddle is not frozen after release.  On the middle
branch at \(\rho_0=-1/2\),

\[
 \xi^m=-0.8551591\ldots,
 \qquad
 \dot\rho=\varepsilon(\xi-\mu).
\tag{1.4}
\]

For the fold-unfolding box near \(\mu=0\), the right side is negative along
the saddle tracker.  Forward time therefore carries it toward the lower fold
\(\mathfrak f_-\), not back toward the proved right-fold chart
\(\mathfrak f_0\).  One may instead start with the selected right-fold
history and continue it **forward** to the reset layer.  That is a legitimate
selection strategy, but it is an outer continuation theorem, not an ambient
backward RFDE solve and not a consequence of (1.3).

## 2. What the special-flow theorem can still supply

The negative verdict is about sufficiency, not usefulness.  The fold graph
can provide an exact seed for a selected repelling history.  At a simple
canonical gap root, the retained attracting and repelling histories coincide
inside the uncut fold tube.  Taking a repelling exit history from that tube
and applying the physical RFDE semiflow forward is unambiguous.  If this
orbit remains on a normally hyperbolic middle-branch tube until it reaches
\(\rho_0\), it supplies a selected complete-history saddle tracker at the
reset section.

This construction has two honest qualifications.

1. It inherits the declared canonical preparation.  Different compatible
   preparations may move the exact finite-\(\delta\) tracker by a flat amount,
   even when every algebraic canard coefficient agrees.
2. Forward continuation selects one history but does not construct the
   codimension-one family of histories that shadow it.  That family requires
   a nonautonomous RFDE exponential trichotomy and a stable-fiber theorem on
   the outer middle branch.

The reset history itself is causal and unique, so there is no remaining
choice of its past.  The selection problem here is different: one must prove
that this explicitly prescribed curve in history space crosses the stable
fiber of the selected saddle tracker, rather than comparing only their
current voltage coordinates.

## 3. An exact counterexample to the fixed-layer shortcut

Every ODE is an RFDE whose functional ignores its history.  Fix an arbitrary
delay \(\tau>0\), constants \(\lambda,\beta,c>0\), and consider

\[
 \dot u=\lambda u,
 \qquad
 \dot y=-\beta y,
 \qquad
 \dot\rho=\varepsilon c.
\tag{3.1}
\]

The curve

\[
 \Gamma_\varepsilon
 =\{(0,0,\rho):\rho\in\mathbb R\}
\tag{3.2}
\]

is an exact saddle-type slow invariant manifold.  Its center-stable set is

\[
 W^{cs}(\Gamma_\varepsilon)=\{u=0\},
\tag{3.3}
\]

which is smooth, codimension one, and separates the signs of the unique
unstable coordinate.  The reset curve

\[
 \mathcal R(a)(s)=(a,0,\rho_0),
 \qquad -\tau\le s\le0,
\tag{3.4}
\]

crosses it once and transversely at \(a=0\).  Hence this example grants more
finite-dimensional geometry than the present unforced RFDE proof has.

Fix an exit coordinate \(R>0\) and a layer-tube constant \(h>0\).  Define
two current-state passage blocks by

\[
\begin{aligned}
 \mathfrak B_+^\varepsilon
 &=\{\phi:R\le \phi_u(0)\le2R,
          \ |\phi_\rho(0)-\rho_0|<h\varepsilon\},\\
 \mathfrak B_-^\varepsilon
 &=\{\phi:-2R\le \phi_u(0)\le-R,
          \ |\phi_\rho(0)-\rho_0|<h\varepsilon\}.
\end{aligned}
\tag{3.5}
\]

These have exactly the fixed-layer recovery scaling used by the physical
passage cylinders.

> **Proposition 3.1 (a unique saddle separator does not imply fixed-layer
> first-hit classification).**  For (3.1)--(3.5), the reset curve has the
> unique transverse separator \(a=0\).  Nevertheless every nonzero reset
> offset satisfying
>
> \[
> 0<|a|\le a_*:=R\exp\!\left(-\frac{\lambda h}{c}\right)
> \tag{3.6}
> \]
>
> reaches neither block in (3.5).  Consequently the unresolved first-hit
> transition set contains the whole interval \([-a_*,a_*]\), not only its
> geometric separator.

**Proof.**  The released solution is

\[
 u(t)=ae^{\lambda t},
 \qquad
 y(t)=0,
 \qquad
 \rho(t)=\rho_0+\varepsilon ct.
\tag{3.7}
\]

For \(a\ne0\), the first signed exit time is

\[
 T_{\rm ex}(a)=\frac1\lambda\log\frac R{|a|}.
\tag{3.8}
\]

At that time,

\[
 |\rho(T_{\rm ex})-\rho_0|
 =\frac{\varepsilon c}{\lambda}\log\frac R{|a|}.
\tag{3.9}
\]

Condition (3.6) makes (3.9) at least \(h\varepsilon\), whereas the
recovery window in (3.5) is open.
Before \(T_{\rm ex}\), the voltage coordinate is outside both blocks.
After that time, \(|u|\) is monotone increasing and \(\rho-\rho_0\) is
monotone increasing, so neither block can be entered later.  Equations
(3.2)--(3.4) prove the separator assertions. \(\square\)

The cancellation of \(\varepsilon\) in (3.6) is important.  Merely taking
\(\varepsilon\) smaller does not create a punctured neighborhood in which
the fixed-layer blocks classify every nonzero offset.  At the canard scale

\[
 |a|=e^{-A/\varepsilon},
\tag{3.10}
\]

equation (3.9) becomes

\[
 |\rho(T_{\rm ex})-\rho_0|
 =\frac{cA}{\lambda}
  +\frac{\varepsilon c}{\lambda}\log R,
\tag{3.11}
\]

which has a nonzero order-one limit.  This is precisely the scale at which a
trajectory can reach the next fold before a frozen-layer argument decides
its channel.

Proposition 3.1 is not asserted to be the global dynamics of the physical
FitzHugh--Nagumo RFDE.  It proves a logical point: no theorem using only a
low-dimensional graph, a local codimension-one stable set, and the existing
fixed-fast-time passage blocks can establish item 1 of Gate R-S.  A global
exchange or return-exclusion statement is indispensable.

## 4. Long-delay audit

The physical delay \(\tau_*=\theta_*/\delta\) creates two different
questions.

### 4.1 Unstable index

On a compact middle-branch segment away from both folds, the frozen
current-state voltage matrix has one unstable and one stable eigenvalue;
the transverse recovery direction is stable.  Since the delayed voltage
operator is multiplied by \(\varepsilon=\delta^2\), a resolvent small-gain
argument on the imaginary axis can preserve the one-dimensional unstable
index independently of \(\tau_*\).  The corresponding calculation has
already been carried out for the collective-clamped saddle.  Along an
unforced moving tracker it must be upgraded from an equilibrium root count
to a nonautonomous exponential trichotomy.

### 4.2 Stable complement

Weak long delay does not give a \(\delta\)-independent stable spectral gap.
Scalar diffusive delay equations in the same scaling possess stable
pseudo-continuous roots with real parts of order

\[
 \delta\log(\delta^2),
\tag{4.1}
\]

which approach the imaginary axis.  This does not rule out normal
hyperbolicity: the collective slow rate is order \(\delta^2\), so (4.1) is
still faster on the slow scale.  It does rule out importing a stable-fiber
theorem with constants based on a fixed negative spectral bound.

A usable proof must work in the fixed scaled-history interval and establish
domination of the strong unstable bundle over a center-stable complement.
It must also control translation of old histories and the parameter jets of
the fiber projection.  None of these properties is part of the proved
special-flow embedding.

## 5. The smallest new theorem package

The following separates the geometric separator from the pulse/quiet event
claim.  It is deliberately narrower than a full physical maximal-canard
theorem.

> **Gate U-SF (unforced outer saddle history and stable fibers).**  Fix an
> outer middle-branch section beyond the outgoing overlap of the right-fold
> chart, the reset section \(\rho=\rho_0\), a compact control box, and the
> scaled complete-history space.  Prove:
>
> 1. the selected repelling history from the exact inner graph matches to the
>    fixed outer section and has a unique physical forward continuation
>    \(\Gamma^m_{\delta,u}\) through the reset section, with every delayed
>    backtrack in the declared uncut outer tube;
> 2. the variational RFDE along \(\Gamma^m_{\delta,u}\) has a one-dimensional
>    strong unstable bundle and a dominated center-stable complement, with
>    estimates sufficient for a \(C^1\) nonautonomous stable foliation in the
>    scaled history space;
> 3. a scalar complete-history fiber coordinate \(G_{\delta,u}\) defines
>    that foliation at \(\rho_0\), and the causal reset satisfies
>    \[
>      \left|\partial_a
>       G_{\delta,u}(\widehat\Phi^R_\delta(a,u))\right|\ge c_a>0;
>    \tag{5.1}
>    \]
> 4. the continuation and fiber maps have the parameter regularity claimed
>    for the reset threshold, without using an ambient backward RFDE.

Items 1--4 would give, by the implicit-function theorem, a unique local
**geometric reset separator**

\[
 a_{\rm sep}(u):
 G_{\delta,u}(\widehat\Phi^R_\delta(a_{\rm sep}(u),u))=0.
\tag{5.2}
\]

This is the shortest credible route to uniqueness of a complete-history
separator.  The inner graph is useful in item 1, but it does not prove the
gate.

To identify (5.2) with the boundary of the existing first-hit outcome sets,
one further theorem is unavoidable.

> **Gate U-EX (drifting exchange and capture).**  Continue the saddle
> tracker and its signed unstable fibers through the full middle-branch
> passage, including the lower-fold chart.  Prove that every nonzero signed
> fiber coordinate in the declared reset neighborhood has exactly one of the
> two stated global outcomes, that its sign selects the outcome, and that no
> later return creates a competing first hit.  The theorem must either:
>
> - use moving channel tubes whose recovery coordinate follows the slow
>   base and then prove their equivalence to the biological pulse/quiet
>   event; or
> - retain the fixed-layer blocks and prove the much stronger global return
>   and capture statement needed to overcome Proposition 3.1.

The lower-fold clause is not optional.  Offsets of order
\(e^{-A/\varepsilon}\) can shadow the middle branch for an order-one slow
distance by (3.11).  The right-fold graph contains no information about
their eventual passage through \(\mathfrak f_-\).

## 6. Stop/go decision

**STOP for the present unforced Gate R-S.**  The proved special-flow graph
cannot be used to mark the gate closed.  It has the wrong outer domain, does
not supply stable fibers for the causal reset histories, and cannot turn
fixed-fast-time layer blocks into an all-offset classification.  The exact
counterexample in Proposition 3.1 remains valid even after granting the
desired low-dimensional saddle separator.

**GO for a two-stage theorem.**

1. Prove Gate U-SF and publish first the unique geometric complete-history
   reset separator (5.2), explicitly without a pulse/quiet boundary claim.
2. Prove Gate U-EX, preferably with slow-base-following exit tubes, and only
   then identify the separator with the physical first-hit boundary.

The collective-recovery-clamped protocol avoids the drifting-exchange seam:
it turns the singular saddle into an exact RFDE equilibrium and already has a
fixed-\(\delta\) stable-manifold separator theorem.  It remains the shortest
proved operational alternative.  It is a controlled threshold and must not
be relabelled as the unforced or canonical maximal-canard threshold.

## 7. Proof-status ledger

| Statement | Status | Reason |
|---|---|---|
| Exact inner complete-history graph near \(\mathfrak f_0\) | Proved elsewhere | Special-flow graph and retained-history theorem |
| The inner graph contains the reset layer \(\rho_0=-1/2\) | False for small \(\delta\) | Scale comparison (1.1)--(1.2) |
| Forward direction from the reset saddle returns to \(\mathfrak f_0\) | False near the declared unfolding | Sign in (1.4); it moves toward \(\mathfrak f_-\) |
| Forward continuation from the inner repelling history to \(\rho_0\) | Well posed for a given history; uniform outer theorem open | Requires long slow-time containment and parameter estimates |
| Stable foliation assigning causal reset histories to that tracker | Open | Not contained in graph existence/uniqueness |
| Unique geometric reset intersection under Gate U-SF | Conditional, exact implication | Complete-history IFT using (5.1) |
| Fixed-layer blocks classify every nonzero offset from local data | False as a logical implication | Proposition 3.1 |
| Physical FHN unforced transition set is nonunique | Not asserted | Requires model-specific global dynamics |
| Physical pulse/quiet boundary under Gate U-SF and U-EX | Conditional, exact implication | Outer stable fibers plus signed lower-fold exchange/capture |

The mathematical gain from this stop/go result is precise: it removes the
false hope that one more local stable-manifold citation closes Paper III and
locates the irreducible new analysis in an outer complete-history foliation
and a drifting two-fold exchange theorem.
