# Eventually smooth selected-event maps for finite-delay RFDEs

Status: **proved formal theorem, fail-closed revision.** This note contains no
model-specific numerical input and proves no concrete return, invariant graph,
crossing, biological onset, routing, capture, or safety statement. In
particular, an ambient event hit is not called a section return without a
terminal section-chart containment hypothesis, and recurrent selected hits
are not used to identify a stable-set germ without section isolation.

The executable theorem record is
[finite_delay_eventually_smooth_selected_return_stage4r.py](../src/canard_control/finite_delay_eventually_smooth_selected_return_stage4r.py),
the atomic generator is
[finite_delay_eventually_smooth_selected_return_stage4r.py](../experiments/finite_delay_eventually_smooth_selected_return_stage4r.py),
and the source-bound result is
[finite_delay_eventually_smooth_selected_return_stage4r.json](../experiments/results/finite_delay_eventually_smooth_selected_return_stage4r.json).

## 1. Setting and the distinction that matters

Let

\[
X=C([-\tau_*,0],\mathbb R^d)
\]

with the supremum norm, where $d<\infty$ and $\tau_*>0$. Consider

\[
\dot x(t)=F(x_t),
\qquad
x_t(\theta)=x(t+\theta),
\tag{1.1}
\]

where $F:U\subset X\to\mathbb R^d$ is $C^r$, $r\ge2$, on an open set.
Every finite system

\[
\dot x(t)=f\bigl(x(t),x(t-\tau_1),\ldots,x(t-\tau_N)\bigr),
\qquad 0\le\tau_j\le\tau_*,
\tag{1.2}
\]

with constant delays and $f\in C^r$ is included. The proof also works for a
general $C^r$ functional $F$ on $X$; discreteness is not used after the
maximum delay is fixed.

Write

\[
\Phi:\Omega\longrightarrow X,
\qquad (t,\phi)\longmapsto\Phi_t(\phi),
\tag{1.3}
\]

for the maximal local semiflow. Here $\Omega$ is relatively open in
$[0,\infty)\times U$ and records the actual solution-existence domain. Every
theorem below explicitly requires its parameterized event tube to lie in
$\Omega$; “the solution exists” is not used as an unquantified shorthand.

There are two different smoothness questions.

1. For fixed $t$, how smoothly does $\Phi_t(\phi)=x_t(\phi)$ depend on the
   initial history $\phi$?
2. How smooth is the joint map
   $S(t,\phi)=\Phi_t(\phi)$ with respect to time and initial history?

For $t<\tau_*$, part of $\Phi_t(\phi)$ is a fixed translation of the initial
history. This piece is affine in $\phi$, so it does not obstruct fixed-time
Fréchet differentiation. It does obstruct time differentiation: varying $t$
moves the evaluation point of an arbitrary continuous function. This is why
fixed-time $C^2$ dependence does not by itself justify a moving complete-
history return.

## 2. Fixed-time initial-history derivatives

On a common existence tube contained in $U$, the integral equation is

\[
x(t;\phi)=\phi(0)+\int_0^tF(x_s(\phi))\,ds.
\tag{2.1}
\]

Standard parameter differentiation of this Volterra equation gives the same
initial-history smoothness as $F$. In particular, the first two derivatives
in directions $h,k\in X$ solve

\[
\begin{aligned}
\dot u_h(t)&=DF(x_t)u_{h,t},&u_{h,0}&=h,\\
\dot v_{hk}(t)&=DF(x_t)v_{hk,t}
 +D^2F(x_t)[u_{h,t},u_{k,t}],&v_{hk,0}&=0.
\end{aligned}
\tag{2.2}
\]

Thus each fixed-time map $\Phi_t$ is $C^2$ in $\phi$. If $F\in C^k$, repeated
differentiation gives a triangular variational hierarchy and $\Phi_t$ is
$C^k$ in $\phi$. This assertion concerns fixed $t$; it makes no claim yet
about differentiating the output segment with respect to $t$.

## 3. Eventual joint operator-valued smoothing

Pointwise time differentiability is not enough to prove joint Fréchet
smoothness of a history-valued map. The required induction must control the
mixed derivatives in multilinear operator norm. For $1\le j\le r$, set

\[
 \Omega_j=\Omega\cap\bigl((j\tau_*,\infty)\times U\bigr)
\tag{3.1}
\]

