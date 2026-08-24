# A full-network nonlinear sign-cone theorem for the clamped rank-one FHN decision stage

## 1. Purpose and exact claim boundary

This note proves a full-network statement for the controlled decision stage
of the fixed two-module FitzHugh--Nagumo delay network. The voltage histories
need not be synchronous, the voltage equation is not linearized, and the
module sizes are arbitrary positive integers. A same-sign complete history
that is separated from the zero-voltage boundary cannot lose its sign before
a declared nodewise detector is reached, provided the voltage scaffold
dominates the recovery deviation by an explicit strict margin. An exponential
estimate for the collective voltage then forces a finite first hit.

The result is narrower than a biological basin theorem. It uses the fixed
rank-one two-module family, the ideal collective recovery clamp, and
complete-history sign assumptions. It proves neither nonlinear
synchronization nor attraction to the synchronous leaf. It does not cover
noise that crosses the voltage sign boundary, a bounded additive realization
of the clamp, a general graph topology, an unforced maximal-canard threshold,
or a post-detector biological pulse or quiet basin.

The finite-excursion corollary reaches the controlled faces \(v_i=3/2\) and
\(v_i=-6/5\). This is a finite voltage excursion while the ideal clamp
remains active. It is not an action-potential theorem, a periodic-attraction
theorem, or a no-return statement across the detector faces \(v_i=\pm1\).

## 2. Fixed rank-one network and collective clamp

Let \(C_1,C_2\) be two nonempty modules of sizes \(n_1,n_2\ge1\), and put
\(N=n_1+n_2\). For \(z\in\mathbb R^N\), define

\[
 \bar z_a=\frac1{n_a}\sum_{i\in C_a}z_i,
 \qquad
 \pi_i=\frac1{2n_a}\quad(i\in C_a),
 \qquad
 x=\pi^Tv=\frac{\bar v_1+\bar v_2}{2}.
\tag{2.1}
\]

Thus every component of \(\pi\) is positive and \(\pi^T\mathbf1=1\). Define
the same-module and cross-module history layers by

\[
 (B_0z)_i=\frac12\bar z_a,
 \qquad
 (B_1z)_i=\frac12\bar z_b,
 \qquad i\in C_a,\quad b\ne a.
\tag{2.2}
\]

They are entrywise nonnegative and obey the exact, size-independent
identities

\[
 B_0\mathbf1=B_1\mathbf1=\frac12\mathbf1,
 \qquad
 \pi^TB_0=\pi^TB_1=\frac12\pi^T,
 \qquad
 B_0+B_1=P:=\mathbf1\pi^T.
\tag{2.3}
\]

In particular, \(P^2=P\), \(Pv=x\mathbf1\), and
\(\pi^T(P-I)=0\). These statements remain exact when \(n_1\ne n_2\);
using the uniform node average instead of (2.1) would destroy that property.

Let

\[
 f(s)=s-\frac{s^3}{3},
 \qquad
 G(s)=\kappa_1s+\kappa_3(s-1)^3,
\tag{2.4}
\]

where \(f\) and \(G\) act componentwise on vectors. Fix

\[
 \varepsilon=\frac15,\qquad
 a=\frac35,\qquad
 D=3,\qquad
 E=2,\qquad
 \tau_0=4\sqrt5,\qquad
 \tau_1=5\sqrt5,\qquad
 \tau_*=\tau_1,
\tag{2.5}
\]

and take

\[
 (\kappa_1,\kappa_3)\in
 U=[0.199999999999,0.200000000001]
   \times[0.249999999999,0.250000000001].
\tag{2.6}
\]

During the controlled decision stage the network is

\[
\begin{aligned}
 \dot v={}&f(v)-w+D(P-I)v\\
 &+\varepsilon\{B_0G(v(t-\tau_0))
                  +B_1G(v(t-\tau_1))-G(v)\},\\
 \dot w={}&\varepsilon(v-a\mathbf1)+E(P-I)w
            -\varepsilon(x-a)\mathbf1.
\end{aligned}
\tag{2.7}
\]

