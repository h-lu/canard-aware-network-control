# Paper III: a causal complete-history reset and pulse/quiet transition theorem

Status: **The reset-history formula, exact memory-erasure statement, recovery
non-erasure obstruction, fixed-δ well-posedness, singular channel blocks,
positive-ε endpoint outcomes, and existence of a nonempty reset-transition
set are proved below.  The abstract simple-boundary and root-transfer
theorems are also proved.  For the physical two-module RFDE, uniqueness of
the reset transition parameter remains conditional on the model-specific
signed-exchange Gate R-S in Section 6.  Identification with a physical or
canonical maximal-canard root additionally requires the unproved
factorization and small preparation error in Section 7.**

The symbolic certificate is
`src/canard_control/causal_reset_separator.py`; its tests are in
`tests/test_causal_reset_separator.py`.  This note concerns the unprepared
physical RFDE and does not modify the frozen JNS manuscript.

## 1. The released RFDE and the operational question

Let

\[
 \dot v=f(v,w)+\varepsilon K\left[
 Bv(t)-C_0^\eta v(t-\tau_0)-C_1^\eta v(t-\tau_1)
 \right],
\tag{1.1}
\]

\[
 \dot w=\varepsilon
 \binom{v_1-\sigma-\mu}{v_2-2\mu}
 -D_wP_\perp(w-w_*),
\tag{1.2}
\]

be the final two-module FitzHugh--Nagumo RFDE.  Here

\[
 \varepsilon=\delta^2,
 \qquad \tau_k=\frac{\theta_k}{\delta},
 \qquad \tau_*:=\max_k\tau_k,
 \qquad B=C_0^\eta+C_1^\eta,
\tag{1.3}
\]

and the modal vectors are

\[
 r=\binom 12,\quad q=\binom 1{-2},\qquad
 \ell=\binom{1/2}{1/4},\quad
 m=\binom{1/2}{-1/4}.
\tag{1.4}
\]

Thus

\[
 v-v_*=r\xi+q\zeta,\qquad
 w-w_*=r\rho+q\kappa.
\tag{1.5}
\]

An operational pulse experiment cannot start from an unnamed member of an
outer Fenichel family.  It must prescribe the voltage and recovery state
seen by every delay line at release.  The purpose of this note is to replace
the underdetermined backward-complete selection rule by a causal protocol:

1. preset the collective recovery coordinate;
2. clamp voltage for at least one maximal physical delay while allowing the
   recovery equations to evolve; and
3. release the unforced RFDE from the resulting explicitly known history.

The collective recovery preset is essential.  A long voltage hold alone
does not wash out an error in \(\rho\); Theorem 2.2 proves this exactly.

## 2. An exact voltage-hold/recovery-preset protocol

Fix a terminal collective recovery value \(\rho_0\).  Let \(a\) parameterize
a declared \(C^2\) voltage-reset curve

\[
 \gamma(a)=v_*+r\xi_a+q\zeta_a,
 \qquad a\in I=[a_-,a_+].
\tag{2.1}
\]

During the final hold \(-T_R\le t\le0\), impose the constant voltage clamp

\[
 v(t)=\gamma(a),
 \qquad T_R\ge\tau_*.
\tag{2.2}
\]

No recovery forcing is used on this final interval.  Instead, set its state
at \(-T_R\) so that the physical recovery equation produces

\[
 \rho(t)=\rho_0+\varepsilon(\xi_a-\mu)t,
 \qquad
 \kappa(t)=\frac{\varepsilon\zeta_a}{D_w}.
\tag{2.3}
\]

Equivalently, the required initial recovery coordinates are

\[
 \rho(-T_R)=\rho_0-\varepsilon(\xi_a-\mu)T_R,
 \qquad
 \kappa(-T_R)=\frac{\varepsilon\zeta_a}{D_w}.
\tag{2.4}
\]

This is a terminal-state preset followed by an ordinary voltage clamp.  In a
dynamic-clamp interpretation, an earlier conditioning waveform creates
(2.4); the final one-delay interval then records a known delay history.  The
mathematics does not assume that an unobserved recovery coordinate
spontaneously takes the value in (2.4).

