# Stage 4J contract: projected residual closure for the inner stable flow

Status: **theorem design / OPEN numerical certificate.**  This contract is
the replacement for propagating the five raw Volterra primitives by a
positive forward majorant.  It does not claim a stable power, graph,
separator, or onset until every acceptance inequality below is directed.

## 1. Why the next residual must already be stable

Stage 4H proves that one return contains only

\[
 \varnothing,\qquad (\tau _0),\qquad(\tau _1),
 \qquad(\tau _0,\tau _0).
\]

It also shows a sampled phase-fixed signed row of about
\(4.14\times10^{-3}\), whereas taking the raw and rank-one pieces
separately gives about \(5.64\).  Stage 4I validates small local residuals
for the raw primitives, but their unprojected forward error excites the
one-dimensional unstable mode.  The resulting primitive tubes are huge even
though the signed answer is small.  This is a rigorous obstruction to that
error propagation, not evidence that the stable flow is large.

Stage 4J must therefore construct the final history operator

\[
 \mathcal S(t,s)=\mathcal U(t,s)P_s(s),
 \qquad P_s(t)=I-q_t f_t,                              \tag{1.1}
\]

before taking an absolute value.  Here \(q_t\) and \(f_t\) are the same
transported unstable column and atom--density covector used by Stages 3 and
4D, normalized by \(f_t(q_t)=1\).  In one coherent transported gauge,

\[
 f_t\mathcal U(t,s)=f_s,\qquad
 \mathcal U(t,s)q_s=q_t,\qquad
 P_s(t)\mathcal U(t,s)=\mathcal U(t,s)P_s(s).          \tag{1.2}
\]

A time-dependent rescaling of \(q_t\) and \(f_t\) inserts the corresponding
ratio \(c(t)/c(s)\) into the first two identities.  Only the projection and
its intertwining identity are gauge invariant; these are the objects used
below.

## 2. A posteriori projected-residual lemma

Let \(0\le s\le t\le T\), and let
\(\widehat{\mathcal S}(t,s)\) be a piecewise-polynomial approximation to
\(\mathcal S(t,s)\) in the declared complete-history norm.  It must be formed
as one common projected object, not as separately rounded approximations to
\(\mathcal U\) and \(qf\).  Define the initial defect by

\[
 D_s=P_s(s)-\widehat{\mathcal S}(s,s).
\]

Let \(R(t,s)\) denote the complete method-of-steps residual: differential
residual, history-transport boundary residual, delay-activation seams, and
ordinary cell seams.  Require the analytic stable constraints

\[
 P_s(s)D_s=D_s,\qquad P_s(t)R(t,s)=R(t,s).             \tag{2.1}
\]

The clean way to obtain (2.1) is to apply the same exact projection to the
guide and its residual before any norm.  The adjoint identity in (1.2) then
proves \(f_tR(t,s)=0\); a small numerical value of a separately computed
pairing is not a substitute.

For a chosen \(\alpha\ge0\), define

\[
\begin{aligned}
 K&=\sup_{0\le s\le t\le T}
       e^{\alpha(t-s)}\|\mathcal S(t,s)\|,\\
 \widehat K&=\sup_{0\le s\le t\le T}
       e^{\alpha(t-s)}\|\widehat{\mathcal S}(t,s)\|,\\
 \Delta&=\sup_s\|D_s\|
   +\sup_{s\le t}\int_s^t
       e^{\alpha(r-s)}\|R(r,s)\|\,dr .                 \tag{2.2}
\end{aligned}
\]

Duhamel's formula stays inside the stable bundle and gives

\[
 K\le\widehat K+K\Delta.                               \tag{2.3}
\]

Hence

\[
 \Delta<1
 \quad\Longrightarrow\quad
 K\le K_{\rm int}:=\frac{\widehat K}{1-\Delta}.        \tag{2.4}
\]

This is the noncircular closure: the unknown exact stable-flow constant
occurs linearly on both sides and is solved by a radii inequality.  No
unprojected fundamental-matrix norm enters (2.3).

Let \(\Pi_T\) be the exact event correction at the terminal section and let
\(\widehat M_s\) be the terminal signed row obtained from the same guide.
Let \(C_{\Pi,T}\) be a directed upper bound for \(\|\Pi_T\|\), let
\(\Delta_T\) be the preprojection endpoint defect/residual budget, and let
\(\varepsilon_{\Pi,T}\) contain the event-row guide, phase-speed denominator,
and arithmetic errors not already in \(\widehat M_s\).  Then

