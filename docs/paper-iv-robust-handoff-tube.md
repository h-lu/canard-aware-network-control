# A robust finite-horizon shutdown tube for balanced delayed FHN networks

Status: **proved for an explicit open cylinder in the full RFDE history
space, uniformly over every finite balanced topology**. Exact synchrony is
not required. Small errors in the handoff state, the remote voltage history,
the gains, \(\varepsilon\) and \(a\), and the nominally closed additive inputs
are allowed. Every voltage component retains the desired sign until the
network first enters an explicit terminal block in finite time.

This is a mathematical robustness theorem for the final handoff segment.
With zero input residual it contains the autonomous handoff theorem
as a special case. With nonzero residual it is a shutdown-error theorem, not
an uncontrolled trajectory. The result does not prove that feedback reaches
this entrance cylinder, and it does not identify the resulting excursion with
a biological action potential.

Executable sources:

- [fhn_robust_handoff_tube.py](../src/canard_control/fhn_robust_handoff_tube.py),
- [fhn_robust_handoff_tube.py](../experiments/fhn_robust_handoff_tube.py),
- [fhn_robust_handoff_tube.json](../experiments/results/fhn_robust_handoff_tube.json).

The result is bound to two frozen parents:

- the autonomous-handoff artifact, SHA-256
  38f612771fd5f7e50ffd4f77103ea680b447fd11a7af25cc5ccea95b9bf606f2;
- the bounded preparation-and-control artifact, SHA-256
  090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9.

## 1. Nearby model family and residual input

Let \(N\geq1\). The matrices are nonnegative and satisfy

\[
 P\mathbf1=\mathbf1,
 \qquad
 B_j\mathbf1=\frac12\mathbf1,
 \quad j=0,1.
\tag{1.1}
\]

The additional stationary-distribution identities in the balanced parent
class remain in force, although the max-norm argument below only uses (1.1).
No symmetry, reversibility, or normality of \(P\) is assumed.

After the handoff, consider

\[
\begin{aligned}
 \dot v={}&f(v)-w+3(P-I)v\\
 &+\widetilde\varepsilon\kappa_1
 \{B_0v(t-\tau_0)+B_1v(t-\tau_1)-v\}\\
 &+\widetilde\varepsilon\kappa_3
 \{B_0h(v(t-\tau_0))+B_1h(v(t-\tau_1))-h(v)\}
 +d^v(t),\\
 \dot w={}&\widetilde\varepsilon
 (v-\widetilde a\mathbf1)+2(P-I)w+d^w(t),
\end{aligned}
\tag{1.2}
\]

where \(f(s)=s-s^3/3\), \(h(s)=(s-1)^3\), and the delays remain fixed at

\[
 \tau_0=4\sqrt5,
 \qquad
 \tau_1=5\sqrt5.
\tag{1.3}
\]

The strict parameter box is

\[
\begin{aligned}
 0.199999999998&<\kappa_1<0.200000000002,\\
 0.249999999998&<\kappa_3<0.250000000002,\\
 |\widetilde\varepsilon-1/5|&<10^{-6},\\
 |\widetilde a-3/5|&<10^{-6}.
\end{aligned}
\tag{1.4}
\]

The gain box lies inside the closed rational box used by the frozen phase
barriers. In the comparison orbit below, \(\kappa_1,\kappa_3\) take their
actual values, while \(\varepsilon=1/5\) and \(a=3/5\). Thus gain changes are
covered by uniformity of the old barrier, whereas the perturbations of
\(\varepsilon\) and \(a\) appear explicitly in the tracking estimate.

The functions \(d^v,d^w\) are arbitrary-sign measurable residual inputs. On
the relevant branch horizon \(H_\sigma\), their norm assumption is

\[
 \mathop{\rm ess\,sup}_{0\leq t\leq H_\sigma}
 \|d^v(t)\|_\infty<10^{-5},
 \qquad
 \mathop{\rm ess\,sup}_{0\leq t\leq H_\sigma}
 \|d^w(t)\|_\infty<10^{-5}.
\tag{1.5}
\]

No sign, continuity, bandwidth, or slew-rate condition is hidden in (1.5).
The residuals model imperfect closing of additive mathematical inputs. They
are not a hardware model.

## 2. The RFDE phase space and the open entrance cylinder

Set