Rescale the release history to the fixed interval
\(\vartheta=\delta t\in[-\theta_*,0]\).  It is

\[
 \boxed{
 \widehat\Phi^R_{\delta}(a,\mu)(\vartheta)
 =\binom{
 v_*+r\xi_a+q\zeta_a
 }{
 w_*+r[\rho_0+\delta(\xi_a-\mu)\vartheta]
       +q\delta^2\zeta_a/D_w
 }.}
\tag{2.5}
\]

The actual history supplied to the physical RFDE is the pullback

\[
 \Phi^R_\delta(a,\mu)(s)
 =\widehat\Phi^R_\delta(a,\mu)(\delta s),
 \qquad -\tau_*\le s\le0.
 \tag{2.5a}
\]

Thus \(\widehat\Phi^R_\delta\) is the fixed-interval representation used
for uniform estimates, whereas
\(\Phi^R_\delta\in C([-\tau_*,0],\mathbb R^4)\) is the physical history.

The redistribution parameter \(\eta\) does not enter (2.5).  It enters only
the released vector field.

> **Theorem 2.1 (exact causal complete-history reset).**  Let
> \(T_R\ge\tau_*\), fix \(D_w>0\), and use (2.2)--(2.4).  Then:
>
> 1. (2.3) solves the physical recovery equation (1.2) exactly throughout
>    the hold;
> 2. (2.5a), equivalently its scaled representation (2.5), is the complete
>    history at release and is independent of every
>    voltage value before \(-T_R\);
> 3. every delayed voltage argument used by the released RFDE at any
>    \(t\ge0\) belongs either to the declared hold or to the post-release
>    solution;
> 4. the delayed feedback at the instant of release is exactly zero for
>    every \(\eta\), and the endpoint modal coordinates are
>    \[
>      (\xi,\zeta,\rho,\kappa)
>      =(\xi_a,\zeta_a,\rho_0,\delta^2\zeta_a/D_w);
>    \tag{2.6}
>    \]
> 5. on every compact \(a,\mu\) box, the fixed-interval history map (2.5)
>    has uniform \(C^2_aC^1_\mu\) bounds as \(\delta\downarrow0\), provided
>    \(\gamma\) has the corresponding bounds.

**Proof.**  Projecting (1.2) with \(\ell\) and \(m\) gives the exact
equations

\[
 \dot\rho=\varepsilon(\xi-\mu),
 \qquad
 \dot\kappa=\varepsilon\zeta-D_w\kappa.
\tag{2.7}
\]

Equations (2.2)--(2.3) satisfy (2.7).  Since a query at release has
\(-\tau_k\ge-T_R\), its voltage value is the declared value in (2.2).  At a
later time \(t\), the query \(t-\tau_k\) is either nonnegative or is still
at least \(-\tau_k\ge-T_R\).  Hence no post-release evaluation can recover
pre-hold voltage data.  The recovery equation has no delayed recovery
argument, and its current endpoint is fixed by (2.3).  This proves items
1--3.

At a constant voltage history,

\[
 Bv_R-C_0^\eta v_R-C_1^\eta v_R=0
\tag{2.8}
\]

by (1.3), which proves the first assertion in item 4; (2.6) follows from
(2.3).  Finally, on the fixed interval the only history-length factor is
\(\delta(\xi_a-\mu)\vartheta\).  It and its declared derivatives are
uniformly bounded because \(|\vartheta|\le\theta_*\).  This proves item 5.
\(\square\)

The duration condition is sharp for exact memory overwrite.  If
\(T_R<\tau_*\), the atom at \(-\tau_*\) queries a voltage value before the
hold at release.  Its layer matrix is nonzero in the declared positive
\(\eta\)-range, so two pre-hold histories with the same controlled segment
can give different right derivatives at \(t=0\).

The physical history (2.5a) is a legitimate continuous RFDE history.  The left voltage
derivative is zero because of the clamp, while the right derivative after
release need not be zero.  Thus one should not falsely declare (2.5a) to be
on the \(C^1\) solution manifold at \(t=0\).  The released solution is a
classical right solution and acquires the usual retarded smoothing after one
maximal delay.

