# Outer attraction and two-sided routing in the leaky RFDE

Status: **conditional history-space theorem plus two proved anchors and one
source-bound numerical outer target.** The exact outer periodic RFDE orbit,
its simple neutral multiplier, the qualitative codimension-one stable
manifold of the inner orbit, the physical pulse-history curve, the quiet
Razumikhin basin, and complete-history quiet capture for $J=0.30$ are
proved. This note derives the weakest direct inequalities that would join
those objects. The center outer zero index, stable projection and power
constants, quantitative inner stable graph, signed exit cylinder, and both
exit-face attachments remain open. Therefore no separator, $J_c$, onset,
outer capture, two-sided routing, or safety-control theorem is claimed.

The executable contract is
[the routing source](../src/canard_control/leaky_outer_two_sided_routing_contract.py),
the generator is
[the routing experiment](../experiments/leaky_outer_two_sided_routing_contract.py),
and the tracked result is
[the routing result](../experiments/results/leaky_outer_two_sided_routing_contract.json).

## 1. History spaces and the proof spine

Put

\[
 X=C([-r,0],\mathbb R^2),\qquad
 Y=C([-r,0],\mathbb R)\times\mathbb R,
 \qquad r=5\sqrt5.
\]

The proved projection

\[
 \pi(\phi_v,\phi_w)=(\phi_v,\phi_w(0)),\qquad \|\pi\|=1
\]

determines the future, and after one maximum delay the full semiflow factors
through the compatible reduced-history lift. We therefore construct the
phase sections and return maps in $Y$, but every routing target is a set of
complete histories. The quiet target is tested directly in $X$; the outer
target is tested after projection to $Y$ and then pulled back by the exact
factorization.

The shortest proof chain is

\[
\begin{gathered}
 K(J)\pitchfork W^s_{\rm loc}(\Gamma_i)
 \quad\Longrightarrow\quad
 \hbox{signed first exit through }E_-\hbox{ or }E_+\\
 \Longrightarrow
 \begin{cases}
 E_-\longrightarrow\mathcal B_q,\\
 E_+\longrightarrow\mathcal T_o,
 \end{cases}
 \quad\Longrightarrow\quad
 J<J_c\to E_q,\quad J=J_c\to\Gamma_i,\quad J>J_c\to\Gamma_o.
\end{gathered} \tag{1.1}
\]

Here $\mathcal B_q$ is the proved quiet Razumikhin sublevel and
$\mathcal T_o$ is a quantitative outer attracting tube. Each arrow in
(1.1) needs its own history-space estimate. Neither a planar phase portrait
nor a sampled trajectory supplies any of them.

## 2. A quantitative outer attracting tube

Let $\Sigma_o\subset Y$ be a phase section through the validated outer
orbit and let $P_o$ be its first-return map. Removing the neutral phase
direction gives a stable section space $E_o^s$. The outer zero-index
calculation must first show that every nonneutral multiplier is strictly
inside the unit disk. That qualitative count is necessary, but it is not a
norm estimate.

Choose a rate $\rho_o<1$, strictly outside the stable spectrum, and prove

\[
 \|A_o^n\|\le K_o\rho_o^n,
 \qquad A_o=DP_o(0),\quad n\ge0. \tag{2.1}
\]

The history-space Riesz projection and phase-chart norms must also be
bounded. In particular, a zero-free Fourier pencil cannot simply be read as
a resolvent bound for the continuous-history monodromy.

Nonnormality may make $\|A_o\|>1$, even when the spectrum is well inside
the disk. The weakest useful return-map test therefore allows an arbitrary
integer $m\ge1$. Write

\[
 P_o^m(z)=A_o^m z+N_m(z),\qquad N_m(0)=DN_m(0)=0,
\]

and validate on $\|z\|\le r_o$ that

\[
 \|DN_m(z)\|\le C_m\|z\|. \tag{2.2}
\]

Then

\[
 q_m:=K_o\rho_o^m,\qquad
 \Lambda_o:=q_m+C_mr_o. \tag{2.3}
\]

> **Lemma 2.1 (outer section contraction).** Suppose the phase-fixed return
> map and its inter-return flow tube are validated on a section ball of
> radius at least $r_o$. If
>
> \[
> K_o\rho_o^m+C_mr_o<1, \tag{2.4}
> \]
>
> then $P_o^m$ maps that ball strictly into itself and is a contraction
> there. The flow sweep of the ball over the intervening $m$ returns is a
> local orbital attracting tube for $\Gamma_o$.

Indeed, (2.2) and the mean-value theorem give

\[
 \|P_o^m(z_1)-P_o^m(z_2)\|
 \le\Lambda_o\|z_1-z_2\|.
\]

