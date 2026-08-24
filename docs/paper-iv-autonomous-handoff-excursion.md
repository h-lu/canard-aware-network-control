# A controlled-to-autonomous excursion theorem for balanced delayed FHN networks

Status: **proved on the exactly prepared synchronous leaf, uniformly over the
tracked gain box and every finite topology in the balanced two-half-delay-layer
class**.  The onset is controlled.  After the stated handoff face, both
additive inputs are exactly zero and a method-of-steps argument proves a
finite autonomous voltage excursion without reversal before the terminal
face.

This note closes a specific gap in the bounded staged control chain.  It does
not identify the excursion with a biological action potential and does not
prove a pulse basin, a quiet basin, a return to rest, or attraction to the
tracked periodic branch.

Executable sources:

- [fhn_autonomous_handoff_excursion.py](../src/canard_control/fhn_autonomous_handoff_excursion.py),
- [fhn_autonomous_handoff_excursion.py](../experiments/fhn_autonomous_handoff_excursion.py),
- [fhn_autonomous_handoff_excursion.json](../experiments/results/fhn_autonomous_handoff_excursion.json).

The parent result is
[the balanced bounded control chain](paper-iv-balanced-general-topology-bounded-control-chain.md),
whose pinned artifact has SHA-256
`090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9`.

## 1. Same model and handoff protocol

Let \(N\geq1\).  Let \(P,\pi,B_0,B_1\) satisfy the nonnegative balanced
two-half-delay-layer assumptions of the parent theorem:

\[
 P\mathbf 1=\mathbf 1,
 \qquad \pi^TP=\pi^T,
 \qquad B_j\mathbf 1=\frac12\mathbf 1,
 \qquad \pi^TB_j=\frac12\pi^T.
\tag{1.1}
\]

The baseline network is unchanged:

\[
\begin{aligned}
 \dot v={}&f(v)-w+3(P-I)v\\
 &+\varepsilon\kappa_1
 \{B_0v(t-\tau_0)+B_1v(t-\tau_1)-v\}\\
 &+\varepsilon\kappa_3
 \{B_0h(v(t-\tau_0))+B_1h(v(t-\tau_1))-h(v)\}+u^v,\\
 \dot w={}&\varepsilon(v-a\mathbf1)+2(P-I)w+u^w,
\end{aligned}
\tag{1.2}
\]

where

\[
 f(s)=s-\frac{s^3}{3},\qquad h(s)=(s-1)^3,
 \qquad \varepsilon=\frac15,\qquad a=\frac35,
\tag{1.3}
\]

and

\[
 \tau_0=4\sqrt5,\qquad \tau_1=5\sqrt5.
\tag{1.4}
\]

It is convenient to write

\[
 G(s)=\kappa_1s+\kappa_3(s-1)^3.
\tag{1.5}
\]

The proof is uniform on the slightly enlarged rational box

\[
 \widehat U=
 [0.199999999998,0.200000000002]
 \times[0.249999999998,0.250000000002],
\tag{1.6}
\]

which contains the tracked microscopic gain box.

The parent theorem supplies bounded additive feedback that creates the exact
complete history

\[
 \Phi_r(\theta)=(r\mathbf1,0),
 \qquad -\tau_1\leq\theta\leq0,
\tag{1.7}
\]

for \(r=1/2\) or \(r=-1/2\).  After this preparation, set \(u^v=0\) and
retain the bounded recovery cancellation

\[
 u^w=-\{\varepsilon(v-a\mathbf1)+2(P-I)w\}
\tag{1.8}
\]

only until the handoff face specified below.  Thus \(w=0\) during the
controlled decision interval.  At handoff, close (1.8) as well:

\[
 \boxed{u^v=u^w=0.}
\tag{1.9}
\]

There is no overwrite, impulse, or change of vector field at handoff.

## 2. Exact synchrony and the frozen-delay step

The row-mass identities (1.1) make the synchronous history subspace
invariant both before and after handoff.  Starting from (1.7), write

\[
 v(t)=s(t)\mathbf1,\qquad w(t)=q(t)\mathbf1.
\tag{2.1}
\]

The scaffold terms vanish and both delay layers have total mass one.  While
the recovery cancellation is active, \(q=0\).  Once (1.9) is imposed, the
uncontrolled synchronous RFDE is

\[
\begin{aligned}
 \dot s={}&f(s)-q+\varepsilon
 \left\{\frac{G(s(t-\tau_0))+G(s(t-\tau_1))}{2}-G(s)\right\},\\
 \dot q={}&\varepsilon(s-a).
\end{aligned}
\tag{2.2}
\]

Suppose that the sum of the controlled handoff time and the subsequent
autonomous-excursion time is less than \(\tau_0\).  Both delayed arguments in
(2.2) then remain in the prepared part of the history.  The first method of
steps reduces (2.2) exactly to

