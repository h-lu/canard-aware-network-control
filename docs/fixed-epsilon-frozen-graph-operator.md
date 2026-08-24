# The frozen synchronous graph operator at fixed epsilon

## 1. Scope

This note fixes an executable nonlocal operator for the next
fixed-parameter problem in the
[sliding-window bridge](fixed-epsilon-sliding-window-w1p-bridge.md).  It
also fixes one admissible global graph cutoff and a separate conditional
planar preparation rule.  The construction determines exactly what a
validated continuation must solve; it does **not** compute the fixed point,
validate the positive-amplitude history hull, construct the selected traces,
or prove a fixed-
\(\varepsilon\) canard root.

The distinction between the two cutoffs is structural.  The
\(C^\infty\) cutoff \(\chi_{\rm graph}\) makes the graph transform a global
complete-field problem.  The \(C^3\) cutoff \(\chi_{\rm plan}\) joins a
subsequently computed graph perturbation to \(q_0\) near the canonical planar
tails.  The latter never enters the graph transform.  This implements the
separation required by the
[growing-tube graph theorem](growing-tube-graph-proof.md) and the
[Green/phase trace construction](green-phase-selected-traces.md).

## 2. The exact synchronous fixed-point equation

Put

\[
 q_0(X,Y)=(Y-X^2,-X),\qquad
 \rho_*=\frac1{\sqrt5},
\]

and, for a complete vector field \(Q\), write

\[
 P_\tau^Q(u)=\pi_X\Phi_Q^{-\tau}(u),
 \qquad \tau\in\{4,5,\Theta_*\}.
\tag{2.1}
\]

The sign in (2.1) is part of the contract: these are backward-flow slots.
On the uncut physical hull the exact synchronous graph equation is

\[
 Q_Y(X,Y)=-X+\rho\nu,
\tag{2.2}
\]

\[
\begin{aligned}
 Q_X(u)={}&Y-X^2
 +\rho\left[-\frac{X^3}{3}
 +\frac15\left(\frac{P_4^Q(u)+P_5^Q(u)}2-X\right)\right]\\
 &+\rho^2\eta\left[X^2-(P_{\Theta_*}^Q(u))^2\right]\\
 &+\frac{\rho^3}{4}
 \left[\frac{(P_4^Q(u))^3+(P_5^Q(u))^3}{2}-X^3\right].
\end{aligned}
\tag{2.3}
\]

There is no Taylor remainder in (2.2)--(2.3); the equations are the exact
synchronous restriction of the
[quadratic period-locked model](quadratic-period-locked-selected-root.md).
At \(\rho=0\), the map is the constant map \(Q=q_0\).  At
\(\eta=0\), the \(\Theta_*\)-slot drops out of the value equation, but it is
still required for the history embedding and for

\[
 \left.\partial_\eta\mathcal T_X(Q;\rho,\nu,\eta)
 \right|_{Q\ {\rm fixed}}
 =\rho^2\left[X^2-(P_{\Theta_*}^Q)^2\right].
\tag{2.4}
\]

Thus \(H^{\rm gr}=0\) in the synchronous quotient eliminates the stable
network fibre only.  It does not eliminate the scalar delayed history or
turn (2.3) into a local polynomial ODE.

At \(\rho=0\), the field derivative of the graph transform is zero.  On the
singular core, where
\(\Phi_{q_0}^{-\tau}\gamma_0(s)=\gamma_0(s-\tau)\), differentiation of the
fixed-point equation therefore gives the exact first graph jet

\[
 \left.\partial_\rho Q(\gamma_0(s))\right|_{\rho=0}
 =\left(\frac{s^3}{24}+\frac9{20},\nu\right).
\tag{2.5}
\]

Equation (2.5) identifies the unjoined core graph jet.  It does not yet prove
that the separate planar preparation (Section 6) realizes the seed's
prescribed \(20/21\) join, because that statement requires the actual
jointly regular graph family and its prepared traces.

## 3. A frozen global graph extension

Use the global polynomial coordinates

