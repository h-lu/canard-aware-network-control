# Contingency models if the long-delay family is not \(K_1\)-admissible

Status: **model-selection memorandum, not a theorem.** The calculations
below identify the first nonzero \(\eta\)-coefficient on the formal invariant
graph. They also isolate exactly which repair makes the classical
Krupa--Szmolyan \(K_1\) construction applicable. A claimed maximal-canard
formula still requires the indicated parameterized splitting proposition and
the exact invariant-history reduction.

The recommendation is Option A: keep the final two-module matrices and the
fast source-history coupling, but use fixed physical delays. This changes one
scaling assumption, preserves the complete projected-delay constraint and the
transverse-return mechanism, and removes the nonlocal \(K_1\) tail. Its first
hidden-topology threshold term is one order later than in the current
long-delay model:

\[
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =\frac{K(\tau _0-\tau _1)}{4\alpha}\eta\delta^4
 +O(\delta^5|\eta|+\delta^4\eta^2),
 \qquad \alpha=\frac{\sqrt6}{4}.
\tag{R}
\]

Formula (R) is the coefficient to prove, not yet a proved theorem.

## 1. What can fail for the present long-delay family

The current physical delays are

\[
 \tau_k=\frac{\theta_k}{\delta},\qquad
 0<\theta_0<\theta_1,\qquad \delta=\sqrt\varepsilon.
\tag{1}
\]

They become fixed translations \(s\mapsto s-\theta_k\) in the \(K_2\) time
\(s=\delta t\). This is why the special-flow construction works on every
fixed compact \(K_2\) tube. It is not enough for the entry/exit chart.

For the canard blow-up, the chart transition has

\[
 r_2=r_1\sqrt{\epsilon_1},\qquad
 x_2=\frac{x_1}{\sqrt{\epsilon_1}},
\tag{2}
\]

and \(K_2\) time is \(\sqrt{\epsilon_1}\) times the desingularized \(K_1\)
time. A fixed \(K_2\) delay therefore becomes a \(K_1\) backtrack of length

\[
 \frac{\theta_k}{\sqrt{\epsilon_1}}.
\tag{3}
\]

The obstruction is visible without estimating an abstract RFDE. Along the
singular canard \(x_2(s)=s/2\), a translated state, expressed in the current
\(K_1\) scale, contains

\[
 \sqrt{\epsilon_1}\,x_2(s-\theta_k)
 =x_1-\frac{\theta_k}{2}\sqrt{\epsilon_1}.
\tag{4}
\]