The same bound with $z_2=0$ gives invariance. A finite inter-return flow
Lipschitz bound transfers convergence at sampled returns to orbital
convergence throughout each return interval. This proof never inverts the
RFDE semiflow.

The executable evaluator implements exactly (2.3)--(2.4). It deliberately
requires the zero index, stable Riesz projection, stable power constant,
phase chart, return-map domain, nonlinear derivative coefficient, and
inter-return flow tube as distinct inputs. All but neutral simplicity are
currently absent.

### 2.1 A nonlinear estimate that is already proved

The directed outer-orbit strip gives

\[
 \sup_t|V_o(t)-1|\le B_o<2.489870745669841,
\]

with more than $0.010129$ of margin to $|v-1|=2.5$. Thus a full-history
radius $r_*=0.01$ around the orbit remains in the proved voltage strip.

For a voltage perturbation $p$, the nonlinear remainder in the current
cubic is

\[
 -V_op^2-\frac13p^3,
\]

while the instantaneous and delayed $H(v)=(v-1)^3$ remainders are

\[
 -\varepsilon\kappa_3\{3(V_o-1)p^2+p^3\},
 \qquad
 \frac{\varepsilon\kappa_3}{2}
 \{3(V_{o,j}-1)p_j^2+p_j^3\}.
\]

Since $\varepsilon\kappa_3=10^{-3}$, exact triangle inequalities give

\[
 \|F(\Gamma_o+\eta)-F(\Gamma_o)-DF(\Gamma_o)\eta\|
 \le C_R(r)\|\eta\|_X^2, \tag{2.5}
\]

where

\[
 C_R(r)=1+B_o+\frac r3
       +2\varepsilon\kappa_3(3B_o+r). \tag{2.6}
\]

On the same tube,

\[
 \|D^2F\|\le
 B_2(r):=2(1+B_o+r)+12\varepsilon\kappa_3(B_o+r). \tag{2.7}
\]

The result artifact evaluates (2.6)--(2.7) outward. These are genuine
continuous-history vector-field estimates. They are useful inputs to a
variational method-of-steps proof, but they do not by themselves bound the
Poincare map over a $26.6$-unit return. In particular, they are not used to
promote an outer attracting tube.

## 3. Signed exit from the inner stable sheet

Assume a quantitative inner graph has been constructed on a phase section,

\[
 W^s_{\rm loc}(\Gamma_i)\cap\Sigma_i
 =\{(u,z):u=h(z)\}.
\]

Straighten it with the signed coordinate

\[
 \delta=u-h(z). \tag{3.1}
\]

If $P_i(u,z)=(U(u,z),Z(u,z))$, define

\[
 G(u,z)=U(u,z)-h(Z(u,z)). \tag{3.2}
\]

Stable-graph invariance gives $G(h(z),z)=0$. Because the unstable
coordinate is one-dimensional, the scalar mean-value formula yields the
exact factorization

\[
 \delta_+=G(u,z)=a(\delta,z)\delta, \tag{3.3}
\]

with

\[
 a(\delta,z)=\int_0^1
 \partial_uG(h(z)+s\delta,z)\,ds. \tag{3.4}
\]

This direct signed-factor estimate is weaker than constructing a full
invariant cone. Orient the unstable coordinate so that its multiplier is
positive. If

\[
 1<m_-\le a(\delta,z)\le m_+ \tag{3.5}
\]

throughout the pre-exit cylinder, the sign is preserved and the magnitude
strictly increases. The validated multiplier interval already gives

\[
 1.8191337257\ldots\le\mu_u\le2.2218949501\ldots. \tag{3.6}
\]

Consequently it is sufficient to prove a factor variation

\[
 |a(\delta,z)-\mu_u|\le E_a,\qquad
 E_a<1.8191337257\ldots-1. \tag{3.7}
\]

Then $m_-=\mu_- -E_a>1$ and $m_+=\mu_+ +E_a$.

The stable row must not leave through the side of the cylinder before the
signed exit. A direct sufficient estimate is

\[
 \|Z(h(z)+\delta,z)\|
 \le q_z\|z\|+b_z|\delta|,
 \qquad q_zr_z+b_zd_{\rm ex}<r_z. \tag{3.8}
\]

> **Lemma 3.1 (signed first exit).** Suppose (3.3), (3.5), and (3.8) hold
> on $\|z\|\le r_z$, $|\delta|\le d_{\rm ex}$, and the coordinate chart
> extends to $|\delta|\le m_+d_{\rm ex}$. Every point with
> $0<|\delta_0|<d_{\rm ex}$ reaches, after finitely many returns, exactly
> one of the closed bounded slabs
>
> \[
> E_\pm=\{(\delta,z):
> d_{\rm ex}\le\pm\delta\le m_+d_{\rm ex},
> \ \|z\|\le r_z\}. \tag{3.9}
> \]
>
> The sign is the sign of $\delta_0$, and
>
> \[
> n_{\rm ex}\le
> \left\lceil
> \frac{\log(d_{\rm ex}/|\delta_0|)}{\log m_-}
> \right\rceil. \tag{3.10}
> \]

