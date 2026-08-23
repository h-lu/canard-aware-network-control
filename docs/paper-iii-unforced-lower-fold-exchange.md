# Paper III Gate U-EX: lower-fold exchange, an exact obstruction, and a repaired event

Status: **the singular lower-fold orientation and middle-branch unstable
action of the declared two-module FHN model are proved. An exact Airy
ODE-subclass theorem proves that the initial sign relative to a selected
repelling trajectory does not classify every nonzero offset through a
drifting ordinary fold: in that exact Airy model the fold-side event root has
a nonzero exponentially small shift. Thus geometric and fold-event roots need
not coincide, and Gate U-EX, as previously worded, is too strong. A causal
one-passage event using moving slow-base tubes and a lower-fold section is
defined below. Its upgrade and nonzero-shift factorization for the full
long-delay RFDE, and its equivalence to the biological pulse/quiet first-hit
event, remain open under explicit hypotheses.**

The executable algebra, action quadrature, and Airy identities are in
src/canard_control/unforced_lower_fold_exchange.py; regressions are in
tests/test_unforced_lower_fold_exchange.py. This note does not change the
frozen JNS manuscript.

## 1. Why this gate changes the claimed threshold

Suppose Gate U-SF supplies a selected middle-branch history and a scalar
complete-history unstable coordinate $g$ on the reset section
$\rho_0=-1/2$. The old Gate U-EX asked for

\[
 g<0\Longleftrightarrow\text{pulse},\qquad
 g>0\Longleftrightarrow\text{quiet},
 \tag{1.1}
\]

for **every** nonzero $g$ in a fixed reset neighborhood, with $g=0$ the
unique physical separator. This is not an innocuous continuation of a
local stable-fiber theorem.

Along the physical middle branch,

\[
 \dot\rho=\varepsilon(\xi^m(\rho)-\mu)<0.
 \tag{1.2}
\]

The trajectory moves from $\rho_0$ toward the lower fold
$\mathfrak f_-$. A normal offset grows by an exponential factor of order
$\exp(\mathcal A_-/\varepsilon)$. Consequently offsets of order
$\exp(-\mathcal A_-/\varepsilon)$ reach the lower-fold chart before a
signed outer exit decides them. An ordinary dynamic fold then has its own
transition map. There is no reason for that map's zero to be the selected
repelling trajectory $g=0$; Section 4 proves in the exact fold normal form
that it is not.

This creates three distinct objects:

1. the **geometric middle-history coordinate** $g=0$, supplied only after
   Gate U-SF;
2. the **lower-fold exchange coordinate** defined by a one-passage fold
   section; and
3. the **biological pulse/quiet boundary**, defined by downstream detector
   hits.

They may be exponentially close. They cannot be declared equal without a
separate factorization and capture theorem.

## 2. The physical lower fold is an ordinary drifting saddle-node

Recall the exact singular critical graph

\[
 G(a,b)=2a^3+2a-4b-b^3-4=0,
 \tag{2.1}
\]

\[
 \xi(a)=\sigma\left(\frac{a-1}{2}+\frac{b(a)}4\right),
 \qquad
 \rho(a)=\frac{\sigma}{2}\bigl(a-a^3+b(a)\bigr),
 \qquad \sigma=\sqrt{3/2}.
 \tag{2.2}
\]

The exact Sturm calculation in the physical-pulse note locates the lower
fold at

\[
 -\frac{743}{1000}<a_-<-\frac{742}{1000}.
 \tag{2.3}
\]

Since $G_b=-4-3b^2<0$, rational endpoint evaluation gives

\[
 -\frac{1174}{1000}<b_-<-\frac{1171}{1000}.
 \tag{2.4}
\]

Indeed,
$G(-743/1000,-1174/1000)=775121/10^8>0$ and
$G(-742/1000,-1171/1000)=-2262753/(2\cdot10^8)<0$,
while $G_a>0$ and $G_b<0$.

Differentiate (2.1):

