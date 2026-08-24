# Dobrushin-uniform transverse decay and local periodic attraction

Status: **proved on the \(\eta=0\) slice of the quadratic period-locked
dual-scaffold RFDE for every finite balanced topology with
\(\tau(Q)\le1/4\).**  The transverse linear decay rate \(0.007\) is uniform
in network size and admitted topology.  Combined with the validated
synchronous unstable-index theorem, this gives local nonlinear orbital
attraction, with asymptotic phase, for each fixed finite admitted network.
No network-uniform nonlinear basin is asserted.

The executable directed certificate is
[fhn_dobrushin_periodic_attraction.py](../src/canard_control/fhn_dobrushin_periodic_attraction.py),
the generator is
[fhn_dobrushin_periodic_attraction.py](../experiments/fhn_dobrushin_periodic_attraction.py),
and the refusal tests are
[test_fhn_dobrushin_periodic_attraction.py](../tests/test_fhn_dobrushin_periodic_attraction.py).

## 1. The admitted periodic network

Let \(Q\ge0\) be a finite row-stochastic matrix with a strictly positive
stationary probability row \(\pi^T\), and let
\(\Pi=\mathbf1\pi^T\).  Assume

\[
 \tau(Q)\le 1-\gamma,
 \qquad \gamma\ge\frac34.
\tag{1.1}
\]

Let \(B_0,B_1\ge0\) satisfy

\[
 B_j\mathbf1=\frac12\mathbf1,
 \qquad
 \pi^TB_j=\frac12\pi^T,
 \qquad j=0,1.
\tag{1.2}
\]

No identity between \(B_0+B_1\), \(Q\), and \(\Pi\) is required.  Consider
the quadratic period-locked dual-scaffold RFDE

\[
\begin{aligned}
 \dot v={}&v-\frac13v^{\circ3}-w+3(Q-I)v\\
 &+\varepsilon\kappa_1
 \{B_0v(t-\tau_0)+B_1v(t-\tau_1)-v\}\\
 &+\varepsilon\kappa_3
 \{B_0H(v(t-\tau_0))+B_1H(v(t-\tau_1))-H(v)\}\\
 &+\varepsilon\eta\Pi\!\left[
 (v(t)-\mathbf1)^{\circ2}
 -(v(t-\tau_*)-\mathbf1)^{\circ2}\right],\\
 \dot w={}&\varepsilon(v-a\mathbf1)+2(Q-I)w,
 \qquad H(v)=(v-\mathbf1)^{\circ3}.
\end{aligned}
\tag{1.3}
\]

Fix

\[
 \varepsilon=\frac15,qquad a=\frac35,qquad
 \tau_0=4\sqrt5,qquad \tau_1=5\sqrt5,qquad \tau_*=T_*,
\tag{1.4}
\]

and the validated microscopic gain box

\[
 |\kappa_1-0.2|\le10^{-12},
 \qquad |\kappa_3-0.25|\le10^{-12}.
\tag{1.5}
\]

The theorem below is on \(\eta=0\).  On synchrony, (1.1)--(1.2) reduce
(1.3) exactly to the validated scalar periodic equation, independently of
\(N,Q,B_0,B_1\).  Thus every member of the class contains the same
synchronous periodic orbit \((V(t)\mathbf1,W(t)\mathbf1)\).

## 2. Exact collective/transverse variational split

Put \(E=\ker\pi^T\).  The identities in (1.1)--(1.2) imply

\[
 QE\subset E,qquad B_jE\subset E,qquad
 \mathbb R^N=\operatorname{span}\{\mathbf1\}\oplus E.
\tag{2.1}
\]

Along the synchronous orbit define

\[
\begin{aligned}
 g(t)&=1-V(t)^2-\varepsilon\kappa_1
       -3\varepsilon\kappa_3(V(t)-1)^2,\\
 r_j(t)&=\varepsilon\left[
       \kappa_1+3\kappa_3(V(t-\tau_j)-1)^2\right].
\end{aligned}
\tag{2.2}
\]

For a pure transverse perturbation \((x,y)\in E\times E\), the exact
variational RFDE is

\[
\begin{aligned}
 \dot x(t)={}&\{g(t)I+3(Q-I)\}x(t)-y(t)\\
 &+r_0(t)B_0x(t-\tau_0)
  +r_1(t)B_1x(t-\tau_1),\\
 \dot y(t)={}&\varepsilon x(t)+2(Q-I)y(t).
\end{aligned}
\tag{2.3}
\]

There is no modal diagonalization in (2.3).  It is one operator equation on
the whole \((2N-2)\)-dimensional transverse space.

The quadratic carrier creates no missing transverse term.  At any
synchronous base history its pure-transverse derivative is

