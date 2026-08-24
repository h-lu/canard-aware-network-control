# A balanced-general-topology controlled sign-cone theorem for delayed FHN networks

## 1. Result and scope

This note removes the rank-one and two-module restrictions from the
controlled sign-cone decision theorem. The network may be directed,
reducible, nonnormal, and nonsymmetric; the node count is arbitrary and the
voltage history need not be synchronous. The required structure is
positivity and balance, not contraction:

- a nonnegative row-stochastic instantaneous scaffold \(P\);
- one normalized strictly positive stationary row vector \(\pi^T\);
- nonnegative delay layers \(B_j\) with prescribed row masses
  \(\alpha_j\) and the same left balance;
- an ideal nodewise recovery clamp \(w_i\equiv0\) during the decision stage.

Under these hypotheses the positive and negative complete-history orthants
are invariant. The Perron-weighted mean \(x=\pi^Tv\) satisfies the same
one-sided nonlinear FHN growth inequalities as the scalar decision equation.
Consequently a nonzero current mean forces a nodewise hit of \(+1\) or
\(-1\) by an explicit deadline, and the same argument gives finite
controlled excursions to \(+3/2\) and \(-6/5\).

No Dobrushin coefficient, spectral gap, irreducibility, unique stationary
distribution, or rank-one representation is used. The stronger nodewise
clamp is essential to this version. The theorem does not prove a bounded
actuator, transverse attraction, full-network periodic hyperbolicity,
general-topology canard-root equivalence, a biological pulse or quiet basin,
or hardware realizability.

## 2. Balanced finite-network class

Let \(N\ge1\), let \(\mathbf1\in\mathbb R^N\) be the all-ones column, and let
\(P\in\mathbb R^{N\times N}\) satisfy

\[
 P_{ik}\ge0,
 \qquad
 P\mathbf1=\mathbf1.
\tag{2.1}
\]

Assume that a row vector \(\pi^T\) has been chosen such that

\[
 \pi_i>0,
 \qquad
 \pi^T\mathbf1=1,
 \qquad
 \pi^TP=\pi^T.
\tag{2.2}
\]

The vector \(\pi\) need not be the unique stationary distribution. In
particular, (2.1)--(2.2) allow reducible matrices: a positive convex
combination of stationary measures on disjoint closed classes is sufficient.
Irreducibility is one way to obtain a positive stationary vector, but it is
not an assumption of the theorem.

Fix a finite number \(J\ge1\) of delay layers and finite nonnegative delays
\(0\le\tau_j<\infty\). Let
\(B_j\in\mathbb R^{N\times N}\), \(j=1,\ldots,J\), and let
\(\alpha_j\ge0\) satisfy

\[
 (B_j)_{ik}\ge0,
 \qquad
 B_j\mathbf1=\alpha_j\mathbf1,
 \qquad
 \pi^TB_j=\alpha_j\pi^T,
 \qquad
 \sum_{j=1}^J\alpha_j=1.
\tag{2.3}
\]

The layers need not commute with \(P\) or with one another. They need not be
rank one, symmetric, primitive, or individually stochastic. A zero weight
\(\alpha_j=0\) simply forces \(B_j=0\) by nonnegativity and the row-mass
condition.

The exact consequences used below are

\[
 \pi^T(P-I)=0,
 \qquad
 \pi^TB_j=\alpha_j\pi^T,
 \qquad
 (P-I)\mathbf1=0,
 \qquad
 B_j\mathbf1=\alpha_j\mathbf1.
\tag{2.4}
\]

## 3. FHN decision equation under a nodewise recovery clamp

Let

\[
 f(s)=s-\frac{s^3}{3},
 \qquad
 G(s)=\kappa_1s+\kappa_3(s-1)^3,
\tag{3.1}
\]

with \(\varepsilon=1/5\), \(D=3\), and

\[
 (\kappa_1,\kappa_3)\in
 U=[0.199999999999,0.200000000001]
 \times[0.249999999999,0.250000000001].
\tag{3.2}
\]

The arguments below work for every \(D\ge0\); the numerical certificate uses
the same \(D=3\) FHN model as the tracked scalar branch.