\[
 b'=\frac{6a^2+2}{3b^2+4},
 \qquad
 b''=\frac{12a(3b^2+4)-(6a^2+2)6bb'}{(3b^2+4)^2}.
 \tag{2.5}
\]

The first term in $b''$ is bounded below by
$-12(743/1000)/(4+3(1171/1000)^2)>-1.1$, while the second term is
positive. Hence

\[
 -6a_-+b''(a_-)>6(742/1000)-1.1>0,
 \qquad \rho''(a_-)>0.
 \tag{2.6}
\]

Thus $\rho$ has a nondegenerate minimum at the lower fold. Direct
evaluation gives $\rho''(a_-)=2.282205636\ldots$; this decimal is only a
diagnostic.

Let $A_-=D_vf(v_-,w_-)$. Its determinant vanishes and its trace is
strictly negative. Choose

\[
 p=\binom{1/2}{v_{-,1}^2-1/2}>0,
 \qquad
 \widetilde q=\binom{1+v_{-,2}^2}{1/2}>0,
 \qquad
 q=\frac{\widetilde q}{\widetilde q^Tp}.
 \tag{2.7}
\]

Then $A_-p=0$, $q^TA_-=0$, and $q^Tp=1$. Put
$y=\rho-\rho_-$, and let $x$ be the fast center coordinate in the
$p$-direction. The leading center equation is

\[
 \dot x=\alpha x^2+\beta y+\text{higher-order terms},
 \tag{2.8}
\]

where

\[
 \alpha=\frac12q^TD_v^2f[p,p]
 =-q_1v_{-,1}p_1^2-q_2v_{-,2}p_2^2>0,
 \qquad
 \beta=q^Tf_\rho=-q^T\binom12<0.
 \tag{2.9}
\]

Both inequalities are exact: (2.3)--(2.4) make both fold voltages negative,
and $v_{-,1}^2>1/2$, so all components in (2.7) are positive. Finally,

\[
 \dot y=\varepsilon(\xi_- -\mu)+\text{higher-order terms}.
 \tag{2.10}
\]

For example, uniformly for $|\mu|\le1/2$, this leading drift is negative.
The diagnostic values at $\mu=0$ are

\[
\begin{aligned}
 \rho_-&=-0.9221564930\ldots,&
 \xi_-&=-1.4259744890\ldots,\\
 \operatorname{tr}A_-&=-3.389003415\ldots,&
 \alpha&=0.4559546365\ldots,\\
 \beta&=-2.397441997\ldots.&
\end{aligned}
\tag{2.11}
\]

> **Proposition 2.1 (proved singular lower-fold orientation).** The lower
> fold of the declared two-module FHN fast layer is a nondegenerate ordinary
> fold with one strong stable fast direction. On the bistable side $y>0$,
> the branch $x<0$ is attracting and the branch $x>0$ is the saddle middle
> branch. For the declared unfolding box near $\mu=0$, the slow flow carries
> both branches toward $y=0$. The leading reduced orientation is therefore
>
> \[
>   \dot x=\alpha x^2-|\beta|y+\cdots,
>   \qquad \dot y=-\varepsilon c_-+\cdots,
>   \qquad \alpha,|\beta|,c_->0.
>   \tag{2.12}
> \]

The proof is (2.3)--(2.10). This is precisely the ordinary-fold geometry
treated by blow-up in the finite-dimensional setting; see
[Krupa--Szmolyan](https://doi.org/10.1137/S0036141099360919). That paper
does not supply the missing complete-history theorem for the present delay
$\theta/\sqrt\varepsilon$.

## 3. The exact physical outer action

Let $a_R$ be the middle equilibrium at $\rho_0=-1/2$. Along the middle
branch the positive fast eigenvalue is

\[
 \lambda_u(a)
 =\frac12\left(\operatorname{tr}A(a)
 +\sqrt{\operatorname{tr}A(a)^2-4\det A(a)}\right)>0.
 \tag{3.1}
\]

For any $\mu>\xi(a_R)$, define

\[
 \boxed{
 \mathcal A_-(\mu)
 =\int_{a_-}^{a_R}
   \frac{\lambda_u(a)\rho'(a)}{\mu-\xi(a)}\,da.}
 \tag{3.2}
\]

Every factor in the integrand is positive in the interior. The integrand
extends continuously by zero at the lower fold. Hence
$\mathcal A_-(\mu)>0$. Notice that
$\xi'(a)=\sigma(1/2+b'(a)/4)>0$, so the single condition
$\mu>\xi(a_R)$ makes the slow drift point toward the lower fold on the
whole retained segment. Linearization about an exact middle tracker gives

\[
 \log\frac{|g(a)|}{|g(a_R)|}
 =\frac1\varepsilon
   \int_a^{a_R}
   \frac{\lambda_u(\alpha)\rho'(\alpha)}
        {\mu-\xi(\alpha)}\,d\alpha
   +\text{subexponential correction}.
 \tag{3.3}
\]

At the declared reset and $\mu=0$, executable quadrature gives

\[
 a_R=0.02354566467\ldots,\qquad
 \xi(a_R)=-0.8551590808\ldots,\qquad
 \mathcal A_-(0)=0.2792680505\ldots.
 \tag{3.4}
\]

The positivity and formula (3.2) are proved; the decimal in (3.4) is not an
interval enclosure. Its scale is already informative:

\[
 e^{-\mathcal A_-/0.01}=7.45\ldots\times10^{-13}.
 \tag{3.5}
\]

Thus a floating-point scan at ordinary reset spacings cannot resolve the
part of Gate U-EX that decides whether a trajectory exits before the lower
fold.

## 4. Exact Airy theorem: the geometric sign is not the fold-side sign

The obstruction can be proved without an asymptotic remainder. Consider

\[
 \dot x=x^2-y,
 \qquad
 \dot y=-\varepsilon,
 \qquad \varepsilon>0.
 \tag{4.1}
\]

This is an ODE and therefore an RFDE whose functional ignores its history,
for every assigned delay length. It has the same ordinary-fold orientation
as (2.12). Its selected graph is already a codimension-one invariant
center-stable sheet in the $(x,y)$ plane. If a genuine stable direction is
desired, adjoining $\dot z=-z$ makes that sheet
$\{x=x_0(y)\}\times\mathbb R_z$ without changing any calculation below.
Put

\[
 z=\frac{y}{\varepsilon^{2/3}}.
 \tag{4.2}
\]

For $c\ge0$, the exact Riccati family

\[
 x_c(y)=\varepsilon^{1/3}
 \frac{\operatorname{Bi}'(z)+c\operatorname{Ai}'(z)}
      {\operatorname{Bi}(z)+c\operatorname{Ai}(z)}
 \tag{4.3}
\]

solves (4.1) while $y$ decreases from a fixed $y_0>0$ to the fold.
The member $c=0$ is the selected repelling solution: as
$y/\varepsilon^{2/3}\to+\infty$, it shadows $x=+\sqrt y$.

The Airy Wronskian gives, for every $c>0$,

\[
 x_c(y_0)-x_0(y_0)
 =-\frac{\varepsilon^{1/3}c}
 {\pi\operatorname{Bi}(z_0)
 [\operatorname{Bi}(z_0)+c\operatorname{Ai}(z_0)]}<0.
 \tag{4.4}
\]

Hence every $c>0$ begins on the same negative side of the selected
repelling trajectory. At the fold, however,

\[
 \operatorname{Bi}(0)=\sqrt3\operatorname{Ai}(0),
 \qquad
 \operatorname{Bi}'(0)=-\sqrt3\operatorname{Ai}'(0),
 \tag{4.5}
\]

so

\[
 \operatorname{sign}x_c(0)=\operatorname{sign}(\sqrt3-c).
 \tag{4.6}
\]

> **Theorem 4.1 (exact drifting-fold sign obstruction).** In (4.1), the
> selected repelling trajectory is $c=0$. Every $c>0$ starts on its negative
> side. Nevertheless every $0<c<\sqrt3$ reaches the fold on the same
> positive side as the selected trajectory, whereas every $c>\sqrt3$
> reaches the negative fold side. The unique fold-side event root is
> $c=\sqrt3$, not $c=0$.

This is an all-offset statement: it includes arbitrarily small negative
offsets, not just offsets above an $\varepsilon$-dependent deadband.

At the reset section the event root is shifted from the selected repelling
trajectory by

\[
\begin{aligned}
 \Delta x_{\rm EX}
 &=-\frac{\varepsilon^{1/3}\sqrt3}
 {\pi\operatorname{Bi}(z_0)
 [\operatorname{Bi}(z_0)+\sqrt3\operatorname{Ai}(z_0)]}\\
 &\sim-\sqrt{3y_0}
 \exp\left\{-\frac{4y_0^{3/2}}{3\varepsilon}\right\}.
\end{aligned}
\tag{4.7}
\]

Thus the two roots agree to every algebraic order in $\varepsilon$, but
they differ for every fixed $\varepsilon>0$. This distinction is exactly
what an all-offset U-EX theorem must see.

Theorem 4.1 is not a counterexample to a particular detector outcome of the
full FHN RFDE. It is a counterexample to the proposed deduction

\[
 \text{local middle-history separator}
 \quad\Longrightarrow\quad
 \text{all-offset signed lower-fold outcome}.
 \tag{4.8}
\]

Proposition 2.1 places the physical singular model in the same ordinary-fold
orientation, but this alone transfers neither the Airy coefficient nor its
nonvanishing.  Equality or non-equality of the physical geometric and event
roots remains conditional on the full complete-history factorization
(6.1)--(6.2).

## 5. Moving slow-base tubes: the smallest coherent passage event

Fixed-layer blocks require $|\rho-\rho_0|=O(\varepsilon)$. They cannot
observe trajectories that spend $O(\varepsilon^{-1})$ fast time near the
middle branch. Replace them by a tube whose base follows the slow tracker.

Assume Gate U-SF has supplied, for
$\rho\in[\rho_c(\varepsilon),\rho_0]$,

- a selected history $\Gamma^m_{\varepsilon,u}(\rho)$;
- a $C^1$ complete-history relative-growth graph defining coordinate
  $G_{\varepsilon,u,\rho}(\phi)$, with $G=0$ on the selected middle
  history; and
- a monotone current recovery coordinate along all retained histories.

Choose

\[
 \rho_c(\varepsilon)=\rho_-+L\varepsilon^{2/3},
 \qquad
 r_\varepsilon(\rho)\asymp
 \min\{r_0,\sqrt{\rho-\rho_-}\}.
 \tag{5.1}
\]

Define the moving outer tube

\[
 \mathfrak T^m_\varepsilon
 =\left\{\phi:\rho_c(\varepsilon)<\rho(\phi_w(0))<\rho_0,
 \ |G_{\varepsilon,u,\rho}(\phi)|<r_\varepsilon(\rho)
 \right\}.
 \tag{5.2}
\]

Its first boundary hit has three possibilities:

\[
 G=-r_\varepsilon(\rho),\qquad
 G=+r_\varepsilon(\rho),\qquad
 \rho=\rho_c(\varepsilon).
 \tag{5.3}
\]

The first two are signed **outer side exits**. The third is a **lower-fold
cap**, not an unresolved failure. A lower-fold transition map carries the
cap to a fixed outgoing section $\Sigma_-^{\rm out}$. Choose a transverse
signed coordinate $S_-$ on that section and define

\[
 \mathscr S^{\rm fold}_{\varepsilon,u}(a)
 =S_-\bigl(\Pi_-^\varepsilon
       (x^R_{\tau_c(a)}(a,u))\bigr).
 \tag{5.4}
\]

Here $\tau_c(a)$ is the first cap hit and $\Pi_-^\varepsilon$ is the
complete-history fold passage. The experiment stops at the first side exit
or at $\Sigma_-^{\rm out}$. Thus (5.3)--(5.4) define a finite, causal,
one-passage event and do not assume an infinite-time no-return theorem.

> **Definition 5.1 (repaired operational coordinate).** The zero of
> $\mathscr S^{\rm fold}_{\varepsilon,u}$, when unique and transverse, is
> the **unforced lower-fold exchange threshold**. It is a new operational
> safety coordinate. It is not called the unforced maximal-canard root and
> is not called the biological pulse threshold until the comparison and
> capture theorems in Sections 6--7 are proved.

The radius in (5.1) is essential. A fixed normal radius does not match the
coalescing stable and saddle branches. The cap scale
$y=O(\varepsilon^{2/3})$, $x=O(\varepsilon^{1/3})$ is the ordinary-fold
blow-up scale.

## 6. The exact conditional theorem needed for the physical RFDE

The following theorem separates the implication from the hypotheses that
remain to be proved for the model.

There is a specific long-delay seam. The ordinary-fold passage lasts
$O(\varepsilon^{-1/3})$ in fast time, whereas

\[
 \tau_j=\theta_j\varepsilon^{-1/2},
 \qquad
 \frac{\tau_j}{\varepsilon^{-1/3}}
 =\theta_j\varepsilon^{-1/6}\longrightarrow\infty.
 \tag{6.0}
\]

Every delayed query during the fold passage therefore points back into the
incoming outer history. Its slow-base backtrack is
$O(\varepsilon\tau_j)=O(\sqrt\varepsilon)$, which is larger than the local
$O(\varepsilon^{2/3})$ fold scale. The delayed voltage force remains
pointwise $O(\varepsilon)$ on bounded histories, so it does not change the
leading signs in Proposition 2.1, but a local current-state fold reduction
cannot discard those incoming histories when proving an exponentially
accurate event map.

Let $U\Subset U^\circ$ be a compact control box. Suppose, uniformly for
$u\in U^\circ$ and $0<\varepsilon\le\varepsilon_0$, that:

1. **Outer histories.** Gate U-SF supplies the tracker, moving tube, and a
   uniformly $C^1$ reset fiber coordinate
   $g=G_{\varepsilon,u,\rho_0}(\widehat\Phi^R_\varepsilon(a,u))$, with
   $|\partial_ag|\ge c_g>0$.
2. **Outer exchange.** Until a side or cap hit, sign is preserved and the
   cap entry coordinate has the uniform factorization
   \[
     X_{\rm in}
     =P_\varepsilon(u)e^{\mathcal A_-(u)/\varepsilon}g
       +R^{\rm out}_\varepsilon(g,u),
     \tag{6.1}
   \]
   where $\mathcal A_-\in C^1(U^\circ)$,
   $\inf_U\mathcal A_->0$, and the $C^1$ norms of
   $P_\varepsilon$, $P_\varepsilon^{-1}$, and their parameter derivatives
   are uniformly subexponential. The normalized $C^1$ remainder is $o(1)$
   on the exponentially scaled cap tube.
3. **Complete-history fold map.** The cap-to-outgoing-section map exists
   for every retained complete history, is $C^1$, and
   \[
     S_-\circ\Pi_-^\varepsilon(X_{\rm in},u)
     =B_\varepsilon(u)+Q_\varepsilon(u)X_{\rm in}
       +R^{\rm fold}_\varepsilon(X_{\rm in},u),
     \tag{6.2}
   \]
   where the $C^1$ norms of
   $B_\varepsilon$, $B_\varepsilon^{-1}$, $Q_\varepsilon$, and
   $Q_\varepsilon^{-1}$ are uniformly subexponential and the normalized
   $C^1$ remainder is $o(1)$. The leading cap root
   $-B_\varepsilon/Q_\varepsilon$ stays in a declared compact subset of the
   fold-input chart.
4. **No corner ambiguity.** Side and cap hits are transverse, their
   intersections are assigned by one declared priority rule, and the
   resulting one-passage event is continuous across the chart overlaps.
   The joint remainder bounds in (6.1)--(6.2), after composition and
   division by
   $Q_\varepsilon P_\varepsilon e^{\mathcal A_-/\varepsilon}$, must give
   the uniform $C^1$ remainder displayed in (6.6); separate pointwise
   little-$o$ estimates are not sufficient.

> **Theorem 6.1 (conditional RFDE lower-fold root).** Under hypotheses
> 1--4, after shrinking the reset interval, the repaired fold event has one
> $C^1$ root $a_{\rm EX}(u)$. If $a_{\rm geo}(u)$ is the geometric root
> $g=0$, then
>
> \[
>  g(a_{\rm EX}(u),u)
>  =-\frac{B_\varepsilon(u)}
>  {Q_\varepsilon(u)P_\varepsilon(u)}
>  e^{-\mathcal A_-(u)/\varepsilon}(1+o(1)),
>  \tag{6.3}
> \]
>
> uniformly on $U$. In particular,
>
> \[
>  \varepsilon\log
>  |a_{\rm EX}(u)-a_{\rm geo}(u)|
>  \longrightarrow-\mathcal A_-(u),
>  \tag{6.4}
> \]
>
> and for every $0<\Lambda<\inf_U\mathcal A_-$,
>
> \[
>  \|a_{\rm EX}-a_{\rm geo}\|_{C^1(U)}
>  \le C_\Lambda
>  e^{-(\inf_U\mathcal A_- -\Lambda)/\varepsilon}.
>  \tag{6.5}
> \]

**Proof.** Substitute (6.1) into (6.2) and divide by
$Q_\varepsilon P_\varepsilon e^{\mathcal A_-/\varepsilon}$. The
normalized map is

\[
 g+\frac{B_\varepsilon}{Q_\varepsilon P_\varepsilon}
 e^{-\mathcal A_-/\varepsilon}
 +o_{C^1}(e^{-\mathcal A_-/\varepsilon}).
 \tag{6.6}
\]

The derivative in $g$ is uniformly separated from zero, so the implicit-
function theorem gives one root and (6.3). Uniform two-sided
subexponential bounds give (6.4). Differentiating (6.6) produces at most
polynomial $1/\varepsilon$ factors and parameter derivatives of uniformly
subexponential coefficients; every such factor is absorbed by
$e^{\Lambda/\varepsilon}$, which proves (6.5). Finally
$|\partial_ag|\ge c_g$, together with the uniform $C^1$ upper bound,
transfers the result from $g$ to $a$. $\square$

Theorem 6.1 is a proved implication, not a verification of hypotheses 1--4
for the physical RFDE. The Airy theorem identifies the expected
$B_0\ne0$ ordinary-fold mechanism. The main RFDE work is to prove that the
weak long-delay terms preserve (6.1)--(6.2) on complete histories with the
required uniform remainders.

## 7. Why weighted-gradient and cooperativity do not prove no-return

The frozen fast layer has the valuable exact properties

\[
 (4f_1,f_2)^T=-\nabla_vU,
 \qquad
 \dot U=-4f_1^2-f_2^2,
 \tag{7.1}
\]

and an irreducible Metzler current Jacobian. They prove the two singular
heteroclinic channels at fixed recovery. They do not give a Lyapunov or
order theorem for the released RFDE.

First, in the full equation $w$ drifts and the voltage field contains
delayed forcing. Along a released orbit,

\[
 \frac{d}{dt}U(v(t);w(t))
 =-4f_1^2-f_2^2
  +\nabla_vU\cdot(\varepsilon\,\text{delay forcing})
  +\partial_wU\cdot\dot w.
 \tag{7.2}
\]

The last two terms have no fixed sign. They are $O(\varepsilon)$ only
pointwise and can accumulate over $O(\varepsilon^{-1})$ fast time.

Second, for positive $K$ and entrywise-positive delay layers,

\[
 D_{v(t-\tau_j)}\dot v=-\varepsilon K C_j^\eta
 \tag{7.3}
\]

has strictly negative entries. Thus the full history functional fails the
usual quasimonotonicity condition for a cooperative RFDE. Strong
cooperativity of the frozen current layer cannot be copied to history
space.

Consequently, biological equivalence needs an additional statement:

> **Gate U-CAP (physical capture and no-return; open).** Prove that each
> signed outer side exit and each signed lower-fold outgoing history enters
> its declared pulse or quiet detector block before the competing block,
> uniformly on the control box, and that no later itinerary changes the
> declared first hit. The proof must use RFDE trapping/capture regions or a
> finite observation protocol; it cannot cite (7.1) as a global RFDE
> Lyapunov function.

For an operational experiment, the mathematically cheapest repair is to
stop at the one-passage event (5.3)--(5.4). If an infinite-horizon
biological event is required, Gate U-CAP is irreducible.

## 8. Fixed epsilon versus epsilon-uniform status

For each fixed $\varepsilon>0$, standard RFDE smooth dependence gives a
local $C^1$ fold-section event root once a finite passage, a transverse
section, and a nonzero parameter derivative have actually been verified.
This fixed-$\varepsilon$ fact says nothing uniform as
$\varepsilon\downarrow0$.

The all-offset statement is singular for two reasons.

1. Its derivative through the middle passage is of order
   $e^{\mathcal A_-/\varepsilon}$.
2. The relevant histories include reset offsets below every algebraic power
   of $\varepsilon$, and the tube radius shrinks to the fold scale in
   (5.1).

Thus an ordinary local RFDE stable-manifold theorem at one fixed
$\varepsilon$ cannot prove (6.1)--(6.5). Uniformity requires U-OUT\({}^+\)
tracker and relative-growth graph bounds, logarithmic amplification control,
a complete-history fold blow-up, and uniform chart overlaps. Work on finite-dimensional
entry--exit maps, for example
[Hsu--Ruan](https://doi.org/10.1137/19M1295507), clarifies the action
mechanism but does not include the present diverging physical delay.
Similarly, delayed FHN/canard analyses by
[Krupa--Touboul](https://doi.org/10.1007/s00332-015-9268-3) and
[Krupa--Touboul](https://doi.org/10.1007/s10884-015-9478-2) do not by
themselves identify this causal reset event for the weak
$\theta/\sqrt\varepsilon$ history scaling.

The 2026 delayed van der Pol high-order calculation addresses a local canard
parameter and critical orbit. Gate U-EX instead asks how exponentially
small complete-history offsets are amplified over a fixed slow distance and
then sorted by a second, ordinary lower fold. The two analyses are
complementary, not duplicate.

## 9. Hostile proof-status ledger

| Statement | Status | Exact reason |
|---|---|---|
| The physical singular lower fold is nondegenerate and has orientation (2.12) | **Proved** | Rational fold box, nullvectors, Hessian, and slow-drift signs |
| The physical middle action (3.2) is positive | **Proved** | Every factor is positive on the open middle segment |
| $\mathcal A_-(0)=0.2792680505\ldots$ | **Numerical diagnostic** | Accurate quadrature, not interval-enclosed |
| Every nonzero initial fiber sign must select a different fold side | **False as a general implication** | Exact Airy Theorem 4.1 |
| The geometric history root equals the fold-side event root at fixed $\varepsilon$ | **Need not hold; not decided for the physical RFDE** | Exact nonzero shift (4.7) in the Airy normal form; physical comparison requires (6.1)--(6.2) |
| The two roots agree to all algebraic orders | **Proved in the Airy model; conditional for FHN RFDE** | (4.7); physical transfer needs (6.1)--(6.2) |
| Moving-tube/fold event (5.3)--(5.4) is a coherent causal definition | **Defined exactly** | Finite first passage with declared cap and priority rule |
| Full FHN RFDE has a unique $C^1$ fold-event root | **Conditional** | Exact implication Theorem 6.1; hypotheses 1--4 open |
| Full FHN fold-event root has exponent $\mathcal A_-$ | **Conditional** | Requires the complete-history factorization (6.1)--(6.2) |
| Frozen weighted-gradient/cooperative structure excludes every RFDE return | **False inference** | Indefinite terms (7.2) and negative delayed derivatives (7.3) |
| Repaired fold event equals biological pulse/quiet first-hit | **Open** | Requires Gate U-CAP |
| Repaired fold event equals the right-fold canonical canard root | **Open** | Requires reset-to-canard factorization and a proved comparison of the exponential shifts |

The research contribution that survives the audit is sharper than the old
claim: the paper should study a **lower-fold exchange threshold on complete
histories** and prove its comparison factorization.  The shift is exactly
nonzero in the Airy normal form and only conditional for the physical RFDE;
in neither case may a local middle-branch separator automatically be called
the pulse boundary.