\[
 \|M_s\|
 \le \|\widehat M_s\|
      +C_{\Pi,T}K_{\rm int}\Delta_T
      +\varepsilon_{\Pi,T}.                            \tag{2.5}
\]

The sampled event factor is about \(2.01358\), so it cannot be replaced by
one.

Thus a directed inequality

\[
 \rho_{\rm term}:=\|\widehat M_s\|
                  +C_{\Pi,T}K_{\rm int}\Delta_T
                  +\varepsilon_{\Pi,T}
 <\rho_s<1                                             \tag{2.6}
\]

proves \(\|M_s^n\|\le\rho_s^n\) in the same section norm, so the stable
power constant is \(K_s=1\).  If a different equivalent norm is used, its
two comparison constants must be inserted explicitly in (2.5)--(2.6).

## 3. Required common complete-history object

The source must build one Taylor--Bernstein representation of the
rank-one-deflated evolution.  Its propagated voltage-density component is

\[
 S(t,\theta)=K(t,\theta)
       -q_t\frac{f_t(K(t,\theta))}{f_t(q_t)}.          \tag{3.1}
\]

There is no moving event projection \(\Pi_t\) in (3.1); inserting one would
introduce a \(\dot\Pi_t\) term and change the residual equation.  The phase
correction is applied once, at \(T\), through the terminal operator in
(2.5).

The complete-history operator contains more than the propagated density.  It
also contains the current atoms and the unadvanced translation/identity
block of the initial history, with the same \(P_s\) deflation.  The
intermediate norm in Stage 4H is dominated by this block.  Therefore
\(\widehat K\), \(R\), and \(\Delta\) must cover it continuously; closing
only the active \((t,\theta)\) density triangles cannot prove (2.4).

On every active support triangle, the four exact words are inserted
symbolically before (3.1) is expanded.  The following data must remain
correlated until after the final subtraction:

1. the orbit and coefficient Taylor models;
2. the \(q_t\) history;
3. every atom and density coefficient of \(f_t\);
4. the normalization \(f_t(q_t)\);
5. the current-recovery atom and voltage-history density;
6. at the terminal time only, the event correction, phase-speed
   denominator, and their uncertainty.

The total variation is bounded outward from the final Bernstein boxes for
\(S\).  A cell may be split until its sign is resolved, or bounded by its
Bernstein supremum times its exact width.  Gaussian quadrature, mesh
stabilization, and the difference of two already-absolute bounds are not
proof evidence.

## 4. Acceptance gates and result fields

A Stage-4J result may set the phase-fixed one-step stable-map and numerical
stable-power flags to true only if all of the following are present and
strict:

- exact parent-byte and source hashes for Stages 3, 4D, 4H, and 4I;
- all active support triangles and output-time cells covered;
- the current atoms and unadvanced translation/identity history block
  covered in the same norm;
- common signed residual and initial defect enclosed at 192 bits or higher;
- differential, history-boundary, activation-seam, and cell-seam residuals
  all included in \(\Delta\);
- the analytic stable constraints (2.1), with all approximate-row errors
  propagated in the same projection;
- directed \(\widehat K\), \(\Delta<1\), and
  \(K_{\rm int}=\widehat K/(1-\Delta)\);
- directed terminal guide norm, \(C_{\Pi,T}\), preprojection \(\Delta_T\),
  and separate event-row error \(\varepsilon_{\Pi,T}\);
- the strict inequality (2.6) for the declared \(\rho_s\);
- continuous output-phase supremum and outward density integration;
- a fresh independent replay and hostile tests that reject omission of any
  word, rank-one term, history boundary, activation seam, event correction,
  tail, cell seam, or normalization error.

The result must keep the following fields null or false even when (2.6)
closes:

- the other five nonlinear return-Hessian blocks;
- the split-ball self-map and contraction constants;
- the quantitative stable graph and its derivative bound;
- the physical pulse/stable-sheet crossing;
- interval Newton, unique onset, and two-sided routing.

Closing Stage 4J supplies the linear stable ingress required by the
six-block Lyapunov--Perron theorem.  It is a necessary bridge, not the final
separator theorem.