During the decision stage, impose the ideal nodewise state constraint

\[
 w_i(t)=0,\qquad i=1,\ldots,N.
\tag{3.3}
\]

This is stronger than fixing only \(\pi^Tw\). It may be represented formally
by nodewise recovery inputs that cancel the entire recovery vector field, but
no bound on those inputs is proved. After (3.3), the voltage RFDE is

\[
 \dot v
 =f(v)+D(P-I)v
 +\varepsilon\left\{
   \sum_{j=1}^J B_jG(v(t-\tau_j))-G(v)\right\}.
\tag{3.4}
\]

All vector nonlinearities in (3.4) act componentwise. Let
\(\tau_*=\max_j\tau_j\) and use the phase space
\(C([-\tau_*,0],\mathbb R^N)\).

The nodewise clamp is a real strengthening of the control protocol. Without
it, a componentwise term \(-w_i\) remains at the zero-voltage boundary, and a
collective clamp alone does not yield general-topology orthant invariance
without an additional recovery-versus-scaffold margin.

## 4. RFDE orthant invariance

Define the closed history orthants

\[
 \mathcal K_+
 =\{\phi:\phi_i(\theta)\ge0
       \text{ for all }i,\theta\},
 \qquad
 \mathcal K_-
 =\{\phi:\phi_i(\theta)\le0
       \text{ for all }i,\theta\}.
\tag{4.1}
\]

The key boundary property is non-strict quasipositivity, not strict inward
pointing.

> **Lemma 4.1 (positive and negative history orthants are invariant).**
> Every solution of (3.4) with initial history in \(\mathcal K_+\) remains
> componentwise nonnegative. Every solution with initial history in
> \(\mathcal K_-\) remains componentwise nonpositive.

**Proof.** Let \(\psi\in\mathcal K_+\) and suppose
\(\psi_i(0)=0\). Since \(f(0)=0\), \(D\ge0\), and \(P\ge0\),

\[
 D\{(P-I)\psi(0)\}_i=D(P\psi(0))_i\ge0.
\tag{4.2}
\]

The gain function is strictly increasing because

\[
 G'(s)=\kappa_1+3\kappa_3(s-1)^2>0.
\tag{4.3}
\]

Thus \(G(\psi_k(-\tau_j))\ge G(0)\). The nonnegative row of \(B_j\)
has mass \(\alpha_j\), so

\[
 \left\{\sum_{j=1}^J
 B_jG(\psi(-\tau_j))\right\}_i
 \ge \sum_{j=1}^J\alpha_jG(0)=G(0).
\tag{4.4}
\]

The current subtraction in (3.4) is exactly \(G(\psi_i(0))=G(0)\).
Hence the \(i\)-th RFDE vector-field component is nonnegative at every
positive-orthant boundary history.

For completeness, this tangent condition gives invariance even when the
boundary derivative is zero. On any bounded time interval the polynomial
RFDE field is locally Lipschitz. Compare a history with its componentwise
positive part. The boundary inequality above and local Lipschitz continuity
give a Dini inequality

\[
 D^+M(t)\le L M(t),
 \qquad
 M(t)=\max_i\sup_{t-\tau_*\le s\le t}(-v_i(s))_+.
\tag{4.5}
\]

Since \(M(0)=0\), Gronwall's inequality gives \(M(t)=0\). Repeating this
argument on consecutive bounded continuation intervals proves positive
orthant invariance.

If \(\psi\in\mathcal K_-\) and \(\psi_i(0)=0\), then
\((P\psi(0))_i\le0\), every delayed \(G\)-value is at most \(G(0)\), and
the inequalities (4.2)--(4.4) reverse. The vector field is nonpositive at
the negative-orthant boundary. Applying the same negative-part argument to
\(-v\) proves invariance of \(\mathcal K_-\). \(\square\)

Lemma 4.1 allows tangency and zero components. It does not assert that every
boundary component points strictly inward, nor that every node becomes
strictly positive or strictly negative.

## 5. Exact balanced mean equation

Let