\[
 \sigma=-2X,\qquad d=Y-X^2+\frac12.
\tag{3.1}
\]

For \(r\ge0\), define

\[
 c(r)=
 \begin{cases}
 1,&0\le r\le1,\\
 \displaystyle
 \frac{e^{-1/(2-r)}}{e^{-1/(r-1)}+e^{-1/(2-r)}},&1<r<2,\\
 0,&r\ge2.
 \end{cases}
\tag{3.2}
\]

Then \(c\in C^\infty\), with flat joins at one and two.  Freeze

\[
 \chi_{\rm graph}(X,Y)
 =c\!\left(\frac{|\sigma|}{537}\right)c(|d|).
\tag{3.3}
\]

It equals one on \(|\sigma|\le537,|d|\le1\), and vanishes outside
\(|\sigma|<1074,|d|<2\).  This profile is \(C^\infty\), hence it has the
bounded derivatives through order 12 required by the grade-nine jet family,
and it is frozen independently of \((\rho,\nu,\eta)\).  We cut each physical
forcing channel by precisely the current and delayed state slots on which
that channel depends.  With
\(w_j=\chi_{\rm graph}(u_j)\), the explicit global extension is

\[
\begin{aligned}
 \mathcal T_{S,X}={}&w_0(Y-X^2)\\
 &+\rho\left[-w_0\frac{X^3}{3}
 +\frac{w_0w_4w_5}{5}
   \left(\frac{x_4+x_5}{2}-X\right)\right.\\[-1mm]
 &\hspace{20mm}\left.
 +\rho\eta w_0w_\Theta(X^2-x_\Theta^2)
 +\frac{\rho^2w_0w_4w_5}{4}
  \left(\frac{x_4^3+x_5^3}{2}-X^3\right)
 \right],\\
 \mathcal T_{S,Y}={}&-w_0X+\rho\nu.
\end{aligned}
\tag{3.4}
\]

Equation (3.4) agrees exactly with (2.2)--(2.3) whenever every state slot is
in the plateau.  It is a bounded \(C^\infty\) vector-field datum, so every
candidate in the declared \(C_b^1\) fixed-point neighbourhood has a complete
two-sided flow; the bounded constant slow drift outside the current support does not
affect completeness.  Since \(\mathcal T_{S,Y}\) is known once
\((\rho,\nu)\) are fixed, the only global unknown is the scalar function
\(q=Q_X\).

The termwise slot sets in (3.4) are \(\{0\}\), \(\{0,4,5\}\),
\(\{0,\Theta_*\}\), \(\{0,4,5\}\), and the empty set for the slow
unfolding.  In particular, at \(\eta=0\) both the value equation and its
field derivative are globally independent of the otherwise inactive
\(\Theta_*\)-slot.  That slot remains present in (2.4) and in the enlarged
history horizon.

Writing down (3.4) does not prove that the target-amplitude retained hull lies
in the plateau, nor that \(I-D_q\mathcal T_S\) is invertible.  These remain
the two main validation tasks.

### 3.1 Why the longitudinal radius is 537

The jet rectangle used by the growing-tube theorem is

\[
 (a,b,c,e)\in\{0,\ldots,3\}\times\{0,\ldots,3\}
 \times\{0,1\}\times\{0,1,2\}.
\]

It contains 96 multi-indices and 28 distinct
\((\hbox{total grade},\hbox{parameter grade})\) blocks.  Hence the proof's
nesting depth is

\[
 D=2(28)+4=60.
\tag{3.5}
\]

For the directed period-lock horizon

\[
 7.3970862959520600<\Theta_*<7.3970863004241961,
\]

the theorem-native quantities are

\[
 T_{\rm buf}=\Theta_*+1,
 \qquad B_*=(D+1)T_{\rm buf}+2,
\]

and directed arithmetic gives

\[
 514.2222640530756<B_*<514.2222643258760.
\tag{3.6}
\]

For the fixed reference graph target \(\widehat S=4+18=22\), the proof-native
plateau requirement is therefore

\[
 536.2222640530756<\widehat S+B_*<536.2222643258760.
\tag{3.7}
\]