> **Theorem 2.2 (what the hold cannot erase).**  Compare two final holds
> with the same clamped voltage but with modal recovery errors
> \((\Delta\rho_-,\Delta\kappa_-)\) at \(-T_R\).  Their endpoint errors are
>
> \[
>  \Delta\rho(0)=\Delta\rho_-,
>  \qquad
>  \Delta\kappa(0)=e^{-D_wT_R}\Delta\kappa_-.
> \tag{2.9}
> \]
>
> Consequently a one-delay voltage hold exactly overwrites delayed voltage
> memory and exponentially suppresses transverse recovery error, but it
> does not suppress collective recovery error at all.

**Proof.**  Subtract the two copies of (2.7).  The difference equations are
\(\Delta\dot\rho=0\) and
\(\Delta\dot\kappa=-D_w\Delta\kappa\), whose solutions give (2.9).
\(\square\)

This obstruction is operationally important: a claimed pulse threshold is
not reproducible under this protocol unless \(\rho(-T_R)\) is preset,
measured and conditioned on, or included as an additional experimental
coordinate.

### 2.1 A nondegenerate reset coordinate

The endpoint map from \((\xi_a,\zeta_a,\rho_0)\) to modal state is

\[
 (\xi_a,\zeta_a,\rho_0)
 \longmapsto
 (\xi_a,\zeta_a,\rho_0,\delta^2\zeta_a/D_w),
\tag{2.10}
\]

and has rank three for every \(\delta>0\).  Since the history feedback
vanishes at release, the critical projection of the released fast field
satisfies the exact identity

\[
 \partial_{\rho_0}F_c^R=-1,
 \qquad
 \partial_{\rho_0}F_\perp^R=0.
\tag{2.11}
\]

Thus the recovery preset injects transversely into the critical fast force.
Equation (2.11) does not by itself prove a simple pulse-threshold root after
the long canard passage; it rules out degeneracy at the first instant of
release only.

## 3. Fixed-\(\delta\) release and entry maps

Let

\[
 \mathcal C_{\tau_*}=C([ -\tau_*,0],\mathbb R^4).
\tag{3.1}
\]

For each fixed \(\delta>0\), (1.1)--(1.2) is a finite-atomic retarded
equation with a polynomial current field and bounded linear evaluation
operators.  Denote its solution from the physical history (2.5a) by

\[
 x^R(t;a,\lambda),\qquad
 \lambda=(\mu,\eta,K,D_w),
\tag{3.2}
\]

Here \(\delta\) and the positive delay locations \(\theta_k\) are fixed.
Differentiability with respect to a moving delay evaluation is a stronger
statement and is not used in this lemma.

> **Lemma 3.1 (causal entry family).**  Fix \(\delta>0\), the positive
> delays, a compact parameter box with \(D_w\ge d_0>0\), and a finite time
> interval.  Then (3.2) exists uniquely and depends \(C^1\) on
> \((a,\lambda)\), with
> the usual loss of one state derivative only at the release corner.  If a
> \(C^1\) section \(s_{\rm in}(x)=0\) is reached at an interior time
> \(t_{\rm in}>\tau_*\) and
>
> \[
>  Ds_{\rm in}(x^R(t_{\rm in}))
>  \dot x^R(t_{\rm in})\ne0,
> \tag{3.3}
> \]
>
> then the hit time and the complete entry history
>
> \[
>  \mathcal E^R_\delta(a,\lambda)(s)
>  =x^R(t_{\rm in}(a,\lambda)+s;a,\lambda),
>  \quad -\tau_*\le s\le0,
> \tag{3.4}
> \]
>
> are locally unique and \(C^1\).  In particular, (3.4) is selected by
> forward causality and requires no backward RFDE continuation.