\[
 x(t)=\pi^Tv(t).
\tag{5.1}
\]

> **Lemma 5.1 (topology disappears from the balanced mean).** Every solution
> of (3.4) satisfies
> \[
> \dot x
> =\pi^Tf(v)
> +\varepsilon\left\{
>   \sum_{j=1}^J\alpha_j\pi^TG(v(t-\tau_j))
>   -\pi^TG(v)\right\}.
> \tag{5.2}
> \]

**Proof.** Multiply (3.4) by \(\pi^T\). The instantaneous scaffold vanishes
by \(\pi^T(P-I)=0\), and each delayed layer projects according to
\(\pi^TB_j=\alpha_j\pi^T\). \(\square\)

No norm estimate, mixing estimate, or network reduction error appears in
(5.2). It is an exact identity.

## 6. Nonlinear one-sided growth constants

The exact secant identity is

\[
 G(s)-G(0)
 =s\{\kappa_1+\kappa_3(s^2-3s+3)\}.
\tag{6.1}
\]

For \(0\le s\le H\le3/2\),

\[
 f(s)\ge\left(1-\frac{H^2}{3}\right)s,
 \qquad
 G(s)-G(0)\le(\kappa_1+3\kappa_3)s.
\tag{6.2}
\]

For \(-H\le s\le0\),

\[
 f(s)\le\left(1-\frac{H^2}{3}\right)s,
\tag{6.3}
\]

and

\[
 G(s)-G(0)
 \ge
 \{\kappa_1+\kappa_3(H^2+3H+3)\}s.
\tag{6.4}
\]

Define

\[
 c_+(H)=1-\frac{H^2}{3}
 -\varepsilon(\kappa_1+3\kappa_3),
 \qquad 0<H\le\frac32,
\tag{6.5}
\]

and

\[
c_-(H)=1-\frac{H^2}{3}
-\varepsilon\{\kappa_1+\kappa_3(H^2+3H+3)\}.
\tag{6.6}
\]

Here (6.6) is used for \(H>0\) whenever its right-hand side is positive.

> **Lemma 6.1 (topology-independent mean growth).** Suppose a positive
> solution has not yet reached the face \(H\), so that
> \(0\le v_i(t)<H\) for every \(i\). Then
> \[
> \dot x(t)\ge c_+(H)x(t).
> \tag{6.7}
> \]
> If a negative solution has not yet reached \(-H\), then
> \[
> \dot x(t)\le c_-(H)x(t).
> \tag{6.8}
> \]

**Proof.** In the positive orthant, Lemma 4.1 makes every delayed voltage
nonnegative, so strict monotonicity of \(G\) gives
\(G(v_k(t-\tau_j))\ge G(0)\). Because
\(\sum_j\alpha_j=1\), the total delayed contribution in (5.2) is at least
\(G(0)\). Apply (6.2) componentwise and use
\(\pi^T\mathbf1=1\) to obtain (6.7).

In the negative orthant, every delayed \(G\)-value is at most \(G(0)\).
Equations (6.3)--(6.4) then give (6.8). \(\square\)

Neither proof requires delayed monotonic ordering such as
\(v(t-\tau_j)\le v(t)\).

## 7. General-topology nodewise first-hit theorem

For \(H>0\), define the first nodewise positive and negative face times

\[
 T_+(H)=\inf\{t\ge0:\max_i v_i(t)=H\},
 \qquad
 T_-(H)=\inf\{t\ge0:\min_i v_i(t)=-H\}.
\tag{7.1}
\]

If a face is already met at \(t=0\), the corresponding first-hit statement
is immediate. The nontrivial case has all current components strictly inside
the target box.

