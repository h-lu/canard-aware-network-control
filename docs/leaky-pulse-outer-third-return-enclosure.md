# A directed complete-history enclosure at the (J=0.32) third return

Status: **proved single-pulse ambient history-ball inclusion; no attracting-tube or
basin conclusion.** For the exact quiet initial history and the physical
pulse (u(t)=8/25) on (0leq t<1), this calculation isolates the third
positive crossing of the phase-zero voltage level of the validated outer
Fourier center. At that event it bounds the reduced and complete histories
relative to phase zero of the exact, phase-fixed outer RFDE orbit. The outer
Floquet zero index, stable projection and power bounds, and a quantitative
attracting-tube radius remain open. Consequently this result is not outer
capture, two-sided routing, an onset theorem, or a value of (J_c).

The executable source is
[the third-return enclosure](../src/canard_control/leaky_pulse_outer_third_return_enclosure.py),
the generator is
[the experiment](../experiments/leaky_pulse_outer_third_return_enclosure.py),
and the source-bound output is
[the result](../experiments/results/leaky_pulse_outer_third_return_enclosure.json).

## 1. The statement actually proved

Let

\[
 X=C([-5\sqrt5,0],\mathbb R^2),\qquad
 Y=C([-5\sqrt5,0],\mathbb R)\times\mathbb R
\]

carry their componentwise maximum norms. Let (z_J) be the exact RFDE
solution from the exact quiet equilibrium history under the pulse
(u=J=8/25) on ([0,1)), and let (z_o) be the unique phase-fixed outer
periodic orbit in the validated Wiener ball. The event level is the exact
binary64 number bound by the old routing target,

\[
 c_0=0.056096728550787761\ldots .
\]

There are exactly six crossings of (v_J=c_0) before the end of the
directed horizon (43\sqrt5), with orientations

\[
 (-,+,-,+,-,+).
\]

In particular, the third positive crossing (t_3) is unique and satisfies

\[
\begin{split}
94.9619021653635192071796733171
 &\leq t_3\\
 &\leq94.9619021653635201634498045684 .
\end{split}
\]

For the phase-zero histories ((z_o)_0), the directed result proves

\[
 \|(z_J)_{t_3}-(z_o)_0\|_Y
 \leq 2.637078616900037\times10^{-5},
\]

and, more strongly,

\[
 \|(z_J)_{t_3}-(z_o)_0\|_X
 \leq 2.637078616900037\times10^{-5}. \tag{1.1}
\]

Thus the single (J=0.32) event history lies in the complete-history ball
of radius (10^{-4}) about the exact outer orbit at phase zero, with margin
at least

\[
 7.362921383099962\times10^{-5}. \tag{1.2}
\]

The phrase *history ball* in (1.1)--(1.2) is literal and ambient in \(X\).
The pulse event is defined by the old routing contract's binary64 level,
whereas the exact periodic orbit at phase zero need not lie on that same
exact point-evaluation section. Thus (1.1) does not assert a common
Poincaré section, and it does not say that the ball is invariant or
attracting.

## 2. Directed method of steps and event count

The delays are (4\sqrt5) and (5\sqrt5), and the pulse releases at
(t=1). We use the exactly ordered union

\[
 \{n\sqrt5/24\}\cup\{1+n\sqrt5/24\}.
\]

It contains both families of propagated delay breakpoints and the pulse
release. Every delayed cell therefore translates to a previously completed
cell with the same normalized coordinate. On each of the 2064 cells through
(43\sqrt5), a degree-24 MPFR Taylor polynomial is used only as a guide. A
quadratic-(P) logarithmic-norm inequality encloses its error against the
exact RFDE solution. All cells close. The global numerical bounds are

\[
 E_{P,\max}<4.984\times10^{-22},\qquad
 R_{\max}<1.566\times10^{-27},
\]

and the smallest fixed-point closure margin is positive,

\[
 m_{\rm cell}>1.715\times10^{-40}.
\]

Bernstein ranges enlarged by these flow errors exclude the section level on
2058 cells. On each of the six remaining cells, direct interval evaluation
of the RFDE fast field gives a strict derivative sign and the two cell
endpoints have opposite section signs. Hence each contains exactly one
crossing and there are no omitted crossings. A second directed sign test on
the normalized interval

\[
 [0.324758328677411,\;0.324758328677425]
\]