\[
 \dot s=f(s)-q+\varepsilon\{G(r)-G(s)\},
 \qquad \dot q=\varepsilon(s-a).
\tag{2.3}
\]

Section 5 verifies the required strict time inequality, rather than assuming
it.

## 3. Controlled detector and handoff times

For the positive chart, retain (1.8) until \(s=1\).  The balanced sign-cone
growth estimate, now with the exact initial mean \(1/2\), gives

\[
 c_+(1)=\frac23-\varepsilon
 (\kappa_1^++3\kappa_3^+)
 \geq0.47666666666506666666666666666666666666666666666613,
\tag{3.1}
\]

where \((\kappa_1^+,\kappa_3^+)\) is the upper corner of
\(\widehat U\).  Hence the positive handoff occurs by

\[
 T^c_+\leq\frac{\log2}{c_+(1)}
 \leq1.454154924256514595725963380723086942974805049239.
\tag{3.2}
\]

For the negative chart, the face \(-1\) remains the externally latched onset
detector, but it is not yet a valid autonomous no-return face.  Keep (1.8)
active until

\[
 s=-\frac{28}{25}=-1.12.
\tag{3.3}
\]

Continuity ensures that the \(-1\) detector has already been crossed.  On the
box \([-28/25,0]\),

\[
\begin{aligned}
 c_-\!\left(\frac{28}{25}\right)
={}&1-\frac{(28/25)^2}{3}\\
&-\varepsilon\left\{
 \kappa_1^++\kappa_3^+
 \left((28/25)^2+3(28/25)+3\right)\right\}\\
\geq{}&0.16114666666322090666666666666666666666666666666640.
\end{aligned}
\tag{3.4}
\]

Therefore the negative handoff occurs by

\[
 T^c_-\leq
 \frac{\log((28/25)/(1/2))}{c_-(28/25)}
 \leq5.004607805834394101947888237543824115831011696470.
\tag{3.5}
\]

These are times from release of the prepared history, not from the beginning
of preparation.

## 4. Exact phase barriers after all controls close

### 4.1 Positive corridor

Put \(x=s\) and \(y=q\).  On the first method-of-steps interval with
\(r=1/2\), (2.3) has the form

\[
 \dot x=q_+(x;\kappa)-y,
 \qquad \dot y=\varepsilon(x-a),
\tag{4.1}
\]

where

\[
 q_+(x;\kappa)=f(x)-\varepsilon\left\{
 \kappa_1(x-1/2)+\kappa_3((x-1)^3+1/8)\right\}.
\tag{4.2}
\]

For \(1\leq x\leq3/2\), the two expressions multiplying the gains are
nonnegative.  Thus \(q_+(x;\kappa)\geq q_+^\flat(x)\), where
\(q_+^\flat\) uses the upper corner of \(\widehat U\).  Moreover,

\[
 (q_+^\flat)'(x)
 =1-x^2-\varepsilon\{\kappa_1^++3\kappa_3^+(x-1)^2\}<0.
\tag{4.3}
\]

Divide \([1,3/2]\) into twenty intervals of length \(1/40\).  The executable
certificate gives a continuous piecewise-linear function \(B_+\), with
\(B_+(1)=0\), whose slope on the \(j\)-th interval is \(m_j>0\).  If \(x_j\)
is that interval's right endpoint, its exact rational checks are

\[
 d_j=q_+^\flat(x_j)-B_+(x_j)>0,
 \qquad
 m_jd_j-\varepsilon(x_j-a)>0.
\tag{4.4}
\]

At a boundary point \(y=B_+(x)\), equations (4.3)--(4.4) imply

\[
 \frac{d}{dt}\{y-B_+(x)\}<0.
\tag{4.5}
\]

At a grid point, \(B_+\) is continuous.  The slope on the interval to the
right satisfies that interval's version of (4.4), so the upper right Dini
derivative of \(y-B_+(x)\) is still negative.  Induction over the twenty
closed intervals therefore handles every nonsmooth corner; no differentiable
global interpolation of the barrier is being assumed.

Consequently the hypograph \(0\leq y\leq B_+(x)\) is forward invariant
until the terminal face.  On the \(j\)-th interval, \(\dot x\geq d_j\), so
the crossing time is at most \((1/40)/d_j\).  Exact rational summation gives

\[
 \dot x\geq0.13728722697074999999999999999999999999999999999979
\tag{4.6}
\]

throughout the certified corridor and

\[
 T^a_+\leq1.278339402787582773861681613826836042069901030143.
\tag{4.7}
\]

At the \(x=3/2\) first hit,

\[
 0\leq y\leq
 0.18521277302875000000000000000000000000000000000025.
\tag{4.8}
\]

### 4.2 Negative corridor

Set \(z=-s\) and \(p=-q\).  With \(r=-1/2\), equation (2.3) becomes