**Proof.**  On the first method-of-steps interval every delayed term is a
known \(C^1\) parameter family from (2.5a), so standard ODE existence,
uniqueness, and variational equations apply.  Induction over the finitely
many step intervals meeting the declared time horizon proves the same
claims for (3.2).  The dissipative cubic voltage terms prevent finite-time
escape: on each step a quadratic energy satisfies a Gronwall inequality
with the already bounded delayed voltage as input.  Apply the implicit-
function theorem to
\(s_{\rm in}(x^R(t;a,\lambda))\) using (3.3), and then take the history
segment to obtain (3.4).  The condition \(t_{\rm in}>\tau_*\) places the
whole entry history after the release corner. \(\square\)

This is a fixed-\(\delta\) theorem.  Uniform differentiability as
\(\delta\downarrow0\) over slow times of order \(\varepsilon^{-1}\) is the
exchange problem, not a consequence of the method of steps.

## 4. Pulse and quiet passage blocks

Fix the singular layer

\[
 \rho_0=-\frac12.
\tag{4.1}
\]

Theorem 3.1 of
`paper-iii-physical-outer-pulse-bridge.md` gives a saddle
\(v^m(\rho_0)\), an attracting lower equilibrium, an attracting upper
equilibrium, and two monotone heteroclinic branches.  The lower branch
crosses

\[
 \Sigma_{\rm p}^0=\{H=7/5\},
\tag{4.2}
\]

and the upper branch crosses

\[
 \Sigma_{\rm q}^0=\{H=0\},
\tag{4.3}
\]

once and transversely, where \(H=-\ell^T(v-v_*)\).

Choose disjoint compact flow boxes
\(\mathcal B_{\rm p}^0,\mathcal B_{\rm q}^0\) around short pieces of those
crossings.  Their entrance and exit faces are nearby regular \(H\)-levels,
and the remaining faces are chosen tangent to the local flow-box
coordinates.  These are passage blocks, not assertions of invariant sets.

The RFDE lift is a current-state/bounded-history cylinder, not a sup-norm
ball around a constant history. Fix one admissible compact weak-gain/delay
parameter box. Then fix \(M>0\) and choose nested recovery constants
\(0<c_{\rm in}<c_{\rm out}\), allowed to depend on that box but not on
\(\varepsilon\) or the physical delay length. Write

\[
 \mathfrak B_{j,M}^\varepsilon
 =\left\{\phi\in\mathcal C_{\tau_*}:
   \phi_v(0)\in\mathcal B_j^0,
   |\rho(\phi_w(0))-\rho_0|<c_{\rm out}\varepsilon,
   |\kappa(\phi_w(0))|<c_{\rm out}\varepsilon,
   \|\phi_v\|_\infty<M\right\}.
 \tag{4.4}
\]

Its entrance and exit faces are defined by the corresponding current
voltage faces of \(\mathcal B_j^0\).  A transverse hit means that the
current-state entrance defining function has nonzero derivative along the
RFDE solution.  Similarly, \(\mathfrak U_{j,M}^\varepsilon\) denotes the
cylinder obtained from a small current-voltage neighborhood of a fixed
point on the corresponding singular connection, the **inner** recovery
bounds \(c_{\rm in}\varepsilon\), and
\(\|\phi_v\|_\infty<M\). The constants are chosen so that the compact reset
endpoint families used below enter the inner cylinders. No claim is made
that the old portion of a
long history becomes close to a constant history in \(O(1)\) fast time.