and, whenever $a+b\le j$, write

\[
 \mathscr J_{a,b}(t,\phi)
 =\partial_t^aD_\phi^b\Phi_t(\phi)
 \in\mathcal L^b(X,X),
 \qquad \mathcal L^0(X,X):=X.
\tag{3.2}
\]

### Lemma 3.1 (operator-valued method-of-steps smoothing)

If $F\in C^k(U,\mathbb R^d)$, then for every $1\le j\le k$ and every
$a,b\ge0$ with $a+b\le j$, the jet $\mathscr J_{a,b}$ exists and is
continuous in the norm of $\mathcal L^b(X,X)$ on $\Omega_j$. Consequently,

\[
 (t,\phi)\longmapsto\Phi_t(\phi)
 \quad\hbox{is jointly Fréchet }C^k\hbox{ on }\Omega_k.
\tag{3.3}
\]

### Proof

Fixed-time differentiation of (2.1) supplies the pure initial-data jets and
their triangular retarded variational equations. For $j=1$ and $t>\tau_*$,
the arbitrary translated initial-history piece has cleared the complete
output segment. The solution and first-variation integral equations then give
$\mathscr J_{1,0}$ continuously in $X$ and $\mathscr J_{0,1}$ continuously
in $\mathcal L(X,X)$, not merely direction by direction.

Assume the operator-norm assertion through order $j-1$. The highest pure
spatial jet of order $j$ satisfies a linear Volterra variational equation
with coefficient $DF(x_s)$; its inhomogeneous source is a finite Banach
Faà di Bruno sum of $D^qF(x_s)$ applied to lower-order operator-valued jets.
The mixed time jets are then obtained by differentiating the equation. If
$t>j\tau_*$, the earliest time in the complete output segment satisfies

\[
 t-\tau_*>(j-1)\tau_*.
\tag{3.4}
\]

Thus every lower jet appearing in each summand is covered by the induction
hypothesis on the whole history interval. The Banach chain rule and local
Volterra estimates on a compact sub-tube give continuity in the appropriate
multilinear operator norm. More explicitly, at each base point one first
chooses a compact trajectory-time interval contained in the solution domain;
continuity of $D^qF$ and continuous dependence of solutions then provide a
smaller initial-history neighborhood on which the Volterra bounds are
uniform. This constructs all $\mathscr J_{a,b}$ with $a+b\le j$ and closes
the induction. Since the argument is local at each point of the open set
$\Omega_j$, no uniform derivative bound on an unbounded set of histories is
being assumed. ∎

For $j=2$, the physical-time part of the induction includes