gives the event bracket above. Its time radius is

\[
 E_{\rm time}\leq4.781350656257\times10^{-16},
\]

while the exact event speed is bounded below by (0.8908941).

## 3. Continuous-history comparison

The delayed history from (t_3-5\sqrt5) to (t_3) consists of 241 exact
union-grid restrictions. On each one, the pulse guide is affinely restricted
and the 257-node outer trigonometric interpolant is expanded to degree 24 in
the same local variable. Bernstein bounds are applied to the difference
polynomial, and the analytic Fourier Taylor remainder is added. The largest
such remainder is below (3.564\times10^{-30}). This proves, continuously
in history time rather than on a sample mesh,

\[
 E_{\rm guide}\leq5.618781639851\times10^{-6},
 \qquad
 E_{\rm flow}\leq6.928770072425\times10^{-23}. \tag{3.1}
\]

The exact outer orbit differs from the binary64 Fourier center in the
validated unweighted component Wiener ball of radius (R_A=10^{-5}), and
its period differs by at most (R_T=10^{-5}). A same-phase coefficient
bound alone would miss the physical-time phase change over a delayed
history. With the validated phase-tangent bound (M_\theta), we instead use

\[
 E_{\rm orbit}
 \leq R_A+
 M_\theta\frac{(5\sqrt5)R_T}{\bar T(\bar T-R_T)}
 \leq2.075200452851\times10^{-5}. \tag{3.2}
\]

This is why (E_{\rm orbit}) is larger than the coefficient correction
radius itself.

Finally, the exact decomposition used in (1.1) is

\[
 E_{\rm hist}
 =E_{\rm guide}+E_{\rm flow}+E_{\rm orbit}
  +E_{\rm time}F_{\rm tube}+E_{\rm section}. \tag{3.3}
\]

Here

\[
F_{\rm tube}<0.964042,\qquad
E_{\rm time}F_{\rm tube}<4.61\times10^{-16},\qquad
E_{\rm section}<1.81\times10^{-16}.
\]

The last term encloses both the directed DFT interpolation identity at phase
zero and the \(1.81\times10^{-16}\) difference between the old routing
contract's exact binary64 section level and the stored phase-zero Fourier
node. It is not replaced by a binary64 equality assumption.

## 4. What this removes, and what it does not

The old (J=0.32) record compared 4097 sampled history points from three
ordinary integrations. It selected a useful target but did not bound a
continuous history, event time, integration error, or exact outer-orbit
correction. Equations (1.1)--(3.3) remove all four defects for this one
pulse.

There are two honest ways to turn (1.1) into future local capture. First, a
validated *ambient orbital* attracting tube of radius larger than
\(2.637078616900037\times10^{-5}\) would contain the event history directly.
Second, one may use an exact phase chart
\(\Pi_{\rm ph}\) from the ambient ball to an exact Poincaré section. If its
projection bound is \(Q_{\rm ph}\), a section return theorem would require

\[
 Q_{\rm ph}E_{\rm hist}<r_{\rm sec},\qquad
 P_o(B_{r_{\rm sec}})\subseteq B_{r_{\rm sec}},\qquad
 \sup_{B_{r_{\rm sec}}}\|DP_o\|\leq q+C r_{\rm sec}<1. \tag{4.1}
\]

Under these additional hypotheses, (1.1) gives entry into the contractive
return domain and hence local outer capture for this pulse. This route can
bypass a prior global outer zero count, but it cannot bypass the phase chart.
In particular, merely adding the old-level/phase-zero discrepancy to
\(E_{\rm section}\) does not put the two histories on one exact section.
Neither an ambient attracting tube nor the data in (4.1) are currently
validated. The available binary64 finite sections suggest substantial
contraction, but they are not a directed bound for the exact history return
map; the capture flag therefore remains false.
Moreover, a single pulse is not a propagated complete exit face. Therefore
the following remain false in the artifact:

- outer attracting-tube entry and outer basin capture;
- propagation of the positive face of the inner signed exit cylinder;
- two-sided basin routing and a unique physical onset;
- identification of a physical (J_c), or frequency--amplitude--safety
  controllability.

The new certificate closes the local outer-attachment *target* for
(J=0.32). The global routing theorem still requires a quantitative outer
attracting tube and a uniform family enclosure starting from the complete
positive inner exit face.