> **Lemma 4.1 (two robust RFDE passage blocks).**  The boxes can be chosen
> so that there are cylinders
> \(\mathfrak U_{\rm p,M}^\varepsilon,
> \mathfrak U_{\rm q,M}^\varepsilon\) as above and constants
> \(\varepsilon_0,c_0,T_0>0\)
> with the following property.  For the fixed compact parameter box and
> \(0<\varepsilon\le\varepsilon_0\), histories in
> \(\mathfrak U_{j,M}^\varepsilon\) reach
> \(\mathfrak B_{j,M'}^\varepsilon\), for one fixed \(M'>M\), before time
> \(T_0\), cross its current-state flow box once,
> and satisfy \(|\dot H|\ge c_0\) on the retained passage.  They do not
> reach the other block first.

**Proof.**  The singular crossings are regular and lie on disjoint compact
heteroclinic pieces.  The flow-box theorem gives disjoint boxes and uniform
entrance/exit signs.  Here is the uniform estimate despite
\(\tau_*=\theta_*/\delta\).  On a fixed fast-time interval, dissipativity of
the cubic gives a bound \(M'\) for the current and sampled voltages that
depends on \(M\) and the compact parameter box but not on \(\tau_*\).
The delayed term is therefore bounded by \(C\varepsilon M'\), while (2.7)
gives

\[
 |\rho(t)-\rho_0|+|\kappa(t)|\le C\varepsilon,
 \qquad 0\le t\le T_0.
 \tag{4.5}
\]

Let \(v^0\) be the frozen singular fast orbit with the same current voltage.
Until either path leaves the chosen compact flow-box neighborhood, local
Lipschitz continuity gives

\[
 |v^\varepsilon(t)-v^0(t)|
 \le L\int_0^t|v^\varepsilon(s)-v^0(s)|\,ds
      +C\varepsilon t.
 \tag{4.6}
\]

Gronwall's inequality yields a uniform \(O(\varepsilon)\) difference on
\([0,T_0]\), independently of the delay length and of the unreplaced old
part of the bounded history.  Shrinking the current-voltage cylinders now
preserves the two flow boxes, their ordering, and the fixed-sign transverse
\(H\)-crossings.  This is the model-specific uniform version of Corollary
3.2 in the physical pulse-bridge note. Increasing
\(c_{\rm out}-c_{\rm in}\) once, using the constant in (4.5), guarantees
that every inner-cylinder history remains in the outer recovery tube at the
target hit. \(\square\)

The boxes classify two finite fast passages.  They do not yet prove that
every reset history near the operational transition reaches one of them.

## 5. A proved positive-\(\varepsilon\) reset-transition theorem

Let \(W^s(v^m(\rho_0))\) denote the one-dimensional stable manifold of the
singular fast saddle.  Choose a \(C^2\) voltage-clamp curve
\(\gamma:I\to\mathbb R^2\) satisfying

\[
 \gamma(0)=v^m(\rho_0),\qquad
 \gamma'(0)\notin T_{v^m}W^s(v^m),
\tag{5.1}
\]

and orient it so the negative side lies below the stable separator.  The
experimentally simplest choice is the straight line
\(\gamma(a)=v^m+a e_u\), where \(e_u>0\) is the unstable eigenvector.
The local stable-manifold theorem and Theorem 3.1 give fixed
\(a_-<0<a_+\) for which the forward orbit from \(\gamma(a_-)\) enters the
pulse block and that from \(\gamma(a_+)\) enters the quiet block.  Thus the
hold does not require an exact parameterization of the nonlinear unstable
manifold.

Use this \(\gamma\) in the reset history (2.5a), with \(\rho_0=-1/2\).  For
a released trajectory define first-hit times

\[
 \tau_j(a;\delta,\lambda)
 =\inf\{t>0:x^R_t(a,\lambda)\in
                \mathfrak B_{j,M'}^\varepsilon\},
 \qquad j\in\{{\rm p},{\rm q}\},
\tag{5.2}
\]

with \(\inf\varnothing=+\infty\).  Define the transverse first-hit outcome
sets

\[
\begin{aligned}
 \mathcal P_{\delta,\lambda}
 &=\{a:\tau_{\rm p}<\tau_{\rm q}
       \text{ in }[0,+\infty],
       \text{ and the pulse hit is transverse}\},\\
 \mathcal Q_{\delta,\lambda}
 &=\{a:\tau_{\rm q}<\tau_{\rm p}
       \text{ in }[0,+\infty],
       \text{ and the quiet hit is transverse}\},
\end{aligned}
\tag{5.3}
\]

and the unresolved transition set

\[
 \mathcal S_{\delta,\lambda}
 =I\setminus(\mathcal P_{\delta,\lambda}
              \cup\mathcal Q_{\delta,\lambda}).
\tag{5.4}
\]

The alternatives in (5.3) merely say “this block is hit first”; disjoint
blocks cannot be hit simultaneously.

> **Theorem 5.1 (nonempty causal reset-transition set).**  For every fixed
> compact physical parameter box, there is \(\varepsilon_0>0\) such that,
> for \(0<\varepsilon\le\varepsilon_0\),
>
> \[
>  a_-\in\mathcal P_{\delta,\lambda},
>  \qquad
>  a_+\in\mathcal Q_{\delta,\lambda}.
> \tag{5.5}
> \]
>
> The sets \(\mathcal P_{\delta,\lambda}\) and
> \(\mathcal Q_{\delta,\lambda}\) are disjoint and relatively open in
> \(I\).  Consequently \(\mathcal S_{\delta,\lambda}\) is a nonempty
> compact set separating the two endpoint outcomes.

**Proof.**  At \(\varepsilon=0\), the transverse reset curve crosses the
stable manifold of the saddle.  Local saddle dynamics sends its two fixed
endpoints into neighborhoods of the lower and upper singular unstable
branches, which then reach the two declared blocks.  At positive
\(\varepsilon\), their current states differ from the corresponding
singular reset points only in
\(\kappa=\varepsilon\zeta_{a_\pm}/D_w\); their histories remain uniformly
bounded because

\[
 \sup_{-\theta_*\le\vartheta\le0}
 |\delta(\xi_{a_\pm}-\mu)\vartheta|=O(\delta).
\tag{5.6}
\]

The uniform estimate (4.5)--(4.6) first carries the current states of these
two reset orbits into the two declared entrance cylinders; their released
histories satisfy one common (M)-bound by (2.5a). Lemma 4.1 then proves
(5.5), uniformly on the compact parameter box.
A transverse first hit persists with its ordering under small changes of
the initial history and parameters, by Lemma 3.1 and the implicit-function
theorem.  Hence the two outcome sets are relatively open; they are disjoint
by the first-hit definition.  If their union were all of \(I\), it would be
a separation of the connected interval into two nonempty disjoint open
sets.  Thus the complement (5.4) is nonempty.  It is closed in compact
\(I\), hence compact.  Every connected subset joining the two endpoints
must meet it. \(\square\)

Theorem 5.1 is stronger than a numerical sign scan: for all sufficiently
small positive \(\varepsilon\), it proves two opposite operational outcomes
and at least one intervening transition history.  It deliberately does not
rename the whole set (5.4) a basin boundary.  It may contain a no-hit band,
a third long-time outcome, a nontransverse hit, or several separator
histories.  Eliminating those alternatives is the remaining exchange
problem.

This proved transition is prepared directly on the bistable layer
\(\rho_0=-1/2\).  It is not yet a theorem that a reset made on an attracting
outer branch passes through the fold and reaches this transition with the
canonical canard gap as its signed coordinate.  That additional
fold-to-layer exchange is precisely the comparison problem in Sections
6--7.

## 6. The smallest model-specific separator obstruction

The exact local conclusion needs one signed forward exchange statement.
Write the physical parameter tuple as \(u=(\mu,\bar u)\), where \(\mu\) is
the unfolding in (1.1)--(1.2) and \(\bar u\) collects all other controls,
and fix a neighborhood \(J\times U\subset I\times\mathbb R^m\).

> **Gate R-S (signed reset exchange; open for the physical RFDE).**  Prove
> that there is a \(C^1\) scalar map
>
> \[
>  g_\delta:J\times U\longrightarrow\mathbb R
> \tag{6.1}
> \]
>
> and \(c_g>0\), uniform in the declared small-\(\delta\) range, such that:
>
> 1. every reset trajectory in the box has exactly one of three outcomes:
>    a transverse pulse first-hit in the sense of (5.3), a transverse quiet
>    first-hit in the sense of (5.3), or the unique separating trajectory;
> 2. after one fixed orientation,
>    \[
>      g_\delta<0\iff a\in\mathcal P_{\delta,u},\qquad
>      g_\delta>0\iff a\in\mathcal Q_{\delta,u},
>    \tag{6.2}
>    \]
>    and \(g_\delta=0\) precisely on the separating trajectory;
> 3. \(|\partial_a g_\delta|\ge c_g\) throughout the zero tube; and
> 4. all complete-history endpoint terms are included in (6.1), with no
>    replacement by a current-state sign.

> **Theorem 6.1 (exact local channel boundary under Gate R-S).**  If Gate
> R-S holds and \(g_\delta(a_0,u_0)=0\), then, after shrinking
> \(J\times U\), there is a unique \(C^1\) reset threshold
>
> \[
>  a_R:U\longrightarrow J,\qquad
>  g_\delta(a_R(u),u)=0.
> \tag{6.3}
> \]
>
> Moreover
>
> \[
>  \partial_{J}\mathcal P_{\delta,u}
>  =\partial_{J}\mathcal Q_{\delta,u}
>  =\mathcal S_{\delta,u}\cap J
>  =\{a_R(u)\}.
> \tag{6.4}
> \]
>
> Thus the channel-event correction is exactly zero:
>
> \[
>  a_{\rm pulse}^{\rm channel}(u)-a_R(u)=0.
> \tag{6.5}
> \]

**Proof.**  The implicit-function theorem and item 3 give the unique branch
(6.3).  Its derivative cannot change sign after shrinking the box.  The
sign equivalences (6.2) put the two open outcomes on opposite sides of this
branch and item 1 excludes a third local outcome.  This proves (6.4).
Equation (6.5) is then the definition of the first-channel boundary, not an
asymptotic estimate. \(\square\)

Gate R-S is an exact event-separator hypothesis, so (6.5) remains a
definition-level tautology relative to its root \(a_R\).  The lower-fold Airy
audit shows that its scalar \(g_\delta\) cannot be constructed merely by
relabeling the initial U-SF geometric fiber coordinate: arbitrarily small
offsets of one initial sign can reach both fold sides.  For the two-module
RFDE, the model construction must instead pass through the moving outer tube
and complete-history lower-fold score of the repaired Gate U-EX and then prove
Gate U-CAP.  Finite-time persistence decides offsets away from the shrinking
central layer but not that layer.  Nothing in Theorem 6.1 asserts
\(a_R=a_{\rm geo}\) or equality with a maximal-canard root.

## 7. Relation to the canonical local canard root

The reset history (2.5a) is unique and causal, but it is generally not a
point on the preparation-indexed complete-history graph used for the local
JNS canard root.  Causality removes selection nonuniqueness; it does not
make two different preparations equal.

Let \(d_\delta(\mu,\bar u)\) be a canonical scalar gap with simple root
\(\mu_c(\bar u)\). A comparison first requires a declared \(C^1\) path from the
physical unfolding to the reset curve,

\[
 a=\mathfrak a_\delta(\mu,\bar u),
 \qquad
 g_\delta^R(\mu,\bar u)
 :=g_\delta(\mathfrak a_\delta(\mu,\bar u),\mu,\bar u).
 \tag{7.0}
\]

Suppose this pullback of the signed reset exchange, after division by a
nonzero multiplier \(M_\delta\), has the form

\[
 \frac{g_\delta^R(\mu,\bar u)}{M_\delta(\mu,\bar u)}
 =d_\delta(\mu,\bar u)+e_\delta(\mu,\bar u).
\tag{7.1}
\]

The following root-transfer statement is exact.

> **Lemma 7.1 (quantitative preparation-to-reset root transfer).**  Fix
> \(\bar u\) and an interval
> \([\mu_c-R,\mu_c+R]\).  Suppose \(d_\delta'\) has fixed sign and
> \(|d_\delta'|\ge m>0\), while
>
> \[
>  \|\partial_\mu e_\delta\|_\infty\le q<m,
>  \qquad
>  \frac{|e_\delta(\mu_c)|}{m-q}<R.
> \tag{7.2}
> \]
>
> Then (7.1) has exactly one root \(\mu_R\) in that interval and
>
> \[
>  |\mu_R-\mu_c|
>  \le\frac{|e_\delta(\mu_c)|}{m-q}.
> \tag{7.3}
> \]
>
> If \(e_\delta(\mu_c)=0\), the two roots agree exactly.  If the right side
> of (7.3) is superalgebraic or exponential, the root difference has the
> same stated bound.

**Proof.**  Reverse orientation if necessary so that \(d_\delta'\ge m\).
Then \((d_\delta+e_\delta)'\ge m-q>0\), so there is at most one root.  At
distance \(R\), the change in \(d_\delta\) has magnitude at least \(mR\),
while the change in \(e_\delta\) is at most \(qR\).  Condition (7.2) gives
opposite endpoint signs and hence existence.  At the root, the mean-value
theorem gives

\[
 (m-q)|\mu_R-\mu_c|
 \le |e_\delta(\mu_c)|,
\]

which is (7.3). \(\square\)

For the physical reset protocol, neither the comparison path (7.0), the
factorization (7.1), nor a small bound on \(e_\delta\) has been proved. In
particular, Theorem 2.1 does
not imply that \(e_\delta\) is flat: a reset history may enter the fold tube
with an order-one preparation displacement.  A canonical-root comparison
therefore requires an entry/exchange calculation, not merely one-delay
memory erasure.

## 8. Channel boundary versus amplitude detector

Theorem 6.1 concerns which of two blocks is reached first.  Once Gate R-S is
proved, its threshold is the separator (6.3) exactly.

An amplitude detector instead fixes an observable and a level, for example

\[
 \max_{0\le t\le T_*}H(x^R(t;a,u))=A_*.
\tag{8.1}
\]

Its threshold need not equal \(a_R\).  Differentiability of (8.1) requires a
unique interior nondegenerate maximum and exclusion of peak switching.  A
transverse crossing of \(H=A_*\) is stable under parameter changes and is
not itself an event boundary.  If a model-specific landing chart of the
form in Theorem 5.2 of the physical pulse-bridge note is proved with
\(a-a_R\) replacing \(\mu-\mu_{\rm can}\), then the amplitude threshold is
exponentially close with the detector action.  No such landing chart is
proved by the reset construction.

## 9. Proof-status ledger

| Statement | Status | Evidence or missing step |
|---|---|---|
| Released history (2.5a), represented on the fixed interval by (2.5), solves the controlled hold and overwrites delayed voltage memory | Proved exactly | Theorem 2.1 and symbolic residuals |
| A hold of one maximal delay erases unknown collective recovery | False | Exact invariant error in Theorem 2.2 |
| Transverse recovery error is washed out | Proved exactly | Factor \(e^{-D_wT_R}\) in (2.9) |
| Reset endpoint has three independent modal preparation coordinates | Proved exactly | Rank-three map (2.10) |
| Recovery preset enters the critical release force nondegenerately | Proved exactly | Identity (2.11) |
| Fixed-\(\delta\) forward entry history and transverse hit map | Proved | Method of steps and implicit-function theorem |
| Disjoint positive-\(\varepsilon\) pulse/quiet passage blocks | Proved on fixed fast pieces | Singular flow boxes plus RFDE continuous dependence |
| Opposite reset endpoint outcomes for small \(\varepsilon\) | Proved | Lemma 4.1 applied to the two unstable branches |
| Nonempty causal reset-transition set | Proved | Connectedness argument in Theorem 5.1 |
| Unique reset separator and simple root | Conditional abstract theorem; model application open | Gate R-S |
| Equality with the preparation-indexed canonical canard root | Not asserted | Requires (7.1) with a proved small \(e_\delta\) |
| Channel-event correction after Gate R-S | Exactly zero relative to its event root \(a_R\) | Equation (6.5); no geometric/canard equality is asserted |
| Amplitude-detector correction | Conditional | Requires the quantitative landing/peak chart |

The causal protocol therefore closes the *selection* ambiguity: the
released complete history is explicit.  It does not, by itself, close the
positive-\(\varepsilon\) canard exchange or turn a topological transition
set into a unique differentiable threshold.  Realizing the abstract Gate R-S
for the physical RFDE now requires U-SF for the geometric history coordinate,
the repaired moving-tube/complete-history fold map for its event root, and
U-CAP for biological first-hit capture.  Comparing any resulting event root
with a physical or canonical maximal-canard root remains the additional
factorization problem in Section 7.