The chosen radius 537 has a certified margin greater than
\(0.7777356741240\).  This arithmetic explains why neither the seed plateau
20 nor the trace radius 22 can be reused as a graph cutoff.  It also exposes
the cost of applying the small-amplitude proof literally at the fixed target:
a full tensor discretization of the entire theorem-native rectangle would be
wasteful.  A sharper local reachable-hull theorem remains the preferred
validation route.

Independently of radius, the seed's septic profile is only \(C^3\); it cannot be reused as a graph cutoff for the grade-nine jet construction, which needs
bounded cutoff derivatives through order 12.

The choice \(\widehat S=22\) here freezes the current computational reference
datum.  It does not assert that the seed value \(S=4\) equals the
non-explicit \(S_{\delta_*}\) allowed by the asymptotic growing-tube theorem.

For a fully serialized nesting datum we choose

\[
 \kappa_j=\frac{61-j}{62},\qquad j=0,\ldots,60.
\tag{3.8}
\]

This is a strictly decreasing sequence in \((0,1)\).  Freezing it does not
validate the target-amplitude inclusions (23) of the growing-tube proof;
those inequalities remain open.

## 4. The residual derivative

Let \(y_\tau(r)=\Phi_Q^{-r}(u)\), \(0\le r\le\tau\).  For a field direction
\(V\), the induced backward-flow variation is the initial-value problem

\[
 \zeta'(r)=-DQ(y_\tau(r))\zeta(r)-V(y_\tau(r)),
 \qquad \zeta(0)=0.
\tag{4.1}
\]

Put \(\xi_\tau=\pi_X\zeta(\tau)\).  On the uncut hull,

\[
\begin{aligned}
 D_Q\mathcal T_X[V]={}&
 \left(\frac\rho{10}+\frac{3\rho^3x_4^2}{8}\right)\xi_4
 +\left(\frac\rho{10}+\frac{3\rho^3x_5^2}{8}\right)\xi_5\\
 &-2\rho^2\eta x_\Theta\xi_\Theta.
\end{aligned}
\tag{4.2}
\]

Thus the scalar residual derivative is

\[
 D_q\mathcal R[V](u)=V(u)-D_Q\mathcal T_X[V](u).
\tag{4.3}
\]

The source implements (4.1), the full cutoff-slot gradients of (3.4), and
(4.3).  These are algebraic evaluators.  A validated ODE flow/variation
integrator, a discretization of \(q\), and a radii-polynomial inverse bound
have not yet been supplied.

## 5. The scalar graph cannot close polynomially

At \(\rho=0\), (3.1) puts the singular field in the exact form

\[
 \sigma'=1-2d,\qquad d'=\sigma d.
\tag{5.1}
\]

Along \(d=0\), differentiation of the backward flow with respect to the
initial normal coordinate gives

\[
 \left.\partial_dP_t^{q_0,X}(\sigma,d)\right|_{d=0}
 =-\int_0^t e^{-\sigma r+r^2/2}\,dr
 =-\int_{-t}^{0}e^{\sigma r+r^2/2}\,dr.
\tag{5.2}
\]

Consequently, if \(K_t(\sigma)\) denotes the positive integral in (5.2),
the first graph coefficient satisfies

\[
 \left.\partial_dQ_{1,X}\right|_{d=0}
 =-\frac{K_4(\sigma)+K_5(\sigma)}{10}.
\tag{5.3}
\]

This function is nonzero and tends to zero as \(\sigma\to+\infty\), so it
cannot be a polynomial.  Hence even the first two-dimensional graph jet has
no finite polynomial closure.  The polynomial Gaussian seed is possible
only after restriction to the single orbit \(d=0\); it cannot replace the
two-dimensional fixed point.

## 6. A separate full-plane planar preparation rule

Suppose a later validation supplies a graph field \(Q^{\rm gr}\) which is
jointly \(C^3\) in \((\sigma,d)\) up to both boundaries of \(|d|\le1\), and write

\[
 \Delta(\sigma,d)=Q^{\rm gr}(\Gamma(\sigma,d))-q_0(\Gamma(\sigma,d)).
\]