\[
 X_N=C([-\tau_1,0],\mathbb R^{2N}),
 \qquad
 \|\phi\|_{X_N}
 =\sup_{-\tau_1\leq\theta\leq0}
 \max\{\|\phi^v(\theta)\|_\infty,
       \|\phi^w(\theta)\|_\infty\}.
\tag{2.1}
\]

The positive and negative branch data are

\[
\begin{array}{c|c|c|c|c}
 \sigma&r_\sigma&s^0_\sigma&s^1_\sigma&H_\sigma\\ \hline
 +&1/2&1&3/2&
 1.278339402787582773861681613826836042069901030142172264\\
 -&-1/2&-28/25&-6/5&
 0.4444584011141191698086150978017082389825931513417759996
\end{array}
\tag{2.2}
\]

For both delays define the remote history windows

\[
 I_{j,\sigma}=[-\tau_j,H_\sigma-\tau_j],
 \qquad j=0,1.
\tag{2.3}
\]

The directed parent bound

\[
 H_\sigma<8.944271909999158785636694674925104941762473438424472008
 \leq\tau_0
\tag{2.4}
\]

shows that every \(I_{j,\sigma}\) lies strictly before the handoff time. These
are exactly the history portions sampled by the two delayed layers for
\(0\leq t\leq H_\sigma\).

Let \(\delta_0=\delta_h=10^{-4}\). The entrance cylinder
\(\mathcal C_\sigma\subset X_N\) consists of histories satisfying

\[
\begin{aligned}
 \|\phi^v(0)-s^0_\sigma\mathbf1\|_\infty&<\delta_0,\\
 \|\phi^w(0)\|_\infty&<\delta_0,\\
 \max_{j=0,1}\sup_{\theta\in I_{j,\sigma}}
 \|\phi^v(\theta)-r_\sigma\mathbf1\|_\infty&<\delta_h.
\end{aligned}
\tag{2.5}
\]

Evaluation at zero and restriction to a compact subinterval are continuous
maps on \(X_N\). All inequalities in (2.5) are strict. Hence
\(\mathcal C_\sigma\) is an open cylinder in the full RFDE history space, not
merely a relatively open subset of the synchronous leaf. Apart from the two
endpoint constraints in (2.5), no restriction is placed on the voltage away
from the remote windows or on the recovery history away from \(\theta=0\),
because the first method-of-steps interval never samples those values.

Condition (2.5) is an entrance hypothesis. A small amplitude or handoff-time
error that leaves the current state inside the first two inequalities is
covered. This theorem does not prove that the earlier bounded feedback sends
an arbitrary perturbed preparation history into \(\mathcal C_\sigma\); robust
entrance-cylinder reachability remains open.

## 3. The synchronous comparison paths

Fix the actual gains in (1.4). Let

\[
 (\bar v,\bar w)=(s_\sigma\mathbf1,q_\sigma\mathbf1)
\tag{3.1}
\]

be the nominal synchronous path with
\(\varepsilon=1/5\), \(a=3/5\), initial state
\((s^0_\sigma\mathbf1,0)\), and frozen delayed voltage
\(r_\sigma\mathbf1\). The pinned autonomous-handoff theorem gives a time
\(t^*_\sigma\leq H_\sigma\) at which
\(s_\sigma=s^1_\sigma\). Before that hit,

\[
 \dot s_+\geq
 0.1372872269707499999999999999999999999999999999997965513
\tag{3.2}
\]

on the positive branch, and

\[
 -\dot s_-\geq
 0.07484260258816079999999999999999999999999999999988048404
\tag{3.3}
\]

on the negative branch. At the nominal terminal hit,

\[
 0\leq q_+(t^*_+)\leq
 0.1852127730287500000000000000000000000000000000002499532
\tag{3.4}
\]

and

\[
 -0.1575073974086500000000000000000000000000000000002482193
 \leq q_-(t^*_-)\leq0.
\tag{3.5}
\]

The old phase barriers are used only for (3.2)--(3.5). Robustness is supplied
by the max-norm tube below.

## 4. A topology-uniform max-norm estimate

Write

\[
 e^v=v-s_\sigma\mathbf1,
 \qquad
 e^w=w-q_\sigma\mathbf1,
\tag{4.1}
\]

and set

\[
 E_v=\|e^v\|_\infty,
 \qquad E_w=\|e^w\|_\infty,
 \qquad E=\max\{E_v,E_w\}.
\tag{4.2}
\]

We work up to the first exit from \(E<R\), where

\[
 R=0.0006.
\tag{4.3}
\]