\[
x''(s)=DF(x_s)\bigl[\theta\mapsto x'(s+\theta)\bigr],
\qquad s>\tau_*.
\tag{3.5}
\]

The earliest time in the returned segment is $t-\tau_*$, so $t>2\tau_*$
places (3.5), the time derivative of the first variation, and all mixed
second jets on the entire segment. Strict inequalities avoid propagated
compatibility faces. The thresholds are sufficient; neither necessity nor
optimality is asserted.

## 4. Parameterized selected-event theorem

Let $M$ be a Banach section-coordinate space, let $D\subset M$ be open, and
let

\[
 \iota:D\longrightarrow U
\tag{4.1}
\]

be $C^2$. The ambient specialization is $M=X$ and $\iota=\mathrm{id}$.
Let $V\subset X$ be open and let $g:V\to\mathbb R$ be $C^2$. Assume

\[
 (t,\iota(u))\in\Omega,
 \qquad \Phi_t(\iota(u))\in V
 \qquad ((t,u)\in I\times D),
\tag{4.2}
\]

and put

\[
 S(t,u)=\Phi_t(\iota(u)),
 \qquad H(t,u)=g(S(t,u)).
\tag{4.3}
\]

Assume one common interval $I=[T_-,T_+]$ satisfies

\[
T_->2\tau_*,
\tag{4.4}
\]

and there are positive constants $\delta_-,\delta_+,a_*$ such that

\[
\sup_{u\in D}H(T_-,u)\le-\delta_-<0,
\qquad
\inf_{u\in D}H(T_+,u)\ge\delta_+>0,
\tag{4.5}
\]

\[
\partial_tH(t,u)\ge a_*>0
\qquad ((t,u)\in I\times D).
\tag{4.6}
\]

### Theorem 4.1

Under (4.1)--(4.6), every $u\in D$ has exactly one event time
$T(u)\in(T_-,T_+)$ satisfying $H(T(u),u)=0$. The map

\[
T:D\to\mathbb R
\]

is $C^2$, and the moving complete-history hit

\[
R:D\to X,
\qquad R(u)=\Phi_{T(u)}(\iota(u)),
\tag{4.7}
\]

is $C^2$ and satisfies $R(D)\subset g^{-1}(0)$. At this level $R$ is a
selected complete-history **hit map**.

### Proof

By Lemma 3.1, (4.2), and (4.4), $S$ and therefore $H=g\circ S$ are jointly $C^2$ on
$I\times D$. The endpoint signs give an event by the intermediate value
theorem. The positive speed makes $H(\cdot,u)$ strictly increasing, so the
event is unique. Since $H_t\ne0$, the Banach implicit-function theorem gives
a local $C^2$ event-time branch at each $u$. Uniqueness makes these local
branches agree on overlaps, producing the displayed global map on $D$.
Finally, (4.7) is a composition of the jointly $C^2$ map $S$ with
$u\mapsto(T(u),u)$. ∎

The signs in (4.5) supply existence. The speed in (4.6) supplies both
uniqueness in the common window and the implicit-function denominator. No
statement about earlier events enters this regularity proof.

### Ambient hit versus induced section return

Taking $M=X$ and $\iota=\mathrm{id}$ in Theorem 4.1 gives an ambient map into
$g^{-1}(0)$. It is not a section self-map merely because its image satisfies
the terminal event equation. To obtain a section return, assume in addition
that $\iota$ parameterizes an initial section patch, that

\[
 R(D)\subset\Sigma_{\mathrm{out}},
\tag{4.8}
\]

and that $\chi:\Sigma_{\mathrm{out}}\to D_{\mathrm{out}}$ is a $C^2$
terminal section chart. Only then is

\[
 P=\chi\circ R:D\longrightarrow D_{\mathrm{out}}
\tag{4.9}
\]

the induced $C^2$ selected section return. A self-return additionally requires
$D_{\mathrm{out}}\subset D$ in the chosen chart. Neither (4.8) nor this
self-domain containment is supplied by the event theorem.

## 5. Derivative formulas

Evaluate all derivatives of $S$ and $H$ below at $(T(u),u)$. For directions
$h,k\in M$, one has

\[
T_h=-\frac{H_u[h]}{H_t},
\tag{5.1}
\]

and

\[
T_{hk}=-\frac{
H_{uu}[h,k]
+H_{tu}[h]T_k
+H_{tu}[k]T_h
+H_{tt}T_hT_k}{H_t}.
\tag{5.2}
\]

The derivatives of the event function are

\[
\begin{aligned}
H_{uu}[h,k]
 & =D^2g(S)[S_u h,S_u k]+Dg(S)S_{uu}[h,k],\\
H_{tu}[h]
 & =D^2g(S)[S_t,S_u h]+Dg(S)S_{tu}h,\\
H_{tt}
 & =D^2g(S)[S_t,S_t]+Dg(S)S_{tt}.
\end{aligned}
\tag{5.3}
\]

The complete-history hit derivatives are

\[
DR[h]=S_u[h]+S_tT_h,
\tag{5.4}
\]

\[
D^2R[h,k]=S_{uu}[h,k]
+S_{tu}[h]T_k+S_{tu}[k]T_h
+S_{tt}T_hT_k+S_tT_{hk}.
\tag{5.5}
\]

Equation (5.5) contains the moving-time correction exactly once. If $g$ is
affine, all $D^2g$ terms vanish and these formulas reduce to the usual
event-aligned variational identities.

## 6. Safe $C^k$ extension

Let $1\le k\le r$, replace $C^2$ by $C^k$ in the hypotheses on $\iota$ and
$g$, and retain the open-domain containments (4.2). Lemma 3.1 supplies every
mixed jet

\[
 \partial_t^aD_\phi^b\Phi_t(\phi)
 \in\mathcal L^b(X,X),
 \qquad a+b\le k,
\tag{6.1}
\]

continuously in operator norm once $t>k\tau_*$. Consequently the safe joint
threshold for the parameterized complete segment is

\[
t>k\tau_*.
\tag{6.2}
\]

Consequently, if $F,g\in C^k$ and the common event window satisfies

\[
T_->k\tau_*,
\tag{6.3}
\]

then the same proof gives $T\in C^k(D,\mathbb R)$ and the hit map
$R\in C^k(D,X)$. If the terminal chart hypotheses (4.8)--(4.9) hold with
$\chi\in C^k$, the induced section return $P=\chi\circ R$ is $C^k$.
Conditions (6.2)--(6.3) are uniform sufficient conditions; no necessity or
optimality is asserted. In particular, pointwise solution derivatives are
not being substituted for the operator-norm assertion in Lemma 3.1.

## 7. Why fixed-time smoothness is insufficient

Consider the scalar linear equation

\[
x'(t)=x(t-\tau_*).
\]

For $0<r<\tau_*$,

\[
x(r;\phi)=\phi(0)+\int_0^r\phi(s-\tau_*)\,ds.
\]

Let $\ell$ be a nonzero bounded linear functional and vary the upper limit:

\[
J(\phi)=\int_0^{r_0+\ell(\phi)}\phi(s-\tau_*)\,ds.
\]

The first derivative is

\[
DJ(\phi)h
=\int_0^r h(s-\tau_*)\,ds
 +\phi(r-\tau_*)\ell(h).
\]

A second differentiation in two nonzero time directions requires the
derivative of $\phi$ at $r-\tau_*$. Such a derivative is unavailable on an
open ball of arbitrary continuous histories. This elementary variable-limit
example does not prove (6.2) sharp, but it shows exactly why fixed-time
Fréchet smoothness cannot be substituted for moving-translation smoothness.

## 8. Selected branch versus event ordinal

Theorem 4.1 proves one unique selected event in the declared window. It does
not count earlier events. Calling this branch the $m$-th admissible return
requires an additional directed count or exclusion of all earlier admissible
events. In particular:

- no-earlier-hit is unnecessary for $C^k$ regularity of the selected hit and,
  when (4.8)--(4.9) hold, of the induced selected return;
- it is necessary when a first-return or exact ordinal label is claimed;
- negative-oriented or out-of-patch crossings may exist without affecting
  the selected branch theorem.

Thus an “$m$-th selected return” is smooth whenever its own common window
lies beyond the smoothing threshold. The integer $m$ matters only through
the event time unless an ordinal theorem is also requested.

## 9. Finite networks

A network with finitely many nodes and finitely many coordinates per node is
simply (1.1) with a larger finite $d$. The proof uses the Banach chain rule,
the maximum delay, and a scalar implicit-function theorem. Hence the
qualitative threshold

\[
T_->k\tau_*
\]

does not depend on network size. Bounds for a concrete solution tube,
derivatives, event margins, or inverse speed may of course deteriorate with
dimension. No infinite-network or infinite-dimensional node-state extension
is asserted.

## 10. Direct selected returns and the stable-set germ

Let $\Phi$ be a continuous semiflow on a metric phase space and let $\Gamma$
be a compact periodic orbit of period $P$. Fix $p\in\Gamma$. Let $N$ be a
local section patch containing $p$ and impose the isolation condition

\[
 \overline N\cap\Gamma=\{p\}.
\tag{10.1}
\]

Equivalently for the proof, every sequence $y_n\in N$ with
$\operatorname{dist}(y_n,\Gamma)\to0$ must satisfy $y_n\to p$. Let

\[
 \Theta:N\longrightarrow[\Theta_-,\Theta_+],
 \qquad
 Q:N\longrightarrow N,
 \qquad
 Q(x)=\Phi_{\Theta(x)}(x),
\tag{10.2}
\]

be continuous, where

\[
 0<\Theta_-\le\Theta_+<\infty,
 \qquad \Theta(p)=mP,
 \qquad Q(p)=p
\tag{10.3}
\]

for an integer $m\ge1$. Assume one common local tube $\mathcal G$ contains

\[
 \Phi_s(x),\qquad x\in N,\quad 0\le s\le\Theta(x).
\tag{10.4}
\]

Define the two local sets on their exact domains by

\[
\begin{aligned}
 W_N^s(Q)
  &=\{x\in N:Q^n(x)\in N\ \hbox{for every }n,
                    \ Q^n(x)\to p\},\\
 W_{\mathcal G}^s(\Gamma)
  &=\{x:\Phi_t(x)\in\mathcal G\ \hbox{for every }t\ge0,
       \ \operatorname{dist}(\Phi_t(x),\Gamma)\to0\}.
\end{aligned}
\tag{10.5}
\]

The condition $Q:N\to N$ is the recurrent selected-hit hypothesis in a
precise domain form; it is not inferred from bounded return times.

### Lemma 10.1

Under these hypotheses,

\[
W_N^s(Q)=N\cap W_{\mathcal G}^s(\Gamma).
\tag{10.6}
\]

### Proof

For $x\in N$, define

\[
 t_0=0,
 \qquad
 t_n=\sum_{j=0}^{n-1}\Theta(Q^j(x)).
\tag{10.7}
\]

The lower bound in (10.3) gives $t_n\to\infty$, and the semiflow identity
gives $Q^n(x)=\Phi_{t_n}(x)$. If $Q^n(x)\to p$, every
$t\in[t_n,t_{n+1}]$ lies on an arc of length at most $\Theta_+$ issuing from
$Q^n(x)$. Joint continuity, uniformly for $0\le s\le\Theta_+$, sends these
arcs to arcs of $\Gamma$ issuing from $p$; (10.4) supplies the local-tube
condition. Hence the flow orbit belongs to $W_{\mathcal G}^s(\Gamma)$.

Conversely, flow convergence gives
$\operatorname{dist}(Q^n(x),\Gamma)\to0$ along $t_n$. Since $Q^n(x)\in N$,
compactness of $\Gamma$ together with (10.1) forces $Q^n(x)\to p$. This last
step is exactly where section isolation is used; recurrence alone would not
prove convergence to the phase point $p$. ∎

After shrinking isolated section patches, (10.6) gives

\[
 \operatorname{germ}_p W^s(Q)
 =\operatorname{germ}_p\bigl(\Sigma\cap W^s(\Gamma)\bigr).
\tag{10.8}
\]

Thus a direct near-$mP$ return of the same semiflow identifies the
periodic-orbit stable-set germ without first proving $Q=P^m$. The identity
$Q=P^m$ on suitable nested domains is a convenient sufficient algebraic
route, and is needed when literal identity with a chosen one-period branch or
its ordinal labeling is desired. It is not needed for (10.8). First-return
status is also unnecessary for (10.8).

Only if $Q$ is $C^2$, $p$ is its hyperbolic fixed point, and $DQ(p)$ has the
required splitting does a stable graph theorem for $Q$ construct this same
stable-set germ.

## 11. Application checklist and boundary

To invoke the theorem for a concrete RFDE one must validate:

1. finite dimension, fixed bounded delays, and $F\in C^k$ on an open tube;
2. a $C^k$ initial-history parameterization
   $\iota:D\subset M\to U$ with $D$ open in a Banach coordinate space;
3. containment of $I\times\iota(D)$ in the open maximal-semiflow domain
   $\Omega$;
4. an open event domain $V$, a map $g:V\to\mathbb R$ of class $C^k$, and
   $\Phi_t(\iota(D))\subset V$ throughout the common event window;
5. the strict smoothing inequality $T_->k\tau_*$;
6. two strict endpoint signs and one uniform positive event speed;
7. terminal section-chart containment and a $C^k$ inverse chart only if the
   hit is to be called an induced section return;
8. earlier-event counting only if an ordinal or first-return claim is made;
9. for stable-germ identification, $Q:N\to N$, $Q(p)=p$,
   $\Theta(p)=mP$, bounded positive return times, one intervening-flow tube,
   and $\overline N\cap\Gamma=\{p\}$.

Stage 4R supplies none of these concrete numerical inputs. It also does not
cover state-dependent delays, neutral equations, infinite delays, infinite
networks, or infinite-dimensional node states.

Background on fixed-time RFDE smoothness and Poincaré maps is given in
O. Diekmann, S. A. van Gils, S. M. Verduyn Lunel, and H.-O. Walther,
*Delay Equations: Functional-, Complex-, and Nonlinear Analysis*, Chapters
VII.4 and XIV.3 (Springer, 1995). Lemma 3.1 records the additional
operator-valued induction needed here; the parameterized selected-event
composition, hit/return distinction, and isolated-section stable-germ proof
are displayed explicitly above.