\[
 2\Pi\!\left[
 (V(t)-1)x(t)-(V(t-\tau_*)-1)x(t-\tau_*)\right]=0,
\tag{2.4}
\]

because \(\pi^Tx=0\) at every history slot.  Thus (2.3) is independent of
\(\eta\).  Full-network attraction is nevertheless claimed only at
\(\eta=0\), because the synchronous Floquet index has not been validated on
a nonzero \(\eta\)-interval.

## 3. Oscillation Dini inequalities

On \(E\), \(\operatorname{osc}z=\max_i z_i-\min_i z_i\) is a norm.  The
Dobrushin and balance identities give

\[
 \operatorname{osc}(Qz)\le(1-\gamma)\operatorname{osc}z,
 \qquad
 \operatorname{osc}(B_jz)\le\frac12\operatorname{osc}z.
\tag{3.1}
\]

Set

\[
 X(t)=\operatorname{osc}x(t),qquad
 Y(t)=\operatorname{osc}y(t).
\tag{3.2}
\]

Choose indices attaining the maximum and minimum of a component.  The
standard upper-Dini derivative formula for a finite maximum, followed by
(3.1), gives directly from (2.3)

\[
\begin{aligned}
 D^+X(t)
 &\le -(3\gamma-g_*)X(t)+Y(t)
       +\overline H\{X(t-\tau_0)+X(t-\tau_1)\},\\
 D^+Y(t)
 &\le -2\gamma Y(t)+\varepsilon X(t).
\end{aligned}
\tag{3.3}
\]

Here the source-validated coefficient bounds are

\[
 g(t)\le g_*,qquad
 \frac12r_j(t)\le\overline H,qquad
 \beta:=2\overline H.
\tag{3.4}
\]

The factor \(1/2\) in (3.1) is essential: \(r_jB_j\) has induced
oscillation gain at most \(r_j/2\le\overline H\).  Thus the two arbitrary
balanced delay layers have exactly the same worst-case total bound
\(\beta\) as the earlier rank-one difference mode.

For any \(c>0\), define

\[
 M(t)=\max\{X(t),cY(t)\},qquad
 M_t=\sup_{t-\tau_1\le s\le t}M(s).
\tag{3.5}
\]

If \(X\) realizes the maximum, then \(Y\le M/c\); if \(cY\) realizes it,
then \(X\le M\).  Hence

\[
 D^+M(t)\le-\alpha_{\gamma,c}M(t)+\beta M_t,
\tag{3.6}
\]

where

\[
 \boxed{
 \alpha_{\gamma,c}
 =\min\left\{3\gamma-g_*-\frac1c,
               2\gamma-c\varepsilon\right\}.}
\tag{3.7}
\]

Therefore the explicit, topology-checkable gain condition is

\[
 \boxed{\alpha_{\gamma,c}>\beta.}
\tag{3.8}
\]

Equivalently, some positive weight exists whenever

\[
 3\gamma-g_*-\beta>0,qquad 2\gamma-\beta>0,qquad
 (3\gamma-g_*-\beta)(2\gamma-\beta)>\varepsilon.
\tag{3.9}
\]

The extra sign conditions in (3.9) exclude the irrelevant case in which
both factors are negative.

## 4. Directed closure at \(\gamma=3/4\)

The source-bound Wiener and global-current certificates give

\[
\begin{aligned}
 g_*&\le
 0.8295652173920941398865781421878852635779889294313747929,\\
 \beta&\le
 0.9128836864233778194038236770051088529207536404034029522,\\
 \tau_1&\le
 11.18033988749894848204586834365638117720309179811817116.
\end{aligned}
\tag{4.1}
\]

Take \(\gamma=3/4\) and \(c=5/2\).  Directed recomposition yields

\[
\begin{aligned}
 3\gamma-g_*-c^{-1}&\ge
 1.020434782607905860113421857812114736422011070566161987,\\
 2\gamma-c\varepsilon&\ge
 0.9999999999999999999999999999999999999999999999986315445,\\
 \alpha_{\gamma,c}-\beta&\ge
 0.08711631357662218059617632299489114707924635959377460826.
\end{aligned}
\tag{4.2}
\]

At \(\lambda=0.007\),

\[
 \alpha_{\gamma,c}-\lambda-\beta e^{\lambda\tau_1}
 \ge
 0.005801775562507711930814267303951807974802876856215296382>0.
\tag{4.3}
\]

Halanay's inequality therefore proves

\[
 M(t)\le C e^{-0.007t}
 \sup_{-\tau_1\le s\le0}M(s),
\tag{4.4}
\]

with a constant independent of \(N,Q,B_0,B_1\) in the admitted class.
Every larger Dobrushin gap only improves (3.7), so the same certificate
holds for all \(\gamma\ge3/4\).