Choose nodes and weights

\[
 (b_1,b_2,b_3,b_4)=(1,2,3,4),\qquad
 (a_1,a_2,a_3,a_4)=(10,-20,15,-4).
\tag{6.1}
\]

They satisfy the exact Seeley identities

\[
 \sum_{k=1}^4a_k(-b_k)^j=1,
 \qquad j=0,1,2,3,
\tag{6.2}
\]

while the fourth moment is \(-119\).  For
\(0<t<1/2\), extend across either normal boundary by

\[
 E_\perp\Delta(\sigma,\pm(1+t))
 =c(1+2t)\sum_{k=1}^4a_k
 \Delta(\sigma,\pm(1-b_kt)).
\tag{6.3}
\]

All samples in (6.3) remain inside \(|d|\le1\).  Equation (6.2) matches the
normal derivatives through order three at \(|d|=1\), and the flat factor
\(c(1+2t)\) joins the extension to zero at \(|d|=3/2\).  Tangential
derivatives pass through the finite sum.  Therefore (6.3) is a global
\(C^3\) extension whenever the input graph perturbation is \(C^3\) on the
closed strip; it does not require sixth derivatives, as a boundary Taylor
formula would.

Let \(\chi_{\rm plan}\) be the septic cutoff equal to one for
\(|\sigma|\le20\) and zero for \(|\sigma|\ge21\).  Define

\[
 Q^{\rm pr}=q_0+\chi_{\rm plan}(\sigma)E_\perp\Delta.
\tag{6.4}
\]

Then \(Q^{\rm pr}-q_0\in C_c^3\), so \(Q^{\rm pr}\) is a full-plane
\(C^3\) field, equals
\(Q^{\rm gr}\) on \(|\sigma|\le20,|d|\le1\), and equals \(q_0\) on the
tail neighborhoods \(|\sigma|\ge21\).  This is an implication, not yet an instantiated canonical preparation: the required computed graph and the
positive-amplitude containment of its retained depth-two hull are still
missing.

## 7. Status ledger

| Statement | Status |
|---|---|
| Exact uncut \(0,4,5,\Theta_*\) slot algebra and \(\rho=0\) identity | **Proved / encoded** |
| Singular-core first graph jet \((s^3/24+9/20,\nu)\) | **Proved** |
| Explicit bounded \(C^\infty\) graph extension and complete-field datum | **Constructed** |
| Directed 28-block, depth-60 nesting arithmetic and radius-537 margin | **Validated** |
| Backward-flow variation equation and cutoff residual row | **Encoded algebraically** |
| Nonpolynomial first graph-jet obstruction | **Proved** |
| Seeley \(C^3\) identities and conditional full-plane preparation rule | **Proved / constructed conditionally** |
| Small-amplitude graph theorem hypotheses at \(\rho_*=1/\sqrt5\) | **Open** |
| Interval backward-flow evaluator and operator discretization | **Open** |
| Graph fixed point, residual/inverse enclosure, and positive-amplitude hull | **Open** |
| Realization of the Gaussian first jet by this same preparation | **Open** |
| Nonlinear selected traces and positive-amplitude regularized-gap root | **Open** |
| Fixed-\(\varepsilon\) complete-history root and network Fredholm lift | **Open** |
| Physical onset and biological pulse-control chain | **Open** |

The next validation should not discretize the full
\(|\sigma|\le537\) rectangle naively.  It should combine analytic exterior
bounds with a directed reachable-hull decomposition, or prove a sharper
fixed-parameter local graph theorem, and then continue the scalar fixed point
from \(\rho=0\) to \(1/\sqrt5\).

## 8. Reproduction

From the repository root run

```sh
PYTHONPATH=src /usr/bin/python3 \
  experiments/fixed_epsilon_frozen_graph_operator.py
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fixed_epsilon_frozen_graph_operator.py
```

The JSON result stores the exact equations, cutoff identifiers, directed
nesting intervals, Seeley moments, parent hashes, and a strict proved/open
claim ledger.