The slab, rather than the codimension-one face
$|\delta|=d_{\rm ex}$, is essential: a discrete return may overshoot the
face by as much as $m_+$. This makes (3.9) the correct compact initial set
for the finite routing calculation.

At present the multiplier interval in (3.6) is proved, but $h$, $E_a$,
$q_z$, $b_z$, $r_z$, and $d_{\rm ex}$ are not quantitatively validated.
The actual signed-exit evaluator therefore returns null bounds and a false
conclusion.

## 4. Directed attachment of the two exit slabs

Each slab in (3.9) is a closed bounded subset of an infinite-dimensional
history space and is generally not compact. A routing calculation must start
from every history in that slab, not from a plotted representative. It may
either propagate a genuine function-space enclosure, or first prove a
smoothing/equicontinuity bound and then use a finite polynomial head with a
rigorous infinite-dimensional tail radius. A finite parameterization without
that tail is not an enclosure of the slab.

On each causal method-of-steps cell, let $\widehat z$ be a polynomial guide
depending on normalized time and all exit-face parameters. Let $R_i$ be the
error in a declared state norm. The basic error inequality is

\[
 D^+R_i
 \le \mu_iR_i+b_{i0}R_{i,\tau_0}+b_{i1}R_{i,\tau_1}
      +E_{{\rm res},i}. \tag{4.1}
\]

All coefficients in (4.1), the initial face enclosure, and the delayed
errors must be outward bounds over the entire time--face cell. The
polynomial residual is converted to a tensor Bernstein basis; its convex
hull then bounds every time and face parameter, rather than selected nodes.
The cellwise Gronwall step must close strictly before the next cell is used
as delayed input.

### 4.1 Quiet attachment

The quiet basin is

\[
 \mathcal B_q=\left\{\phi\in X:
 \sup_{-r\le\theta\le0}
 (\phi(\theta)-E_q)^TP(\phi(\theta)-E_q)\le\frac1{125}
 \right\}. \tag{4.2}
\]

Suppose a final retained-history Bernstein calculation gives

\[
 B_P\ge
 \sup_{\theta,\eta_-}
 (\widehat z(T+\theta,\eta_-)-E_q)^T
 P(\widehat z(T+\theta,\eta_-)-E_q), \tag{4.3}
\]

where $\eta_-$ ranges over the whole negative exit slab, and the propagated
$P$-norm error is at most $E_P$. The single sufficient inequality is

\[
 \boxed{\sqrt{B_P}+E_P<\frac1{\sqrt{125}}.} \tag{4.4}
\]

It places the complete retained history of every point of $E_-$ inside
(4.2), after which the proved Razumikhin theorem gives exponential
convergence to $E_q$.

For $J=0.30$, the existing directed calculation already proves (4.4), with
a $P$-norm margin greater than $0.01167$. This is a single-history anchor,
not an enclosure of $E_-$. Nevertheless, continuous dependence of the RFDE
semiflow and the strict interior margin imply two genuine qualitative
consequences:

- an open, non-explicit history neighborhood of $K(0.30)$ lies in the quiet
  basin;
- because $J\mapsto K(J)$ is continuous, a non-explicit open pulse interval
  around $0.30$ is quiet-captured.

Neither consequence reaches the candidate separator bracket near
$0.3011353$, and neither identifies the negative exit slab.

### 4.2 Outer attachment

For the positive slab, choose the same exact outer phase section used in
the attracting-tube theorem. On each face cell, enclose an event bracket
$[T_-,T_+]$ with opposite section signs and

\[
 Dh_oF\ge a_o>0 \tag{4.5}
\]

throughout the bracketed history tube. This gives one and only one positive
crossing for every initial history in the cell.

Let the directed error terms be:

- $E_{\rm guide}$: continuous reduced-history distance from the polynomial
  guide to the candidate outer history;
- $E_{\rm flow}$: method-of-steps history error;
- $E_{\rm orbit}$: the proved correction from the candidate polynomial to
  the exact outer orbit;
- $E_t$: event-time error;
- $F_{\rm tube}$: history speed on the event tube;
- $E_{\rm section}$: exact-section reference and phase error.

Then

\[
 E_{\rm raw}=E_{\rm guide}+E_{\rm flow}+E_{\rm orbit}
              +E_tF_{\rm tube}+E_{\rm section}. \tag{4.6}
\]

If $Q_o$ bounds the phase-chart projection and $r_o$ is the validated outer
section-ball radius, the complete attachment test is