Equation (2.7) is exactly the linear-plus-cubic delayed actuator written in
the compact notation (2.4). It is considered on the controlled history leaf

\[
 \mathcal X_{\rm cl}
 =\{\phi\in C([-\tau_*,0],\mathbb R^{2N}):
       \pi^T\phi_w(\theta)=0
       \text{ for every }\theta\in[-\tau_*,0]\}.
\tag{2.8}
\]

Multiplication of the recovery equation by \(\pi^T\) gives

\[
 \frac{d}{dt}\pi^Tw=0.
\tag{2.9}
\]

Hence a solution starting in \(\mathcal X_{\rm cl}\) satisfies

\[
 \dot w_i=\varepsilon(v_i-x)-Ew_i.
\tag{2.10}
\]

The subtraction in (2.7) is an ideal common state-feedback clamp. No claim
is made here that it is available as a bounded laboratory actuator.

## 3. Complete-history sign corridors

Fix \(m>0\), \(W_0\ge0\), and a target magnitude \(H>m\). A positive
history belongs to \(\mathcal C_+(m,H,W_0)\) if it lies in
\(\mathcal X_{\rm cl}\) and satisfies

\[
 \phi_{v,i}(\theta)\ge m
 \quad\text{for every }i\text{ and }-\tau_*\le\theta\le0,
 \qquad
 0<\phi_{v,i}(0)<H,
\tag{3.1}
\]

and

\[
 \max_i\sup_{-\tau_*\le\theta\le0}
 |\phi_{w,i}(\theta)|\le W_0.
\tag{3.2}
\]

A negative history belongs to \(\mathcal C_-(m,H,W_0)\) if

\[
 \phi_{v,i}(\theta)\le-m
 \quad\text{for every }i\text{ and }-\tau_*\le\theta\le0,
 \qquad
 -H<\phi_{v,i}(0)<0,
\tag{3.3}
\]

together with (3.2). Conditions (3.1) and (3.3) constrain the entire delay
history, not just its endpoint. No upper magnitude bound on the past voltage
history is needed: the global monotonicity of \(G\) supplies the delayed-term
sign used below.

The positive distance \(m\) from the zero boundary is essential. Same-sign
histories that approach zero arbitrarily closely are not covered. Likewise,
large recovery histories are excluded by the strict scaffold condition in
Theorem 6.1.

## 4. Exact collective and recovery identities

The following identities are the two mechanisms behind the result.

> **Lemma 4.1 (collective voltage equation).** Every solution of (2.7) in
> \(\mathcal X_{\rm cl}\) satisfies
> \[
> \dot x=\pi^Tf(v)
> +\varepsilon\left\{
> \frac12\pi^TG(v(t-\tau_0))
> +\frac12\pi^TG(v(t-\tau_1))
> -\pi^TG(v)\right\}.
> \tag{4.1}
> \]

**Proof.** The recovery term vanishes because \(\pi^Tw=0\), and the voltage
scaffold vanishes because \(\pi^T(P-I)=0\). Applying the two projection
identities in (2.3) to the delayed layers gives (4.1). \(\square\)

> **Lemma 4.2 (componentwise recovery bound).** Suppose that, on
> \(0\le s\le t\), either \(0\le v_i(s)\le H\) for every \(i\), or
> \(-H\le v_i(s)\le0\) for every \(i\). Then
> \[
> |w_i(t)|\le e^{-Et}|w_i(0)|
> +\frac{\varepsilon H}{E}(1-e^{-Et})
> \le W_H,
> \qquad
> W_H:=\max\left\{W_0,\frac{\varepsilon H}{E}\right\}.
> \tag{4.2}
> \]

**Proof.** In either box, \(x\) lies in the same interval as every \(v_i\),
so \(|v_i-x|\le H\). Variation of constants in (2.10) gives (4.2).
\(\square\)

## 5. Nonlinear collective growth inside a sign corridor

Since the gains are positive,