> **Theorem 7.1 (balanced-general-topology controlled first hit).**
> Assume (2.1)--(2.3), \(0\le\tau_j<\infty\) for the finite family
> \(j=1,\ldots,J\), \(D\ge0\), and the ideal nodewise clamp (3.3).
>
> 1. Let the initial history lie in \(\mathcal K_+\), assume
>    \(0\le v_i(0)<H\), \(x_0:=\pi^Tv(0)>0\),
>    \(0<H\le3/2\), and \(c_+(H)>0\). Then
>    \[
>      T_+(H)\le\frac1{c_+(H)}\log\frac{H}{x_0}.
>    \tag{7.2}
>    \]
> 2. Let the initial history lie in \(\mathcal K_-\), assume
>    \(H>0\), \(-H<v_i(0)\le0\), \(x_0:=\pi^Tv(0)<0\), and
>    \(c_-(H)>0\). Then
>    \[
>      T_-(H)\le\frac1{c_-(H)}\log\frac{H}{|x_0|}.
>    \tag{7.3}
>    \]
>
> Both statements hold for every finite \(N\), uniformly over every topology
> satisfying the balance and nonnegativity assumptions.

**Proof.** In the positive case, Lemma 4.1 preserves the positive orthant.
If no node has reached \(H\), Lemma 6.1 and Gronwall's inequality give

\[
 x(t)\ge x_0e^{c_+(H)t}.
\tag{7.4}
\]

Before the first hit the current state remains in the compact box
\([0,H]^N\). The finitely delayed polynomial RFDE therefore has the standard
continuation property through every finite time before that hit.

At the right-hand side of (7.2), (7.4) gives \(x(t)\ge H\). But if every
component were still strictly below \(H\), the positive normalized weights
\(\pi_i\) would give \(x(t)<H\), a contradiction. The negative proof is the
same: (6.8) gives

\[
 x(t)\le x_0e^{c_-(H)t},
\tag{7.5}
\]

which reaches \(-H\) by (7.3), while a convex combination of components
strictly above \(-H\) must remain above \(-H\). \(\square\)

The theorem requires only a nonzero current mean, not a uniform
componentwise distance from zero. Components may start at zero and may touch
zero later; orthant invariance prevents them from crossing to the opposite
sign. This is stronger than the collective-clamp theorem because the
nodewise recovery term has been removed exactly.

## 8. Directed detector and excursion constants

The certificate fixes a uniform mean magnitude

\[
 |x_0|\ge0.06.
\tag{8.1}
\]

This is only for the published uniform deadlines. Theorem 7.1 itself uses
the actual nonzero \(|x_0|\).

### 8.1 Detector faces \(H=1\)

For \(H=1\),

\[
 c_+(1)=\frac23-\varepsilon(\kappa_1+3\kappa_3),
 \qquad
 c_-(1)=\frac23-\varepsilon(\kappa_1+7\kappa_3).
\tag{8.2}
\]

The 160-bit directed certificate gives

\[
 c_+(1)\ge
 0.4766666666658666666666666666666666666666666666646126692,
\tag{8.3}
\]

\[
 c_-(1)\ge
 0.2766666666650666666666666666666666666666666666635348367.
\tag{8.4}
\]

Thus every eligible positive history satisfying (8.1) has a nodewise
\(+1\) hit by

\[
 T_+(1)\le
 5.902260244961031137243652536848575659808442962835976857,
\tag{8.5}
\]

and every eligible negative history has a nodewise \(-1\) hit by

\[
 T_-(1)\le
 10.16895439798665070214560551365587630590745188143446848.
\tag{8.6}
\]

### 8.2 Finite controlled excursions

For \(H_+=3/2\),

\[
 c_+(H_+)\ge
 0.05999999999919999999999999999999999999999999999887256099,
\tag{8.7}
\]

and therefore

\[
 T_+(3/2)\le
 53.64793041518531822556111535054706952219400607031937024.
\tag{8.8}
\]

For \(H_-=6/5\),

\[
 c_-(H_-)\ge
 0.07799999999819199999999999999999999999999999999574747383,
\tag{8.9}
\]

and

\[
 T_-(6/5)\le
 38.40682402081321193929299824780490405780298576531744953.
\tag{8.10}
\]

By continuity, a trajectory reaching \(+3/2\) crosses \(+1\), and a
trajectory reaching \(-6/5\) crosses \(-1\). The detector can be externally
latched. The theorem does not assert a no-return property across \(\pm1\),
nor does it identify these finite voltage excursions with full biological
action potentials or quiet basins.