\[
 \boxed{Q_oE_{\rm raw}<r_o.} \tag{4.7}
\]

Equations (4.5)--(4.7), together with Lemma 2.1, prove that every history in
$E_+$ converges orbitally to $\Gamma_o$.

## 5. A concrete $J=0.32$ outer-side target

To remove an otherwise arbitrary choice of routing time, the executable
contract integrates the physical $J=0.32$ pulse to the third positive
crossing of the 180-step outer candidate section. Three same-method
refinements place the crossing near

\[
 t\approx94.96190216536
\]

and give a 4097-point reduced-history distance from the outer candidate of
about $5.62\times10^{-6}$. The exact outer orbit is already validated within
Wiener radius $10^{-5}$ of that candidate.

These observations select the following directed target budget:

| term | requested bound |
|---|---:|
| continuous Bernstein guide distance $E_{\rm guide}$ | $10^{-5}$ |
| method-of-steps error $E_{\rm flow}$ | $5\times10^{-6}$ |
| proved orbit correction $E_{\rm orbit}$ | $10^{-5}$ |
| event-time error $E_t$ | $10^{-6}$ |
| event-tube history speed $F_{\rm tube}$ | $3$ |
| section/phase error $E_{\rm section}$ | $5\times10^{-6}$ |
| chart norm target $Q_o$ | $2$ |
| outer section radius target $r_o$ | $10^{-4}$ |

The arithmetic design gives

\[
 E_{\rm raw}\le3.3\times10^{-5},\qquad
 Q_oE_{\rm raw}\le6.6\times10^{-5}<10^{-4}. \tag{5.1}
\]

Equation (5.1) is an **error allocation**, not evidence: the continuous
Bernstein guide distance, directed flow error, event bracket and speed,
chart norm, section radius, and outer attracting tube have not been
validated. In particular, the 4097-point maximum is not inserted as
$E_{\rm guide}$. The calculation merely identifies a short, concrete finite
segment that a later directed enclosure can target.

Nor does the $J=0.32$ trajectory attach $E_+$. It is one pulse history,
whereas Lemma 3.1 produces a complete exit slab. A final proof must either
enclose the slab directly or prove that it enters a smaller parameterized
family containing the $J=0.32$ anchor.

## 6. Conditional two-sided routing theorem

> **Theorem 6.1 (conditional local biological onset).** Assume:
>
> 1. the physical pulse curve has a unique transverse intersection
>    $K(J_c)\in W^s_{\rm loc}(\Gamma_i)$ on the declared pulse interval;
> 2. Lemma 3.1 holds and assigns the two signs of the pulse gap to $E_-$
>    and $E_+$;
> 3. the negative slab satisfies (4.1)--(4.4);
> 4. Lemma 2.1 and the positive-slab estimates (4.5)--(4.7) hold.
>
> Then, after fixing the orientation,
>
> \[
> \begin{cases}
> J<J_c&\Longrightarrow \Phi_tK(J)\to E_q,\\
> J=J_c&\Longrightarrow
>       \operatorname{dist}(\Phi_tK(J),\Gamma_i)\to0,\\
> J>J_c&\Longrightarrow
>       \operatorname{dist}(\Phi_tK(J),\Gamma_o)\to0.
> \end{cases} \tag{6.1}
> \]

The proof is exactly the concatenation in (1.1). The first exit time may
diverge logarithmically as $J\to J_c$, but the routing hypotheses begin
afresh at two fixed exit slabs and require one finite-horizon enclosure for
each entire slab. Their certified horizons therefore do not inherit the
pre-exit logarithmic divergence. This distinction is why the routing
calculation should begin at (3.9), rather than attempt a uniform finite-time
enclosure of every pulse arbitrarily close to $J_c$.

## 7. Current claim boundary and next certificate

The contract promotes only the following theorem-level deductions:

- the polynomial RFDE has the explicit quadratic and second-derivative
  bounds (2.5)--(2.7) on a radius-$0.01$ history tube around the exact outer
  orbit;
- strict $J=0.30$ capture implies non-explicit open quiet neighborhoods in
  history space and pulse amplitude;
- Lemmas 2.1 and 3.1, and the attachment tests (4.4), (4.7), are rigorous
  sufficient interfaces.

It leaves the following claim flags false:

- the center outer zero index and outer stable resolvent/power constants;
- a quantitative outer attracting tube;
- the quantitative inner stable graph and its signed-factor cylinder;
- attachment of either complete signed exit slab;
- the pulse stable-sheet crossing, two-sided routing, $J_c$, physical onset,
  and frequency--amplitude--safety control.

The next efficient computation is not another long sampled trajectory. It
is a directed variational method of steps on two compact initial slabs, with
tensor Bernstein bounds in time and the slab parameters, after the outer
zero-index/projection and inner graph constants have been supplied.