\[
 G'(s)=\kappa_1+3\kappa_3(s-1)^2>0
 \quad\text{for every }s\in\mathbb R.
\tag{5.1}
\]

Moreover,

\[
 G(s)-G(0)
 =s\{\kappa_1+\kappa_3(s^2-3s+3)\}.
\tag{5.2}
\]

For \(0\le s\le3/2\), the quadratic factor in (5.2) is at most \(3\).
For \(-H\le s\le0\), writing \(u=-s\) gives

\[
 s^2-3s+3=u^2+3u+3\le H^2+3H+3.
\tag{5.3}
\]

Define

\[
 c_+(H)=1-\frac{H^2}{3}
          -\varepsilon(\kappa_1+3\kappa_3),
 \qquad 0<H\le\frac32,
\tag{5.4}
\]

and

\[
 c_-(H)=1-\frac{H^2}{3}
 -\varepsilon\{\kappa_1+
       \kappa_3(H^2+3H+3)\}.
\tag{5.5}
\]

> **Lemma 5.1 (mean growth).** Before any node reaches either the zero
> boundary or the target face \(H\), a solution from
> \(\mathcal C_+(m,H,W_0)\), with \(H\le3/2\), obeys
> \[
> \dot x\ge c_+(H)x.
> \tag{5.6}
> \]
> A solution from \(\mathcal C_-(m,H,W_0)\) obeys
> \[
> \dot x\le c_-(H)x.
> \tag{5.7}
> \]

**Proof.** In the positive corridor, all delayed voltage values are
nonnegative: this is true on the prescribed history interval and remains
true up to a first zero. By (5.1), each delayed \(G\)-value is at least
\(G(0)\). For the current values,

\[
 f(v_i)=v_i\left(1-\frac{v_i^2}{3}\right)
 \ge v_i\left(1-\frac{H^2}{3}\right),
\tag{5.8}
\]

and (5.2) is bounded above by
\(v_i(\kappa_1+3\kappa_3)\). Substitution in (4.1) gives (5.6).

In the negative corridor every delayed value is nonpositive, hence every
delayed \(G\)-value is at most \(G(0)\). Because multiplication by a
negative \(v_i\) reverses the coefficient inequality,

\[
 f(v_i)\le v_i\left(1-\frac{H^2}{3}\right),
 \qquad
 G(v_i)-G(0)\ge
 v_i\{\kappa_1+\kappa_3(H^2+3H+3)\}.
\tag{5.9}
\]

Equations (4.1) and (5.9) give (5.7). \(\square\)

No delayed monotonic ordering such as
\(v_i(t-\tau_j)\le v_i(t)\) is used. Only the complete-history sign and the
global monotonicity (5.1) are required.

## 6. Zero-boundary exclusion and nodewise first hit

> **Theorem 6.1 (full-network nonlinear sign-cone first hit).** Let
> \(0<H\le3/2\) on the positive side, and let \(H>0\) on the negative side.
> Assume the corresponding constant \(c_+(H)\) or \(c_-(H)\) is strictly
> positive. If
> \[
> Dm>W_H
> =\max\left\{W_0,\frac{\varepsilon H}{E}\right\},
> \tag{6.1}
> \]
> then the following statements hold for every pair of positive module sizes
> and every gain pair in \(U\).
>
> 1. For every \(\phi\in\mathcal C_+(m,H,W_0)\), no voltage component can
>    reach zero before a component reaches \(H\). Some node reaches \(H\)
>    at a time \(T_+\) satisfying
>    \[
>      T_+\le\frac1{c_+(H)}\log\frac{H}{x(0)}
>      \le\frac1{c_+(H)}\log\frac{H}{m}.
>    \tag{6.2}
>    \]
> 2. For every \(\phi\in\mathcal C_-(m,H,W_0)\), no voltage component can
>    reach zero before a component reaches \(-H\). Some node reaches
>    \(-H\) at a time \(T_-\) satisfying
>    \[
>      T_-\le\frac1{c_-(H)}\log\frac{H}{|x(0)|}
>      \le\frac1{c_-(H)}\log\frac{H}{m}.
>    \tag{6.3}
>    \]