\[
 \dot z=q_-(z;\kappa)-p,
 \qquad \dot p=\varepsilon(z+a),
\tag{4.9}
\]

where

\[
 q_-(z;\kappa)=f(z)-\varepsilon\left\{
 \kappa_1(z-1/2)+\kappa_3((z+1)^3-27/8)\right\}.
\tag{4.10}
\]

On \(28/25\leq z\leq6/5\), this vector is again bounded below by the
upper-gain-corner polynomial \(q_-^\flat\), which is strictly decreasing.
Indeed, throughout this interval,

\[
 (q_-^\flat)'(z)
 =1-z^2-\varepsilon\{\kappa_1^++3\kappa_3^+(z+1)^2\}<0.
\]

Sixteen intervals of length \(1/200\) and the same hypograph argument give

\[
 \dot z\geq
 0.07484260258816079999999999999999999999999999999988
\tag{4.11}
\]

and

\[
 T^a_-\leq
 0.444458401114119169808615097801708238982593151342.
\tag{4.12}
\]

At the \(z=6/5\), equivalently \(s=-6/5\), first hit,

\[
 -0.15750739740865000000000000000000000000000000000025
 \leq q\leq0.
\tag{4.13}
\]

The strict velocity bounds (4.6) and (4.11) are finite-horizon no-reversal
statements.  They do not say that the terminal faces remain one-way after the
frozen-delay interval ends.

## 5. Closing the RFDE method-of-steps loop

Combining the controlled and autonomous times gives

\[
 T^c_++T^a_+
 \leq2.732494327044097369587644994549922985044706079381,
\tag{5.1}
\]

and

\[
 T^c_-+T^a_-
 \leq5.449066206948513271756503335345532354813604847816.
\tag{5.2}
\]

The directed lower endpoint of the shortest delay is

\[
 \tau_0=4\sqrt5
 \geq8.944271909999158785636694674925104941762473438424.
\tag{5.3}
\]

Hence the two strict method-of-steps margins are respectively

\[
 \tau_0-(T^c_++T^a_+)
 \geq6.211777582955061416049049680375181956717667359046036396,
\tag{5.4}
\]

and

\[
 \tau_0-(T^c_-+T^a_-)
 \geq3.495205703050645513880191339579572586948768590622239497.
\tag{5.5}
\]

Thus the frozen delayed value used in Section 4 is an exact RFDE fact, not a
short-time approximation.

Adding the parent's complete-history preparation deadline gives deadlines
from the beginning of bounded control:

\[
 T^{\rm all}_+
 \leq17.229459004898445700748446074876990846174886423053,
\tag{5.6}
\]

\[
 T^{\rm all}_-
 \leq19.946030884802861602917304415672600215943785191487.
\tag{5.7}
\]

## 6. Main controlled-to-autonomous theorem

> **Theorem 6.1 (two finite autonomous handoff corridors).**
> Let \(N\geq1\), let the topology satisfy (1.1), and let the gains lie in
> the tracked microscopic box, hence in \(\widehat U\).  Start from any
> initial datum in the bounded cylinder of the parent theorem and use its
> bounded additive preparation to create either \(\Phi_{1/2}\) or
> \(\Phi_{-1/2}\).
>
> 1. From \(\Phi_{1/2}\), retain recovery cancellation until the synchronous
>    face \(v=\mathbf1\), then impose \(u^v=u^w=0\).  The uncontrolled
>    baseline network reaches
>
>    \[
>      v=\frac32\mathbf1,
>      \qquad
>      0\leq w_i\leq0.18521277302875000000000000000000000000000000000025
>    \]
>
>    by (5.1), and every voltage component is strictly increasing between
>    handoff and that face.
> 2. From \(\Phi_{-1/2}\), latch the synchronous detector
>    \(v=-\mathbf1\), retain recovery cancellation until
>    \(v=-(28/25)\mathbf1\), then impose \(u^v=u^w=0\).  The uncontrolled
>    baseline network reaches
>
>    \[
>      v=-\frac65\mathbf1,
>      \qquad
>      -0.15750739740865000000000000000000000000000000000025
>      \leq w_i\leq0
>    \]
>
>    by (5.2), and every voltage component is strictly decreasing between
>    handoff and that face.
>
> The conclusions hold for every finite balanced topology in (1.1), but only
> on the exactly prepared synchronous leaf.

**Proof.**  The parent bounded-control theorem creates (1.7) and realizes
(1.8) with a bounded additive input.  Exact synchrony reduces every topology
to (2.2).  The controlled growth estimates in Section 3 reach the declared
handoff faces.  The strict inequalities (5.4)--(5.5) keep the subsequent
trajectory inside the first method-of-steps interval, so (2.3) is exact.
The rational hypograph barriers in Section 4 force the stated terminal hits,
recovery bounds, and velocity signs.  Lifting the scalar solution by
\(\mathbf1\) gives the network conclusion.  \(\square\)