### 4.1 Why an asymmetric scaffold does not enlarge the max norm

Let \(i\) be active for \(E_v\), so
\(|e^v_i|=E_v\), and let
\(\xi_i=\operatorname{sign}(e^v_i)\). Row stochasticity and nonnegativity give

\[
\begin{aligned}
 \xi_i\{(Pe^v)_i-e^v_i\}
 &\leq\sum_kP_{ik}|e^v_k|-|e^v_i|\\
 &\leq E_v\sum_kP_{ik}-E_v=0.
\end{aligned}
\tag{4.4}
\]

The same calculation applies to an active recovery component. Thus both
\(3(P-I)\) and \(2(P-I)\) are dissipative in the upper Dini derivative of the
nodewise \(\ell^\infty\) norm. This is a row-by-row argument; it does not use
symmetry of \(P\).

### 4.2 Delayed and local nonlinearities

On the remote windows, (2.5) and the nonnegative half-row masses of \(B_j\)
give

\[
 \left\|B_0\delta v(t-\tau_0)
       +B_1\delta v(t-\tau_1)\right\|_\infty
 \leq\delta_h.
\tag{4.5}
\]

For all remote values in (2.5), \(h\) has Lipschitz constant below \(7\).
The directed coefficient check is

\[
 \widetilde\varepsilon
 (\kappa_1+7\kappa_3)<\frac25.
\tag{4.6}
\]

In the \(R\)-neighborhood of the two nominal corridors, the one-sided
Lipschitz constant of \(f\) is below \(1/50\). Since \(h\) is increasing and
\(\widetilde\varepsilon,\kappa_3>0\), the local cubic difference appears with
a minus sign and is dissipative at an active component. The local linear
delayed-minus-current term is dissipative for the same reason.

The reference coupling bracket multiplying
\(|\widetilde\varepsilon-1/5|\) is below \(2\) on both corridors. Also
\(|s_\sigma-3/5|\leq9/5<2\) and
\(\widetilde\varepsilon<201/1000\). Combining these bounds with (1.5) gives

\[
\begin{aligned}
 D^+E_v
 &\leq\frac1{50}E_v+E_w
 +\frac25\delta_h+2(10^{-6})+10^{-5},\\
 D^+E_w
 &\leq\frac{201}{1000}E_v
 +2(10^{-6})+\frac{201}{1000}(10^{-6})+10^{-5}.
\end{aligned}
\tag{4.7}
\]

Both forcing terms are bounded above by the exact rational number

\[
 b=\frac{13}{250000}=0.000052.
\tag{4.8}
\]

Consequently

\[
 D^+E\leq\frac{21}{20}E+b.
\tag{4.9}
\]

The coefficient \(21/20\) contains a strict rational margin \(3/100\) over
the actual bound \(51/50\).

### 4.3 Directed Gronwall closure

Since \(E(0)<10^{-4}\), (4.9) yields

\[
 E(t)\leq
 e^{(21/20)t}10^{-4}
 +\frac{e^{(21/20)t}-1}{21/20}\,0.000052.
\tag{4.10}
\]

MPFR evaluation with upward rounding at the two public horizons gives

\[
 E(t)\leq
 0.0005228040534029681427608666290366623487309941879054806624
 <R
\tag{4.11}
\]

on the positive branch and

\[
 E(t)\leq
 0.0001889207819203155639160672374822448740135301440115884132
 <R
\tag{4.12}
\]

on the negative branch. The directed lower slacks are respectively

\[
 0.0000771959465970318572391333709633376512690058120945193376
\tag{4.13}
\]

and

\[
 0.0004110792180796844360839327625177551259864698559884115868.
\tag{4.14}
\]

The usual first-exit argument now closes the bootstrap: an exit through
\(E=R\) before \(t^*_\sigma\) would contradict (4.11) or (4.12).

## 5. Componentwise direction and terminal blocks

For direction of every component, rather than only the max-norm error, bound
the absolute voltage-field difference. On the bootstrap enclosure,

\[
 |f(v_i)-f(s_\sigma)|\leq\frac{13}{10}E,
 \qquad
 |h(v_i)-h(s_\sigma)|\leq15E.
\tag{5.1}
\]

Moreover

\[
 \|3(P-I)e^v\|_\infty\leq6E,
\tag{5.2}
\]

and the remaining local linear, local cubic, and recovery-error coefficients
make the total state coefficient strictly less than \(10\). Therefore