**Proof.** Consider the positive case and stop the solution at the first
time that some component reaches either \(0\) or \(H\). Up to that time,
Lemma 5.1 and Gronwall's inequality give

\[
 x(t)\ge x(0)e^{c_+(H)t}\ge m.
\tag{6.4}
\]

Suppose that the first exit occurs at a zero component \(v_i(t_0)=0\).
At that boundary \(f(0)=0\), and the voltage scaffold equals

\[
 D(P-I)v_i=Dx(t_0)\ge Dm.
\tag{6.5}
\]

All delayed values have remained nonnegative. By the nonnegativity and row
masses of \(B_0,B_1\), together with (5.1),

\[
 \{B_0G(v(t_0-\tau_0))+B_1G(v(t_0-\tau_1))\}_i
 \ge G(0).
\tag{6.6}
\]

The current value is also \(G(v_i(t_0))=G(0)\). Lemma 4.2 and (6.1) now
give

\[
 \dot v_i(t_0)\ge Dm-W_H>0.
\tag{6.7}
\]

This contradicts a first contact with zero from above. Hence the first exit
must occur at \(H\), unless no exit occurs before the time in (6.2). The
latter alternative is impossible: (6.4) would give \(x(t)\ge H\), whereas
strict inequalities \(v_i(t)<H\) and positive weights \(\pi_i\) would give
\(x(t)<H\).

For the negative case, Lemma 5.1 gives

\[
 x(t)\le x(0)e^{c_-(H)t}\le-m.
\tag{6.8}
\]

At a hypothetical first zero component, every delayed \(G\)-value is at
most \(G(0)\), so

\[
 \dot v_i(t_0)\le-Dm+W_H<0.
\tag{6.9}
\]

This contradicts first contact with zero from below. Finally, if no
component reached \(-H\) by the time in (6.3), then (6.8) would imply
\(x(t)\le-H\) while every component remained strictly greater than \(-H\),
again a contradiction. \(\square\)

The proof is fully nonlinear in all voltage components. It uses neither a
transverse variational equation nor a smallness assumption on differences
between nodes. Network size enters only through the positive probability
weights (2.1) and the exact identities (2.3), so the statement is uniform in
all \(n_1,n_2\ge1\). It does not extend automatically to delay layers that
lose positivity or the exact \(\pi\)-projection identities.

## 7. Certified detector and finite-excursion constants

### 7.1 Nodewise detector at \(\pm1\)

Take \(H=1\). Then

\[
 c_+(1)=\frac23-\varepsilon(\kappa_1+3\kappa_3),
 \qquad
 c_-(1)=\frac23-\varepsilon(\kappa_1+7\kappa_3).
\tag{7.1}
\]

The directed certificate gives, uniformly on \(U\),

\[
 c_+(1)\ge
 0.4766666666658666666666666666666666666666666666649547831,
\tag{7.2}
\]

\[
 c_-(1)\ge
 0.2766666666650666666666666666666666666666666666645611784.
\tag{7.3}
\]

For the concrete cone \(m=0.04\), \(W_0=0.1\), directed arithmetic gives

\[
 W_1\le
 0.1000000000000000000000000000000000000000000000001026342
\tag{7.4}
\]

and

\[
 Dm-W_1\ge
 0.01999999999999999999999999999999999999999999999987940486>0.
\tag{7.5}
\]

Consequently a node reaches the declared detector \(+1\) within

\[
 T_+\le
 6.752886345888677744639642535625357328139237051228752807,
\tag{7.6}
\]

or reaches the detector \(-1\) within

\[
 T_-\le
 11.63449093332584072781267474078388756133659130843392546,
\tag{7.7}
\]

according to the sign cone. These are nodewise first-hit detectors; the
result does not say that the nodes synchronize at the face.

### 7.2 Positive controlled excursion to \(3/2\)