Thus the reduced delayed term need not extend as a \(C^4\), let alone a
\(C^5\), vector field to \(\epsilon_1=0\). Proposition 3.4 and the endpoint
estimates in Proposition 3.5 of
[Krupa--Szmolyan (2001)](https://doi.org/10.1137/S0036141099360919)
cannot simply be invoked for this family. Polynomially weighted \(K_2\)
estimates do not remove the half-power in (4).

This is a compatibility warning, not a proof that the long-delay theorem is
false. A genuinely nonlocal \(K_1\) theory might still prove it. The point of
the repairs below is to avoid making that new theory a prerequisite for the
flagship result.

## 2. Algebra that every repair keeps

Retain

\[
 C_0^\eta=C_0+\eta T,\qquad
 C_1^\eta=C_1-\eta T,\qquad B=C_0+C_1,
\tag{5}
\]

and the modal vectors \(r,q,\ell\) from the final model. The exact identities

\[
 \ell^TC_0^\eta r=\frac13,\qquad
 \ell^TC_1^\eta r=\frac23,
\tag{6}
\]

hold independently of \(\eta\), while

\[
 P_\perp\mathcal H_\eta[rx]
 =\eta q\,[x(-\tau_1)-x(-\tau_0)]
\tag{7}
\]

is nonzero. Consequently every option below keeps the total gain and the
**entire delay measure seen by the critical projection**, not just one
moment, fixed under the topology deformation. What changes between the
options is where (7) enters and how large a backtrack is seen in \(K_2\).

## 3. Option A: fixed physical delays in the fast source

### 3.1 Model change

Keep model (M) verbatim except replace (1) by

\[
 0<\tau_0<\tau_1\leq \tau_{\max},\qquad
 \tau_k\ \hbox{independent of }\delta.
\tag{8}
\]

In \(K_2\), its scaled delay is

\[
 \theta_k(\delta)=\delta\tau_k.
\tag{9}
\]

The matrices, their positivity interval, the equilibrium, the transverse
recovery scaffold, and the exact identities (5)--(7) are unchanged.

### 3.2 First \(\eta\)-jet

Write

\[
 \Delta_\delta X
 =X(s-\delta\tau_0)-X(s-\delta\tau_1).
\]

On a \(C^3\) special flow,

\[
 \Delta_\delta X
 =\delta(\tau_1-\tau_0)X'(s)+O(\delta^2).
\tag{10}
\]

For the singular canard

\[
 X_0(s)=-\frac{s}{2\alpha},
\]

this becomes

\[
 \Delta_\delta X_0
 =\frac{\delta(\tau_0-\tau_1)}{2\alpha}
 \quad\hbox{exactly}.
\tag{11}
\]

The transverse equation still contains

\[
 -\delta K\eta\Delta_\delta X.
\]

It is now an order-\(\delta^2\), rather than order-\(\delta\), forcing of
the algebraic transverse graph. If

\[
 Z=Z_0+\delta Z_1+\delta^2Z_2+\cdots,
 \qquad Z_0=-\frac\alpha2X^2,
\]

then

\[
 \partial_\eta Z_2\big|_{\eta=0}
 =-\frac{K(\tau_0-\tau_1)}{4\alpha}.
\tag{12}
\]

The nonlinear return \(-2\alpha\delta XZ\) consequently first enters the
critical \(K_2\) field at order \(\delta^3\):

\[
 \partial_\eta q_{3,X}(\gamma_0(s))
 =-\frac{K(\tau_0-\tau_1)}{4\alpha}s,
 \qquad \partial_\eta q_{3,Y}=0.
\tag{13}
\]

With the normalized adjoint

\[
 \psi(s)=e^{-s^2/2}(s,1)^T,
\]

the mixed Melnikov coefficient is

\[
 M_{3,\eta}
 =-\frac{K(\tau_0-\tau_1)}{4\alpha}\sqrt{2\pi}.
\tag{14}
\]

Since the normalized derivative in the unfolding direction is
\(\sqrt{2\pi}\), (14) gives the candidates

\[
\begin{aligned}
 \nu_c(\delta,\eta)-\nu_c(\delta,0)
 &=\frac{K(\tau_0-\tau_1)}{4\alpha}\eta\delta^2
   +O(\delta^3|\eta|+\delta^2\eta^2),\\
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 &=\frac{K(\tau_0-\tau_1)}{4\alpha}\eta\delta^4
   +O(\delta^5|\eta|+\delta^4\eta^2).
\end{aligned}
\tag{15}
\]

The corresponding Krupa--Szmolyan parameter satisfies

\[
 \lambda_{{\rm KS},c}(\delta,\eta)
 -\lambda_{{\rm KS},c}(\delta,0)
 =-\frac{K(\tau_0-\tau_1)}4\eta\delta^4+\cdots.
\tag{16}
\]

### 3.3 Why classical \(K_1\) geometry is available

At the chart scaling, a bounded physical backtrack corresponds to
\(K_1\)-time size \(r_1\tau_k\), rather than (3). Equivalently, the
\(K_2\) translation in (9) has the chart factor

\[
 \frac{\delta\tau_k}{\sqrt{\epsilon_1}}=r_1\tau_k.
\tag{17}
\]

This is smooth at \(\epsilon_1=0\). More invariantly, after the
bounded-delay special-flow reduction, every delayed evaluation is a
bounded-physical-time flow-back map. Its transformation through the blow-up
is a smooth parameterized map. The reduced planar field can therefore be
extended across the \(K_1\) boundary and the standard center manifolds and
foliations can be constructed.

The remaining geometric result is a **third-order parameterized
Krupa--Szmolyan splitting**, because (13) is \(q_3\), not \(q_2\). This is a
finite-dimensional higher-jet extension of the published endpoint argument;
it no longer requires a nonlocal \(K_1\) theorem.

### 3.4 Novelty and full-history lift

Fixed-delay weak-feedback scalar expansions are already part of the delayed
van der Pol literature. In particular,
[Zhang et al. (2026)](https://doi.org/10.1137/24M1696548) treat one delayed
van der Pol oscillator by a nonlocal center-manifold flow expansion and a
nonlinear time transformation. Neither “fixed delay” nor an
\(O(\varepsilon^2)\) scalar coefficient is a defensible novelty claim.

The distinct candidate contribution is (15) as a **network directional
derivative**: two positive two-layer networks have identical total gain and
identical complete critical projected delay measure, but different canard
thresholds through a stable transverse mode. A scalar oscillator has no
such invisible topology direction. A rigorous history-level intersection
and a uniform mixed remainder would also be stronger and different in kind
from a formal threshold approximation.

The full-history lift is retained. On the exact special-flow graph, define
the physical-history embedding by following the reduced flow for
\(\delta\vartheta\) units of \(K_2\) time,
\(-\tau_{\max}\leq\vartheta\leq0\). Its value at \(\vartheta=0\) contains
the reduced current point, so the map is injective. If the selected
attracting and repelling reduced curves meet, their entire RFDE histories
are the same embedded history, not merely the same current voltage.

## 4. Option B: put the delayed feedback in the recovery source

To make this option unambiguous, consider

\[
\begin{aligned}
 \dot v&=F(v,w),\\
 \dot w&=\varepsilon g(v,\mu)
 -D_wP_\perp(w-w_*)
 +\varepsilon K\mathcal H_\eta[v_t].
\end{aligned}
\tag{18}
\]

The same source-history operator \(\mathcal H_\eta\) is used, so constant
histories remain equilibria and (5)--(7) remain exact.

### 4.1 With the current long delays: not a repair

For \(\tau_k=\theta_k/\delta\), the critical projection of (18) contributes
at leading \(K_2\) order to the slow equation:

\[
 Y'=-X-K\left[X-\frac13X(s-\theta_0)
                 -\frac23X(s-\theta_1)\right]+O(\delta).
\tag{19}
\]

Thus the unperturbed \(K_2\) problem is no longer the integrable
Krupa--Szmolyan system. Projecting the added source with \(P_\perp\) removes
(19), but it does not remove the \(K_1\) backtrack (3) or the half-power (4).
Moving a long delay from the fast equation to the slow equation is therefore
not, by itself, a \(K_1\) repair.

For reference, in the artificially projected version
\(+\varepsilon KP_\perp\mathcal H_\eta\), the formal long-delay calculation
would give

\[
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =-\frac{K(\theta_0-\theta_1)}{4\alpha D_w}
   \eta\delta^3+\cdots.
\tag{20}
\]

Formula (20) is not \(K_1\)-certified and is not recommended as the flagship
model.

### 4.2 With bounded physical delays

If (18) is combined with (8), the standard \(K_1\) obstruction is removed.
The transverse recovery scaling remains

\[
 w-w_*=-\delta^2rY+\delta^4qW.
\]

Along the leading canard, the first \(\eta\)-dependent recovery graph is

\[
 \partial_\eta W_0
 =-\frac{K(\tau_0-\tau_1)}{2\alpha D_w}.
\tag{21}
\]

It enters the fast transverse graph two orders later:

\[
 \partial_\eta Z_2
 =+\frac{K(\tau_0-\tau_1)}{4\alpha D_w},
\qquad
 \partial_\eta q_{3,X}(\gamma_0(s))
 =+\frac{K(\tau_0-\tau_1)}{4\alpha D_w}s.
\tag{22}
\]

The sign reversal in (22) is caused by the two stable filters
\(w_\perp\mapsto v_\perp\mapsto v_\parallel\). The threshold candidate is

\[
 \boxed{
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =-\frac{K(\tau_0-\tau_1)}{4\alpha D_w}
   \eta\delta^4
 +O(\delta^5|\eta|+\delta^4\eta^2).}
\tag{23}
\]

This variant still has an exact full-history lift after reduction. It is
more invasive than Option A, its interpretation depends on a delayed
recovery pathway, and the new \(D_w^{-1}\) coefficient adds a second filter
that must be estimated. Delayed recovery in FitzHugh--Nagumo-type models is
not itself new. The hidden-topology derivative could remain new, but the
cleanest comparison with the scalar 2026 paper is weakened rather than
strengthened.

## 5. Option C: a smooth bounded delay window with a long-delay crossover

The maximal class that is immediately compatible with the classical charts
is not “arbitrary bounded dependence on \(\delta\).” Require

\[
 \tau_k(\delta)=\widehat\tau_k(\delta^2),
 \qquad \widehat\tau_k\in C^8,
 \qquad 0<\widehat\tau_k(\varepsilon)\leq\tau_{\max}.
\tag{24}
\]

Then

\[
 \theta_k(\delta)=\delta\widehat\tau_k(\delta^2),
\tag{25}
\]

and the \(K_1\) translation is
\(r_1\widehat\tau_k(r_1^2\epsilon_1)\), which is smooth at the chart
boundary. An arbitrary term linear in \(\delta\) inside
\(\tau_k(\delta)\) is not harmless: since
\(\delta=r_1\sqrt{\epsilon_1}\), it can reintroduce half-powers. Smoothness
in \(\varepsilon=\delta^2\), not only boundedness, is the safe contract.

For the fast-source model, put

\[
 d_0=\widehat\tau_0(0)-\widehat\tau_1(0).
\]

The repaired coefficient is

\[
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =\frac{Kd_0}{4\alpha}\eta\delta^4
 +O(\delta^5|\eta|+\delta^4\eta^2).
\tag{26}
\]

More generally, if the first nonzero delay-gap jet is

\[
 \widehat\tau_0(\varepsilon)-\widehat\tau_1(\varepsilon)
 =d_m\varepsilon^m+O(\varepsilon^{m+1}),
\]

then the first candidate term is

\[
 \frac{Kd_m}{4\alpha}\eta\delta^{4+2m}.
\tag{27}
\]

A useful smooth cap that agrees approximately with the present long-delay
law away from the asymptotic endpoint is

\[
 \tau_k^{\rm cap}(\varepsilon)
 =\frac{\Theta_k}{\sqrt{\varepsilon+\varepsilon_d}},
 \qquad \varepsilon_d>0\ \hbox{fixed}.
\tag{28}
\]

It is bounded and \(C^\infty\) in \(\varepsilon\geq0\). The composite
coefficient suggested by (15) is

\[
 \Delta\mu_c
 \sim
 \frac{K(\Theta_0-\Theta_1)}{4\alpha}
 \frac{\eta\delta^4}{\sqrt{\delta^2+\varepsilon_d}}.
\tag{29}
\]

For \(\delta^2\gg\varepsilon_d\), (29) resembles the current
\(O(\delta^3)\) law; for \(\delta^2\ll\varepsilon_d\), it crosses over to
the \(K_1\)-regular \(O(\delta^4)\) law. A theorem uniform as
\(\varepsilon_d\downarrow0\) would be a separate two-parameter result.
With fixed \(\varepsilon_d>0\), the standard proof and the full-history lift
are available, but their constants may deteriorate like powers of
\(\varepsilon_d^{-1/2}\).

The cap itself is a regularization, not a flagship novelty. A rigorously
proved two-regime crossover with uniform error could become an additional
result, but it would enlarge the paper substantially.

## 6. Comparison and decision

| option | classical \(K_1\) available? | first hidden-topology threshold | model intervention | full-history lift | assessment |
|---|---:|---:|---:|---:|---|
| current \(\tau=\theta/\delta\) | not from standard KS theory | \(+K(\theta_0-\theta_1)\eta\delta^3/(4\alpha)\) | none | inner tube yes; global matching open | high-payoff, high-risk |
| A: fixed physical \(\tau\) | yes, after bounded-delay graph reduction | \(+K(\tau_0-\tau_1)\eta\delta^4/(4\alpha)\) | one scaling line | yes | **recommended proof model** |
| B: recovery-source, long delay | no; full source also changes \(q_0\) | projected variant: \(-K(\theta_0-\theta_1)\eta\delta^3/(4\alpha D_w)\) | equation architecture | conditional on new \(K_1\) theory | reject as repair |
| B plus bounded physical \(\tau\) | yes | \(-K(\tau_0-\tau_1)\eta\delta^4/(4\alpha D_w)\) | equation architecture plus scaling | yes | defensible backup, not minimal |
| C: \(\varepsilon\)-smooth bounded window | yes for a fixed window | \(+Kd_0\eta\delta^4/(4\alpha)\) | delay law | yes; nonuniform as cap is removed | numerical bridge/appendix |

There is a structural tradeoff. With weak gain \(\varepsilon K\), bounded
physical delays, bounded \(\eta\), and the fixed-data cancellation, a delayed
critical state changes only by \(O(\delta^2)\) in physical variables over one
delay interval. The hidden transverse round trip consequently appears at
\(O(\delta^4)=O(\varepsilon^2)\) in the threshold. Retaining an
\(O(\delta^3)\) term requires a delay of order \(1/\delta\), an unbounded
actuation such as \(K=O(1/\delta)\), or a non-smooth parameter scaling. Each
choice reopens the very \(K_1\) regularity problem that the repair is meant to
remove.

## 7. Minimal proof and computation package for Option A

The repaired flagship theorem can be completed without a nonlocal \(K_1\)
theory if the following gates are closed.

1. **Exact symbolic chart.** Regenerate the existing exact blow-up with
   \(X(s-\theta_k)\) replaced by \(X(s-\delta\tau_k)\). Verify (10)--(13)
   from the physical vector field, not from a separately typed reduced
   equation.
2. **Bounded-delay history graph through the fold charts.** Prove at least
   \(C^8\) parameter regularity in \((x,y,\varepsilon,\mu,\eta)\) and show
   that the \(K_1\) flow-back is the smooth bounded-time map described by
   (17).
3. **Third-order mixed splitting.** Extend the normalized
   Krupa--Szmolyan gap by one more \(K_2\) jet and differentiate the \(K_1\)
   endpoint identities in \(\eta\). The required whole-line integral is
   exactly (14).
4. **Simple root and exact history equality.** Apply the implicit-function
   theorem to the normalized gap, then use the injective special-flow
   embedding to lift the reduced intersection to a common RFDE history.
5. **Independent numerical check.** For several fixed small nonzero
   \(\eta\), verify

   \[
    \frac{\mu_c(\delta,\eta)-\mu_c(\delta,0)}
         {\eta\delta^4}
    \longrightarrow \frac{K(\tau_0-\tau_1)}{4\alpha}.
   \]

   Use \(K=0\), \(\eta=0\), and \(\tau_0=\tau_1\) as exact negative controls,
   and separate history interpolation error from the threshold fit.

The long-delay \(O(\delta^3)\) result can remain a clearly labeled conjecture
or a numerical comparison. The paper's theorem should use Option A unless a
separate proof closes the nonlocal \(K_1\) compatibility problem.