All constants in (8.3)--(8.10) are independent of \(N\), \(P\), the
individual \(B_j\), and any topology mixing rate.

## 9. Why Dobrushin contraction and uniqueness are absent

A Dobrushin coefficient controls contraction of differences between nodes.
The proof above never estimates those differences. It uses only:

1. nonnegative matrices and normalized row masses to preserve the orthants;
2. a common left balance to cancel the scaffold and project the delayed
   layers in the mean equation;
3. positivity and normalization of \(\pi\) to turn a mean threshold into a
   nodewise threshold.

Thus a reducible permutation scaffold is allowed. It has no strict
Dobrushin contraction and has nonunique stationary distributions, yet any
chosen strictly positive stationary mixture that is also respected by the
delay layers satisfies the theorem.

Strict positivity of every \(\pi_i\) is not needed for the local boundary
calculation. It is retained so that \(x=\pi^Tv\) is a faithful collective
coordinate involving every node. Uniqueness of \(\pi\) is not required.

## 10. Algebraic inheritance of the synchronous branch

Return temporarily to the unclamped baseline FHN network

\[
\begin{aligned}
 \dot v={}&f(v)-w+D(P-I)v\\
 &+\varepsilon\left\{
   \sum_{j=1}^J B_jG(v(t-\tau_j))-G(v)\right\},\\
 \dot w={}&\varepsilon(v-a\mathbf1)+E(P-I)w.
\end{aligned}
\tag{10.1}
\]

The row-mass identities in (2.1) and (2.3) make the synchronous history
subspace invariant. Substituting

\[
 v(t)=q(t)\mathbf1,\qquad w(t)=p(t)\mathbf1
\tag{10.2}
\]

into (10.1) gives exactly

\[
\begin{aligned}
 \dot q={}&f(q)-p
 +\varepsilon\left\{
   \sum_{j=1}^J\alpha_jG(q(t-\tau_j))-G(q)\right\},\\
 \dot p={}&\varepsilon(q-a).
\end{aligned}
\tag{10.3}
\]

The topology has disappeared. In particular, for

\[
 J=2,\qquad
 (\alpha_1,\alpha_2)=\left(\frac12,\frac12\right),\qquad
 (\tau_1,\tau_2)=(4\sqrt5,5\sqrt5),
\tag{10.4}
\]

equation (10.3) is the same scalar periodic RFDE used by the tracked
frequency--amplitude branch. Its synchronous lift exists on every balanced
topology satisfying (2.1)--(2.3).

This is only an invariant-subspace identity. It does not show that the
synchronous periodic solution attracts transverse perturbations, that its
full-network Floquet spectrum is hyperbolic, or that an asynchronous canard
root agrees with the scalar root.

## 11. Staged \((F,A,-r)\) map

Let \(b=(\kappa_1,\kappa_3)\), and let \(F(b)\) and \(A(b)\) be the frequency
and unsquared voltage amplitude of the tracked scalar periodic branch. In a
later decision stage, let the ideal reset prepare the uniform complete
history

\[
 v(\theta)=r\mathbf1,\qquad w(\theta)=0,
 \qquad -\tau_*\le\theta\le0,
\tag{11.1}
\]

and then apply the nodewise recovery clamp. Since (10.3) makes the baseline
periodic outputs topology-independent on synchrony, while \(r\) is a
separate staged reset coordinate, the formal product map remains

\[
 Q_A(b,r)=\bigl(F(b),A(b),-r\bigr).
\tag{11.2}
\]

Consequently its differential has the same block form

\[
 DQ_A(b,r)=
 \begin{pmatrix}
  D_b(F,A)(b) & 0\\
  0 & -1
 \end{pmatrix}.
\tag{11.3}
\]

Equations (11.2)--(11.3) are an algebraic synchronous-branch and staged-reset
inheritance statement. They do not promote the existing scalar target ball
to a theorem about attraction of arbitrary network histories, and they do
not identify the operational reset separator with a general-topology
maximal-canard root.

## 12. Sharp boundaries and counterexamples

The structural assumptions are not decorative.