Take \(H_+=3/2\). Since

\[
 1-\frac{H_+^2}{3}=\frac14,
\tag{7.8}
\]

the directed gain box gives

\[
 c_+(H_+)\ge
 0.05999999999919999999999999999999999999999999999887256099>0.
\tag{7.9}
\]

Here \(\varepsilon H_+/E=0.15\). With the stronger complete-history margin
\(m_{\rm exc}=0.06\) and \(W_0=0.1\), the directed bounds are

\[
 W_{H_+}\le
 0.1500000000000000000000000000000000000000000000002394797,
\tag{7.10}
\]

\[
 Dm_{\rm exc}-W_{H_+}\ge
 0.02999999999999999999999999999999999999999999999978703411>0.
\tag{7.11}
\]

Therefore every eligible positive nonsynchronous history reaches
\(v_i=3/2\) at some node within

\[
 T_{+,\rm exc}\le
 53.64793041518531822556111535054706952219400607031937024.
\tag{7.12}
\]

By continuity, some node crosses \(+1\) before reaching \(+3/2\), so a
nodewise \(+1\) detector can be externally latched before the certified
finite suprathreshold excursion. The node that first triggers \(+1\) need
not be the node that later reaches \(+3/2\).

### 7.3 Negative controlled excursion to \(-6/5\)

Take \(H_-=6/5\). Then

\[
 1-\frac{H_-^2}{3}=\frac{13}{25},
 \qquad
 H_-^2+3H_-+3=\frac{201}{25}=8.04.
\tag{7.13}
\]

The directed certificate gives

\[
 c_-(H_-)\ge
 0.07799999999819199999999999999999999999999999999574747383>0.
\tag{7.14}
\]

Now \(\varepsilon H_-/E=0.12\), and the same
\(m_{\rm exc}=0.06,W_0=0.1\) gives

\[
 W_{H_-}\le
 0.1200000000000000000000000000000000000000000000001744781,
\tag{7.15}
\]

\[
 Dm_{\rm exc}-W_{H_-}\ge
 0.05999999999999999999999999999999999999999999999974512516>0.
\tag{7.16}
\]

Thus some node reaches \(v_i=-6/5\) within

\[
 T_{-,\rm exc}\le
 38.40682402081321193929299824780490405780298576531744953.
\tag{7.17}
\]

Some node necessarily crosses \(-1\) first, so the negative detector may be
externally latched before this finite controlled excursion. Again, the first
detector node and the excursion-face node need not coincide.

### 7.4 Optional ideal hold time

If an ideal full-state overwrite is maintained for one complete delay window
\(\tau_*=5\sqrt5\), then released, it creates a constant complete history and
hence an eligible synchronous member of the sign cone whenever
\(m\le |r|<H\) and \(w=0\). This ideal operation is not a bounded additive
pulse from arbitrary initial data.

Adding the directed upper bound

\[
 \tau_*\le
 11.18033988749894848204586834365638117720309179809627588
\tag{7.18}
\]

to the release deadlines gives the optional total bounds

\[
 T_{+,\rm exc}^{\rm total}\le
 64.82827030268426670760698369420345069939709786855796549,
\tag{7.19}
\]

\[
 T_{-,\rm exc}^{\rm total}\le
 49.58716390831216042133886659146128523500607756346846363.
\tag{7.20}
\]

These totals concern only the ideal overwrite protocol. The nonsynchronous
sign-cone theorem itself begins from an already eligible complete history.

## 8. Meaning of the detector-to-excursion statement

The rigorous operational sequence is

\[
 \text{eligible complete-history sign cone}
 \Longrightarrow
 \text{nodewise }\pm1\text{ crossing and external latch}
 \Longrightarrow
 \text{some node reaches }+3/2\text{ or }-6/5.
\tag{8.1}
\]

The second implication in (8.1) is not a restart of the theorem at the
detector time; it follows from applying Theorem 6.1 directly to the larger
target box from the original complete history. This distinction avoids an
invalid claim that the delayed history at the detector time satisfies a new
margin condition.