The theorem is stronger than a controlled excursion: the recovery actuator
is genuinely closed on the final segment.  It is weaker than autonomous
excitability because the complete history and the handoff face are created
by feedback.

## 7. Why the negative \(-1\) detector is not a no-return face

One might try to close (1.8) as soon as the negative detector reaches
\(s=-1\).  This fails even on the exact synchronous leaf.  Put again
\(z=-s\) and \(p=-q\).  At handoff,

\[
 z=1,\qquad p=0,
\tag{7.1}
\]

and the worst-corner initial vector satisfies

\[
 \dot z(0)=q_-(1;\kappa)
 \geq\frac{24924999999877}{60000000000000}
 >0.4154166666646>0.
\]

Equation (4.9) applies.  Let \(q_-^\sharp\) denote (4.10) evaluated at the lower
gain corner of \(\widehat U\); it is an upper bound for the actual voltage
vector and is strictly decreasing for \(z\geq1\) by the same derivative
identity used in Section 4.2.  An exact rational piecewise-linear lower barrier \(L\), with
seventeen intervals of length \(1/100\), satisfies at each left endpoint
\(x_{j-1}\)

\[
 \varepsilon(x_{j-1}+a)
 -L'_j\{q_-^\sharp(x_{j-1})-L(x_{j-1})\}>0.
\tag{7.2}
\]

The lower barrier is continuous at each grid point, and the outgoing slope
satisfies the next interval's inequality (7.2).  Thus the lower right Dini
derivative of \(p-L(z)\) is positive at every corner as well as in every open
segment.

Thus \(p\geq L(z)\) as long as \(z\) is increasing.  At the final endpoint,

\[
 L(1.17)-q_-^\sharp(1.17)
 =\frac{92721922530336687}{2500000000000000000}>0.
\tag{7.3}
\]

Continuity forces a zero of \(\dot z=q_-(z;\kappa)-p\) before \(z=1.17\).
At such a first zero,
\[
 \ddot z=q_-'(z)\dot z-\dot p=-\varepsilon(z+a)<0,
\tag{7.4}
\]
so it is a strict first local maximum of \(z\), equivalently a strict local
minimum of the voltage \(s=-z\).
The turn also occurs by

\[
 T_{\rm turn}\leq
 \frac{q_-^\sharp(1)}{\varepsilon(1+a)}
 \leq1.298177083339739583333333333333333333333333333337,
\tag{7.5}
\]

because \(p'\geq\varepsilon(1+a)=8/25\) while \(z\geq1\), whereas
\(q_-(z;\kappa)\leq q_-^\sharp(1)\).  The controlled sign-cone estimate
reaches \(-1\) by

\[
 T^c_{-,1}\leq
 2.505351255064924458193156191774920486346433300910,
\tag{7.6}
\]

so the complete decision-release clock satisfies

\[
 T^c_{-,1}+T_{\rm turn}
 \leq3.803528338404664041526489525108253819679766634246
 <\tau_0.
\tag{7.7}
\]

The directed frozen-delay slack is at least
\(5.140743571594494744110205149816851122082606804184454807\).
Therefore the same method-of-steps reduction is valid for the obstruction.

It follows that closing recovery cancellation at \(-1\) produces a first
local voltage reversal before the trajectory reaches \(-1.17\), and hence
before \(-1.2\).  This disproves a monotone no-return theorem from the old
negative detector.  It does **not** prove that the delayed trajectory can
never reach \(-1.2\) at a later time after its first reversal.

## 8. Exact claim boundary

The result proves:

- the same delayed FHN baseline before and after handoff;
- bounded preparation and bounded recovery cancellation only up to handoff;
- \(u^v=u^w=0\) throughout each certified final corridor;
- positive \(1\to3/2\) and negative
  \(-28/25\to-6/5\) autonomous finite excursions;
- strictly signed voltage velocity and therefore no reversal on those finite
  corridors;
- two synchronous terminal faces with explicit recovery-coordinate bounds;
- uniformity in every finite balanced topology, restricted to the exactly
  prepared synchronous leaf;
- a rigorous obstruction to treating the negative \(-1\) detector as a
  monotone no-return face.

It does **not** prove:

- autonomous onset from an uncontrolled quiet history;
- an autonomous excursion for asynchronous histories;
- permanent no-return after either terminal face;
- a biological action potential or a physiological voltage calibration;
- a quiet basin, pulse basin, separatrix, or basin-to-basin transition;
- landing on or attraction to the tracked periodic branch;
- equality between a canard root and either handoff face;
- robustness to model error, measurement noise, bandwidth, slew rate, or
  hardware constraints.

The result validator records every item in the second list as false and
rejects an artifact that promotes any of them.