1. **Nonnegative scaffold.** Row mass alone is insufficient. For example,
   \[
   P=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}
   \tag{12.1}
   \]
   has row sum one and the positive stationary weight
   \(\pi=(1/2,1/2)^T\), but at \(v_1=0<v_2\) the scaffold contribution
   \((Pv)_1=-v_2<0\), so the positive orthant need not be invariant.

2. **Normalized delay row mass.** At a zero component the current control
   value is \(G(0)\). The identity
   \(\sum_j(B_j\mathbf1)_i=1\) is what cancels that constant. If the combined
   row mass differs from one, the boundary term contains an uncontrolled
   multiple of \(G(0)=-\kappa_3\).

3. **Common left balance.** The identity \(\pi^TP=\pi^T\) is required to
   eliminate the instantaneous topology from the mean. The identities
   \(\pi^TB_j=\alpha_j\pi^T\) give the exact projected delay equation (5.2).
   Without them, the claimed topology-independent collective equation is
   false.

4. **Nodewise recovery clamp.** If only \(\pi^Tw=0\) is imposed, individual
   terms \(-w_i\) remain at the orthant boundary. General-topology
   quasipositivity then fails without further componentwise recovery bounds
   or a strictly inward scaffold estimate.

## 13. Claim ledger

The following statements are proved.

- Positive and negative complete-history orthant invariance for every finite
  balanced nonnegative topology under the ideal nodewise recovery clamp.
- Exact topology cancellation in the \(\pi\)-weighted mean equation.
- Fully nonlinear, nonsynchronous, \(N\)-independent nodewise first hits of
  \(\pm1\), with the explicit formula
  \(\log(H/|\pi^Tv(0)|)/c_\pm(H)\).
- Finite controlled excursions to \(+3/2\) and \(-6/5\).
- Absence of any need for rank-one structure, Dobrushin contraction,
  irreducibility, or a unique stationary distribution.
- Algebraic inheritance of the synchronous scalar RFDE and, for the
  reference row masses and delays, the formal staged map
  \(Q_A(b,r)=(F(b),A(b),-r)\).

The following statements are not proved.

- a bounded or noisy implementation of the nodewise state clamp;
- transverse attraction or synchronization from arbitrary histories;
- full-network periodic-orbit hyperbolicity;
- equality between a general-topology network canard root and the scalar
  root;
- a biological pulse basin, quiet basin, action potential, or periodic
  attraction beyond the finite excursion face;
- hardware feasibility or actuator-energy bounds;
- signed, unbalanced, state-dependent, or infinite network topologies.

The safe short claim is:

> For every finite nonnegative balanced topology sharing a positive
> stationary weight, an ideal nodewise-recovery-clamped delayed FHN decision
> stage preserves the voltage history orthants and forces a nonsynchronous,
> fully nonlinear, topology-independent nodewise detector hit and finite
> excursion from every nonzero same-sign collective mean.

## 14. Exact and directed certificate

The certificate is generated by

~~~text
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_general_network_sign_cone.py
~~~

The result artifact is

~~~text
experiments/results/fhn_general_network_sign_cone.json
SHA-256: 1dd606d7f4aec1ea857f1c53d4e60106fc2737089b67e989aa7b192fe3ca43fb
~~~

It is bound to the tracked scalar separator artifact

~~~text
experiments/results/fhn_same_model_separator.json
SHA-256: 9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86
~~~

The exact audit includes a non-rank-one topology with nonuniform positive
\(\pi\), a reducible full-rank permutation topology with a nonunique
stationary distribution, and a three-delay directed cycle. It checks all
row-mass and left-balance residuals with SymPy exact arithmetic. The FHN
factorizations and the central constants

\[
 \frac{143}{300},\qquad
 \frac{83}{300},\qquad
 \frac3{50},\qquad
 \frac{39}{500}
\tag{14.1}
\]

are exact. Public gain-box and deadline endpoints use 160-bit MPFR directed
rounding. The artifact scope explicitly rejects bounded actuation,
transverse attraction, full-network periodic hyperbolicity,
general-topology canard-root equivalence, biological basin capture, and
hardware claims.