The theorem excludes a return to the zero-voltage boundary before the
excursion face. It does not exclude recrossing \(+1\) or \(-1\) after a first
detector hit. The detector must therefore be latched by the external
protocol. No autonomous no-return surface at \(\pm1\) has been proved.

## 9. Necessity of the narrowing conditions

Three restrictions cannot be removed by wording.

1. **Distance from the sign boundary.** At a first zero component the only
   uniform positive scaffold contribution is \(Dx\ge Dm\). If
   \(m\downarrow0\) while \(W_0\) is fixed, the recovery term can dominate.
   The proof gives no all-same-sign theorem without a quantitative margin.

2. **Recovery bound.** If \(W_0\ge Dm\), a boundary component with positive
   recovery can point out of the positive cone. Condition (6.1), or another
   hypothesis controlling recovery, is mathematically indispensable.

3. **Positive rank-one delay layers.** Both the mean estimate and the
   boundary sign use entrywise nonnegativity, unit combined row mass, and
   \(\pi^TB_j=\pi^T/2\). The proof is uniform in module size but is not a
   theorem for arbitrary network topology.

## 10. Claim ledger

The following statements are proved.

- Exact \(\pi\)-projection identities for \(B_0,B_1,P\), for every
  \(n_1,n_2\ge1\).
- Exact invariance of the controlled collective-recovery leaf and the
  componentwise recovery estimate (4.2).
- Fully nonlinear, nonsynchronous positive and negative sign-corridor
  first-hit theorems under the explicit strict inequality (6.1).
- A nodewise \(+1\) or \(-1\) detector with explicit uniform deadlines for
  \(m=0.04,W_0=0.1\).
- A finite controlled positive excursion to \(+3/2\) and negative excursion
  to \(-6/5\), with explicit uniform deadlines for
  \(m_{\rm exc}=0.06,W_0=0.1\).
- An external-latch interpretation of the detector followed by the finite
  excursion.

The following statements are not proved.

- nonlinear synchronization or attraction of nonsynchronous histories;
- robustness to perturbations that cross the voltage sign boundary;
- realization by bounded additive voltage or recovery actuators;
- that the first detector node is the node reaching the excursion face;
- no-return across \(+1\) or \(-1\) after the detector hit;
- an autonomous biological pulse basin, quiet basin, full action potential,
  or periodic attraction beyond the excursion face;
- unforced or maximal-canard onset;
- arbitrary graph topology or arbitrary signed delay layers.

Accordingly, the safe short claim is:

> In the fixed rank-one two-module \(D=3,E=2\) recovery-clamped FHN family,
> every complete-history same-sign cone satisfying an explicit voltage and
> recovery margin has a size-uniform, fully nonlinear nodewise first hit;
> for a stronger explicit margin the ideal controlled trajectory continues
> to a certified finite voltage excursion beyond the latched \(\pm1\)
> detector.

## 11. Reproducibility binding

The directed and exact certificate is generated by

~~~text
PYTHONPATH=build/testdeps:src /usr/bin/python3 \
  experiments/fhn_full_network_nonlinear_sign_cone.py
~~~

The result artifact is

~~~text
experiments/results/fhn_full_network_nonlinear_sign_cone.json
SHA-256: 89c4ff362a8deb9ba722748015ec236f2f0365073e476c27da0b8c079fae6509
~~~

It is source-manifest bound and, in turn, bound to the same-model separator
artifact

~~~text
experiments/results/fhn_same_model_separator.json
SHA-256: 9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86
~~~

The exact audit checks (2.3), the recovery identities, the intrinsic
factorizations, and the cubic boundary factor. The numerical layer uses
160-bit MPFR directed endpoints for every public lower or upper bound. The
artifact scope marks synchronization, attraction, cross-sign noise,
bounded-hardware realization, same-node continuation, detector-face
no-return, biological basin capture, unforced canard onset, and general
topology as false.