## 5. Periodic attraction theorem

> **Theorem 5.1 (Dobrushin-class transverse periodic decay).**  On the
> \(\eta=0\) slice of (1.3), for every gain pair in (1.5), every finite
> topology satisfying (1.1)--(1.2), and every transverse variational history,
> the solution of (2.3) decays exponentially.  The rate \(0.007\) and the
> weighted oscillation norm (3.5) are uniform in network size and topology.

**Proof.**  Equations (2.1)--(2.4) give the exact invariant transverse
equation.  The max--min calculation gives (3.3), balance gives the two
half-layer bounds, and (4.1)--(4.3) verify the strict Halanay inequality.
This proves (4.4). \(\square\)

> **Corollary 5.2 (local full-network orbital attraction).**  Under the
> hypotheses of Theorem 5.1, the synchronous periodic orbit has one
> algebraically simple unit multiplier and every other full-network
> multiplier lies strictly inside the unit disk.  For each fixed finite
> admitted topology, an open history neighborhood converges to a phase
> translate of that orbit.

**Proof.**  The collective/transverse projections commute with the
linearization along synchrony.  The collective block is exactly the
source-validated scalar block, whose nontranslation unstable index is zero
and whose unit multiplier is algebraically simple.  Theorem 5.1 places the
entire transverse history monodromy strictly inside the unit disk.

The quadratic model uses the enlarged horizon \(\tau_*=T_*\), whereas at
\(\eta=0\) the drift reads only the shorter active horizon \(\tau_1\).
Restriction to the active horizon is therefore a quotient semiconjugacy.
Its kernel consists of older history which never enters the drift; the
history shift kills this kernel after any sufficiently large finite number
of periods.  The enlarged monodromy is consequently a nilpotent extension
of the active-horizon monodromy.  Their nonzero spectra, including algebraic
multiplicities, agree, while the inert-history directions contribute only
the multiplier zero.  Thus the enlarged quadratic phase space has the same
simple unit multiplier and no additional unstable multiplier.

For each fixed finite network, (1.3) is a smooth retarded polynomial RFDE.
Its solution semigroup is eventually compact; on the enlarged phase space a
sufficiently high power of the one-period monodromy is compact even if one
period is slightly shorter than \(\tau_*\).  The hypotheses used in
[the synchronous right-half parent](paper-iv-synchronous-floquet-right-half-cover.md)
therefore remain valid after the nilpotent horizon extension.  Applying
[Hale--Verduyn Lunel, Chapter 10, Section 10.3, Theorem 3.3,
pp. 321--324](https://doi.org/10.1007/978-1-4612-4342-7) gives local nonlinear
orbital attraction with asymptotic phase. \(\square\)

The neighborhood in Corollary 5.2 may depend on \(N,Q,B_0,B_1\).  The
uniform linear transverse rate does not by itself produce a uniform
nonlinear basin.

## 6. Why the theorem cannot use \(\gamma>0\) alone

The condition \(\gamma>0\) without a quantitative lower bound cannot imply
a decay rate uniform over closing-gap families.  As \(\gamma\downarrow0\),
matrices \(Q\) may approach the identity;
the instantaneous transverse damping in (3.3) then disappears.  At the
limit \(Q=I\), copies of the synchronous variational equation occur in
transverse directions and inherit its neutral phase mode.  Correspondingly,
the first term in (3.7) tends to \(-g_*-1/c\), so no positive Halanay margin
can survive.  The threshold in (3.8), rather than the qualitative statement
\(\gamma>0\), is the theorem proved here.  This argument does not decide
whether some individual topology with \(0<\gamma<3/4\) is stable by a
sharper Floquet estimate.

## 7. Claim ledger

| Statement | Status |
|---|---|
| Exact general-topology transverse variational equation (2.3) | **Proved** |
| Balanced layer bound and Dobrushin Dini inequality | **Proved** |
| Uniform transverse rate \(0.007\) for \(\tau(Q)\le1/4\) | **Proved** |
| Arbitrary finite network size and admitted directed topology | **Proved** |
| Local nonlinear orbital attraction for each fixed admitted network | **Proved at \(\eta=0\)** |
| Basin size uniform in network size and topology | **Not proved** |
| Every fixed gap \(\gamma>0\) below \(3/4\) | **Not proved; the present Halanay certificate is insufficient** |
| A rate uniform along \(\gamma\downarrow0\) | **Impossible because the limit has transverse phase modes** |
| Full-network attraction for nonzero \(\eta\) | **Not validated** |
| Global synchronization or global periodic attraction | **Not proved** |
| Pulse capture, biological onset, or safety | **Not implied** |