\[
 |\dot v_i-\dot s_\sigma|
 \leq10R+\frac25\delta_h+2(10^{-6})+10^{-5}
 =0.006052.
\tag{5.3}
\]

Equations (3.2)--(3.3) imply the public componentwise bounds

\[
 \dot v_i\geq0.131
\tag{5.4}
\]

on the positive branch and

\[
 \dot v_i\leq-0.068
\tag{5.5}
\]

on the negative branch, until terminal capture. Hence no component reverses
on this finite interval.

At the nominal hit time \(t^*_\sigma\), the tracking tube and
(3.4)--(3.5) place the full network in the blocks

\[
\begin{aligned}
 \mathcal K_+={}&
 [1.4994,1.5006]^N\\
 &\times
 [-0.0006,
  0.1858127730287500000000000000000000000000000000002499532]^N,
\end{aligned}
\tag{5.6}
\]

and

\[
\begin{aligned}
 \mathcal K_-={}&
 [-1.2006,-1.1994]^N\\
 &\times
 [-0.1581073974086500000000000000000000000000000000002482193,
  0.0006]^N.
\end{aligned}
\tag{5.7}
\]

The current-state part of (2.5) lies outside the corresponding voltage slab,
so continuity gives a well-defined first entry into \(\mathcal K_\sigma\), no
later than \(t^*_\sigma\leq H_\sigma\). Nothing here asserts that
\(\mathcal K_\sigma\) is forward invariant after first entry.

## 6. Robust finite-horizon capture theorem

> **Theorem 6.1 (open asynchronous shutdown tube).**
> Let \(N\geq1\), let the fixed delays and balanced topology satisfy
> (1.1)--(1.3), and choose parameters in the strict box (1.4). Select either
> branch \(\sigma\in\{+,-\}\). If the handoff history belongs to the open
> cylinder \(\mathcal C_\sigma\) in (2.5), and the arbitrary-sign residual
> inputs satisfy (1.5), then the Carathéodory RFDE solution exists through its
> first entry into \(\mathcal K_\sigma\). That entry occurs by
> \(H_\sigma\). Before it,
> every voltage component has the strict sign (5.4) or (5.5), and the full
> state remains within \(0.0006\) in nodewise max norm of the corresponding
> nominal synchronous phase-barrier path.

**Proof.** Use the actual gains to select the nominal path in Section 3.
The remote-window condition makes (4.5) valid for every delayed evaluation up
to \(H_\sigma\). At active max-norm components, (4.4), the monotonicity of
\(h\), and the negative current part of the weak coupling leave only the
one-sided \(f\) term, the cross-coordinate error, the bounded history error,
the two parameter errors, and the residual inputs. This gives (4.7)--(4.9).
The directed bounds (4.11)--(4.14) close the first-exit bootstrap. The
absolute field estimate (5.3) and the nominal phase-barrier velocities then
give (5.4)--(5.5). At \(t^*_\sigma\), (4.11)--(4.12) and the nominal landing
bounds give (5.6)--(5.7). \(\square\)

The theorem is uniform in \(N\) and in the balanced topology because all
matrix estimates use row masses rather than dimension-dependent norms. Its
initial histories may be asynchronous. It is nevertheless conditional on
entry into \(\mathcal C_\sigma\).

## 7. Exact claim boundary

The result proves:

- an explicit open cylinder in the full RFDE phase space;
- asynchronous, topology-uniform finite-horizon tracking;
- perturbations of both gains, \(\varepsilon\), and \(a\) in the declared
  strict box;
- arbitrary-sign \(L^\infty\) residuals in both nominally closed additive
  inputs;
- componentwise no reversal until finite terminal-block capture;
- first entry into \(\mathcal K_+\) or \(\mathcal K_-\) by the public horizon.

It does **not** prove:

- robust preparation of the remote history or reachability of the entrance
  cylinder from a larger initial-data set;
- an exactly autonomous trajectory when either residual input is nonzero;
- robustness to delay error or topology outside the balanced class;
- invariance of either terminal block, permanent no-return, or return to rest;
- a biological action potential, physiological calibration, quiet basin, or
  pulse basin;
- actuator bandwidth, slew-rate, energy, saturation, or hardware feasibility;
- landing on or attraction to the tracked periodic branch.

Thus this theorem supplies a finite-horizon robust control tube that can be
used as a mathematically honest bridge toward biological pulse control. It
does not itself complete the biological interpretation.
